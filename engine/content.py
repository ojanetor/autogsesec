"""Loads scenario content and framework mappings, and checks they agree.

Scenario files hold the story and choices only. Mapping files hold the
ratings, NIST controls, and framework versions. Keeping them apart means a
framework update changes the mapping files without touching the stories.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RATINGS = {"correct", "partial", "incorrect"}
TIMELINES = {"immediate", "short_term", "long_term", None}


def _read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_all():
    frameworks = _read_json(DATA_DIR / "frameworks.json")
    known_tactics = set(frameworks["attack_ics"]["tactics"])
    known_controls = set(frameworks["nist_sp800_82"]["controls"])

    scenarios = {}
    for scenario_file in sorted((DATA_DIR / "scenarios").glob("*.json")):
        scenario = _read_json(scenario_file)
        mapping = _read_json(DATA_DIR / "mappings" / scenario_file.name)
        _validate(scenario, mapping, known_tactics, known_controls)
        scenario["mapping"] = mapping["decision_points"]
        scenario["framework_versions"] = mapping["framework_versions"]
        scenario["attack_tactic"] = mapping["attack_tactic"]
        scenarios[scenario["id"]] = scenario
    return scenarios


def _validate(scenario, mapping, known_tactics, known_controls):
    sid = scenario["id"]
    if mapping["scenario_id"] != sid:
        raise ValueError(f"{sid}: mapping file is for {mapping['scenario_id']}")
    if mapping["attack_tactic"] not in known_tactics:
        raise ValueError(f"{sid}: unknown ATT&CK tactic {mapping['attack_tactic']}")

    for point in scenario["decision_points"]:
        point_map = mapping["decision_points"].get(point["id"])
        if point_map is None:
            raise ValueError(f"{sid}: no mapping for decision point {point['id']}")
        for option in point["options"]:
            entry = point_map.get(option["id"])
            where = f"{sid} {point['id']} option {option['id']}"
            if entry is None:
                raise ValueError(f"{where}: missing from mapping file")
            if entry["rating"] not in RATINGS:
                raise ValueError(f"{where}: rating must be correct, partial or incorrect")
            if entry.get("timeline") not in TIMELINES:
                raise ValueError(f"{where}: unknown timeline {entry.get('timeline')}")
            if not entry["nist_controls"]:
                raise ValueError(f"{where}: needs at least one NIST control")
            for control in entry["nist_controls"]:
                if control not in known_controls:
                    raise ValueError(f"{where}: unknown NIST control {control}")