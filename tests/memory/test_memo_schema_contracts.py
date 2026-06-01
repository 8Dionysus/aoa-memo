from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoSchemaContractTestCase(MemoValidatorTestCase):
    def test_inquiry_checkpoint_return_example_validates(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(validate_memo.example_path_for("inquiry_checkpoint.return.example.json"))

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertEqual(errors, [])
    def test_memory_object_schema_rejects_invalid_nullable_datetime(self) -> None:
        validator = validate_memo.validator_for("memory_object.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "memory-objects" / "anchor.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["time"]["valid_to"] = "bogus"

        errors = list(validator.iter_errors(payload))

        self.assertNotEqual(errors, [])
        self.assertTrue(any(list(error.path) == ["time", "valid_to"] for error in errors))
    def test_memo_datetime_checker_accepts_rfc3339_edge_cases(self) -> None:
        values = [
            "2026-04-22t00:00:00Z",
            "2026-04-22T00:00:00z",
            "2026-04-22T00:00:00.123456789012345678901234567890Z",
            "0000-01-01T00:00:00Z",
            "0000-02-29T23:59:59-23:59",
            "2016-12-31T23:59:60Z",
            "2016-12-31t23:59:60.123z",
            "2017-01-01T00:29:60+00:30",
            "2016-12-31T23:29:60-00:30",
            "2017-01-01T05:44:60+05:45",
            "2017-01-01T23:58:60+23:59",
            "2016-12-31T00:00:60-23:59",
        ]

        for value in values:
            with self.subTest(value=value):
                self.assertTrue(validate_memo.is_rfc3339_datetime(value))
    def test_memo_datetime_checker_rejects_rfc3339_drift(self) -> None:
        values = [
            "2026-04-22T00:00:00.Z",
            "\u0662\u0660\u0662\u0666-04-22T00:00:00Z",
            "2026-04-22T00:00:00.\u0661Z",
            "2026-02-30T00:00:00Z",
            "2026-04-22T24:00:00Z",
            "2026-04-22T23:60:00Z",
            "2026-04-22T23:59:61Z",
            "2026-04-22T23:59:59+24:00",
            "2026-04-22T23:59:59+23:60",
            "0000-12-31T23:59:60Z",
            "0000-01-01T00:29:60+00:30",
            "2016-12-31T23:59:60+01:00",
            "2017-01-01T00:59:60+00:30",
            "0001-01-01T00:00:60+23:59",
            "9999-12-31T23:59:60-23:59",
        ]

        for value in values:
            with self.subTest(value=value):
                self.assertFalse(validate_memo.is_rfc3339_datetime(value))
    def test_memo_schema_validator_uses_rfc3339_checker(self) -> None:
        validator = validate_memo.validator_for("memory_object.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "memory-objects" / "anchor.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["time"]["created_at"] = "2026-04-22t00:00:00.123456789z"
        payload["time"]["observed_at"] = "2017-01-01T05:44:60+05:45"
        payload["time"]["valid_from"] = "0000-02-29T00:00:00Z"
        payload["promotion"]["promoted_at"] = "2016-12-31T00:00:60-23:59"

        errors = list(validator.iter_errors(payload))

        self.assertEqual(errors, [])
    def test_inquiry_checkpoint_return_pack_requires_anchor_refs(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(validate_memo.example_path_for("inquiry_checkpoint.return.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("anchor_refs", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("anchor_refs" in message for message in errors))
    def test_inquiry_checkpoint_return_pack_requires_reentry_refs(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(validate_memo.example_path_for("inquiry_checkpoint.return.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("reentry_refs", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("reentry_refs" in message for message in errors))
    def test_inquiry_checkpoint_return_pack_requires_reentry_note(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(validate_memo.example_path_for("inquiry_checkpoint.return.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("reentry_note", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("reentry_note" in message for message in errors))
    def test_bridge_schema_requires_shared_envelope_ref(self) -> None:
        validator = validate_memo.validator_for("bridge.schema.json")
        payload = load_json(validate_memo.example_path_for("bridge.kag-lift.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["bridges"].pop("shared_envelope_ref", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("shared_envelope_ref" in message for message in errors))
    def test_bridge_schema_rejects_empty_outward_refs_without_route_capsule(self) -> None:
        validator = validate_memo.validator_for("bridge.schema.json")
        payload = load_json(validate_memo.example_path_for("bridge.kag-lift.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["bridges"].pop("route_capsule_ref", None)
        payload["bridges"]["tos_refs"] = []
        payload["bridges"]["skill_refs"] = []
        payload["bridges"]["eval_refs"] = []

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("valid under any of the given schemas" in message for message in errors))
    def test_checkpoint_schema_requires_all_eight_mapping_rules(self) -> None:
        validator = validate_memo.validator_for("checkpoint-to-memory-contract.schema.json")
        payload = load_json(validate_memo.example_path_for("checkpoint_to_memory_contract.example.json"))
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["mapping_rules"] = payload["mapping_rules"][:-1]

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("is too short" in message for message in errors))
    def test_return_ready_recall_contract_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_recall_contract_example(
                    "recall_contract.object.working.return.json",
                    expected_mode="working",
                    expected_allowed_scopes=["thread", "session", "project"],
                    expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
                    expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
                    expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
                    expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
                    expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
                    expected_source_route_required=False,
                    expected_checkpoint_continuity_supported=True,
                    expected_return_ready=True,
                    expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                    expected_support_artifact_refs=[
                        "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
                        "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
                        "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
                        "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
                    ],
                )
    def test_recall_contract_schema_rejects_invalid_preferred_anchor_kind(self) -> None:
        validator = validate_memo.validator_for("recall_contract.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "recall" / "recall_contract.object.working.return.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["preferred_anchor_kinds"] = ["state_capsule", "router_capsule"]

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("is not one of" in message for message in errors))
    def test_return_ready_recall_contract_rejects_bad_support_artifact_ref(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.object.working.return.json"
        original_load_json = validate_memo.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["support_artifact_refs"] = ["docs/DOES_NOT_EXIST.md"]

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_recall_contract_example,
                "recall_contract.object.working.return.json",
                expected_mode="working",
                expected_allowed_scopes=["thread", "session", "project"],
                expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
                expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
                expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
                expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
                expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
                expected_source_route_required=False,
                expected_checkpoint_continuity_supported=True,
                expected_return_ready=True,
                expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                expected_support_artifact_refs=["docs/DOES_NOT_EXIST.md"],
            )
    def test_return_ready_recall_contract_requires_capsule_surface(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.object.working.return.json"
        original_load_json = validate_memo.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload.pop("capsule_surface", None)

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_recall_contract_example,
                "recall_contract.object.working.return.json",
                expected_mode="working",
                expected_allowed_scopes=["thread", "session", "project"],
                expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
                expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
                expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
                expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
                expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
                expected_source_route_required=False,
                expected_checkpoint_continuity_supported=True,
                expected_return_ready=True,
                expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                expected_support_artifact_refs=[
                    "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
                    "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
                    "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
                    "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
                ],
            )
    def test_router_semantic_recall_contract_requires_capsule_surface(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.router.semantic.json"
        original_load_json = validate_memo.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload.pop("capsule_surface", None)

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_recall_contract_example,
                "recall_contract.router.semantic.json",
                expected_mode="semantic",
                expected_allowed_scopes=["repo", "project", "ecosystem"],
                expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
                expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
                expected_inspect_surface="generated/memory/memory_catalog.min.json",
                expected_capsule_surface="generated/memory/memory_capsules.json",
                expected_expand_surface="generated/memory/memory_sections.full.json",
                expected_source_route_required=True,
            )
    def test_recall_contract_rejects_nonexistent_capsule_surface_ref(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.object.lineage.json"
        original_load_json = validate_memo.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["capsule_surface"] = "generated/DOES_NOT_EXIST.json"

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_recall_contract_example,
                "recall_contract.object.lineage.json",
                expected_mode="lineage",
                expected_allowed_scopes=["project", "workspace", "ecosystem"],
                expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
                expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
                expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
                expected_capsule_surface="generated/DOES_NOT_EXIST.json",
                expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
                expected_source_route_required=True,
            )
