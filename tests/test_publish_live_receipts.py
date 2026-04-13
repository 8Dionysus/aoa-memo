from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "publish_live_receipts.py"
LIVE_RECEIPT_LOG_PATH = REPO_ROOT / ".aoa" / "live_receipts" / "memo-writeback-receipts.jsonl"
MEMORY_OBJECT_CATALOG_PATH = REPO_ROOT / "generated" / "memory_object_catalog.min.json"
MEMORY_OBJECT_CAPSULES_PATH = REPO_ROOT / "generated" / "memory_object_capsules.json"
MEMORY_OBJECT_SECTIONS_PATH = REPO_ROOT / "generated" / "memory_object_sections.full.json"
ADOPTED_OBJECT_ID = "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
ADOPTED_RECALL_REF = (
    "repo:aoa-memo/generated/memory_object_catalog.min.json#"
    "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
)


def load_module():
    spec = importlib.util.spec_from_file_location("publish_live_receipts", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def build_receipt(event_kind: str = "memo_writeback_receipt") -> dict:
    return {
        "event_kind": event_kind,
        "event_id": "evt-memo-001",
        "observed_at": "2026-04-06T20:10:00Z",
        "run_ref": "run-memo-001",
        "session_ref": "session:test-memo-closeout",
        "actor_ref": "aoa-memo:writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "memory_object",
            "id": ADOPTED_OBJECT_ID,
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "memory_object",
                "ref": ADOPTED_RECALL_REF,
            }
        ],
        "payload": {
            "target_kind": "decision",
            "writeback_class": "memo_surviving_event",
            "review_state": "confirmed",
        },
    }


class MemoPublishLiveReceiptsTests(unittest.TestCase):
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

    def test_publish_live_receipts_rejects_unadopted_object_id(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            input_path = tmp_path / "receipt.json"
            receipt = build_receipt()
            receipt["object_ref"]["id"] = "memo.decision.2026-04-06.session-closeout"
            receipt["evidence_refs"][0]["ref"] = (
                "repo:aoa-memo/generated/memory_object_catalog.min.json#"
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

    def test_checked_in_live_receipts_resolve_to_recall_surface_family(self) -> None:
        module = load_module()
        receipts = module.load_receipts([LIVE_RECEIPT_LOG_PATH])
        self.assertTrue(receipts)

        catalog_by_id = module.load_memory_object_catalog(MEMORY_OBJECT_CATALOG_PATH)
        capsules_by_id = {
            item["id"]: item
            for item in load_json(MEMORY_OBJECT_CAPSULES_PATH)["memory_objects"]
        }
        sections_by_id = {
            item["id"]: item
            for item in load_json(MEMORY_OBJECT_SECTIONS_PATH)["memory_objects"]
        }

        event_ids: set[str] = set()
        for receipt in receipts:
            event_id = receipt["event_id"]
            object_id = receipt["object_ref"]["id"]
            catalog_entry = catalog_by_id[object_id]

            self.assertNotIn(event_id, event_ids)
            event_ids.add(event_id)
            self.assertIn(object_id, capsules_by_id)
            self.assertIn(object_id, sections_by_id)
            self.assertEqual(capsules_by_id[object_id]["kind"], catalog_entry["kind"])
            self.assertEqual(sections_by_id[object_id]["kind"], catalog_entry["kind"])
            self.assertEqual(capsules_by_id[object_id]["source_path"], catalog_entry["source_path"])
            self.assertEqual(sections_by_id[object_id]["source_path"], catalog_entry["source_path"])
            self.assertTrue(sections_by_id[object_id]["sections"])
            if "memory_object_ref" in receipt["payload"]:
                self.assertEqual(receipt["payload"]["memory_object_ref"], catalog_entry["source_path"])


if __name__ == "__main__":
    unittest.main()
