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


if __name__ == "__main__":
    unittest.main()
