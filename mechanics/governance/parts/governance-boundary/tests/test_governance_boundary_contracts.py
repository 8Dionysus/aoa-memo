from __future__ import annotations

import copy
import unittest

from jsonschema import Draft202012Validator

from governance_boundary_support import *  # noqa: F401,F403


class GovernanceBoundaryContractTests(unittest.TestCase):
    def assert_invalid(self, schema: dict[str, object], value: dict[str, object], label: str) -> None:
        errors = validation_errors(schema, value)
        self.assertTrue(errors, f"{label} unexpectedly validated")

    def test_governance_boundary_examples_match_schemas(self) -> None:
        self.assertTrue(GOVERNANCE_BOUNDARY_CONTRACTS)
        missing_pairs: list[str] = []
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema_path, example_path = contract_paths(stem, schema_file)
            if not schema_path.exists():
                missing_pairs.append(f"{example_path.relative_to(ROOT)} -> {schema_path.relative_to(ROOT)}")
            if not example_path.exists():
                missing_pairs.append(f"{schema_path.relative_to(ROOT)} -> {example_path.relative_to(ROOT)}")
        self.assertFalse(missing_pairs, "missing governance-boundary contract pair(s): " + ", ".join(missing_pairs))

        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            with self.subTest(stem=stem):
                schema, example = load_contract(stem, schema_file)
                Draft202012Validator.check_schema(schema)
                errors = validation_errors(schema, example)
                self.assertFalse(errors, f"{stem}: {errors[0].message}" if errors else stem)

    def test_governance_contract_discriminators_stay_bounded(self) -> None:
        writeback_schema, writeback_example = load_contract(
            "governance_memory_writeback",
            "governance_memory_writeback_v1.json",
        )
        decision_schema, decision_example = load_contract(
            "governance_decision_memory_v1",
            "governance_decision_memory_v1.json",
        )

        self.assertEqual(
            writeback_schema["properties"]["status"]["enum"],
            ["proposed", "applied", "held", "rejected"],
        )
        self.assertEqual(
            decision_schema["properties"]["memory_kind"]["const"],
            "governance_decision",
        )
        self.assertFalse(validation_errors(writeback_schema, writeback_example))
        self.assertFalse(validation_errors(decision_schema, decision_example))

    def test_governance_boundary_schemas_reject_unknown_fields(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in object_paths(example):
                exercised += 1
                with self.subTest(stem=stem, path=".".join(str(part) for part in path) or "top"):
                    mutated = copy.deepcopy(example)
                    target = get_path(mutated, path) if path else mutated
                    self.assertIsInstance(target, dict)
                    target["contract_escape"] = "loose-field"
                    self.assert_invalid(schema, mutated, f"{stem} unknown field at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary object fields were exercised")

    def test_governance_boundary_schemas_reject_wrong_types_for_every_field(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, value in walk_values(example):
                exercised += 1
                with self.subTest(stem=stem, path=".".join(str(part) for part in path)):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, wrong_type_value(value))
                    self.assert_invalid(schema, mutated, f"{stem} wrong type at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary fields were exercised")

    def test_governance_boundary_schemas_reject_missing_required_fields(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in required_paths(schema, example):
                exercised += 1
                with self.subTest(stem=stem, path=".".join(str(part) for part in path)):
                    mutated = copy.deepcopy(example)
                    delete_path(mutated, path)
                    self.assert_invalid(schema, mutated, f"{stem} missing required field at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary required fields were exercised")

    def test_governance_boundary_schemas_reject_bad_array_items(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in array_paths(example):
                value = get_path(example, path)
                if not isinstance(value, list):
                    continue
                exercised += 1
                replacement = [wrong_type_value(value[0])] if value else [12345]
                with self.subTest(stem=stem, path=".".join(str(part) for part in path), case="wrong-item"):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, replacement)
                    self.assert_invalid(schema, mutated, f"{stem} wrong array item at {path}")
                if not value or isinstance(value[0], str):
                    with self.subTest(stem=stem, path=".".join(str(part) for part in path), case="empty-string"):
                        mutated = copy.deepcopy(example)
                        set_path(mutated, path, [""])
                        self.assert_invalid(schema, mutated, f"{stem} empty string array item at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary array fields were exercised")

    def test_governance_boundary_schemas_reject_const_escapes(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, _const_value in constrained_paths(schema, example, "const"):
                if not path:
                    continue
                exercised += 1
                with self.subTest(stem=stem, path=".".join(str(part) for part in path)):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, const_escape_value(get_path(example, path)))
                    self.assert_invalid(schema, mutated, f"{stem} const escape at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary const fields were exercised")

    def test_governance_boundary_schemas_reject_enum_escapes(self) -> None:
        exercised = 0
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, _enum_values in constrained_paths(schema, example, "enum"):
                if not path:
                    continue
                exercised += 1
                with self.subTest(stem=stem, path=".".join(str(part) for part in path)):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, ENUM_ESCAPE_VALUE)
                    self.assert_invalid(schema, mutated, f"{stem} enum escape at {path}")
        self.assertGreater(exercised, 0, "no governance-boundary enum fields were exercised")

    def test_governance_boundary_schemas_reject_invalid_numeric_ranges(self) -> None:
        for stem, schema_file in GOVERNANCE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, value in walk_values(example):
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    continue
                with self.subTest(stem=stem, path=".".join(str(part) for part in path), case="negative"):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, -1)
                    self.assert_invalid(schema, mutated, f"{stem} negative number at {path}")




if __name__ == "__main__":
    unittest.main()
