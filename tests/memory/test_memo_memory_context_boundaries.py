from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoMemoryContextBoundaryTestCase(MemoValidatorTestCase):
    def test_memory_readiness_boundary_materialization_validates(self) -> None:
        validate_memo.validate_memory_readiness_boundary_materialization()
    def test_memory_readiness_boundary_rejects_overlapping_delta_refs(self) -> None:
        checkpoint_path = validate_memo.example_path_for("inquiry_checkpoint.return.example.json")
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
        service_path = validate_memo.EXAMPLES / "lifecycle" / "audit_event.service-governed-fallback.example.json"
        payload = load_json(service_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["provenance"]["source_refs"] = [
            "abyss-stack:service_degradation_receipt_v1#service:2026-04-07:hybrid-query-kag-unhealthy",
            "mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md#memory-pressure-map",
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
    def test_checkpoint_validator_rejects_conflicting_duplicate_runtime_mappings(self) -> None:
        contract_path = validate_memo.example_path_for("checkpoint_to_memory_contract.example.json")
        original_load_json = validate_memo.load_json
        payload = load_json(contract_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["mapping_rules"].append(
            {
                "runtime_surface": "transition_record",
                "runtime_refs": ["docs/memory/MEMORY_MODEL.md#checkpoint-route-writeback"],
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
    def test_quest_chronicle_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_quest_chronicle_surface()
    def test_quest_chronicle_surface_rejects_missing_stage_recall_cue(self) -> None:
        chronicle_path = validate_memo.example_path_for("quest_chronicle.example.json")
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
    def test_validate_registry_requires_recurrence_support_docs(self) -> None:
        registry_path = validate_memo.GENERATED / "memory" / "memo_registry.min.json"
        original_load_json = validate_memo.load_json
        payload = load_json(registry_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["core_docs"] = [
            ref
            for ref in payload["core_docs"]
            if ref != "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md"
        ]

        def side_effect(path: Path) -> dict:
            if Path(path) == registry_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_registry)
    def test_validate_registry_rejects_release_version_drift(self) -> None:
        registry_path = validate_memo.GENERATED / "memory" / "memo_registry.min.json"
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
