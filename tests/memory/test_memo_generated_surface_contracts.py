from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoGeneratedSurfaceContractTestCase(MemoValidatorTestCase):
    def test_router_surface_validator_rejects_wrong_capsule_path(self) -> None:
        recall_path = validate_memory_surfaces.EXAMPLES / "recall" / "recall_contract.router.semantic.json"
        original_load_json = validate_memory_surfaces.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["capsule_surface"] = "generated/memory-objects/memory_object_capsules.json"

        def side_effect(path: Path) -> dict:
            if Path(path) == recall_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memory_surfaces, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memory_surfaces.validate_router_recall_contract,
                recall_path,
                "semantic",
                "generated/memory/memory_capsules.json",
            )
    def test_object_surface_validator_rejects_wrong_capsule_path(self) -> None:
        recall_path = validate_memory_object_surfaces.EXAMPLES / "recall" / "recall_contract.object.semantic.json"
        original_load_json = validate_memory_object_surfaces.load_json
        payload = load_json(recall_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["capsule_surface"] = "generated/memory/memory_capsules.json"

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
                expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
            )
    def test_surface_alignment_rejects_duplicate_ids(self) -> None:
        original_load_json = validate_memory_surfaces.load_json
        capsules_path = validate_memory_surfaces.MEMORY_GENERATED / "memory_capsules.json"
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

    def test_object_surface_validator_rejects_artifact_identity_drift(self) -> None:
        full_catalog_path = validate_memory_object_surfaces.FULL_CATALOG_PATH
        full_catalog = load_json(full_catalog_path)
        assert isinstance(full_catalog, dict)
        full_catalog = copy.deepcopy(full_catalog)
        full_catalog["artifact_identity"] = {"artifact_class": "memory_truth"}

        context = self.assert_system_exit_quietly(
            validate_memory_object_surfaces.validate_full_catalog,
            full_catalog,
            {item["id"] for item in full_catalog["memory_objects"]},
        )

        self.assertIn("artifact_identity must stay stable", str(context))

    def test_memory_object_readmodel_bundle_declares_os_abyss_abi_and_slsa_route(self) -> None:
        manifest = load_json(REPO_ROOT / "docs" / "memory" / "artifact-bundles" / "memory_object_readmodels.bundle.json")
        assert isinstance(manifest, dict)

        self.assertEqual(manifest["artifact_class"], "derived_memory_object_readmodel_family")
        self.assertEqual(manifest["owner_repo"], "aoa-memo")
        self.assertEqual(
            manifest["consumer_contract"]["stable_interface"],
            "python scripts/memory/validate_abyss_machine_memory_object_bundle.py --json and abyss-machine artifacts trust-gate --artifact-class derived_memory_object_readmodel_family --consumer-intent agent --json",
        )
        self.assertIn(
            "materialized subject-store verification",
            manifest["consumer_contract"]["consumer_expectation"],
        )
        self.assertIn(
            "durable evidence promotion",
            manifest["consumer_contract"]["consumer_expectation"],
        )
        self.assertIn(
            "not proof or current truth authority",
            manifest["consumer_contract"]["consumer_expectation"],
        )
        self.assertTrue(manifest["consumer_contract"]["subject_store_required"])
        self.assertEqual(
            manifest["consumer_contract"]["admission_gate"],
            "fail_closed_consumer_admission",
        )
        self.assertEqual(
            manifest["artifact_identity"],
            {
                "artifact_class": "derived_memory_object_readmodel_family",
                "abi_epoch": "aoa_memo_memory_object_surfaces_v2",
            },
        )

        subject_paths = {
            item["path"]
            for item in manifest["artifact_subjects"]
        }
        self.assertGreaterEqual(
            subject_paths,
            {
                "generated/memory-objects/memory_object_catalog.min.json",
                "generated/memory-objects/memory_object_catalog.json",
                "generated/memory-objects/memory_object_capsules.json",
                "generated/memory-objects/memory_object_sections.full.json",
                "schemas/generated-surfaces/memory_object_catalog.schema.json",
                "examples/generated-surfaces/memory_object_surface_manifest.json",
                "scripts/memory/generate_memory_object_surfaces.py",
                "scripts/memory/validate_memory_object_surfaces.py",
                "MEMORY_INDEX.md",
                "docs/memory/MEMORY_OBJECT_PROFILES.md",
            },
        )
        commands = "\n".join(manifest["consumer_command"])
        self.assertIn("artifact-class derived_memory_object_readmodel_family", commands.replace("--", ""))
        self.assertIn("evidence-promote", commands)
        self.assertIn("materialize-subjects", commands)
        self.assertIn("trust-gate", commands)
        self.assertIn("registry-latest", commands)
        self.assertIn("--consumer-intent agent", commands)
        self.assertIn("--source-repo aoa-memo", commands)
        self.assertIn("--store-root SUBJECT_STORE_ROOT", commands)
        self.assertIn("--trust-root-mode host_managed", commands)
