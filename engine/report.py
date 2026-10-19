"""After-action report generator (task T8; FR-06, FR-07, FR-08).

Turns a score result from engine.scoring into the report a participant sees:
readiness rating, each decision with its rating and rationale, and the NIST
controls to strengthen, grouped by implementation timeline. Like the scoring
engine, it is a pure function of its inputs: the same session always produces
the same report (NFR-06).
"""

TIMELINE_LABELS = {
    "immediate": "Immediate (within 30 days)",
    "short_term": "Short-term (30 to 90 days)",
    "long_term": "Long-term (more than 90 days)",
}
TIMELINE_ORDER = ["immediate", "short_term", "long_term"]

CONTROL_FAMILIES = {
    "AC": "Access Control",
    "AT": "Awareness and Training",
    "AU": "Audit and Accountability",
    "CM": "Configuration Management",
    "CP": "Contingency Planning",
    "IA": "Identification and Authentication",
    "IR": "Incident Response",
    "PE": "Physical and Environmental Protection",
    "PS": "Personnel Security",
    "SA": "System and Services Acquisition",
    "SC": "System and Communications Protection",
    "SI": "System and Information Integrity",
}


def describe_control(control_id, control_names):
    family_code = control_id.split("-")[0]
    return {
        "id": control_id,
        "name": control_names.get(control_id, "Unknown control"),
        "family": CONTROL_FAMILIES.get(family_code, family_code),
    }


def build_report(scenario, score_result, control_names):
    """Build the after-action report for one scored session.

    scenario:      a scenario dict returned by engine.content.load_all()
    score_result:  the dict returned by engine.scoring.score_session()
    control_names: {control_id: name}, from engine.content.load_control_names()
    """
    points = {p["id"]: p for p in scenario["decision_points"]}

    findings = []
    for result in score_result["results"]:
        point = points[result["decision_point_id"]]
        option = next(o for o in point["options"] if o["id"] == result["option_id"])
        findings.append({
            "decision_point_id": result["decision_point_id"],
            "prompt": point["prompt"],
            "choice": option["text"],
            "rating": result["rating"],
            "points": result["points"],
            "rationale": result["rationale"],
            "controls": [describe_control(c, control_names) for c in result["nist_controls"]],
            "timeline": result["timeline"],
            "timeline_label": TIMELINE_LABELS.get(result["timeline"]),
        })

    # Each control is recommended once, at the earliest timeline any gap needs it.
    # score_result["gaps"] is already ordered immediate -> short_term -> long_term.
    recommended = {}
    for gap in score_result["gaps"]:
        for control_id in gap["nist_controls"]:
            if control_id not in recommended:
                recommended[control_id] = {
                    **describe_control(control_id, control_names),
                    "timeline": gap["timeline"],
                    "decision_points": [],
                }
            recommended[control_id]["decision_points"].append(gap["decision_point_id"])

    recommendations = []
    for timeline in TIMELINE_ORDER:
        controls = [c for c in recommended.values() if c["timeline"] == timeline]
        if controls:
            recommendations.append({
                "timeline": timeline,
                "label": TIMELINE_LABELS[timeline],
                "controls": controls,
            })

    return {
        "scenario_id": scenario["id"],
        "title": scenario["title"],
        "framework_versions": dict(scenario["framework_versions"]),
        "readiness": score_result["readiness"],
        "earned": score_result["earned"],
        "possible": score_result["possible"],
        "percent": score_result["percent"],
        "findings": findings,
        "strengths": [f for f in findings if f["rating"] == "correct"],
        "gaps": [f for f in findings if f["rating"] != "correct"],
        "recommendations": recommendations,
    }