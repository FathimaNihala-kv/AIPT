from config import CONDITION_OPTIONS, SEVERITY_OPTIONS

CONDITION_SCORE = {
    "Excellent": 100,
    "Good": 85,
    "Fair": 65,
    "Poor": 45,
    "Damaged": 25,
    "Needs Replacement": 10,
    "Not Inspected": 0,
}

SEVERITY_WEIGHT = {
    "None": 0,
    "Minor": 0.5,
    "Moderate": 1.0,
    "Major": 1.5,
    "Critical": 2.0,
}


def calculate_overall_score(items):
    if not items:
        return 0.0
    total = 0.0
    for item in items:
        condition_score = CONDITION_SCORE.get(item.get("condition"), 0)
        severity_weight = SEVERITY_WEIGHT.get(item.get("severity"), 0)
        total += max(0, condition_score - severity_weight * 10)
    return round(total / len(items), 2)


def derive_status(score):
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "Fair"
    if score >= 30:
        return "Poor"
    return "Critical"


def build_summary(items):
    score = calculate_overall_score(items)
    rating = derive_status(score)
    critical_items = [item for item in items if item.get("severity") in ["Major", "Critical"]]
    return {
        "overall_score": score,
        "vehicle_health": round(score, 2),
        "condition_rating": rating,
        "total_components": len(items),
        "components_requiring_repair": len(critical_items),
        "critical_issues": critical_items,
    }
