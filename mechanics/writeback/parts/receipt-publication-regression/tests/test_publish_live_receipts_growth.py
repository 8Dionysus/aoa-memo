from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from publish_live_receipts_support import *  # noqa: F401,F403


class MemoPublishLiveReceiptsGrowthTests(unittest.TestCase):
    def test_publish_live_receipts_accepts_growth_refinery_failure_lesson_receipt(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            input_path.write_text(
                json.dumps(build_growth_receipt("growth_refinery_failure_lesson"), indent=2) + "\n",
                encoding="utf-8",
            )

            receipts = module.load_receipts([input_path])

        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["event_kind"], "memo_growth_writeback_receipt")

    def test_publish_live_receipts_requires_growth_lane_ref_for_growth_receipt(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_growth_receipt("growth_refinery_recovery_pattern")
            receipt["payload"].pop("growth_lane_ref")
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("payload.growth_lane_ref", str(ctx.exception))

    def test_publish_live_receipts_rejects_cross_repo_growth_object_ref(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_growth_receipt("growth_refinery_recovery_pattern")
            receipt["object_ref"]["repo"] = "aoa-playbooks"
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("object_ref.repo", str(ctx.exception))

    def test_publish_live_receipts_requires_growth_lane_evidence_refs(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_growth_receipt("growth_refinery_recovery_pattern")
            receipt["evidence_refs"] = receipt["evidence_refs"][:-1]
            input_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(module.ReceiptPublishError) as ctx:
                module.load_receipts([input_path])

        self.assertIn("required growth-refinery evidence ref", str(ctx.exception))

    def test_publish_live_receipts_preserves_jsonl_line_boundaries(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            log_path = tmp_path / "memo-writeback-receipts.jsonl"
            existing_receipt = build_receipt()
            existing_receipt["event_id"] = "evt-memo-existing"
            existing_receipt["run_ref"] = "run-memo-existing"
            input_path.write_text(json.dumps(build_receipt(), indent=2) + "\n", encoding="utf-8")
            log_path.write_text(json.dumps(existing_receipt, sort_keys=True, ensure_ascii=False), encoding="utf-8")

            receipts = module.load_receipts([input_path])
            appended, skipped = module.append_new_receipts(log_path=log_path, receipts=receipts)

            self.assertEqual(appended, 1)
            self.assertEqual(skipped, 0)
            lines = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["event_id"], "evt-memo-existing")
            self.assertEqual(json.loads(lines[1])["event_id"], "evt-memo-001")

    def test_tracked_receipt_fixture_resolves_to_recall_surface_family(self) -> None:
        module = load_module()
        receipts = module.load_receipts([RECEIPT_FIXTURE_PATH])
        self.assertTrue(receipts)

        catalog_by_id = module.load_memory_object_catalog(MEMORY_OBJECT_CATALOG_PATH)
        growth_lanes_by_ref = module.load_growth_refinery_writeback_lanes(GROWTH_REFINERY_LANES_PATH)
        capsules_by_id = {
            item["id"]: item
            for item in load_json(MEMORY_OBJECT_CAPSULES_PATH)["memory_objects"]
        }
        sections_by_id = {
            item["id"]: item
            for item in load_json(MEMORY_OBJECT_SECTIONS_PATH)["memory_objects"]
        }

        event_ids: set[str] = set()
        reviewed_candidate_target_kinds: set[str] = set()
        growth_lane_target_kinds: set[str] = set()
        for receipt in receipts:
            event_id = receipt["event_id"]
            self.assertNotIn(event_id, event_ids)
            event_ids.add(event_id)
            if receipt["event_kind"] == "memo_writeback_receipt":
                object_id = receipt["object_ref"]["id"]
                catalog_entry = catalog_by_id[object_id]
                self.assertIn(object_id, capsules_by_id)
                self.assertIn(object_id, sections_by_id)
                self.assertEqual(capsules_by_id[object_id]["kind"], catalog_entry["kind"])
                self.assertEqual(sections_by_id[object_id]["kind"], catalog_entry["kind"])
                self.assertEqual(capsules_by_id[object_id]["source_path"], catalog_entry["source_path"])
                self.assertEqual(sections_by_id[object_id]["source_path"], catalog_entry["source_path"])
                self.assertTrue(sections_by_id[object_id]["sections"])
                if "memory_object_ref" in receipt["payload"]:
                    self.assertEqual(receipt["payload"]["memory_object_ref"], catalog_entry["source_path"])
                if receipt["payload"]["writeback_class"] == "reviewed_candidate":
                    reviewed_candidate_target_kinds.add(receipt["payload"]["target_kind"])
                    self.assertIn("runtime_surface", receipt["payload"])
                    self.assertIn(
                        receipt["payload"]["writeback_anchor_ref"],
                        {ref["ref"] for ref in receipt["evidence_refs"]},
                    )
                continue

            lane_ref = receipt["payload"]["growth_lane_ref"]
            lane = growth_lanes_by_ref[lane_ref]
            growth_lane_target_kinds.add(receipt["payload"]["target_kind"])
            self.assertEqual(receipt["event_kind"], "memo_growth_writeback_receipt")
            self.assertEqual(receipt["object_ref"]["kind"], lane["object_ref_kind"])
            self.assertEqual(receipt["object_ref"]["id"], lane["memory_id"])
            self.assertEqual(receipt["payload"]["source_example_ref"], lane["source_path"])
            evidence_refs = {ref["ref"] for ref in receipt["evidence_refs"]}
            self.assertIn(lane["primary_ref"], evidence_refs)
            self.assertIn(
                f"repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                evidence_refs,
            )
            for required_ref in lane["required_evidence_refs"]:
                self.assertIn(required_ref, evidence_refs)
        self.assertEqual(reviewed_candidate_target_kinds, {"claim", "pattern", "bridge"})
        self.assertEqual(growth_lane_target_kinds, {"failure_lesson", "recovery_pattern"})




if __name__ == "__main__":
    unittest.main()
