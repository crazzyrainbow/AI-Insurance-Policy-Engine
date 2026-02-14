"""
Query Classification System for Insurance Policy Analysis

Classifies user queries into specific use-case categories and determines
optimal retrieval and reasoning strategies.
"""

from typing import List, Dict, Tuple
from enum import Enum


class QueryCategory(str, Enum):
    """Query categories based on insurance domain expertise"""
    
    # Coverage queries
    COVERAGE_CHECK = "coverage_check"  # Is X covered?
    ELIGIBILITY = "eligibility"  # Am I eligible for X?
    LIMITS = "limits"  # What are the limits for X?
    SUB_LIMITS = "sub_limits"  # Are there sub-limits?
    
    # Exclusion queries
    EXCLUSIONS = "exclusions"  # What is NOT covered?
    EXCLUSION_SCOPE = "exclusion_scope"  # Does exclusion Y apply to X?
    
    # Conditions & Requirements
    CONDITIONS = "conditions"  # What conditions must be met?
    REQUIREMENTS = "requirements"  # What documents/approvals needed?
    WAITING_PERIOD = "waiting_period"  # How long is the waiting period?
    PRE_AUTH = "pre_auth"  # Is pre-authorization required?
    
    # Financial queries
    DEDUCTIBLE = "deductible"  # What is the deductible?
    COPAY = "copay"  # What are the copay amounts?
    REIMBURSEMENT = "reimbursement"  # How much will be reimbursed?
    MAXIMUM_CLAIM = "maximum_claim"  # What is the maximum claimable amount?
    
    # Structural/Legal queries
    POLICY_DEFINITION = "policy_definition"  # Define/explain term X
    OBLIGATIONS = "obligations"  # What are insured obligations?
    DISPUTE_RESOLUTION = "dispute_resolution"  # How are disputes handled?
    TERMINATION = "termination"  # When can policy be terminated?
    
    # Comparison queries
    COMPARISON = "comparison"  # Compare coverages/policies
    BENCHMARK = "benchmark"  # How does this compare to standard?
    
    # Risk/Gap Analysis
    GAPS = "gaps"  # What coverage gaps exist?
    AMBIGUITY = "ambiguity"  # Are there ambiguous clauses?
    RISK_ASSESSMENT = "risk_assessment"  # What are the risks?
    
    # Procedural queries
    CLAIM_PROCESS = "claim_process"  # How to file a claim?
    DEADLINE = "deadline"  # What is the deadline for X?
    NETWORK = "network"  # Are these hospitals in-network?
    
    # Change/Compliance queries
    CHANGE_CLAUSE = "change_clause"  # What happens on change of ownership?
    COMPLIANCE = "compliance"  # Is this compliant with X regulation?
    MISREPRESENTATION = "misrepresentation"  # What about false declarations?
    
    # General queries
    SUMMARY = "summary"  # Summarize the policy
    OVERVIEW = "overview"  # Give me an overview of X


class UseCase(str, Enum):
    """High-level use-case categories"""
    
    HOSPITAL_TPA = "hospital_tpa"  # Hospital/TPA verification
    EMPLOYER = "employer"  # Employer reviewing policy
    BANK = "bank"  # Financial institution assessment
    LEGAL = "legal"  # Legal/compliance review
    BROKER = "broker"  # Insurance broker analysis
    FAMILY = "family"  # Family member seeking help
    VENDOR = "vendor"  # Service provider verification
    DUE_DILIGENCE = "due_diligence"  # M&A due diligence
    AUDITOR = "auditor"  # Audit/investigation
    DATA_PROTECTION = "data_protection"  # Governance review


