from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_quest_chronicle_example_validates_against_schema() -> None:
    validator = validate_memo.validator_for("quest_chronicle.schema.json")
    example = load_json("examples/quest_chronicle.example.json")

    validator.validate(example)


def test_quest_chronicle_doc_keeps_witness_only_boundary() -> None:
    doc = (REPO_ROOT / "docs" / "QUEST_CHRONICLE_WRITEBACK.md").read_text(encoding="utf-8")

    for fragment in [
        "A quest chronicle is a witness object.",
        "replace source-owned quest state",
        "replace source-owned campaign or playbook meaning",
        "become a player sheet or runtime inventory",
        "using chronicle notes as a hidden project backlog",
    ]:
        assert fragment in doc


def test_quest_chronicle_surfaces_stay_discoverable_and_non_sovereign() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    example = load_json("examples/quest_chronicle.example.json")

    assert "docs/QUEST_CHRONICLE_WRITEBACK.md" in readme
    assert "schemas/quest_chronicle.schema.json" in readme
    assert "examples/quest_chronicle.example.json" in readme
    assert example["public_safe"] is True
    assert "witness" in example["notes"].lower()
    assert "not quest authority" in example["notes"].lower()
