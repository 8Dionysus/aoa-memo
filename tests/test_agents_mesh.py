from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class AgentsMeshTestCase(unittest.TestCase):
    def run_script(self, *args: str) -> None:
        completed = subprocess.run(
            (sys.executable, *args),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            self.fail(
                f"{' '.join(args)} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

    def test_agents_mesh_validators_pass(self) -> None:
        for args in (
            ("scripts/validate_agents_mesh.py",),
            ("scripts/build_agents_mesh_index.py", "--check"),
            ("scripts/validate_agents_mesh_index.py",),
        ):
            with self.subTest(script=args):
                self.run_script(*args)

    def test_agents_mesh_index_names_current_cards(self) -> None:
        payload = json.loads((REPO_ROOT / "generated/agents_mesh.min.json").read_text())

        self.assertEqual("aoa_memo_agents_mesh_index_v1", payload["schema_version"])
        self.assertEqual("agents-md-mesh-v1", payload["source_of_truth"])
        self.assertEqual("config/agents_mesh.json", payload["config_ref"])
        self.assertEqual("DESIGN.AGENTS.md", payload["authority_ref"])
        self.assertEqual(58, payload["counts"]["canonical"])
        self.assertEqual(0, payload["counts"]["migration"])

        paths = {card["path"] for card in payload["cards"]}
        self.assertEqual(
            {
                ".agents/AGENTS.md",
                ".agents/skills/AGENTS.md",
                ".agents/spark/AGENTS.md",
                ".github/AGENTS.md",
                "AGENTS.md",
                "config/AGENTS.md",
                "docs/AGENTS.md",
                "docs/decisions/AGENTS.md",
                "examples/AGENTS.md",
                "generated/AGENTS.md",
                "manifests/AGENTS.md",
                "mechanics/AGENTS.md",
                "mechanics/antifragility/AGENTS.md",
                "mechanics/antifragility/docs/AGENTS.md",
                "mechanics/antifragility/legacy/AGENTS.md",
                "mechanics/agon/AGENTS.md",
                "mechanics/agon/docs/AGENTS.md",
                "mechanics/agon/legacy/AGENTS.md",
                "mechanics/adoption/AGENTS.md",
                "mechanics/adoption/docs/AGENTS.md",
                "mechanics/adoption/legacy/AGENTS.md",
                "mechanics/governance/AGENTS.md",
                "mechanics/governance/docs/AGENTS.md",
                "mechanics/governance/legacy/AGENTS.md",
                "mechanics/shape-guard/AGENTS.md",
                "mechanics/shape-guard/docs/AGENTS.md",
                "mechanics/shape-guard/legacy/AGENTS.md",
                "mechanics/checkpoint/AGENTS.md",
                "mechanics/checkpoint/docs/AGENTS.md",
                "mechanics/checkpoint/legacy/AGENTS.md",
                "mechanics/readiness-boundary/AGENTS.md",
                "mechanics/readiness-boundary/docs/AGENTS.md",
                "mechanics/readiness-boundary/legacy/AGENTS.md",
                "mechanics/consumer-handoff/AGENTS.md",
                "mechanics/consumer-handoff/docs/AGENTS.md",
                "mechanics/consumer-handoff/legacy/AGENTS.md",
                "mechanics/operational-gate/AGENTS.md",
                "mechanics/operational-gate/docs/AGENTS.md",
                "mechanics/operational-gate/legacy/AGENTS.md",
                "mechanics/recurrence-support/AGENTS.md",
                "mechanics/recurrence-support/docs/AGENTS.md",
                "mechanics/recurrence-support/legacy/AGENTS.md",
                "mechanics/lineage-harvest/AGENTS.md",
                "mechanics/lineage-harvest/docs/AGENTS.md",
                "mechanics/lineage-harvest/legacy/AGENTS.md",
                "mechanics/retention/AGENTS.md",
                "mechanics/retention/docs/AGENTS.md",
                "mechanics/retention/legacy/AGENTS.md",
                "mechanics/titan/AGENTS.md",
                "mechanics/titan/docs/AGENTS.md",
                "mechanics/titan/legacy/AGENTS.md",
                "mechanics/writeback/AGENTS.md",
                "mechanics/writeback/docs/AGENTS.md",
                "mechanics/writeback/legacy/AGENTS.md",
                "quests/AGENTS.md",
                "schemas/AGENTS.md",
                "scripts/AGENTS.md",
                "tests/AGENTS.md",
            },
            paths,
        )

    def test_release_check_runs_agents_mesh_gate(self) -> None:
        text = (REPO_ROOT / "scripts" / "release_check.py").read_text(encoding="utf-8")
        for snippet in (
            "scripts/validate_agents_mesh.py",
            "scripts/build_agents_mesh_index.py",
            "--check",
            "scripts/validate_agents_mesh_index.py",
        ):
            self.assertIn(snippet, text)

    def test_agents_mesh_ignores_dependency_checkouts(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "agents_mesh.json").read_text())
        self.assertIn(".deps", config["ignored_directory_names"])
        self.assertIn(".deps", config["top_level_exemptions"])


if __name__ == "__main__":
    unittest.main()
