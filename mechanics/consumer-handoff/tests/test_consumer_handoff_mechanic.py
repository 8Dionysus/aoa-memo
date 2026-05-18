from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


class ConsumerHandoffMechanicTestCase(unittest.TestCase):
    def test_consumer_handoff_registers_active_docs(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        handoff = packages["consumer-handoff"]

        self.assertEqual("Consumer Handoff Memo Mechanic", handoff["title"])
        self.assertIn("operation", handoff)
        self.assertEqual(
            [
                "AGENT_MEMORY_POSTURE_SEAM.md",
                "KAG_SOURCE_EXPORT.md",
                "KAG_TOS_BRIDGE_CONTRACT.md",
                "MEMORY_EVAL_GUARDRAILS.md",
                "ORCHESTRATOR_MEMORY_ALIGNMENT.md",
                "PLAYBOOK_MEMORY_SCOPES.md",
            ],
            handoff["docs"],
        )

        for filename in handoff["docs"]:
            self.assertTrue(
                (REPO_ROOT / "mechanics" / "consumer-handoff" / "docs" / filename).is_file()
            )
            self.assertFalse((REPO_ROOT / "docs" / filename).exists())

    def test_consumer_handoff_preserves_stronger_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "consumer-handoff" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "aoa-agents",
            "aoa-playbooks",
            "aoa-evals",
            "aoa-kag",
            "Tree-of-Sophia",
            "aoa-routing",
            "abyss-stack",
            "without absorbing memo authority",
        ):
            self.assertIn(snippet, readme)

    def test_consumer_handoff_updates_generated_and_quest_refs(self) -> None:
        registry = json.loads((REPO_ROOT / "generated" / "memo_registry.min.json").read_text())
        expected_refs = {
            "mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md",
            "mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md",
            "mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md",
            "mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md",
            "mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md",
        }
        self.assertTrue(expected_refs.issubset(set(registry["core_docs"])))

        for quest_id in ("AOA-MEM-Q-0004", "AOA-MEM-Q-0005", "AOA-MEM-Q-0006"):
            quest = (
                REPO_ROOT / "quests" / "memo" / "captured" / f"{quest_id}.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md",
                quest,
            )

    def test_downstream_feed_regression_is_package_local(self) -> None:
        package_test = (
            REPO_ROOT
            / "mechanics"
            / "consumer-handoff"
            / "tests"
            / "test_downstream_feed_contracts.py"
        )

        self.assertTrue(package_test.is_file())
        self.assertFalse((REPO_ROOT / "tests" / "test_downstream_feed_contracts.py").exists())


if __name__ == "__main__":
    unittest.main()
