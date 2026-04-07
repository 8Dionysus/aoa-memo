from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


def load_module(script_name: str):
    path = SCRIPTS_ROOT / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_memory_object_surfaces = load_module("generate_memory_object_surfaces.py")
generate_kag_export = load_module("generate_kag_export.py")
generate_runtime_writeback_targets = load_module("generate_runtime_writeback_targets.py")
generate_runtime_writeback_intake = load_module("generate_runtime_writeback_intake.py")
generate_runtime_writeback_governance = load_module("generate_runtime_writeback_governance.py")

GENERATED_ROOT = REPO_ROOT / "generated"
EXAMPLES_ROOT = REPO_ROOT / "examples"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class MemoDownstreamFeedContractsTests(unittest.TestCase):
    def test_doctrine_family_contracts_stay_aligned(self) -> None:
        catalog = load_json(GENERATED_ROOT / "memory_catalog.min.json")
        capsules = load_json(GENERATED_ROOT / "memory_capsules.json")
        sections = load_json(GENERATED_ROOT / "memory_sections.full.json")

        self.assertEqual(
            set(catalog.keys()),
            {"catalog_version", "source_of_truth", "memo_surfaces"},
        )
        self.assertEqual(
            set(capsules.keys()),
            {"capsule_version", "source_of_truth", "memo_surfaces"},
        )
        self.assertEqual(
            set(sections.keys()),
            {"sections_version", "source_of_truth", "memo_surfaces"},
        )
        self.assertEqual(catalog["catalog_version"], 1)
        self.assertEqual(capsules["capsule_version"], 1)
        self.assertEqual(sections["sections_version"], 1)

        catalog_ids = [item["id"] for item in catalog["memo_surfaces"]]
        capsule_ids = [item["id"] for item in capsules["memo_surfaces"]]
        section_ids = [item["id"] for item in sections["memo_surfaces"]]

        self.assertEqual(catalog_ids, capsule_ids)
        self.assertEqual(catalog_ids, section_ids)
        self.assertEqual(catalog_ids, sorted(catalog_ids))
        self.assertEqual(len(catalog_ids), len(set(catalog_ids)))

    def test_object_family_matches_generator_outputs(self) -> None:
        expected = generate_memory_object_surfaces.build_surface_family()

        for name, payload in expected.items():
            current = load_json(GENERATED_ROOT / name)
            self.assertEqual(current, payload)

        min_catalog = load_json(GENERATED_ROOT / "memory_object_catalog.min.json")
        capsules = load_json(GENERATED_ROOT / "memory_object_capsules.json")
        sections = load_json(GENERATED_ROOT / "memory_object_sections.full.json")

        self.assertEqual(
            set(min_catalog.keys()),
            {"catalog_kind", "catalog_version", "memory_objects", "source_of_truth"},
        )
        self.assertEqual(
            set(capsules.keys()),
            {"capsule_version", "memory_objects", "source_of_truth"},
        )
        self.assertEqual(
            set(sections.keys()),
            {"memory_objects", "sections_version", "source_of_truth"},
        )
        self.assertEqual(min_catalog["catalog_kind"], "min")
        self.assertEqual(min_catalog["catalog_version"], 1)
        self.assertEqual(capsules["capsule_version"], 1)
        self.assertEqual(sections["sections_version"], 1)

        object_ids = [item["id"] for item in min_catalog["memory_objects"]]
        capsule_ids = [item["id"] for item in capsules["memory_objects"]]
        section_ids = [item["id"] for item in sections["memory_objects"]]

        self.assertEqual(capsule_ids, section_ids)
        self.assertTrue(set(object_ids).issubset(capsule_ids))

        shared_scope_classes = set(generate_memory_object_surfaces.SHARED_SCOPE_CLASSES)
        for item in min_catalog["memory_objects"]:
            self.assertIn("scope_classes", item)
            self.assertTrue(item["scope_classes"])
            self.assertTrue(set(item["scope_classes"]).issubset(shared_scope_classes))

    def test_kag_export_stays_generator_backed(self) -> None:
        current = load_json(GENERATED_ROOT / "kag_export.min.json")
        expected = generate_kag_export.build_kag_export_payload()

        self.assertEqual(current, expected)
        self.assertEqual(
            set(current.keys()),
            {
                "owner_repo",
                "kind",
                "object_id",
                "primary_question",
                "summary_50",
                "summary_200",
                "source_inputs",
                "entry_surface",
                "section_handles",
                "direct_relations",
                "provenance_note",
                "non_identity_boundary",
            },
        )
        self.assertEqual(current["owner_repo"], "aoa-memo")
        self.assertEqual(current["kind"], "bridge")
        self.assertEqual(current["entry_surface"]["path"], "generated/memory_object_capsules.json")
        self.assertEqual(
            [item["role"] for item in current["source_inputs"]],
            ["primary", "supporting"],
        )

    def test_recall_contract_examples_keep_expected_surface_family_routes(self) -> None:
        expected = {
            "recall_contract.semantic.json": {
                "inspect_surface": "generated/memo_registry.min.json",
                "capsule_surface": None,
                "expand_surface": "docs/MEMORY_MODEL.md",
                "mode": "semantic",
            },
            "recall_contract.router.semantic.json": {
                "inspect_surface": "generated/memory_catalog.min.json",
                "capsule_surface": "generated/memory_capsules.json",
                "expand_surface": "generated/memory_sections.full.json",
                "mode": "semantic",
            },
            "recall_contract.working.json": {
                "inspect_surface": "generated/memory_catalog.min.json",
                "capsule_surface": None,
                "expand_surface": "docs/RUNTIME_WRITEBACK_SEAM.md",
                "mode": "working",
            },
            "recall_contract.lineage.json": {
                "inspect_surface": "generated/memory_catalog.min.json",
                "capsule_surface": None,
                "expand_surface": "docs/KAG_TOS_BRIDGE_CONTRACT.md",
                "mode": "lineage",
            },
            "recall_contract.router.lineage.json": {
                "inspect_surface": "generated/memory_catalog.min.json",
                "capsule_surface": "generated/memory_capsules.json",
                "expand_surface": "generated/memory_sections.full.json",
                "mode": "lineage",
            },
            "recall_contract.object.working.json": {
                "inspect_surface": "generated/memory_object_catalog.min.json",
                "capsule_surface": None,
                "expand_surface": "generated/memory_object_sections.full.json",
                "mode": "working",
            },
            "recall_contract.object.working.return.json": {
                "inspect_surface": "generated/memory_object_catalog.min.json",
                "capsule_surface": "generated/memory_object_capsules.json",
                "expand_surface": "generated/memory_object_sections.full.json",
                "mode": "working",
            },
            "recall_contract.object.semantic.json": {
                "inspect_surface": "generated/memory_object_catalog.min.json",
                "capsule_surface": "generated/memory_object_capsules.json",
                "expand_surface": "generated/memory_object_sections.full.json",
                "mode": "semantic",
            },
            "recall_contract.object.lineage.json": {
                "inspect_surface": "generated/memory_object_catalog.min.json",
                "capsule_surface": "generated/memory_object_capsules.json",
                "expand_surface": "generated/memory_object_sections.full.json",
                "mode": "lineage",
            },
        }

        for name, contract in expected.items():
            payload = load_json(EXAMPLES_ROOT / name)
            self.assertEqual(payload["mode"], contract["mode"])
            self.assertEqual(payload["inspect_surface"], contract["inspect_surface"])
            self.assertEqual(payload.get("capsule_surface"), contract["capsule_surface"])
            self.assertEqual(payload.get("expand_surface"), contract["expand_surface"])

    def test_checkpoint_to_memory_contract_keeps_execution_safe_writeback_mapping(self) -> None:
        payload = load_json(EXAMPLES_ROOT / "checkpoint_to_memory_contract.example.json")

        self.assertEqual(payload["contract_type"], "checkpoint_to_memory_contract")
        self.assertEqual(payload["contract_id"], "aoa-memo.runtime-writeback.v1")
        self.assertEqual(payload["checkpoint_artifact"]["artifact_name"], "inquiry_checkpoint")
        self.assertEqual(
            payload["checkpoint_artifact"]["schema_ref"],
            "schemas/inquiry_checkpoint.schema.json",
        )
        self.assertEqual(payload["checkpoint_artifact"]["posture"], "route_artifact_not_memory_object")
        self.assertEqual(payload["runtime_boundary"]["scratchpad_posture"], "runtime_local_only")
        self.assertEqual(payload["runtime_boundary"]["checkpoint_export_kind"], "state_capsule")
        self.assertEqual(payload["runtime_boundary"]["distillation_review_posture"], "review_required")
        self.assertEqual(
            payload["runtime_boundary"]["review_boundary_refs"],
            [
                "docs/WRITEBACK_TEMPERATURE_POLICY.md#writeback-classes",
                "docs/MEMORY_MODEL.md#checkpoint-route-writeback",
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
            "docs/WRITEBACK_TEMPERATURE_POLICY.md#inquiry-checkpoint-packs",
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
        current = load_json(GENERATED_ROOT / "runtime_writeback_targets.min.json")
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
        current = load_json(GENERATED_ROOT / "runtime_writeback_intake.min.json")
        expected = generate_runtime_writeback_intake.build_runtime_writeback_intake_payload()

        self.assertEqual(current, expected)
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-memo")
        self.assertEqual(
            current["source_of_truth"],
            {
                "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
                "checkpoint_to_memory_contract": "examples/checkpoint_to_memory_contract.example.json",
                "runtime_writeback_seam": "docs/RUNTIME_WRITEBACK_SEAM.md",
                "quest_evidence_writeback": "docs/QUEST_EVIDENCE_WRITEBACK.md",
            },
        )

        runtime_surfaces = [item["runtime_surface"] for item in current["targets"]]
        self.assertEqual(runtime_surfaces, sorted(runtime_surfaces))
        self.assertEqual(len(runtime_surfaces), len(set(runtime_surfaces)))
        self.assertTrue(all(item["owner_review_refs"] for item in current["targets"]))
        self.assertTrue(
            all("docs/RUNTIME_WRITEBACK_SEAM.md" in item["owner_review_refs"] for item in current["targets"])
        )
        self.assertTrue(
            all("docs/QUEST_EVIDENCE_WRITEBACK.md" in item["owner_review_refs"] for item in current["targets"])
        )

        reviewed_candidates = [
            item for item in current["targets"] if item["writeback_class"] == "reviewed_candidate"
        ]
        self.assertTrue(reviewed_candidates)
        self.assertTrue(all(item["requires_human_review"] for item in reviewed_candidates))
        self.assertTrue(all(item["review_state_default"] == "proposed" for item in reviewed_candidates))
        self.assertTrue(all(item["intake_posture"] == "review_candidate_only" for item in reviewed_candidates))

    def test_runtime_writeback_governance_surface_stays_generator_backed(self) -> None:
        current = load_json(GENERATED_ROOT / "runtime_writeback_governance.min.json")
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
                "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
                "runtime_writeback_intake": "generated/runtime_writeback_intake.min.json",
            },
        )
        self.assertTrue(all(item["governance_passed"] for item in current["targets"]))
        self.assertTrue(all(item["in_writeback_targets"] for item in current["targets"]))
        self.assertTrue(all(item["in_writeback_intake"] for item in current["targets"]))
        self.assertTrue(all(item["blockers"] == [] for item in current["targets"]))

        by_surface = {item["runtime_surface"]: item for item in current["targets"]}
        self.assertEqual(by_surface["checkpoint_export"]["intake_posture"], "capturable_runtime_export")
        self.assertEqual(by_surface["distillation_claim_candidate"]["intake_posture"], "review_candidate_only")

    def test_repo_docs_align_on_contract_hardening_stage(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        charter = (REPO_ROOT / "CHARTER.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("`aoa-memo` is in contract hardening.", readme)
        self.assertIn("This repository is in contract hardening.", charter)
        self.assertNotIn("This repository is in bootstrap.", charter)
        self.assertIn("`aoa-memo` is in contract hardening.", roadmap)

    def test_readme_surfaces_read_only_validation_and_targeted_generation_routes(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        for command in (
            "python scripts/validate_memo.py",
            "python scripts/validate_memory_surfaces.py",
            "python scripts/validate_memory_object_surfaces.py",
            "python scripts/validate_lifecycle_audit_examples.py",
            "python -m pytest -q tests",
        ):
            self.assertIn(command, readme)

        for command in (
            "python scripts/generate_memory_object_surfaces.py",
            "python scripts/generate_kag_export.py",
            "python scripts/generate_runtime_writeback_targets.py",
            "python scripts/generate_runtime_writeback_intake.py",
            "python scripts/generate_phase_alpha_writeback_map.py",
        ):
            self.assertIn(command, readme)

        self.assertIn("git status -sb", readme)

    def test_contributing_surfaces_current_validation_battery(self) -> None:
        contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

        for command in (
            "python scripts/validate_memo.py",
            "python scripts/validate_memory_surfaces.py",
            "python scripts/validate_memory_object_surfaces.py",
            "python scripts/validate_lifecycle_audit_examples.py",
            "python -m pytest -q tests",
        ):
            self.assertIn(command, contributing)

        self.assertIn("git status -sb", contributing)


if __name__ == "__main__":
    unittest.main()
