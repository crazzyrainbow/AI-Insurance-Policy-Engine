def format_policy_summary(structured: dict) -> dict:
    """
    Converts raw classified clauses into human-readable grouped summary.
    This is a PRESENTATION layer, not reasoning.
    """

    def _clean(clause: str) -> str:
        return clause.replace("\n", " ").strip()

    summary = {
        "what_is_covered": [],
        "key_limits": [],
        "important_conditions": [],
        "major_exclusions": []
    }

    for c in structured.get("coverage", []):
        summary["what_is_covered"].append(_clean(c))

    for c in structured.get("limits", []):
        summary["key_limits"].append(_clean(c))

    for c in structured.get("conditions", []):
        summary["important_conditions"].append(_clean(c))

    for c in structured.get("exclusions", []):
        summary["major_exclusions"].append(_clean(c))

    return summary
