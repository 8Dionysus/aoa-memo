from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_current_stage_names_landed_kag_export_slice(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        memo_registry = json.loads(
            (REPO_ROOT / "generated" / "memo_registry.min.json").read_text(encoding="utf-8")
        )

        families = {
            family["family"]
            for family in memo_registry["generated_surface_families"]
        }

        self.assertIn("kag_export", families)
        self.assertIn("The current KAG-facing adoption slice now publishes", roadmap)
        self.assertIn("`generated/kag_export.min.json`", roadmap)
        self.assertNotIn("The next KAG-facing adoption slice publishes", roadmap)

    def test_roadmap_matches_current_v0_2_1_writeback_surfaces(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        memo_registry = json.loads(
            (REPO_ROOT / "generated" / "memo_registry.min.json").read_text(encoding="utf-8")
        )

        registry_version = memo_registry["version"]
        self.assertEqual("0.2.1", registry_version)
        self.assertIn(f"v{registry_version}", readme)
        self.assertIn(f"[{registry_version}]", changelog)
        self.assertIn(f"v{registry_version}", roadmap)

        for relative_path in (
            "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
            "docs/GROWTH_REFINERY_WRITEBACK.md",
            "docs/QUEST_CHRONICLE_WRITEBACK.md",
            "generated/runtime_writeback_targets.min.json",
            "generated/runtime_writeback_intake.min.json",
            "generated/runtime_writeback_governance.min.json",
            "docs/RUNTIME_WRITEBACK_SEAM.md",
            "examples/recovery_pattern_memory.rollback_followthrough.example.json",
            "examples/recovery_pattern_memory.component_refresh.example.json",
            "docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md",
            "examples/provenance_thread.self-agency-continuity.example.json",
            "generated/phase_alpha_writeback_map.min.json",
            "scripts/publish_live_receipts.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

        self.assertIn("checkpoint recall", changelog)
        self.assertIn("growth-refinery writeback", roadmap)
        self.assertIn("roadmap drift", roadmap)


if __name__ == "__main__":
    unittest.main()
