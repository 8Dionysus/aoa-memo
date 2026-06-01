from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from downstream_feed_contracts_support import *  # noqa: F401,F403


class MemoDownstreamFeedRuntimeWritebackTests(unittest.TestCase):
    def test_checkpoint_to_memory_contract_keeps_execution_safe_writeback_mapping(self) -> None:
        payload = load_json(CHECKPOINT_EXAMPLES_ROOT / "checkpoint_to_memory_contract.example.json")

        self.assertEqual(payload["contract_type"], "checkpoint_to_memory_contract")
        self.assertEqual(payload["contract_id"], "aoa-memo.runtime-writeback.v1")
        self.assertEqual(payload["checkpoint_artifact"]["artifact_name"], "inquiry_checkpoint")
        self.assertEqual(
            payload["checkpoint_artifact"]["schema_ref"],
            "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
        )
        self.assertEqual(payload["checkpoint_artifact"]["posture"], "route_artifact_not_memory_object")
        self.assertEqual(payload["runtime_boundary"]["scratchpad_posture"], "runtime_local_only")
        self.assertEqual(payload["runtime_boundary"]["checkpoint_export_kind"], "state_capsule")
        self.assertEqual(payload["runtime_boundary"]["distillation_review_posture"], "review_required")
        self.assertEqual(
            payload["runtime_boundary"]["review_boundary_refs"],
            [
                "mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md#writeback-classes",
                "docs/memory/MEMORY_MODEL.md#checkpoint-route-writeback",
                "repo:aoa-agents/docs/AGENT_MEMORY_POSTURE.md",
            ],
        )

        mappings = payload["mapping_rules"]
        self.assertEqual(
            [
                (item["runtime_surface"], item["target_kind"], item["writeback_class"])
                for item in mappings
            ],
            [
                ("checkpoint_export", "state_capsule", "checkpoint_export"),
                ("approval_record", "decision", "memo_surviving_event"),
                ("transition_record", "decision", "memo_surviving_event"),
                ("execution_trace", "episode", "memo_surviving_event"),
                ("review_trace", "audit_event", "memo_surviving_event"),
                ("distillation_claim_candidate", "claim", "reviewed_candidate"),
                ("distillation_pattern_candidate", "pattern", "reviewed_candidate"),
                ("distillation_bridge_candidate", "bridge", "reviewed_candidate"),
            ],
        )

        checkpoint_export = next(item for item in mappings if item["runtime_surface"] == "checkpoint_export")
        self.assertFalse(checkpoint_export["requires_human_review"])
        self.assertEqual(checkpoint_export["review_state_default"], "captured")
        self.assertIn(
            "mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md#inquiry-checkpoint-packs",
            checkpoint_export["runtime_refs"],
        )

        reviewed_candidates = [
            item
            for item in mappings
            if item["writeback_class"] == "reviewed_candidate"
        ]
        self.assertEqual(
            [item["target_kind"] for item in reviewed_candidates],
            ["claim", "pattern", "bridge"],
        )
        self.assertTrue(all(item["requires_human_review"] for item in reviewed_candidates))
        self.assertTrue(
            all(item["review_state_default"] == "proposed" for item in reviewed_candidates)
        )

    def test_runtime_writeback_targets_surface_stays_generator_backed(self) -> None:
        current = load_json(WRITEBACK_GENERATED_ROOT / "runtime_writeback_targets.min.json")
        expected = generate_runtime_writeback_targets.build_runtime_writeback_targets_payload()

        self.assertEqual(current, expected)
        self.assertEqual(
            set(current.keys()),
            {"schema_version", "layer", "contract_id", "source_of_truth", "runtime_boundary", "targets"},
        )
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-memo")
        self.assertEqual(current["contract_id"], "aoa-memo.runtime-writeback.v1")

        by_surface = {entry["runtime_surface"]: entry for entry in current["targets"]}
        self.assertEqual(len(by_surface), len(current["targets"]))
        self.assertEqual(by_surface["checkpoint_export"]["target_kind"], "state_capsule")
        self.assertFalse(by_surface["checkpoint_export"]["requires_human_review"])
        self.assertEqual(by_surface["distillation_claim_candidate"]["writeback_class"], "reviewed_candidate")
        self.assertTrue(by_surface["distillation_claim_candidate"]["requires_human_review"])
        self.assertTrue(all(entry["runtime_refs"] for entry in current["targets"]))

    def test_runtime_writeback_targets_generator_rejects_missing_required_mapping_field(self) -> None:
        original_read_json = generate_runtime_writeback_targets.read_json
        contract_path = generate_runtime_writeback_targets.CONTRACT_PATH
        payload = load_json(contract_path)
        self.assertIsInstance(payload, dict)
        payload = json.loads(json.dumps(payload))
        payload["mapping_rules"][0].pop("review_state_default", None)

        def side_effect(path: Path) -> object:
            if Path(path) == contract_path:
                return payload
            return original_read_json(path)

        with self.assertRaises(SystemExit):
            with patch.object(generate_runtime_writeback_targets, "read_json", side_effect=side_effect):
                generate_runtime_writeback_targets.build_runtime_writeback_targets_payload()

    def test_runtime_writeback_intake_surface_stays_generator_backed(self) -> None:
        current = load_json(WRITEBACK_GENERATED_ROOT / "runtime_writeback_intake.min.json")
        expected = generate_runtime_writeback_intake.build_runtime_writeback_intake_payload()

        self.assertEqual(current, expected)
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-memo")
        self.assertEqual(
            current["source_of_truth"],
            {
                "runtime_writeback_targets": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json",
                "checkpoint_to_memory_contract": "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json",
                "runtime_writeback_seam": "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
                "quest_evidence_writeback": "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md",
            },
        )

        runtime_surfaces = [item["runtime_surface"] for item in current["targets"]]
        self.assertEqual(runtime_surfaces, sorted(runtime_surfaces))
        self.assertEqual(len(runtime_surfaces), len(set(runtime_surfaces)))
        self.assertTrue(all(item["owner_review_refs"] for item in current["targets"]))
        self.assertTrue(
            all("mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" in item["owner_review_refs"] for item in current["targets"])
        )
        self.assertTrue(
            all("mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md" in item["owner_review_refs"] for item in current["targets"])
        )

        reviewed_candidates = [
            item for item in current["targets"] if item["writeback_class"] == "reviewed_candidate"
        ]
        self.assertTrue(reviewed_candidates)
        self.assertTrue(all(item["requires_human_review"] for item in reviewed_candidates))
        self.assertTrue(all(item["review_state_default"] == "proposed" for item in reviewed_candidates))
        self.assertTrue(all(item["intake_posture"] == "review_candidate_only" for item in reviewed_candidates))

    def test_runtime_writeback_governance_surface_stays_generator_backed(self) -> None:
        current = load_json(WRITEBACK_GENERATED_ROOT / "runtime_writeback_governance.min.json")
        expected = generate_runtime_writeback_governance.build_runtime_writeback_governance_payload()

        self.assertEqual(current, expected)
        self.assertEqual(
            set(current.keys()),
            {"schema_version", "layer", "scope", "source_of_truth", "targets"},
        )
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-memo")
        self.assertEqual(current["scope"], "runtime-writeback")
        self.assertEqual(
            current["source_of_truth"],
            {
                "runtime_writeback_targets": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json",
                "runtime_writeback_intake": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json",
            },
        )
        self.assertTrue(all(item["governance_passed"] for item in current["targets"]))
        self.assertTrue(all(item["in_writeback_targets"] for item in current["targets"]))
        self.assertTrue(all(item["in_writeback_intake"] for item in current["targets"]))
        self.assertTrue(all(item["blockers"] == [] for item in current["targets"]))

        by_surface = {item["runtime_surface"]: item for item in current["targets"]}
        self.assertEqual(by_surface["checkpoint_export"]["intake_posture"], "capturable_runtime_export")
        self.assertEqual(by_surface["distillation_claim_candidate"]["intake_posture"], "review_candidate_only")



if __name__ == "__main__":
    unittest.main()
