from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]


class ShapeGuardMechanicTestCase(unittest.TestCase):
    def test_shape_guard_registers_via_negativa_as_operation(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "mechanics" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        shape_guard = packages["shape-guard"]

        self.assertEqual("Shape Guard Memo Mechanic", shape_guard["title"])
        self.assertEqual(["VIA_NEGATIVA_CHECKLIST.md"], shape_guard["docs"])
        self.assertIn("operation", shape_guard)
        self.assertIn("not a topic bucket", config["classification_rule"])

        active_path = REPO_ROOT / "mechanics" / "shape-guard" / "docs" / "VIA_NEGATIVA_CHECKLIST.md"
        self.assertTrue(active_path.is_file())
        former_flat_path = "/".join(("docs", "VIA_NEGATIVA_CHECKLIST.md"))
        self.assertFalse((REPO_ROOT / "docs" / "VIA_NEGATIVA_CHECKLIST.md").exists())
        self.assertFalse(
            (REPO_ROOT / "mechanics" / "governance" / "docs" / "VIA_NEGATIVA_CHECKLIST.md").exists()
        )

    def test_shape_guard_card_preserves_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "shape-guard" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "proof",
            "current health",
            "action authority",
            "aoa-evals",
            "aoa-agents",
            "abyss-stack",
        ):
            self.assertIn(snippet, readme)

        legacy_index = (
            REPO_ROOT / "mechanics" / "shape-guard" / "legacy" / "INDEX.md"
        ).read_text(encoding="utf-8")
        former_flat_path = "/".join(("docs", "VIA_NEGATIVA_CHECKLIST.md"))
        self.assertIn(former_flat_path, legacy_index)
        former_governance_path = "/".join(
            ("mechanics", "governance", "docs", "VIA_NEGATIVA_CHECKLIST.md")
        )
        self.assertIn(former_governance_path, legacy_index)


if __name__ == "__main__":
    unittest.main()
