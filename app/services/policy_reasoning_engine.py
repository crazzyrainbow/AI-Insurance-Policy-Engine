import uuid
import re
import numpy as np
from typing import List, Dict, Any

from app.services.vector_service import search_documents, hybrid_rerank
from app.infrastructure.embeddings import generate_embedding


# ============================================================
# CONFIG
# ============================================================

MAX_CLAUSE_LENGTH = 1200
MIN_CLAUSE_LENGTH = 40
TOP_K_CLAUSES = 25           # Limit reasoning scope
SIMILARITY_THRESHOLD = 0.45  # Clause relevance cutoff


# ============================================================
# COSINE SIMILARITY
# ============================================================

def _cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))


# ============================================================
# CLAUSE EXTRACTION
# ============================================================

def _extract_clauses(documents: List[str]) -> List[str]:

    clauses = []

    for doc in documents:
        sentences = re.split(r'(?<=[.!?])\s+', doc)

        for s in sentences:
            clean = s.strip()
            if MIN_CLAUSE_LENGTH <= len(clean) <= MAX_CLAUSE_LENGTH:
                clauses.append(clean)

    return clauses


# ============================================================
# SEMANTIC CLAUSE RANKING (NEW)
# ============================================================

def _rank_clauses_by_question(question: str, clauses: List[str]):

    q_embedding = generate_embedding(question)

    scored = []

    for clause in clauses:
        c_embedding = generate_embedding(clause)
        sim = _cosine_similarity(q_embedding, c_embedding)
        scored.append((clause, sim))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:TOP_K_CLAUSES]


# ============================================================
# LEGAL CLAUSE CLASSIFICATION (Deterministic)
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
# STRUCTURE POLICY KNOWLEDGE
# ============================================================

def _build_structured_map(scored_clauses):

    structured = {
        "coverage": [],
        "exclusions": [],
        "limits": [],
        "conditions": []
    }

    for clause, score in scored_clauses:

        if score < SIMILARITY_THRESHOLD:
            continue

        category = _classify_clause(clause)

        if category in structured:
            structured[category].append(clause)

    # Trim noise
    for key in structured:
        structured[key] = structured[key][:5]

    return structured


# ============================================================
# VERDICT ENGINE
# ============================================================

def _derive_verdict(structured):

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
# CONFIDENCE ENGINE (Semantic + Structural)
# ============================================================

def _calculate_confidence(structured, top_similarity):

    structural_score = (
        len(structured["coverage"]) * 3 +
        len(structured["limits"]) * 2 +
        len(structured["conditions"]) * 2 +
        len(structured["exclusions"]) * 2
    )

    confidence = min((structural_score / 10) * 0.6 + top_similarity * 0.4, 1.0)

    return round(confidence, 2)


# ============================================================
# MAIN POLICY REASONING PIPELINE
# ============================================================

def answer_question(question: str, session_id: str = None):

    if session_id is None:
        session_id = str(uuid.uuid4())

    # 1️⃣ Retrieve Relevant Policy Sections
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
            "analysis": {"verdict": "not_specified"},
            "confidence": 0.0,
            "decision_trace": {"reason": "No relevant policy text retrieved."},
            "evidence": [],
            "sources": []
        }

    # 2️⃣ Extract Clauses
    clauses = _extract_clauses(documents)

    # 3️⃣ Rank Clauses Semantically
    scored_clauses = _rank_clauses_by_question(question, clauses)

    top_similarity = scored_clauses[0][1] if scored_clauses else 0

    # 4️⃣ Build Legal Structure
    structured = _build_structured_map(scored_clauses)

    # 5️⃣ Derive Verdict
    verdict = _derive_verdict(structured)

    # 6️⃣ Confidence
    confidence = _calculate_confidence(structured, top_similarity)

    # 7️⃣ Evidence
    evidence = [{"clause": c[0]} for c in scored_clauses[:3]]

    # 8️⃣ Sources
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

    return {
        "session_id": session_id,
        "question": question,
        "analysis": {
            "verdict": verdict,
            "coverage": structured["coverage"],
            "exclusions": structured["exclusions"],
            "limits": structured["limits"],
            "conditions": structured["conditions"]
        },
        "confidence": confidence,
        "decision_trace": {
            "top_similarity": round(top_similarity, 3),
            "coverage_clauses": len(structured["coverage"]),
            "limit_clauses": len(structured["limits"]),
            "condition_clauses": len(structured["conditions"]),
            "exclusion_clauses": len(structured["exclusions"])
        },
        "evidence": evidence,
        "sources": unique_sources
    }
