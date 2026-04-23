from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo
import validate_memory_object_surfaces
import validate_memory_surfaces
import generate_kag_export


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class MemoValidatorTestCase(unittest.TestCase):
    def assert_system_exit_quietly(self, func, /, *args, **kwargs) -> SystemExit:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as context:
                    func(*args, **kwargs)
        return context.exception

    def guardrail_payload(self) -> dict:
        payload = load_json(validate_memo.EXAMPLES / "memory_eval_guardrail_pack.example.json")
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)

    def assert_guardrail_payload_fails(self, payload: dict) -> None:
        guardrail_path = validate_memo.EXAMPLES / "memory_eval_guardrail_pack.example.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == guardrail_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_memory_eval_guardrail_pack)

    def kag_export_payload(self) -> dict:
        payload = load_json(generate_kag_export.KAG_EXPORT_PATH)
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)

    def assert_kag_export_payload_fails(self, payload: dict) -> None:
        export_path = generate_kag_export.KAG_EXPORT_PATH
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == export_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_kag_source_export)

    def questbook_payload(self, quest_id: str) -> dict:
        payload = load_json(REPO_ROOT / "quests" / f"{quest_id}.yaml")
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)

    def test_inquiry_checkpoint_return_example_validates(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "inquiry_checkpoint.return.example.json")

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertEqual(errors, [])

    def test_memory_readiness_boundary_materialization_validates(self) -> None:
        validate_memo.validate_memory_readiness_boundary_materialization()

    def test_memory_readiness_boundary_rejects_overlapping_delta_refs(self) -> None:
        checkpoint_path = validate_memo.EXAMPLES / "inquiry_checkpoint.return.example.json"
        payload = load_json(checkpoint_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["canon_delta_refs"] = list(payload["memory_delta_refs"])
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == checkpoint_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_memory_readiness_boundary_materialization
            )

    def test_memory_readiness_boundary_rejects_service_trace_without_owner_boundary_ref(self) -> None:
        service_path = validate_memo.EXAMPLES / "audit_event.service-governed-fallback.example.json"
        payload = load_json(service_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["provenance"]["source_refs"] = [
            "abyss-stack:service_degradation_receipt_v1#service:2026-04-07:hybrid-query-kag-unhealthy",
            "docs/MEMORY_READINESS_BOUNDARY.md#memory-pressure-map",
        ]
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == service_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_memory_readiness_boundary_materialization
            )

    def test_memory_object_schema_rejects_invalid_nullable_datetime(self) -> None:
        validator = validate_memo.validator_for("memory_object.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "anchor.example.json")
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
        payload = load_json(REPO_ROOT / "examples" / "anchor.example.json")
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
        payload = load_json(REPO_ROOT / "examples" / "inquiry_checkpoint.return.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("anchor_refs", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("anchor_refs" in message for message in errors))

    def test_inquiry_checkpoint_return_pack_requires_reentry_refs(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "inquiry_checkpoint.return.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("reentry_refs", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("reentry_refs" in message for message in errors))

    def test_inquiry_checkpoint_return_pack_requires_reentry_note(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "inquiry_checkpoint.return.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["return_pack"].pop("reentry_note", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("reentry_note" in message for message in errors))

    def test_bridge_schema_requires_shared_envelope_ref(self) -> None:
        validator = validate_memo.validator_for("bridge.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "bridge.kag-lift.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["bridges"].pop("shared_envelope_ref", None)

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("shared_envelope_ref" in message for message in errors))

    def test_bridge_schema_rejects_empty_outward_refs_without_route_capsule(self) -> None:
        validator = validate_memo.validator_for("bridge.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "bridge.kag-lift.example.json")
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
        payload = load_json(REPO_ROOT / "examples" / "checkpoint_to_memory_contract.example.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["mapping_rules"] = payload["mapping_rules"][:-1]

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("is too short" in message for message in errors))

    def test_checkpoint_validator_rejects_conflicting_duplicate_runtime_mappings(self) -> None:
        contract_path = validate_memo.EXAMPLES / "checkpoint_to_memory_contract.example.json"
        original_load_json = validate_memo.load_json
        payload = load_json(contract_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["mapping_rules"].append(
            {
                "runtime_surface": "transition_record",
                "runtime_refs": ["docs/MEMORY_MODEL.md#checkpoint-route-writeback"],
                "target_kind": "audit_event",
                "writeback_class": "memo_surviving_event",
                "temperature_hint": "cool",
                "review_state_default": "confirmed",
                "requires_human_review": False,
                "notes": "Conflicting duplicate mapping for regression coverage.",
            }
        )

        def side_effect(path: Path) -> dict:
            if Path(path) == contract_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_checkpoint_to_memory_contract)

    def test_runtime_writeback_targets_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_targets()

    def test_runtime_writeback_targets_surface_rejects_review_state_drift(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["review_state_default"] = "captured"
                break

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)

    def test_runtime_writeback_targets_surface_rejects_duplicate_runtime_surface(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["targets"][1]["runtime_surface"] = "checkpoint_export"

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)

    def test_runtime_writeback_targets_surface_rejects_incomplete_runtime_boundary(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["runtime_boundary"] = {}

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)

    def test_runtime_writeback_intake_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_intake()

    def test_runtime_writeback_intake_surface_rejects_owner_review_ref_drift(self) -> None:
        intake_path = validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(intake_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["targets"][0]["owner_review_refs"] = ["docs/RUNTIME_WRITEBACK_SEAM.md"]

        def side_effect(path: Path) -> dict:
            if Path(path) == intake_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_intake)

    def test_runtime_writeback_intake_surface_rejects_reviewed_candidate_posture_drift(self) -> None:
        intake_path = validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(intake_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["intake_posture"] = "capturable_runtime_export"
                break

        def side_effect(path: Path) -> dict:
            if Path(path) == intake_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_intake)

    def test_live_receipt_log_rejects_uncataloged_object_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-missing-object",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-missing-object",
                "session_ref": "session:memo-missing-object",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": "memo.decision.2099-01-01.missing",
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_catalog_entry",
                        "ref": "repo:aoa-memo/generated/memory_object_catalog.min.json#memo.decision.2099-01-01.missing",
                        "role": "catalog",
                    }
                ],
                "payload": {
                    "target_kind": "decision",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

    def test_live_receipt_log_accepts_cataloged_object_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object",
                "session_ref": "session:memo-cataloged-object",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()

    def test_live_receipt_log_rejects_cataloged_object_without_capsule_hydration(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-missing-capsule",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-missing-capsule",
                "session_ref": "session:memo-cataloged-object-missing-capsule",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
            capsules_path = validate_memo.GENERATED / "memory_object_capsules.json"
            capsules = load_json(capsules_path)
            assert isinstance(capsules, dict)
            capsules = copy.deepcopy(capsules)
            capsules["memory_objects"] = [
                item
                for item in capsules["memory_objects"]
                if isinstance(item, dict) and item.get("id") != object_id
            ]
            original_load_json = validate_memo.load_json

            def side_effect(path: Path) -> dict:
                if Path(path) == capsules_path:
                    return copy.deepcopy(capsules)
                return original_load_json(path)

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with patch.object(validate_memo, "load_json", side_effect=side_effect):
                    ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_rejects_event_kind_actor_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-actor-drift",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-actor-drift",
                "session_ref": "session:memo-cataloged-object-actor-drift",
                "actor_ref": "aoa-memo:growth-refinery-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_rejects_cataloged_object_without_expand_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-empty-sections",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-empty-sections",
                "session_ref": "session:memo-cataloged-object-empty-sections",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
            sections_path = validate_memo.GENERATED / "memory_object_sections.full.json"
            sections = load_json(sections_path)
            assert isinstance(sections, dict)
            sections = copy.deepcopy(sections)
            for item in sections["memory_objects"]:
                if isinstance(item, dict) and item.get("id") == object_id:
                    item["sections"] = []
                    break
            original_load_json = validate_memo.load_json

            def side_effect(path: Path) -> dict:
                if Path(path) == sections_path:
                    return copy.deepcopy(sections)
                return original_load_json(path)

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with patch.object(validate_memo, "load_json", side_effect=side_effect):
                    ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_rejects_payload_kind_drift_from_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-payload-kind-drift",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-payload-kind-drift",
                "session_ref": "session:memo-payload-kind-drift",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/claim.example.json",
                    "target_kind": "decision",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

    def test_live_receipt_log_accepts_reviewed_candidate_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.bridge.2026-03-23.tos-lineage-kag-candidate"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-reviewed-bridge",
                "observed_at": "2026-04-13T22:00:00Z",
                "run_ref": "run-memo-reviewed-bridge",
                "session_ref": "session:memo-reviewed-bridge",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/bridge.kag-lift.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                    {
                        "kind": "candidate_seed",
                        "ref": "repo:aoa-memo/examples/claim.tos-bridge-ready.example.json",
                        "role": "candidate-seed",
                    },
                    {
                        "kind": "review_anchor",
                        "ref": "repo:aoa-memo/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
                        "role": "writeback-anchor",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/bridge.kag-lift.example.json",
                    "runtime_surface": "distillation_bridge_candidate",
                    "target_kind": "bridge",
                    "writeback_class": "reviewed_candidate",
                    "review_state": "proposed",
                    "writeback_anchor_ref": "repo:aoa-memo/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()

    def test_live_receipt_log_rejects_reviewed_candidate_without_runtime_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.pattern.2026-04-02.alpha-remediation-recurrence"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-reviewed-pattern-missing-runtime-surface",
                "observed_at": "2026-04-13T22:00:00Z",
                "run_ref": "run-memo-reviewed-pattern-missing-runtime-surface",
                "session_ref": "session:memo-reviewed-pattern-missing-runtime-surface",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/pattern.phase-alpha-remediation-recurrence.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                    {
                        "kind": "review_anchor",
                        "ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
                        "role": "writeback-anchor",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/pattern.phase-alpha-remediation-recurrence.example.json",
                    "target_kind": "pattern",
                    "writeback_class": "reviewed_candidate",
                    "review_state": "confirmed",
                    "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

    def test_live_receipt_log_accepts_growth_refinery_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            lane_ref = "growth_refinery_failure_lesson"
            receipt = {
                "event_kind": "memo_growth_writeback_receipt",
                "event_id": "evt-memo-growth-failure-lesson",
                "observed_at": "2026-04-14T00:05:00Z",
                "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
                "session_ref": "session:memo-growth-refinery-writeback",
                "actor_ref": "aoa-memo:growth-refinery-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "support_memory",
                    "id": "memo:session-growth-cycle-owner-reanchor-first",
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "support_memory",
                        "ref": "repo:aoa-memo/examples/failure_lesson_memory.lineage.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "growth_lane_entry",
                        "ref": f"repo:aoa-memo/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                        "role": "lane",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-playbooks:review_note_v1#AOA-P-0025:owner-reanchor",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-sdk:closeout_context_lineage_v1#session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "Agents-of-Abyss:reviewable_growth_refinery_v1#owner-boundaries",
                        "role": "required-evidence",
                    },
                ],
                "payload": {
                    "growth_lane_ref": lane_ref,
                    "source_example_ref": "examples/failure_lesson_memory.lineage.example.json",
                    "target_kind": "failure_lesson",
                    "review_status": "reviewed",
                    "writeback_class": "growth_refinery_memory",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()

    def test_live_receipt_log_rejects_growth_refinery_receipt_without_lane_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            receipt = {
                "event_kind": "memo_growth_writeback_receipt",
                "event_id": "evt-memo-growth-recovery-pattern",
                "observed_at": "2026-04-14T00:05:00Z",
                "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
                "session_ref": "session:memo-growth-refinery-writeback",
                "actor_ref": "aoa-memo:growth-refinery-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "support_memory",
                    "id": "memo:session-growth-cycle-playbook-reanchor",
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "support_memory",
                        "ref": "repo:aoa-memo/examples/recovery_pattern_memory.lineage.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
                        "role": "required-evidence",
                    },
                ],
                "payload": {
                    "source_example_ref": "examples/recovery_pattern_memory.lineage.example.json",
                    "target_kind": "recovery_pattern",
                    "review_status": "reviewed",
                    "writeback_class": "growth_refinery_memory",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

    def test_questbook_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_questbook_surface()

    def test_questbook_surface_skips_missing_external_eval_schemas(self) -> None:
        missing_evals_root = REPO_ROOT / ".tmp" / "missing-aoa-evals"

        validate_memo.external_quest_schema_validator.cache_clear()
        self.addCleanup(validate_memo.external_quest_schema_validator.cache_clear)
        with patch.object(validate_memo, "AOA_EVALS_ROOT", missing_evals_root):
            with io.StringIO() as stdout, io.StringIO() as stderr:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    validate_memo.validate_questbook_surface()

    def test_questbook_surface_skips_missing_external_orchestrator_catalog(self) -> None:
        missing_agents_root = REPO_ROOT / ".tmp" / "missing-aoa-agents"

        validate_memo.load_live_orchestrator_class_ids.cache_clear()
        self.addCleanup(validate_memo.load_live_orchestrator_class_ids.cache_clear)
        with patch.object(validate_memo, "AOA_AGENTS_ROOT", missing_agents_root):
            with io.StringIO() as stdout, io.StringIO() as stderr:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    validate_memo.validate_questbook_surface()

    def test_questbook_surface_rejects_missing_tracked_reference(self) -> None:
        questbook_path = validate_memo.QUESTBOOK_PATH
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == questbook_path:
                return text.replace("AOA-MEM-Q-0002", "AOA-MEM-Q-9999")
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)

    def test_questbook_surface_rejects_source_owned_boundary_phrase_loss(self) -> None:
        doc_path = validate_memo.QUESTBOOK_DOC
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == doc_path:
                return text.replace("quest state remains source-owned", "quest state remains external")
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)

    def test_questbook_surface_rejects_quest_id_mismatch(self) -> None:
        quest_path = validate_memo.ROOT / "quests" / "AOA-MEM-Q-0002.yaml"
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["id"] = "AOA-MEM-Q-9999"
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)

    def test_questbook_surface_accepts_additive_chronicle_quest(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_questbook_surface()

    def test_quest_chronicle_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_quest_chronicle_surface()

    def test_quest_chronicle_surface_rejects_missing_stage_recall_cue(self) -> None:
        chronicle_path = validate_memo.EXAMPLES / "quest_chronicle.example.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> object:
            payload = original_load_json(path)
            if Path(path) == chronicle_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["stage_witness"][0].pop("next_recall_cue", None)
            return payload

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_quest_chronicle_surface)

    def test_routing_memory_adoption_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_routing_memory_adoption_surface()

    def test_routing_memory_adoption_surface_rejects_router_contract_without_capsule_step(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.router.semantic.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> object:
            payload = original_load_json(path)
            if Path(path) == recall_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload.pop("capsule_surface", None)
            return payload

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_routing_memory_adoption_surface)

    def test_playbook_memory_scope_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_playbook_memory_scope_surface()

    def test_playbook_memory_scope_surface_rejects_widened_working_scope(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.working.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> object:
            payload = original_load_json(path)
            if Path(path) == recall_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["allowed_scopes"] = ["thread", "session", "project", "ecosystem"]
            return payload

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_playbook_memory_scope_surface)

    def test_self_agency_continuity_writeback_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_self_agency_continuity_writeback_surface()

    def test_self_agency_continuity_writeback_rejects_unhydrated_memory_object_id(self) -> None:
        thread_path = validate_memo.EXAMPLES / "provenance_thread.self-agency-continuity.example.json"
        original_load_json = validate_memo.load_json
        payload = load_json(thread_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["memory_object_ids"].append("memo.state.2099-01-01.missing-continuity-relay")

        def side_effect(path: Path) -> object:
            if Path(path) == thread_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_self_agency_continuity_writeback_surface
            )

    def test_questbook_surface_rejects_missing_additive_anchor_doc(self) -> None:
        quest_path = validate_memo.ROOT / "quests" / "AOA-MEM-Q-0003.yaml"
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["anchor_ref"] = {
                    "artifact": "quest_chronicle_writeback",
                    "ref": "docs/DOES_NOT_EXIST.md",
                }
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)

    def test_questbook_surface_rejects_listed_additive_quest_without_file(self) -> None:
        questbook_path = validate_memo.QUESTBOOK_PATH
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == questbook_path:
                return text + "\n- `AOA-MEM-Q-9999` - stale additive quest reference\n"
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)

    def test_validate_registry_requires_recurrence_support_docs(self) -> None:
        registry_path = validate_memo.GENERATED / "memo_registry.min.json"
        original_load_json = validate_memo.load_json
        payload = load_json(registry_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["core_docs"] = [
            ref
            for ref in payload["core_docs"]
            if ref != "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md"
        ]

        def side_effect(path: Path) -> dict:
            if Path(path) == registry_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_registry)

    def test_validate_registry_rejects_release_version_drift(self) -> None:
        registry_path = validate_memo.GENERATED / "memo_registry.min.json"
        original_load_json = validate_memo.load_json
        payload = load_json(registry_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["version"] = "9.9.9-draft"

        def side_effect(path: Path) -> dict:
            if Path(path) == registry_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_registry)

    def test_guardrail_validator_handles_non_string_case_ids_without_type_error(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["case_id"] = []
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_precision_case_without_surface_family(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["input_refs"] = [
            "examples/recall_contract.router.semantic.json",
            "docs/PLAYBOOK_MEMORY_SCOPES.md",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_precision_case_without_recall_contract_ref(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["input_refs"] = [
            "generated/memory_catalog.min.json",
            "generated/memory_capsules.json",
            "generated/memory_sections.full.json",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_provenance_case_without_provenance_thread(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][1]["input_refs"] = [
            "examples/claim.tos-bridge-ready.example.json",
            "examples/bridge.kag-lift.example.json",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_staleness_case_without_lifecycle_examples(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][2]["input_refs"] = [
            "docs/LIFECYCLE.md",
            "docs/MEMORY_TRUST_POSTURE.md",
            "docs/MEMORY_TEMPERATURES.md",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_missing_recall_precision_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["focus"] = "precision_shadow"
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_missing_provenance_fidelity_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][1]["focus"] = "provenance_shadow"
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_missing_staleness_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][2]["focus"] = "staleness_shadow"
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_contradiction_case_without_active_claim(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][3]["input_refs"] = [
            "examples/claim.superseded.example.json",
            "examples/claim.retracted.example.json",
            "docs/LIFECYCLE.md",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_permission_case_without_role_boundary(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][4]["input_refs"] = [
            "docs/BOUNDARIES.md#aoa-agents",
            "docs/OPERATIONAL_BOUNDARY.md#consumer-contracts",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_promotion_case_without_bridge_candidate(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][5]["input_refs"] = [
            "docs/WRITEBACK_TEMPERATURE_POLICY.md",
            "docs/AGENT_MEMORY_POSTURE_SEAM.md#boundary-rule",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_guardrail_validator_rejects_merge_case_without_provenance_thread(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][6]["input_refs"] = [
            "examples/episode.tos-interpretation.example.json",
            "examples/claim.tos-bridge-ready.example.json",
            "examples/bridge.kag-lift.example.json",
        ]
        self.assert_guardrail_payload_fails(payload)

    def test_kag_export_validator_rejects_wrong_owner_repo(self) -> None:
        payload = self.kag_export_payload()
        payload["owner_repo"] = "aoa-kag"
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_wrong_entry_surface(self) -> None:
        payload = self.kag_export_payload()
        payload["entry_surface"]["path"] = "generated/memory_object_sections.full.json"
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_missing_tos_supporting_input(self) -> None:
        payload = self.kag_export_payload()
        payload["source_inputs"] = [payload["source_inputs"][0]]
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_wrong_section_handles(self) -> None:
        payload = self.kag_export_payload()
        payload["section_handles"] = [
            "identity-and-recall",
            "bridges-and-access",
        ]
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_missing_required_direct_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = payload["direct_relations"][:-1]
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_missing_source_memory_object_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = [
            relation
            for relation in payload["direct_relations"]
            if relation["relation_type"] != "source_memory_object"
        ]
        self.assert_kag_export_payload_fails(payload)

    def test_kag_export_validator_rejects_missing_provenance_thread_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = [
            relation
            for relation in payload["direct_relations"]
            if relation["relation_type"] != "provenance_thread"
        ]
        self.assert_kag_export_payload_fails(payload)

    def test_return_ready_recall_contract_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_recall_contract_example(
                    "recall_contract.object.working.return.json",
                    expected_mode="working",
                    expected_allowed_scopes=["thread", "session", "project"],
                    expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
                    expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
                    expected_inspect_surface="generated/memory_object_catalog.min.json",
                    expected_capsule_surface="generated/memory_object_capsules.json",
                    expected_expand_surface="generated/memory_object_sections.full.json",
                    expected_source_route_required=False,
                    expected_checkpoint_continuity_supported=True,
                    expected_return_ready=True,
                    expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                    expected_support_artifact_refs=[
                        "schemas/inquiry_checkpoint.schema.json",
                        "schemas/checkpoint-to-memory-contract.schema.json",
                        "docs/RUNTIME_WRITEBACK_SEAM.md",
                        "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
                    ],
                )

    def test_recall_contract_schema_rejects_invalid_preferred_anchor_kind(self) -> None:
        validator = validate_memo.validator_for("recall_contract.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "recall_contract.object.working.return.json")
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["preferred_anchor_kinds"] = ["state_capsule", "router_capsule"]

        errors = [error.message for error in validator.iter_errors(payload)]

        self.assertTrue(any("is not one of" in message for message in errors))

    def test_return_ready_recall_contract_rejects_bad_support_artifact_ref(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.object.working.return.json"
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
                expected_inspect_surface="generated/memory_object_catalog.min.json",
                expected_capsule_surface="generated/memory_object_capsules.json",
                expected_expand_surface="generated/memory_object_sections.full.json",
                expected_source_route_required=False,
                expected_checkpoint_continuity_supported=True,
                expected_return_ready=True,
                expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                expected_support_artifact_refs=["docs/DOES_NOT_EXIST.md"],
            )

    def test_return_ready_recall_contract_requires_capsule_surface(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.object.working.return.json"
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
                expected_inspect_surface="generated/memory_object_catalog.min.json",
                expected_capsule_surface="generated/memory_object_capsules.json",
                expected_expand_surface="generated/memory_object_sections.full.json",
                expected_source_route_required=False,
                expected_checkpoint_continuity_supported=True,
                expected_return_ready=True,
                expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                expected_support_artifact_refs=[
                    "schemas/inquiry_checkpoint.schema.json",
                    "schemas/checkpoint-to-memory-contract.schema.json",
                    "docs/RUNTIME_WRITEBACK_SEAM.md",
                    "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
                ],
            )

    def test_router_semantic_recall_contract_requires_capsule_surface(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.router.semantic.json"
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
                expected_inspect_surface="generated/memory_catalog.min.json",
                expected_capsule_surface="generated/memory_capsules.json",
                expected_expand_surface="generated/memory_sections.full.json",
                expected_source_route_required=True,
            )

    def test_router_surface_validator_rejects_wrong_capsule_path(self) -> None:
        recall_path = validate_memory_surfaces.EXAMPLES / "recall_contract.router.semantic.json"
        original_load_json = validate_memory_surfaces.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["capsule_surface"] = "generated/memory_object_capsules.json"

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memory_surfaces, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memory_surfaces.validate_router_recall_contract,
                recall_path,
                "semantic",
                "generated/memory_capsules.json",
            )

    def test_object_surface_validator_rejects_wrong_capsule_path(self) -> None:
        recall_path = validate_memory_object_surfaces.EXAMPLES / "recall_contract.object.semantic.json"
        original_load_json = validate_memory_object_surfaces.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["capsule_surface"] = "generated/memory_capsules.json"

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memory_object_surfaces, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memory_object_surfaces.validate_recall_contract,
                recall_path,
                expected_mode="semantic",
                expected_allowed_scopes=["repo", "project", "ecosystem"],
                expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
                expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
                expected_source_route_required=True,
                expected_capsule_surface="generated/memory_object_capsules.json",
            )

    def test_recall_contract_rejects_nonexistent_capsule_surface_ref(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall_contract.object.lineage.json"
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
                expected_inspect_surface="generated/memory_object_catalog.min.json",
                expected_capsule_surface="generated/DOES_NOT_EXIST.json",
                expected_expand_surface="generated/memory_object_sections.full.json",
                expected_source_route_required=True,
            )

    def test_surface_alignment_rejects_duplicate_ids(self) -> None:
        original_load_json = validate_memory_surfaces.load_json
        capsules_path = validate_memory_surfaces.GENERATED / "memory_capsules.json"
        capsules = load_json(capsules_path)
        assert isinstance(capsules, dict)
        capsules = copy.deepcopy(capsules)
        capsules["memo_surfaces"].append(copy.deepcopy(capsules["memo_surfaces"][0]))

        def side_effect(path: Path) -> dict:
            if Path(path) == capsules_path:
                return copy.deepcopy(capsules)
            return original_load_json(path)

        with patch.object(validate_memory_surfaces, "load_json", side_effect=side_effect):
            context = self.assert_system_exit_quietly(validate_memory_surfaces.validate_surface_alignment)

        self.assertIn("duplicate ids detected", str(context))

    def test_object_surface_validator_rejects_scope_classes_drift(self) -> None:
        original_load_json = validate_memory_object_surfaces.load_json
        full_catalog_path = validate_memory_object_surfaces.FULL_CATALOG_PATH
        full_catalog = load_json(full_catalog_path)
        assert isinstance(full_catalog, dict)
        full_catalog = copy.deepcopy(full_catalog)
        full_catalog["memory_objects"][0]["scope_classes"] = ["session"]

        def side_effect(path: Path) -> dict:
            if Path(path) == full_catalog_path:
                return copy.deepcopy(full_catalog)
            return original_load_json(path)

        with patch.object(validate_memory_object_surfaces, "load_json", side_effect=side_effect):
            context = self.assert_system_exit_quietly(
                validate_memory_object_surfaces.validate_full_catalog,
                full_catalog,
                {item["id"] for item in full_catalog["memory_objects"]},
            )

        self.assertIn("scope_classes", str(context))


if __name__ == "__main__":
    unittest.main()