# Keyword mappings for query classification
QUERY_KEYWORDS = {
    QueryCategory.COVERAGE_CHECK: [
        "covered", "is.*covered", "coverage", "will.*cover", "does.*cover",
        "covered under", "eligible for coverage", "covered services"
    ],
    QueryCategory.ELIGIBILITY: [
        "eligible", "eligibility", "am i eligible", "qualify", "qualified",
        "entitled", "who is eligible", "eligibility criteria"
    ],
    QueryCategory.LIMITS: [
        "limit", "maximum", "max", "ceiling", "cap", "up to",
        "limited to", "what is the limit", "limit per year"
    ],
    QueryCategory.SUB_LIMITS: [
        "sub-limit", "sub limit", "sub.limit", "limit per item",
        "per service limit", "service limit"
    ],
    QueryCategory.EXCLUSIONS: [
        "excluded", "exclusion", "not covered", "not included",
        "exclude", "excepted", "not applicable", "what is not"
    ],
    QueryCategory.EXCLUSION_SCOPE: [
        "does exclusion", "apply to", "fall under exclusion",
        "covered under exclusion", "is this excluded"
    ],
    QueryCategory.CONDITIONS: [
        "condition", "conditional", "provided that", "subject to",
        "condition.*apply", "must be.*", "requirement"
    ],
    QueryCategory.REQUIREMENTS: [
        "requirement", "need", "mandatory", "must have", "must provide",
        "documents", "approval", "authorization", "what do i need"
    ],
    QueryCategory.WAITING_PERIOD: [
        "waiting period", "waiting days", "waiting.*period",
        "how long.*wait", "waiting time", "initial waiting period"
    ],
    QueryCategory.PRE_AUTH: [
        "pre.auth", "pre-auth", "preauth", "prior authorization",
        "authorization.*required", "prior approval", "pre.*approval"
    ],
    QueryCategory.DEDUCTIBLE: [
        "deductible", "deductibles", "excess", "out.*pocket",
        "what deductible", "annual deductible"
    ],
    QueryCategory.COPAY: [
        "copay", "co-pay", "copayment", "co payment", "out of pocket"
    ],
    QueryCategory.REIMBURSEMENT: [
        "reimburse", "reimbursement", "how much.*paid", "claim amount",
        "payout", "will.*pay", "reimbursable"
    ],
    QueryCategory.MAXIMUM_CLAIM: [
        "maximum.*claim", "max.*claimable", "total.*claim",
        "annual limit", "claim limit", "annual maximum"
    ],
    QueryCategory.POLICY_DEFINITION: [
        "what.*means", "define", "explanation", "what is",
        "meaning of", "explain", "clarify"
    ],
    QueryCategory.OBLIGATIONS: [
        "obligation", "responsibility", "must", "shall",
        "insured.*obligation", "duty", "requirement"
    ],
    QueryCategory.DISPUTE_RESOLUTION: [
        "dispute", "resolution", "conflict", "arbitration",
        "lawsuit", "legal", "court", "jurisdiction"
    ],
    QueryCategory.TERMINATION: [
        "terminate", "cancellation", "cancel", "lapse",
        "when.*end", "end of coverage", "non-renewal"
    ],
    QueryCategory.COMPARISON: [
        "compare", "difference", "vs", "versus", "same as",
        "similar to", "better than", "how does.*differ"
    ],
    QueryCategory.BENCHMARK: [
        "standard", "benchmark", "industry", "typical",
        "normal coverage", "market standard", "compared to"
    ],
    QueryCategory.GAPS: [
        "gap", "uncovered", "not covered", "missing coverage",
        "what.*not covered", "coverage gap"
    ],
    QueryCategory.AMBIGUITY: [
        "ambiguous", "unclear", "ambiguity", "confusing",
        "vague", "not clear", "meaning unclear"
    ],
    QueryCategory.RISK_ASSESSMENT: [
        "risk", "risky", "exposure", "vulnerable",
        "what.*risk", "what could go wrong"
    ],
    QueryCategory.CLAIM_PROCESS: [
        "claim", "file.*claim", "how to claim", "claim.*process",
        "process.*claim", "claim procedures"
    ],
    QueryCategory.DEADLINE: [
        "deadline", "time.*limit", "how long", "when.*due",
        "notice.*period", "notification", "days.*notify"
    ],
    QueryCategory.NETWORK: [
        "network", "in-network", "in network", "out of network",
        "hospital.*list", "empanelment", "network hospital"
    ],
    QueryCategory.CHANGE_CLAUSE: [
        "change", "ownership", "acquisition", "takeover",
        "change of control", "merge", "sell"
    ],
    QueryCategory.COMPLIANCE: [
        "complian", "regulation", "law", "statutory",
        "legal requirement", "compliant", "regulatory"
    ],
    QueryCategory.MISREPRESENTATION: [
        "misrepresent", "false", "false declaration",
        "incorrect info", "not disclosed", "concealed"
    ],
    QueryCategory.SUMMARY: [
        "summary", "summarize", "overview", "brief",
        "in short", "gist", "key points"
    ],
    QueryCategory.CLAIM_PROCESS: [
        "hospital", "cashless", "reimbursement claim",
        "claim procedure", "how to"
    ],
}

# Use-case specific keywords
USECASE_KEYWORDS = {
    UseCase.HOSPITAL_TPA: [
        "hospital", "tpa", "cashless", "treatment", "eligibility",
        "verify", "approval", "before service"
    ],
    UseCase.EMPLOYER: [
        "employer", "employee", "corporate", "company", "group policy",
        "dependent", "coverage", "benefits"
    ],
    UseCase.BANK: [
        "bank", "loan", "collateral", "financial institution",
        "lending", "risk", "assignable", "coverage sufficient"
    ],
    UseCase.LEGAL: [
        "legal", "liability", "enforce", "due diligence",
        "legal team", "compliance", "enforcement", "indemnity"
    ],
    UseCase.BROKER: [
        "broker", "compare", "policy", "wording", "difference",
        "benchmark", "endorsement", "unusual"
    ],
    UseCase.FAMILY: [
        "family", "help", "claim", "hospital", "expense",
        "reimbursement", "what can we", "out of pocket"
    ],
    UseCase.VENDOR: [
        "vendor", "service provider", "will.*pay", "prior approval",
        "charges", "tariff", "reimbursable", "responsible"
    ],
    UseCase.DUE_DILIGENCE: [
        "acquisition", "m&a", "due diligence", "tail coverage",
        "survive", "change of control", "past"
    ],
    UseCase.AUDITOR: [
        "audit", "audit", "investigat", "compliance", "declaration",
        "incident", "retroactive"
    ],
    UseCase.DATA_PROTECTION: [
        "data protection", "governance", "confidential", "breach",
        "audit", "personal data", "security"
    ],
}


