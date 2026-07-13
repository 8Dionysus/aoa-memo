from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "mechanics"))

import validation_lanes  # noqa: E402
import validate_memo_mechanics as memo_mechanics_validator  # noqa: E402


def release_command_text() -> str:
    return "\n".join(" ".join(step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE)


class MemoMechanicsTestCase(unittest.TestCase):
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

    def test_memo_mechanics_validators_pass(self) -> None:
        for args in (
            ("scripts/mechanics/validate_memo_mechanics.py",),
            ("scripts/mechanics/build_memo_mechanics_index.py", "--check"),
            ("scripts/mechanics/validate_memo_mechanics_index.py",),
        ):
            with self.subTest(script=args):
                self.run_script(*args)

    def test_memo_mechanics_validator_tolerates_deleted_tracked_paths(self) -> None:
        deleted_path = REPO_ROOT / "tests" / "memory" / "test_memo_validators.py"

        with mock.patch.object(memo_mechanics_validator, "tracked_files", return_value=[deleted_path]):
            issues = memo_mechanics_validator.validate()

        self.assertNotIn(str(deleted_path), "\n".join(issues))

    def test_repo_self_indexes_are_outside_authored_mechanics_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir) / "aoa-memo"
            indexes = repo_root / "kag" / "indexes"
            indexes.mkdir(parents=True)
            repository_index = indexes / "repo_event_index.json"
            owner_index = indexes / "provider_readiness_index.json"
            repository_index.write_text(
                '{"schema_version":"aoa-repo-local-kag-repository-index-v2"}\n',
                encoding="utf-8",
            )
            owner_index.write_text(
                '{"schema_version":"aoa-local-kag-record-v1"}\n',
                encoding="utf-8",
            )

            self.assertFalse(
                memo_mechanics_validator.is_text_candidate(repository_index, root=repo_root)
            )
            self.assertTrue(
                memo_mechanics_validator.is_text_candidate(owner_index, root=repo_root)
            )

    def test_memo_mechanics_index_names_packages(self) -> None:
        payload = json.loads((REPO_ROOT / "generated" / "mechanics" / "memo_mechanics.min.json").read_text())

        self.assertEqual("aoa_memo_mechanics_index_v2", payload["schema_version"])
        self.assertEqual("memo-mechanics-v2", payload["source_of_truth"])
        self.assertEqual("config/mechanics/memo_mechanics.json", payload["config_ref"])
        self.assertEqual("mechanics/README.md", payload["authority_ref"])
        self.assertEqual(15, payload["counts"]["packages"])
        self.assertEqual(104, payload["counts"]["docs"])

        packages = {package["slug"]: package for package in payload["packages"]}
        self.assertEqual(
            {
                "antifragility",
                "agon",
                "titan",
                "adoption",
                "governance",
                "shape-guard",
                "checkpoint",
                "readiness-boundary",
                "consumer-handoff",
                "operational-gate",
                "recurrence-support",
                "lineage-harvest",
                "questbook",
                "writeback",
                "retention",
            },
            set(packages),
        )
        self.assertEqual(6, packages["antifragility"]["doc_count"])
        self.assertEqual(27, packages["agon"]["doc_count"])
        self.assertEqual(10, packages["titan"]["doc_count"])
        self.assertEqual(6, packages["adoption"]["doc_count"])
        self.assertEqual(9, packages["governance"]["doc_count"])
        self.assertEqual(1, packages["shape-guard"]["doc_count"])
        self.assertEqual(4, packages["checkpoint"]["doc_count"])
        self.assertEqual(1, packages["readiness-boundary"]["doc_count"])
        self.assertEqual(6, packages["consumer-handoff"]["doc_count"])
        self.assertEqual(5, packages["operational-gate"]["doc_count"])
        self.assertEqual(3, packages["recurrence-support"]["doc_count"])
        self.assertEqual(1, packages["lineage-harvest"]["doc_count"])
        self.assertEqual(1, packages["questbook"]["doc_count"])
        self.assertEqual(17, packages["writeback"]["doc_count"])
        self.assertEqual(7, packages["retention"]["doc_count"])
        for package in packages.values():
            self.assertIn("operation", package)
            self.assertIn("os_abyss_role", package)
            self.assertNotIn("legacy_path", package)

    def test_mechanic_docs_live_under_mechanics_not_docs_root(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "mechanics" / "memo_mechanics.json").read_text())
        for package in config["packages"]:
            slug = package["slug"]
            for filename in package["docs"]:
                self.assertFalse((REPO_ROOT / "docs" / filename).exists())
                self.assertTrue((REPO_ROOT / "mechanics" / slug / "docs" / filename).is_file())

    def test_release_check_runs_memo_mechanics_gate(self) -> None:
        text = release_command_text()
        for snippet in (
            "scripts/mechanics/validate_memo_mechanics.py",
            "scripts/mechanics/build_memo_mechanics_index.py",
            "--check",
            "scripts/mechanics/validate_memo_mechanics_index.py",
            "scripts/mechanics/build_memo_mechanic_cards.py",
            "scripts/mechanics/validate_memo_mechanic_cards.py",
            "scripts/mechanics/build_memo_mechanic_owner_routes.py",
            "scripts/mechanics/validate_memo_mechanic_owner_routes.py",
            "scripts/mechanics/build_memo_mechanic_landing_logs.py",
            "scripts/mechanics/validate_memo_mechanic_landing_logs.py",
        ):
            self.assertIn(snippet, text)

    def test_mechanic_subroutes_and_artifact_topology_are_present(self) -> None:
        topology = (REPO_ROOT / "mechanics" / "ARTIFACT_TOPOLOGY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Root Technical Districts", topology)
        self.assertIn("Mechanic Artifact Lane", topology)
        self.assertIn("Move Rule", topology)

        for slug in (
            "antifragility",
            "agon",
            "titan",
            "adoption",
            "governance",
            "shape-guard",
            "checkpoint",
            "readiness-boundary",
            "consumer-handoff",
            "operational-gate",
            "recurrence-support",
            "lineage-harvest",
            "questbook",
            "writeback",
            "retention",
        ):
            self.assertTrue((REPO_ROOT / "mechanics" / slug / "docs" / "AGENTS.md").is_file())
            self.assertTrue((REPO_ROOT / "mechanics" / slug / "legacy" / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
