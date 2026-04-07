from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_failure_lesson_example_validates_against_schema() -> None:
    schema = load_json("schemas/failure_lesson_memory_v1.json")
    example = load_json("examples/failure_lesson_memory.example.json")

    Draft202012Validator(schema).validate(example)


def test_failure_lesson_surfaces_stay_discoverable_and_non_proof() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    memory_doc = (REPO_ROOT / "docs" / "FAILURE_LESSON_MEMORY.md").read_text(encoding="utf-8")
    recall_doc = (REPO_ROOT / "docs" / "FAILURE_LESSON_RECALL.md").read_text(encoding="utf-8")

    for fragment in [
        "docs/FAILURE_LESSON_MEMORY.md",
        "docs/FAILURE_LESSON_RECALL.md",
        "schemas/failure_lesson_memory_v1.json",
        "examples/failure_lesson_memory.example.json",
    ]:
        assert fragment in readme

    assert "It remains memory, not proof." in memory_doc
    assert "Memo may shape attention." in recall_doc
    assert "It does not overrule source-owned evidence." in recall_doc
