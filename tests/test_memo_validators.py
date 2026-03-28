from __future__ import annotations

import copy
import io
import json
import sys
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

    def test_inquiry_checkpoint_return_example_validates(self) -> None:
        validator = validate_memo.validator_for("inquiry_checkpoint.schema.json")
        payload = load_json(REPO_ROOT / "examples" / "inquiry_checkpoint.return.example.json")

        errors = [error.message for error in validator.iter_errors(payload)]

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
                expected_expand_surface="generated/memory_object_sections.full.json",
                expected_source_route_required=False,
                expected_checkpoint_continuity_supported=True,
                expected_return_ready=True,
                expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
                expected_support_artifact_refs=["docs/DOES_NOT_EXIST.md"],
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


if __name__ == "__main__":
    unittest.main()
