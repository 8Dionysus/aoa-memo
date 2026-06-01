from __future__ import annotations

import copy
import unittest

from jsonschema import Draft202012Validator

from post_release_boundary_support import *  # noqa: F401,F403


class PostReleaseBoundaryContractTests(unittest.TestCase):
    def assert_invalid(self, schema: dict[str, object], value: object, label: str) -> None:
        errors = validation_errors(schema, value)
        self.assertTrue(errors, f"{label} unexpectedly validated")

    def test_post_release_boundary_examples_match_schemas(self) -> None:
        self.assertTrue(POST_RELEASE_BOUNDARY_CONTRACTS)
        missing_pairs: list[str] = []
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema_path, example_path = contract_paths(stem, schema_file)
            if not schema_path.exists():
                missing_pairs.append(f"{example_path.relative_to(ROOT)} -> {schema_path.relative_to(ROOT)}")
            if not example_path.exists():
                missing_pairs.append(f"{schema_path.relative_to(ROOT)} -> {example_path.relative_to(ROOT)}")
        self.assertFalse(missing_pairs, "missing post-release-boundary contract pair(s): " + ", ".join(missing_pairs))

        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            with self.subTest(stem=stem):
                schema, example = load_contract(stem, schema_file)
                Draft202012Validator.check_schema(schema)
                errors = validation_errors(schema, example)
                self.assertFalse(errors, f"{stem}: {errors[0].message}" if errors else stem)

    def test_post_release_boundary_schemas_reject_unknown_fields(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in object_paths(example):
                with self.subTest(stem=stem, path=path):
                    mutated = copy.deepcopy(example)
                    target = get_path(mutated, path) if path else mutated
                    self.assertIsInstance(target, dict)
                    target["contract_escape"] = "loose-field"
                    self.assert_invalid(schema, mutated, f"{stem} unknown field at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_wrong_types_for_every_field(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, value in walk_values(example):
                with self.subTest(stem=stem, path=path):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, wrong_type_value(value))
                    self.assert_invalid(schema, mutated, f"{stem} wrong type at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_missing_required_fields(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in required_paths(schema, example):
                with self.subTest(stem=stem, path=path):
                    mutated = copy.deepcopy(example)
                    delete_path(mutated, path)
                    self.assert_invalid(schema, mutated, f"{stem} missing required {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_bad_array_items(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in array_paths(example):
                with self.subTest(stem=stem, path=path):
                    mutated = copy.deepcopy(example)
                    array_value = get_path(mutated, path)
                    self.assertIsInstance(array_value, list)
                    if array_value:
                        array_value[0] = wrong_type_value(array_value[0])
                    else:
                        array_value.append({"not": "a valid array item"})
                    self.assert_invalid(schema, mutated, f"{stem} bad array item at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_empty_strings(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path in string_paths(example):
                with self.subTest(stem=stem, path=path):
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, "")
                    self.assert_invalid(schema, mutated, f"{stem} empty string at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_const_escapes(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, _constraint in constrained_paths(schema, example, "const"):
                with self.subTest(stem=stem, path=path):
                    value = get_path(example, path)
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, escape_value(value))
                    self.assert_invalid(schema, mutated, f"{stem} const escape at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_enum_escapes(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, _constraint in constrained_paths(schema, example, "enum"):
                with self.subTest(stem=stem, path=path):
                    value = get_path(example, path)
                    mutated = copy.deepcopy(example)
                    set_path(mutated, path, escape_value(value))
                    self.assert_invalid(schema, mutated, f"{stem} enum escape at {path}")
                    exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_bad_datetime_formats(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, constraint in constrained_paths(schema, example, "format"):
                if constraint != "date-time":
                    continue
                for bad_value in (
                    "not-a-date",
                    "2026-02-30T00:00:00Z",
                    "2026-04-22T24:00:00Z",
                    "2026-04-22T00:00:60Z",
                    "2026-04-22T00:00:00+24:00",
                    "0001-01-01T00:59:60+01:00",
                    "9999-12-31T23:59:60-00:01",
                    "\u0662\u0660\u0662\u0666-04-22T00:00:00Z",
                ):
                    with self.subTest(stem=stem, path=path, value=bad_value):
                        mutated = copy.deepcopy(example)
                        set_path(mutated, path, bad_value)
                        self.assert_invalid(schema, mutated, f"{stem} bad date-time at {path}")
                        exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_accept_rfc3339_datetime_variants(self) -> None:
        exercised = 0
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, constraint in constrained_paths(schema, example, "format"):
                if constraint != "date-time":
                    continue
                for valid_value in (
                    "2026-04-22t00:00:00.123456789z",
                    "0000-02-29T00:00:00Z",
                    "2016-12-31T23:59:60Z",
                    "2017-01-01T00:59:60+01:00",
                    "2017-01-01T00:29:60+00:30",
                    "2017-01-01T05:44:60+05:45",
                ):
                    with self.subTest(stem=stem, path=path, value=valid_value):
                        mutated = copy.deepcopy(example)
                        set_path(mutated, path, valid_value)
                        errors = validation_errors(schema, mutated)
                        self.assertFalse(errors, f"{stem}: {errors[0].message}" if errors else stem)
                        exercised += 1
        self.assertGreater(exercised, 0)

    def test_post_release_boundary_schemas_reject_numeric_bound_escapes(self) -> None:
        for stem, schema_file in POST_RELEASE_BOUNDARY_CONTRACTS:
            schema, example = load_contract(stem, schema_file)
            for path, value in walk_values(example):
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    continue
                field_schema = schema_for_path(schema, example, path)
                if not isinstance(field_schema, dict):
                    continue
                if "minimum" in field_schema:
                    with self.subTest(stem=stem, path=path, bound="minimum"):
                        mutated = copy.deepcopy(example)
                        set_path(mutated, path, field_schema["minimum"] - 1)
                        self.assert_invalid(schema, mutated, f"{stem} below minimum at {path}")
                if "maximum" in field_schema:
                    with self.subTest(stem=stem, path=path, bound="maximum"):
                        mutated = copy.deepcopy(example)
                        set_path(mutated, path, field_schema["maximum"] + 1)
                        self.assert_invalid(schema, mutated, f"{stem} above maximum at {path}")


if __name__ == "__main__":
    unittest.main()
