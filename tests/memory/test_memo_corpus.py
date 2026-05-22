from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class MemoCorpusTestCase(unittest.TestCase):
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

    def test_memo_corpus_validator_passes(self) -> None:
        self.run_script("scripts/memory/validate_memo_corpus.py")

    def test_first_corpus_object_records_corpus_decision(self) -> None:
        path = (
            REPO_ROOT
            / "memo"
            / "objects"
            / "decisions"
            / "2026"
            / "reviewed-corpus-district"
            / "object.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual("decision", data["kind"])
        self.assertEqual("memo.decision.2026-05-21.reviewed-corpus-district", data["id"])
        self.assertEqual(
            "docs/decisions/2026-05-21-reviewed-memory-corpus-district.md",
            data["payload_ref"],
        )
        self.assertIn("repo:aoa-memo", data["scope"])
        self.assertEqual("preferred", data["lifecycle"]["current_recall"]["status"])

    def test_corpus_is_not_a_local_memo_port(self) -> None:
        for rel_path in ("memo/PORT.yaml", "memo/candidates", "memo/exports", "memo/local"):
            self.assertFalse((REPO_ROOT / rel_path).exists(), rel_path)

    def test_generated_read_models_include_reviewed_corpus_object(self) -> None:
        object_id = "memo.decision.2026-05-21.reviewed-corpus-district"
        for rel_path in (
            "generated/memory-objects/memory_object_catalog.json",
            "generated/memory-objects/memory_object_catalog.min.json",
            "generated/memory-objects/memory_object_capsules.json",
            "generated/memory-objects/memory_object_sections.full.json",
        ):
            with self.subTest(rel_path=rel_path):
                payload = json.loads((REPO_ROOT / rel_path).read_text(encoding="utf-8"))
                objects = {item["id"]: item for item in payload["memory_objects"]}
                self.assertIn(object_id, objects)
                self.assertEqual("reviewed_corpus", objects[object_id]["source_kind"])
                self.assertEqual(
                    "memo/objects/decisions/2026/reviewed-corpus-district/object.json",
                    objects[object_id]["source_path"],
                )

    def test_generated_read_models_mark_examples_as_teaching_fixtures(self) -> None:
        payload = json.loads(
            (REPO_ROOT / "generated" / "memory-objects" / "memory_object_catalog.json").read_text(
                encoding="utf-8"
            )
        )
        objects = {item["id"]: item for item in payload["memory_objects"]}

        self.assertEqual("aoa-memo-object-read-models-v2", payload["source_of_truth"])
        self.assertEqual("teaching_fixture", objects["memo.anchor.2026-03-23.charter-operating-axis"]["source_kind"])


if __name__ == "__main__":
    unittest.main()
