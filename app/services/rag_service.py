import uuid
import re
from typing import List, Dict, Any

from app.services.vector_service import search_documents, hybrid_rerank
from app.services.query_classifier import classify_query, get_query_focus_areas
from app.services.answer_generator import generate_structured_answer, enrich_response_with_context
from app.domain.policy_formatter import format_policy_summary



# ============================================================
# CONFIG
# ============================================================

MAX_CLAUSE_LENGTH = 1200
MIN_CLAUSE_LENGTH = 40


# ============================================================
# CLAUSE EXTRACTION
# ============================================================

def _extract_clauses(documents: List[str]) -> List[str]:

    clauses = []
    seen = set()

    for doc in documents:
        sentences = re.split(r'(?<=[.!?])\s+', doc)

        for s in sentences:
            clean = s.strip()
            if MIN_CLAUSE_LENGTH <= len(clean) <= MAX_CLAUSE_LENGTH:
                # Deduplicate - ignore near-duplicate clauses
                if clean not in seen:
                    clauses.append(clean)
                    seen.add(clean)

    return clauses


# ============================================================
# QUESTION TYPE DETECTION (Intent Only)
# ============================================================

def _detect_question_type(question: str) -> str:

    q = question.lower()

    if any(x in q for x in [
        "what is covered",
        "summary",
        "overview",
        "describe",
        "explain policy"
    ]):
        return "summary"

    return "specific"


# ============================================================
# LEGAL CLAUSE CLASSIFICATION (Deterministic — Audit Safe)
# ============================================================

def _classify_clause(clause: str) -> str:

    text = clause.lower()

    if any(x in text for x in [
        "we will not pay",
        "shall not be liable",
        "not covered",
        "excluded"
    ]):
        return "exclusions"

    if any(x in text for x in [
        "%",
        "sum insured",
        "maximum payment",
        "deductible",
        "limited to",
        "up to"
    ]):
        return "limits"

    if any(x in text for x in [
        "subject to",
        "provided that",
        "unless",
        "only if"
    ]):
        return "conditions"

    if any(x in text for x in [
        "we will pay",
        "we cover",
        "is covered"
    ]):
        return "coverage"

    return "other"


# ============================================================
# BUILD STRUCTURED POLICY VIEW
# ============================================================

def _build_structured_map(clauses: List[str]):

    structured = {
        "coverage": [],
        "exclusions": [],
        "limits": [],
        "conditions": []
    }

    for clause in clauses:
        category = _classify_clause(clause)

        if category in structured:
            structured[category].append(clause)

    # Trim noise
    for key in structured:
        structured[key] = structured[key][:5]

    return structured


# ============================================================
# LEGAL VERDICT ENGINE
# ============================================================

def _derive_verdict(structured: Dict[str, List[str]], question_type: str):

    if question_type == "summary":
        return "informational"

    if structured["coverage"]:
        if structured["limits"]:
            return "limited"
        if structured["conditions"]:
            return "conditional"
        return "covered"

    if structured["exclusions"]:
        return "excluded"

    return "not_specified"


# ============================================================
# CONFIDENCE (Based on Evidence Density)
# ============================================================

def _calculate_confidence(structured):

    evidence_weight = (
        len(structured["coverage"]) * 3 +
        len(structured["limits"]) * 2 +
        len(structured["conditions"]) * 2 +
        len(structured["exclusions"]) * 2
    )

    return round(min(evidence_weight / 10, 1.0), 2)


# ============================================================
# MAIN PIPELINE - ENHANCED WITH QUERY CLASSIFICATION
# ============================================================

def answer_question(question: str, session_id: str = None):

    if session_id is None:
        session_id = str(uuid.uuid4())

    # 🤖 CLASSIFY THE QUERY
    query_category, use_case, classification_confidence = classify_query(question)
    focus_areas = get_query_focus_areas(query_category, use_case)
    
    # 1️⃣ SEMANTIC RETRIEVAL (WITH FOCUS AREAS)
    raw_results = search_documents(question, k=10)

    documents, metadatas, _ = hybrid_rerank(
        question,
        raw_results,
        top_k=5
    )

    if not documents:
        return {
            "session_id": session_id,
            "question": question,
            "query_category": query_category.value,
            "use_case": use_case.value,
            "analysis": {"verdict": "not_specified"},
            "confidence": 0.0,
            "decision_trace": {"reason": "No relevant policy text retrieved."},
            "evidence": [],
            "sources": [],
            "classification_metadata": {
                "category": query_category.value,
                "use_case": use_case.value,
                "confidence": classification_confidence
            }
        }

    # 2️⃣ PARSE RETRIEVED TEXT
    clauses = _extract_clauses(documents)

    # 3️⃣ INTENT DETECTION
    question_type = _detect_question_type(question)

    # 4️⃣ BUILD LEGAL STRUCTURE
    structured = _build_structured_map(clauses)

    # 5️⃣ GENERATE STRUCTURED ANSWER BASED ON QUERY TYPE
    structured_answer = generate_structured_answer(
        category=query_category,
        clauses=clauses,
        verdict=_derive_verdict(structured, question_type),
        metadata={"focus_areas": focus_areas}
    )

    # 6️⃣ VERDICT
    verdict = _derive_verdict(structured, question_type)

    # Human-readable transformation for summary queries
    formatted_summary = None
    if question_type == "summary":
        formatted_summary = format_policy_summary(structured)

    # 7️⃣ CONFIDENCE
    confidence = _calculate_confidence(structured)

    # 8️⃣ EVIDENCE
    evidence = [{"clause": c} for c in clauses[:3]]

    # 9️⃣ SOURCES
    unique_sources = []
    seen = set()

    for meta in metadatas:
        key = (meta.get("source"), meta.get("page"))
        if key not in seen:
            seen.add(key)
            unique_sources.append({
                "source": meta.get("source"),
                "page": meta.get("page")
            })

    # BUILD RESPONSE
    response = {
        "session_id": session_id,
        "question": question,
        "query_category": query_category.value,
        "use_case": use_case.value,
        "analysis": {
            "verdict": verdict,
            "coverage": structured["coverage"],
            "exclusions": structured["exclusions"],
            "limits": structured["limits"],
            "conditions": structured["conditions"],
            "summary_view": formatted_summary,
            "structured_answer": structured_answer
        },
        "confidence": confidence,
        "decision_trace": {
            "mode": question_type,
            "parsed_clauses": len(clauses),
            "classification_confidence": round(classification_confidence, 3)
        },
        "evidence": evidence,
        "sources": unique_sources,
        "classification_metadata": {
            "category": query_category.value,
            "use_case": use_case.value,
            "confidence": round(classification_confidence, 3),
            "focus_areas": focus_areas
        }
    }
    
    # ENRICH WITH CONTEXT
    response = enrich_response_with_context(
        response,
        query_category,
        use_case,
        classification_confidence
    )
    
    return response
