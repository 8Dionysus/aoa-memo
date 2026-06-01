from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from publish_live_receipts_support import *  # noqa: F401,F403


class MemoPublishLiveReceiptsCoreTests(unittest.TestCase):
    def test_publish_live_receipts_appends_once_and_skips_duplicates(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            log_path = tmp_path / "memo-writeback-receipts.jsonl"
            input_path.write_text(json.dumps(build_receipt(), indent=2) + "\n", encoding="utf-8")

            receipts = module.load_receipts([input_path])
            appended, skipped = module.append_new_receipts(log_path=log_path, receipts=receipts)
            self.assertEqual(appended, 1)
            self.assertEqual(skipped, 0)

            appended, skipped = module.append_new_receipts(log_path=log_path, receipts=receipts)
            self.assertEqual(appended, 0)
            self.assertEqual(skipped, 1)

    def test_publish_live_receipts_counts_duplicates_without_mutating_log(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            log_path = tmp_path / "memo-writeback-receipts.jsonl"
            receipts = [build_receipt(), build_receipt()]

            appended, skipped = module.count_new_receipts(log_path=log_path, receipts=receipts)

            self.assertEqual(appended, 1)
            self.assertEqual(skipped, 1)
            self.assertFalse(log_path.exists())

    def test_publish_live_receipts_dry_run_does_not_create_log(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            log_path = tmp_path / "memo-writeback-receipts.jsonl"
            input_path.write_text(json.dumps(build_receipt(), indent=2) + "\n", encoding="utf-8")

            exit_code = module.main(
                [
                    "--input",
                    str(input_path),
                    "--log-path",
                    str(log_path),
                    "--dry-run",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse(log_path.exists())

    def test_publish_live_receipts_uses_runtime_targets_path_override(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            log_path = tmp_path / "memo-writeback-receipts.jsonl"
            runtime_targets_path = tmp_path / "runtime_writeback_targets.min.json"
            input_path.write_text(
                json.dumps(build_reviewed_candidate_receipt("distillation_claim_candidate"), indent=2) + "\n",
                encoding="utf-8",
            )
            runtime_targets_path.write_text(
                json.dumps(
                    {
                        "targets": [
                            {
                                "runtime_surface": "distillation_claim_candidate",
                                "writeback_class": "reviewed_candidate",
                                "target_kind": "pattern",
                            }
                        ]
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.main(
                    [
                        "--input",
                        str(input_path),
                        "--log-path",
                        str(log_path),
                        "--runtime-targets-path",
                        str(runtime_targets_path),
                        "--dry-run",
                    ]
                )

        self.assertIn("must resolve to target_kind", str(ctx.exception))



if __name__ == "__main__":
    unittest.main()
