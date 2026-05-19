from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]


class LineageHarvestMechanicTestCase(unittest.TestCase):
    def test_lineage_harvest_registers_active_doc(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        lineage_harvest = packages["lineage-harvest"]

        self.assertEqual("Lineage Harvest Memo Mechanic", lineage_harvest["title"])
        self.assertIn("operation", lineage_harvest)
        self.assertEqual(["PATTERN_LINEAGE_MEMORY.md"], lineage_harvest["docs"])

        active_doc = (
            REPO_ROOT
            / "mechanics"
            / "lineage-harvest"
            / "docs"
            / "PATTERN_LINEAGE_MEMORY.md"
        )
        self.assertTrue(active_doc.is_file())
        self.assertFalse((REPO_ROOT / "docs" / "PATTERN_LINEAGE_MEMORY.md").exists())

    def test_lineage_harvest_preserves_stronger_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "lineage-harvest" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "Agents-of-Abyss",
            "source owner",
            "aoa-evals",
            "aoa-stats",
            "aoa-kag",
            "Tree-of-Sophia",
            "aoa-routing",
            "aoa-agents",
            "aoa-playbooks",
            "abyss-stack",
            "without making memo the federation authority",
            "KAG promoter",
            "ToS canon",
            "runtime watchtower",
        ):
            self.assertIn(snippet, readme)

    def test_lineage_harvest_keeps_public_contracts_mechanic_owned(self) -> None:
        parts = (REPO_ROOT / "mechanics" / "lineage-harvest" / "PARTS.md").read_text(
            encoding="utf-8"
        )
        for path in (
            "mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json",
            "mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json",
            "mechanics/governance/parts/federation-boundary/examples/federation_memory_gate_decision.example.json",
            "tests/test_experience_wave3_seed_contracts.py",
        ):
            self.assertIn(path, parts)
            self.assertTrue((REPO_ROOT / path).is_file())

    def test_lineage_refs_point_to_active_mechanic_docs(self) -> None:
        active_ref = "mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md"

        registry = json.loads((REPO_ROOT / "generated" / "memo_registry.min.json").read_text())
        self.assertIn(active_ref, registry["core_docs"])
        self.assertIn("mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json", registry["schemas"])

        catalog = json.loads((REPO_ROOT / "generated" / "memory_catalog.min.json").read_text())
        surfaces = {item["id"]: item for item in catalog["memo_surfaces"]}
        self.assertEqual(
            "mechanics/lineage-harvest/README.md",
            surfaces["AOA-M-0015"]["source_path"],
        )

    def test_lineage_harvest_stays_out_of_adjacent_mechanics(self) -> None:
        for slug in (
            "recurrence-support",
            "governance",
            "writeback",
            "retention",
            "adoption",
        ):
            self.assertFalse(
                (REPO_ROOT / "mechanics" / slug / "docs" / "PATTERN_LINEAGE_MEMORY.md").exists()
            )


if __name__ == "__main__":
    unittest.main()
