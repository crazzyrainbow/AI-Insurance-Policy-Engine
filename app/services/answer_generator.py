"""
Enhanced Answer Generation with Structured Extraction

Provides domain-specific answer templates and structured extraction
for complex insurance policy queries.
"""

from typing import Dict, List, Any
from app.services.query_classifier import QueryCategory, UseCase


class AnswerTemplate:
    """Template for generating answers based on query category"""
    
    @staticmethod
    def format_coverage_answer(clauses: List[str], verdict: str) -> Dict[str, Any]:
        """Format answer for coverage questions"""
        # Extract key phrases from clauses for user-friendly display
        key_points = []
        for clause in clauses[:5]:
            # Extract first 120 chars that contain actual info
            text = ' '.join(clause.split())
            if len(text) > 120:
                text = text[:120] + "..."
            key_points.append(text)
        
        return {
            "answer_type": "coverage_check",
            "is_covered": verdict == "covered",
            "verdict": "Yes" if verdict == "covered" else "Likely No" if verdict == "excluded" else "Unclear",
            "key_points": key_points,
            "next_step": "Confirm with your TPA or insurance company" if verdict == "covered" else "Review policy alternative or exclusions list"
        }
    
    @staticmethod
    def format_limits_answer(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for limit questions"""
        import re
        
        # Clean, deduplicate, and filter clauses
        unique_clauses = []
        seen = set()
        
        for clause in clauses:
            clean = ' '.join(clause.split())
            if (len(clean) < 30 or clean in seen or clean.count(',') > 8):
                continue
            seen.add(clean)
            unique_clauses.append(clean)
        
        # Extract structured limits
        limits = []
        
        for clause in unique_clauses[:15]:
            # Extract numbers followed by context
            percentages = re.findall(r'(\d+)\s*%', clause)
            amounts = re.findall(r'(\d+(?:,\d+)*(?:\.\d+)?)', clause)
            durations = re.findall(r'(\d+)\s*(day|week|month|year)s?', clause, re.IGNORECASE)
            
            if percentages or (amounts and len(amounts) < 3) or durations:
                # Extract context sentence (up to 150 chars)
                sentence = clause[:150] + ("..." if len(clause) > 150 else "")
                limit_entry = {"description": sentence}
                
                if percentages:
                    limit_entry["percentage"] = percentages[0]
                if amounts:
                    limit_entry["amount"] = amounts[0]
                if durations:
                    limit_entry["duration"] = f"{durations[0][0]} {durations[0][1]}s" if durations[0][1][-1].lower() != 's' else f"{durations[0][0]} {durations[0][1]}"
                
                limits.append(limit_entry)
        
        return {
            "answer_type": "limits",
            "limits_breakdown": limits,
            "total_limits_found": len(unique_clauses),
            "message": f"Policy has {len(unique_clauses)} limit-related clauses. Top {len(limits)} shown below."
        }
    
    @staticmethod
    def format_exclusions_answer(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for exclusion questions"""
        # Clean and categorize exclusions
        cleaned_exclusions = []
        for clause in clauses[:8]:
            text = ' '.join(clause.split())
            if len(text) > 140:
                text = text[:140] + "..."
            if text not in cleaned_exclusions:
                cleaned_exclusions.append(text)
        
        return {
            "answer_type": "exclusions",
            "excluded_items": cleaned_exclusions,
            "warning": "NOT COVERED - These items are explicitly excluded",
            "count": len(cleaned_exclusions),
            "recommendation": "Review these carefully before claiming or seek alternatives"
        }
    
    @staticmethod
    def format_requirements_answer(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for requirement/document questions"""
        requirements = {"documents": [], "approvals": [], "notices": [], "other": []}
        
        for clause in clauses[:12]:
            text = ' '.join(clause.split())
            if len(text) > 130:
                text = text[:130] + "..."
            
            clause_lower = text.lower()
            categorized = False
            
            keywords = [
                ("documents", ["document", "certificate", "proof", "bill", "receipt", "invoice", "policy", "id"]),
                ("approvals", ["approval", "authorization", "consent", "approved", "authorize"]),
                ("notices", ["notify", "notice", "inform", "declare", "disclosure"])
            ]
            
            for category, words in keywords:
                if any(word in clause_lower for word in words):
                    requirements[category].append(text)
                    categorized = True
                    break
            
            if not categorized:
                requirements["other"].append(text)
        
        return {
            "answer_type": "requirements",
            "required_documents": requirements["documents"],
            "required_approvals": requirements["approvals"],
            "required_notices": requirements["notices"],
            "other_requirements": requirements["other"],
            "total_items": sum(len(v) for v in requirements.values())
        }
    
    @staticmethod
    def format_conditions_answer(clauses: List[str]) -> Dict[str, Any]:
        \"\"\"Format answer for conditional coverage questions\"\"\"
        clean_conditions = []\n        for clause in clauses[:10]:\n            text = ' '.join(clause.split())\n            if len(text) > 140:\n                text = text[:140] + \"...\"\n            if text not in clean_conditions:\n                clean_conditions.append(text)\n        \n        return {\n            \"answer_type\": \"conditions\",\n            \"conditions_list\": clean_conditions,\n            \"note\": \"Coverage is ONLY valid when these conditions are met\",\n            \"count\": len(clean_conditions),\n            \"warning\": \"Non-compliance may result in claim denial\"\n        }
    
    @staticmethod
    def format_financial_answer(clauses: List[str], financial_type: str) -> Dict[str, Any]:
        """Format answer for financial queries (deductible, copay, etc.)"""
        import re
        
        # Clean and organize financial data
        financial_items = []
        seen_clauses = set()
        
        for clause in clauses[:12]:
            # Clean the clause
            clean = ' '.join(clause.split())
            if clean in seen_clauses or len(clean) < 20:
                continue
            seen_clauses.add(clean)
            
            # Extract key patterns
            percentages = re.findall(r'(\d+)\s*%', clean)
            amounts = re.findall(r'([\$₹₨]\s*[\d,]+(?:\.\d{2})?|\d+(?:,\d+)*(?:\.\d{2})?)', clean)
            
            # Truncate for display
            display_text = clean[:160] + ("..." if len(clean) > 160 else "")
            
            financial_items.append({
                "description": display_text,
                "percentage": percentages[0] if percentages else None,
                "amount": amounts[0] if amounts else None
            })
        
        return {
            "answer_type": financial_type,
            "financial_details": financial_items,
            "total_items": len(financial_items),
            "message": f"Found {len(financial_items)} {financial_type} related terms"
        }
    
    @staticmethod
    def format_obligations_answer(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for insured obligations"""
        obligations = {
            "disclosure": [],
            "payment": [],
            "notification": [],
            "other": []
        }
        
        for clause in clauses:
            clause_lower = clause.lower()
            if any(word in clause_lower for word in ["disclose", "declare", "inform", "statement"]):
                obligations["disclosure"].append(clause)
            elif any(word in clause_lower for word in ["pay", "premium", "payment"]):
                obligations["payment"].append(clause)
            elif any(word in clause_lower for word in ["notify", "notice", "inform", "report"]):
                obligations["notification"].append(clause)
            else:
                obligations["other"].append(clause)
        
        return {
            "answer_type": "obligations",
            "obligations_by_type": obligations,
            "total_obligations": sum(len(v) for v in obligations.values())
        }
    
    @staticmethod
    def format_risk_analysis(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for risk/gap analysis"""
        risk_categories = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "coverage_gaps": []
        }
        
        risk_keywords = {
            "high_risk": ["excluded", "not covered", "void", "cancel", "terminate"],
            "medium_risk": ["limited", "sub-limit", "cap", "condition"],
            "low_risk": ["covered", "included", "eligible"],
            "coverage_gaps": ["gap", "uncovered", "missing"]
        }
        
        for clause in clauses:
            clause_lower = clause.lower()
            for risk_level, keywords in risk_keywords.items():
                if any(kw in clause_lower for kw in keywords):
                    risk_categories[risk_level].append(clause)
        
        return {
            "answer_type": "risk_analysis",
            "risks_identified": risk_categories,
            "total_risks": sum(len(v) for v in risk_categories.values())
        }
    
    @staticmethod
    def format_comparison_answer(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for comparison queries"""
        return {
            "answer_type": "comparison",
            "comparable_items": clauses,
            "note": "These clauses relate to the comparison being made"
        }
    
    @staticmethod
    def format_ambiguity_alert(clauses: List[str]) -> Dict[str, Any]:
        """Format answer for ambiguous clauses"""
        return {
            "answer_type": "ambiguity_alert",
            "ambiguous_clauses": clauses,
            "recommendation": "Seek legal counsel for these clauses before signing or claiming",
            "count": len(clauses)
        }


def generate_structured_answer(
    category: QueryCategory,
    clauses: List[str],
    verdict: str = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generate a structured answer based on query category.
    
    Args:
        category: The classified query category
        clauses: Relevant policy clauses
        verdict: The policy verdict (for coverage queries)
        metadata: Additional metadata
        
    Returns:
        Structured answer dictionary
    """
    
    if category == QueryCategory.COVERAGE_CHECK:
        return AnswerTemplate.format_coverage_answer(clauses, verdict)
    
    elif category in [QueryCategory.LIMITS, QueryCategory.SUB_LIMITS]:
        return AnswerTemplate.format_limits_answer(clauses)
    
    elif category == QueryCategory.EXCLUSIONS:
        return AnswerTemplate.format_exclusions_answer(clauses)
    
    elif category == QueryCategory.REQUIREMENTS:
        return AnswerTemplate.format_requirements_answer(clauses)
    
    elif category == QueryCategory.CONDITIONS:
        return AnswerTemplate.format_conditions_answer(clauses)
    
    elif category in [QueryCategory.DEDUCTIBLE, QueryCategory.COPAY, 
                       QueryCategory.MAXIMUM_CLAIM, QueryCategory.REIMBURSEMENT]:
        return AnswerTemplate.format_financial_answer(clauses, category.value)
    
    elif category == QueryCategory.OBLIGATIONS:
        return AnswerTemplate.format_obligations_answer(clauses)
    
    elif category == QueryCategory.GAPS:
        return AnswerTemplate.format_risk_analysis(clauses)
    
    elif category == QueryCategory.AMBIGUITY:
        return AnswerTemplate.format_ambiguity_alert(clauses)
    
    elif category == QueryCategory.COMPARISON:
        return AnswerTemplate.format_comparison_answer(clauses)
    
    else:
        # Default format
        return {
            "answer_type": category.value,
            "relevant_clauses": clauses,
            "clause_count": len(clauses)
        }


def enrich_response_with_context(
    base_response: Dict[str, Any],
    category: QueryCategory,
    usecase: UseCase,
    classification_confidence: float
) -> Dict[str, Any]:
    """
    Enrich response with metadata about classification and context.
    
    Args:
        base_response: The base response dictionary
        category: Query category
        usecase: Use-case context
        classification_confidence: Confidence in classification
        
    Returns:
        Enriched response
    """
    
    # Add classification metadata
    base_response["query_metadata"] = {
        "category": category.value,
        "use_case": usecase.value,
        "classification_confidence": round(classification_confidence, 2)
    }
    
    # Add context-specific guidance
    guidance_map = {
        QueryCategory.COVERAGE_CHECK: "Confirm with TPA/Insurance company before proceeding",
        QueryCategory.EXCLUSIONS: "Review carefully; uncovered treatments may require out-of-pocket payment",
        QueryCategory.REQUIREMENTS: "Ensure all documents are ready before visiting hospital",
        QueryCategory.CONDITIONS: "Verify these conditions are met; non-compliance may deny claim",
        QueryCategory.CLAIM_PROCESS: "Follow exact procedure and timelines to ensure claim approval",
        QueryCategory.AMBIGUITY: "Ambiguous clauses often cause disputes; seek written clarification",
    }
    
    if category in guidance_map:
        base_response["important_note"] = guidance_map[category]
    
    return base_response
