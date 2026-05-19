from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = (
    REPO_ROOT / "mechanics" / "retention" / "parts" / "post-release-retention"
)

CONTRACTS = {
    "post_release_retention_memory": "post_release_retention_memory_v1.json",
    "post_release_retention_watch": "post_release_retention_watch_v1.json",
}


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_post_release_retention_contracts_are_part_local_and_validate() -> None:
    parts = (REPO_ROOT / "mechanics" / "retention" / "PARTS.md").read_text(
        encoding="utf-8"
    )

    for stem, schema_file in CONTRACTS.items():
        schema_path = PART_ROOT / "schemas" / schema_file
        example_path = PART_ROOT / "examples" / f"{stem}.example.json"
        schema_ref = schema_path.relative_to(REPO_ROOT).as_posix()
        example_ref = example_path.relative_to(REPO_ROOT).as_posix()

        assert schema_ref in parts
        assert example_ref in parts
        assert schema_path.is_file()
        assert example_path.is_file()

        schema = load_json(schema_path)
        example = load_json(example_path)
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(example),
            key=lambda error: list(error.path),
        )
        assert errors == []


def test_post_release_retention_schemas_reject_missing_required_fields() -> None:
    for stem, schema_file in CONTRACTS.items():
        schema = load_json(PART_ROOT / "schemas" / schema_file)
        example = load_json(PART_ROOT / "examples" / f"{stem}.example.json")
        required = schema.get("required")
        assert isinstance(required, list)

        for field in required:
            mutated = dict(example)
            mutated.pop(field)
            errors = list(Draft202012Validator(schema).iter_errors(mutated))
            assert errors
