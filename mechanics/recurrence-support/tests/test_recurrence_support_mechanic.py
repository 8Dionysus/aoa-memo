from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


class RecurrenceSupportMechanicTestCase(unittest.TestCase):
    def test_recurrence_support_registers_active_docs(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        recurrence_support = packages["recurrence-support"]

        self.assertEqual("Recurrence Support Memo Mechanic", recurrence_support["title"])
        self.assertIn("operation", recurrence_support)
        self.assertEqual(
            [
                "RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
                "REVIEWED_CLOSEOUT_RECALL_LANDING.md",
                "WITNESS_TRACE_CONTRACT.md",
            ],
            recurrence_support["docs"],
        )

        for filename in recurrence_support["docs"]:
            self.assertTrue(
                (REPO_ROOT / "mechanics" / "recurrence-support" / "docs" / filename).is_file()
            )
            self.assertFalse((REPO_ROOT / "docs" / filename).exists())

    def test_recurrence_support_preserves_stronger_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "recurrence-support" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "Agents-of-Abyss",
            "aoa-agents",
            "aoa-playbooks",
            "aoa-routing",
            "abyss-stack",
            "aoa-evals",
            "without turning `aoa-memo` into",
            "second route ledger",
            "`return_memory`",
        ):
            self.assertIn(snippet, readme)

    def test_recurrence_support_keeps_technical_contracts_owner_routed(self) -> None:
        parts = (REPO_ROOT / "mechanics" / "recurrence-support" / "PARTS.md").read_text(
            encoding="utf-8"
        )
        for path in (
            "mechanics/checkpoint/schemas/inquiry_checkpoint.schema.json",
            "mechanics/checkpoint/examples/inquiry_checkpoint.example.json",
            "mechanics/checkpoint/examples/inquiry_checkpoint.return.example.json",
            "mechanics/checkpoint/schemas/checkpoint-to-memory-contract.schema.json",
            "mechanics/checkpoint/examples/checkpoint_to_memory_contract.example.json",
            "mechanics/recurrence-support/schemas/witness-trace.schema.json",
            "mechanics/recurrence-support/examples/witness_trace.example.json",
            "examples/recall_contract.object.working.return.json",
            "quests/AOA-MEM-Q-0009.yaml",
            "generated/quest_catalog.min.json",
        ):
            self.assertIn(path, parts)
            self.assertTrue((REPO_ROOT / path).is_file())

    def test_recurrence_refs_point_to_active_mechanic_docs(self) -> None:
        active_refs = (
            "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
            "mechanics/recurrence-support/docs/REVIEWED_CLOSEOUT_RECALL_LANDING.md",
            "mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
        )

        registry = json.loads((REPO_ROOT / "generated" / "memo_registry.min.json").read_text())
        self.assertIn(active_refs[0], registry["core_docs"])
        self.assertIn(active_refs[2], registry["core_docs"])

        quest = (REPO_ROOT / "quests" / "AOA-MEM-Q-0009.yaml").read_text(encoding="utf-8")
        self.assertIn(active_refs[1], quest)

        catalog = json.loads((REPO_ROOT / "generated" / "memory_catalog.min.json").read_text())
        surfaces = {item["id"]: item for item in catalog["memo_surfaces"]}
        self.assertEqual(
            "mechanics/recurrence-support/README.md",
            surfaces["AOA-M-0014"]["source_path"],
        )

    def test_pattern_lineage_stays_out_of_recurrence_support(self) -> None:
        self.assertTrue(
            (
                REPO_ROOT
                / "mechanics"
                / "lineage-harvest"
                / "docs"
                / "PATTERN_LINEAGE_MEMORY.md"
            ).is_file()
        )
        docs_dir = REPO_ROOT / "mechanics" / "recurrence-support" / "docs"
        self.assertFalse((docs_dir / "PATTERN_LINEAGE_MEMORY.md").exists())


if __name__ == "__main__":
    unittest.main()
