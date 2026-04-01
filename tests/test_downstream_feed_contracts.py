from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


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
                "capsule_surface": None,
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


if __name__ == "__main__":
    unittest.main()
