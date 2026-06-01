from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from publish_live_receipts_support import *  # noqa: F401,F403


class MemoPublishLiveReceiptsBoundaryTests(unittest.TestCase):
    def test_publish_live_receipts_rejects_unsupported_event_kind(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            input_path.write_text(
                json.dumps(build_receipt(event_kind="technique_promotion_receipt"), indent=2) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(module.ReceiptPublishError):
                module.load_receipts([input_path])

    def test_publish_live_receipts_rejects_event_kind_actor_drift(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_receipt()
            receipt["actor_ref"] = "aoa-memo:growth-refinery-writeback"
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("actor_ref", str(ctx.exception))
        self.assertIn("aoa-memo:runtime-writeback", str(ctx.exception))

    def test_publish_live_receipts_rejects_unadopted_object_id(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_receipt()
            receipt["object_ref"]["id"] = "memo.decision.2026-04-06.session-closeout"
            receipt["evidence_refs"][0]["ref"] = (
                "repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#"
                "memo.decision.2026-04-06.session-closeout"
            )
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("does not resolve in generated memory-object recall catalog", str(ctx.exception))

    def test_publish_live_receipts_requires_adopted_recall_surface_ref(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_receipt()
            receipt["evidence_refs"] = [
                {
                    "kind": "runtime_review",
                    "ref": "repo:abyss-stack/Logs/phase-alpha/revalidation_pack.json",
                }
            ]
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("must include adopted recall surface ref", str(ctx.exception))

    def test_publish_live_receipts_requires_payload_to_match_adopted_object(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_receipt()
            receipt["payload"]["target_kind"] = "claim"
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("target_kind: must match adopted memory object kind", str(ctx.exception))

    def test_publish_live_receipts_requires_runtime_surface_for_reviewed_candidate(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_reviewed_candidate_receipt("distillation_claim_candidate")
            receipt["payload"].pop("runtime_surface")
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("reviewed_candidate receipts must include a non-empty runtime_surface", str(ctx.exception))

    def test_publish_live_receipts_requires_writeback_anchor_ref_in_evidence_for_reviewed_candidate(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_reviewed_candidate_receipt("distillation_bridge_candidate")
            receipt["evidence_refs"] = receipt["evidence_refs"][:-1]
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("reviewed_candidate receipts must include writeback anchor ref", str(ctx.exception))



if __name__ == "__main__":
    unittest.main()