def classify_query(question: str) -> Tuple[QueryCategory, UseCase, float]:
    """
    Classify a query into query category and use-case.
    
    Args:
        question: The user's question
        
    Returns:
        Tuple of (QueryCategory, UseCase, confidence_score)
    """
    question_lower = question.lower()
    
    # Score each category
    category_scores: Dict[QueryCategory, int] = {}
    for category, keywords in QUERY_KEYWORDS.items():
        score = sum(
            1 for keyword in keywords
            if keyword in question_lower or 
            (keyword.startswith("is.*") and "is" in question_lower and keyword[4:] in question_lower)
        )
        if score > 0:
            category_scores[category] = score
    
    # Score each use-case
    usecase_scores: Dict[UseCase, int] = {}
    for usecase, keywords in USECASE_KEYWORDS.items():
        score = sum(
            1 for keyword in keywords
            if keyword in question_lower
        )
        if score > 0:
            usecase_scores[usecase] = score
    
    # Get best matches
    best_category = (
        max(category_scores.items(), key=lambda x: x[1])[0]
        if category_scores
        else QueryCategory.COVERAGE_CHECK
    )
    
    best_usecase = (
        max(usecase_scores.items(), key=lambda x: x[1])[0]
        if usecase_scores
        else UseCase.FAMILY
    )
    
    # Calculate confidence (0-1)
    max_category_score = max(category_scores.values()) if category_scores else 0
    confidence = min(max_category_score / 3, 1.0)  # Normalize to 0-1
    
    return best_category, best_usecase, confidence


def get_query_focus_areas(category: QueryCategory, usecase: UseCase) -> List[str]:
    """
    Determine which parts of the policy to focus on based on query type.
    
    Args:
        category: The query category
        usecase: The use-case context
        
    Returns:
        List of focus areas to search for
    """
    focus_areas = []
    
    # Category-based focus
    if category in [QueryCategory.COVERAGE_CHECK, QueryCategory.ELIGIBILITY]:
        focus_areas.extend(["coverage", "eligible", "covered", "benefits"])
    
    elif category == QueryCategory.EXCLUSIONS:
        focus_areas.extend(["exclusion", "excluded", "not covered", "exception"])
    
    elif category in [QueryCategory.LIMITS, QueryCategory.SUB_LIMITS]:
        focus_areas.extend(["limit", "maximum", "cap", "ceiling"])
    
    elif category in [QueryCategory.DEDUCTIBLE, QueryCategory.COPAY]:
        focus_areas.extend(["deductible", "copay", "co-pay", "out of pocket"])
    
    elif category == QueryCategory.CONDITIONS:
        focus_areas.extend(["condition", "conditional", "subject to", "provided"])
    
    elif category == QueryCategory.REQUIREMENTS:
        focus_areas.extend(["requirement", "document", "approval", "authorization"])
    
    elif category == QueryCategory.WAITING_PERIOD:
        focus_areas.extend(["waiting", "period", "days", "initial"])
    
    elif category == QueryCategory.PRE_AUTH:
        focus_areas.extend(["authorization", "pre-auth", "approval", "prior"])
    
    elif category == QueryCategory.CLAIM_PROCESS:
        focus_areas.extend(["claim", "process", "procedure", "file"])
    
    elif category == QueryCategory.NETWORK:
        focus_areas.extend(["network", "hospital", "empanel", "in-network"])
    
    # Use-case based focus
    if usecase == UseCase.HOSPITAL_TPA:
        focus_areas.extend(["cashless", "eligibility", "room rent", "icu"])
    
    elif usecase == UseCase.EMPLOYER:
        focus_areas.extend(["dependent", "maternity", "employee", "corporate"])
    
    elif usecase == UseCase.BANK:
        focus_areas.extend(["assignable", "void", "rejec", "termination"])
    
    elif usecase == UseCase.LEGAL:
        focus_areas.extend(["liability", "obligation", "enforce", "dispute"])
    
    elif usecase == UseCase.BROKER:
        focus_areas.extend(["wording", "endorse", "benchmark", "deductible"])
    
    return list(set(focus_areas))  # Remove duplicates
