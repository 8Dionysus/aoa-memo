from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "publish_live_receipts.py"
RECEIPT_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "memo_writeback_receipts.example.jsonl"
MEMORY_OBJECT_CATALOG_PATH = REPO_ROOT / "generated" / "memory_object_catalog.min.json"
MEMORY_OBJECT_CAPSULES_PATH = REPO_ROOT / "generated" / "memory_object_capsules.json"
MEMORY_OBJECT_SECTIONS_PATH = REPO_ROOT / "generated" / "memory_object_sections.full.json"
GROWTH_REFINERY_LANES_PATH = REPO_ROOT / "generated" / "growth_refinery_writeback_lanes.min.json"
ADOPTED_OBJECT_ID = "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
ADOPTED_RECALL_REF = (
    "repo:aoa-memo/generated/memory_object_catalog.min.json#"
    "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
)
REVIEWED_CANDIDATE_CASES = {
    "distillation_claim_candidate": {
        "object_id": "memo.claim.2026-04-03.phase-alpha-runtime-history-later-infra-track",
        "source_path": "examples/claim.phase-alpha-runtime-history-later-infra-track.example.json",
        "target_kind": "claim",
        "review_state": "confirmed",
        "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation.md",
        "candidate_seed_ref": "repo:abyss-stack/Logs/phase-alpha/alpha-04-long-horizon-model-tier-orchestra/distillation_pack.md",
    },
    "distillation_pattern_candidate": {
        "object_id": "memo.pattern.2026-04-02.alpha-remediation-recurrence",
        "source_path": "examples/pattern.phase-alpha-remediation-recurrence.example.json",
        "target_kind": "pattern",
        "review_state": "confirmed",
        "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
        "candidate_seed_ref": "repo:abyss-stack/Logs/phase-alpha/alpha-04-long-horizon-model-tier-orchestra/distillation_pack.md",
    },
    "distillation_bridge_candidate": {
        "object_id": "memo.bridge.2026-03-23.tos-lineage-kag-candidate",
        "source_path": "examples/bridge.kag-lift.example.json",
        "target_kind": "bridge",
        "review_state": "proposed",
        "writeback_anchor_ref": "repo:aoa-memo/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
        "candidate_seed_ref": "repo:aoa-memo/examples/claim.tos-bridge-ready.example.json",
    },
}
GROWTH_LANE_CASES = {
    "growth_refinery_failure_lesson": {
        "memory_id": "memo:session-growth-cycle-owner-reanchor-first",
        "source_path": "examples/failure_lesson_memory.lineage.example.json",
        "target_kind": "failure_lesson",
        "review_status": "reviewed",
        "required_evidence_refs": [
            "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
            "aoa-playbooks:review_note_v1#AOA-P-0025:owner-reanchor",
            "aoa-sdk:closeout_context_lineage_v1#session-growth-cycle",
            "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
            "Agents-of-Abyss:reviewable_growth_refinery_v1#owner-boundaries",
        ],
    },
    "growth_refinery_recovery_pattern": {
        "memory_id": "memo:session-growth-cycle-playbook-reanchor",
        "source_path": "examples/recovery_pattern_memory.lineage.example.json",
        "target_kind": "recovery_pattern",
        "review_status": "reviewed",
        "required_evidence_refs": [
            "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
            "Dionysus:seed_lineage_entry_v1#seed:aoa:session-growth-cycle",
            "aoa-evals:aoa-candidate-lineage-integrity#report:session-growth-cycle",
            "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
            "aoa-stats:candidate_lineage_summary_v1#summary:session-growth-cycle",
        ],
    },
}


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
        "actor_ref": "aoa-memo:runtime-writeback",
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


def build_reviewed_candidate_receipt(runtime_surface: str) -> dict:
    case = REVIEWED_CANDIDATE_CASES[runtime_surface]
    object_id = case["object_id"]
    return {
        "event_kind": "memo_writeback_receipt",
        "event_id": f"evt-{runtime_surface}",
        "observed_at": "2026-04-13T21:05:00Z",
        "run_ref": "run-memo-reviewed-candidate-adoption-2026-04-13",
        "session_ref": "session:2026-04-13-reviewed-candidate-adoption",
        "actor_ref": "aoa-memo:runtime-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "memory_object",
            "id": object_id,
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "memory_object",
                "ref": f"repo:aoa-memo/{case['source_path']}",
                "role": "primary",
            },
            {
                "kind": "memory_catalog_entry",
                "ref": f"repo:aoa-memo/generated/memory_object_catalog.min.json#{object_id}",
                "role": "catalog",
            },
            {
                "kind": "candidate_seed",
                "ref": case["candidate_seed_ref"],
                "role": "candidate-seed",
            },
            {
                "kind": "review_anchor",
                "ref": case["writeback_anchor_ref"],
                "role": "writeback-anchor",
            },
        ],
        "payload": {
            "memory_object_ref": case["source_path"],
            "runtime_surface": runtime_surface,
            "review_state": case["review_state"],
            "target_kind": case["target_kind"],
            "writeback_anchor_ref": case["writeback_anchor_ref"],
            "writeback_class": "reviewed_candidate",
        },
    }


def build_growth_receipt(lane_ref: str) -> dict:
    case = GROWTH_LANE_CASES[lane_ref]
    source_path = case["source_path"]
    return {
        "event_kind": "memo_growth_writeback_receipt",
        "event_id": f"evt-{lane_ref}",
        "observed_at": "2026-04-14T00:05:00Z",
        "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
        "session_ref": "session:2026-04-14-growth-refinery-writeback",
        "actor_ref": "aoa-memo:growth-refinery-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "support_memory",
            "id": case["memory_id"],
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "support_memory",
                "ref": f"repo:aoa-memo/{source_path}",
                "role": "primary",
            },
            {
                "kind": "growth_lane_entry",
                "ref": f"repo:aoa-memo/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                "role": "lane",
            },
        ]
        + [
            {
                "kind": "growth_evidence",
                "ref": ref,
                "role": "required-evidence",
            }
            for ref in case["required_evidence_refs"]
        ],
        "payload": {
            "growth_lane_ref": lane_ref,
            "source_example_ref": source_path,
            "target_kind": case["target_kind"],
            "review_status": case["review_status"],
            "writeback_class": "growth_refinery_memory",
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
                f"repo:aoa-memo/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                evidence_refs,
            )
            for required_ref in lane["required_evidence_refs"]:
                self.assertIn(required_ref, evidence_refs)
        self.assertEqual(reviewed_candidate_target_kinds, {"claim", "pattern", "bridge"})
        self.assertEqual(growth_lane_target_kinds, {"failure_lesson", "recovery_pattern"})


if __name__ == "__main__":
    unittest.main()
