from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from downstream_feed_contracts_support import *  # noqa: F401,F403


class MemoDownstreamFeedDocsRouteTests(unittest.TestCase):
    def test_repo_docs_align_on_contract_hardening_stage(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        charter = (REPO_ROOT / "CHARTER.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("`aoa-memo` is in contract hardening.", readme)
        self.assertIn("This repository is in contract hardening.", charter)
        self.assertNotIn("This repository is in bootstrap.", charter)
        self.assertIn("`aoa-memo` is in contract hardening.", roadmap)

    def test_readme_routes_validation_and_targeted_generation_to_agents(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        scripts_agents = (REPO_ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("Validation starts at [AGENTS](AGENTS.md#verify)", readme)
        self.assertIn("nearest `AGENTS.md`", readme)
        self.assertIn("docs/validation", readme)
        self.assertIn("docs/root/RELEASING", readme)

        root_validation_commands = (
            "python scripts/ci_gate.py --mode source-fast",
            "python scripts/ci_gate.py --mode generated",
            "python scripts/ci_gate.py --mode memory",
            "python scripts/ci_gate.py --mode tests",
            "python scripts/release/release_check.py",
        )
        for command in root_validation_commands:
            self.assertNotIn(command, readme)
            self.assertIn(command, root_agents)
        self.assertIn("docs/validation/COMMAND_AUTHORITY.md", root_agents)
        self.assertIn("docs/validation/validator_inventory.json", root_agents)

        for command in (
            "python scripts/memory/generate_memory_object_surfaces.py",
            "python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py",
            "python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py",
            "python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py",
            "python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py",
        ):
            self.assertIn(command, scripts_agents)

    def test_contributing_surfaces_current_validation_battery(self) -> None:
        contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("Executable validation routes live in [AGENTS](AGENTS.md#verify)", contributing)
        self.assertIn("nearest local `AGENTS.md`", contributing)
        self.assertIn("Do not duplicate the full command battery here", contributing)

        for command in (
            "python scripts/ci_gate.py --mode source-fast",
            "python scripts/ci_gate.py --mode generated",
            "python scripts/ci_gate.py --mode memory",
            "python scripts/ci_gate.py --mode tests",
            "python scripts/release/release_check.py",
        ):
            self.assertIn(command, root_agents)

        self.assertIn("git status -sb", contributing)




if __name__ == "__main__":
    unittest.main()
