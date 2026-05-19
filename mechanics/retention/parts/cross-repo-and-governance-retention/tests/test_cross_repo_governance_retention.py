from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]

RETENTION_CONTRACTS = {
    "cross_repo_retention_result": "cross_repo_retention_result_v1.json",
    "governance_retention_check": "governance_retention_check_v1.json",
}


def load_json(relative_path: str) -> dict[str, object]:
    payload = json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def contract_paths(stem: str, schema_file: str) -> tuple[Path, Path]:
    base = (
        REPO_ROOT
        / "mechanics"
        / "retention"
        / "parts"
        / "cross-repo-and-governance-retention"
    )
    return base / "schemas" / schema_file, base / "examples" / f"{stem}.example.json"


class RetentionMechanicTestCase(unittest.TestCase):
    def test_retention_registers_active_docs(self) -> None:
        config = load_json("config/mechanics/memo_mechanics.json")
        packages = {package["slug"]: package for package in config["packages"]}  # type: ignore[index]
        retention = packages["retention"]

        self.assertEqual("Retention Mechanic", retention["title"])
        self.assertIn("operation", retention)
        self.assertEqual(
            [
                "CROSS_REPO_RETENTION_MEMORY.md",
                "FIRST_OFFICE_RETENTION_MARKERS.md",
                "GOVERNANCE_RETENTION_CHECKS.md",
                "MULTI_OFFICE_RETENTION_MARKERS.md",
                "POST_RELEASE_RETENTION_OUTCOME.md",
                "POST_RELEASE_RETENTION_WATCH.md",
            ],
            retention["docs"],
        )

        for filename in retention["docs"]:
            self.assertTrue((REPO_ROOT / "mechanics" / "retention" / "docs" / filename).is_file())
            self.assertFalse((REPO_ROOT / "docs" / filename).exists())

    def test_retention_preserves_stronger_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "retention" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "abyss-stack",
            "aoa-evals",
            "aoa-agents",
            "stronger retention policy",
            "private data handling",
            "without executing retention",
        ):
            self.assertIn(snippet, readme)

    def test_cross_repo_governance_contracts_are_part_local_and_validate(self) -> None:
        parts = (REPO_ROOT / "mechanics" / "retention" / "PARTS.md").read_text(
            encoding="utf-8"
        )

        for stem, schema_file in RETENTION_CONTRACTS.items():
            with self.subTest(stem=stem):
                schema_path, example_path = contract_paths(stem, schema_file)
                schema_ref = schema_path.relative_to(REPO_ROOT).as_posix()
                example_ref = example_path.relative_to(REPO_ROOT).as_posix()

                self.assertIn(schema_ref, parts)
                self.assertIn(example_ref, parts)
                self.assertTrue(schema_path.is_file())
                self.assertTrue(example_path.is_file())

                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                example = json.loads(example_path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                errors = sorted(
                    Draft202012Validator(schema).iter_errors(example),
                    key=lambda error: list(error.path),
                )
                self.assertFalse(errors, errors[0].message if errors else "")

    def test_cross_repo_governance_schemas_reject_missing_required_fields(self) -> None:
        for stem, schema_file in RETENTION_CONTRACTS.items():
            schema_path, example_path = contract_paths(stem, schema_file)
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            example = json.loads(example_path.read_text(encoding="utf-8"))
            required = schema.get("required")
            self.assertIsInstance(required, list)
            self.assertTrue(required)

            for field in required:
                with self.subTest(stem=stem, field=field):
                    mutated = dict(example)
                    mutated.pop(field)
                    errors = list(Draft202012Validator(schema).iter_errors(mutated))
                    self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
