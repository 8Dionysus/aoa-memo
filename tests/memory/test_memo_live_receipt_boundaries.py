from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


CATALOGED_CLAIM_ID = "memo.claim.2026-03-20.temperature-not-truth"
CLAIM_EXAMPLE_REF = "repo:aoa-memo/examples/memory-objects/claim.example.json"


def catalog_ref(object_id: str) -> str:
    return f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}"


def runtime_receipt(
    *,
    object_id: str = CATALOGED_CLAIM_ID,
    event_id: str = "evt-memo-cataloged-object",
    actor_ref: str = "aoa-memo:runtime-writeback",
    evidence_refs: list[dict] | None = None,
    payload: dict | None = None,
) -> dict:
    return {
        "event_kind": "memo_writeback_receipt",
        "event_id": event_id,
        "observed_at": "2026-04-13T19:00:00Z",
        "run_ref": f"run-{event_id}",
        "session_ref": f"session:{event_id}",
        "actor_ref": actor_ref,
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "memory_object",
            "id": object_id,
            "version": "main",
        },
        "evidence_refs": evidence_refs
        if evidence_refs is not None
        else [
            {"kind": "memory_object", "ref": CLAIM_EXAMPLE_REF, "role": "primary"},
            {"kind": "memory_catalog_entry", "ref": catalog_ref(object_id), "role": "catalog"},
        ],
        "payload": payload
        if payload is not None
        else {
            "memory_object_ref": "examples/memory-objects/claim.example.json",
            "target_kind": "claim",
            "writeback_class": "memo_surviving_event",
            "review_state": "confirmed",
        },
    }


def reviewed_candidate_receipt(*, include_runtime_surface: bool = True) -> dict:
    payload = {
        "memory_object_ref": "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
        "target_kind": "bridge",
        "writeback_class": "reviewed_candidate",
        "review_state": "proposed",
        "writeback_anchor_ref": "repo:aoa-memo/mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
    }
    if include_runtime_surface:
        payload["runtime_surface"] = "distillation_bridge_candidate"
    object_id = "memo.bridge.2026-03-23.tos-lineage-kag-candidate"
    return runtime_receipt(
        object_id=object_id,
        event_id="evt-memo-reviewed-bridge",
        evidence_refs=[
            {
                "kind": "memory_object",
                "ref": "repo:aoa-memo/mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
                "role": "primary",
            },
            {"kind": "memory_catalog_entry", "ref": catalog_ref(object_id), "role": "catalog"},
            {
                "kind": "candidate_source",
                "ref": "repo:aoa-memo/mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim.tos-bridge-ready.example.json",
                "role": "candidate-source",
            },
            {
                "kind": "review_anchor",
                "ref": "repo:aoa-memo/mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
                "role": "writeback-anchor",
            },
        ],
        payload=payload,
    )


def growth_refinery_receipt(*, include_lane_ref: bool = True) -> dict:
    lane_ref = "growth_refinery_failure_lesson"
    evidence_refs = [
        {
            "kind": "support_memory",
            "ref": "repo:aoa-memo/mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory.lineage.example.json",
            "role": "primary",
        },
        {"kind": "growth_evidence", "ref": "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle", "role": "required-evidence"},
        {"kind": "growth_evidence", "ref": "aoa-playbooks:review_note_v1#AOA-P-0025:owner-reanchor", "role": "required-evidence"},
        {"kind": "growth_evidence", "ref": "aoa-sdk:closeout_context_lineage_v1#session-growth-cycle", "role": "required-evidence"},
        {"kind": "growth_evidence", "ref": "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle", "role": "required-evidence"},
        {"kind": "growth_evidence", "ref": "Agents-of-Abyss:reviewable_growth_refinery_v1#owner-boundaries", "role": "required-evidence"},
    ]
    payload = {
        "source_example_ref": "mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory.lineage.example.json",
        "target_kind": "failure_lesson",
        "review_status": "reviewed",
        "writeback_class": "growth_refinery_memory",
    }
    if include_lane_ref:
        evidence_refs.insert(
            1,
            {
                "kind": "growth_lane_entry",
                "ref": f"repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                "role": "lane",
            },
        )
        payload["growth_lane_ref"] = lane_ref
    return {
        "event_kind": "memo_growth_writeback_receipt",
        "event_id": "evt-memo-growth-failure-lesson",
        "observed_at": "2026-04-14T00:05:00Z",
        "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
        "session_ref": "session:memo-growth-refinery-writeback",
        "actor_ref": "aoa-memo:growth-refinery-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "support_memory",
            "id": "memo:session-growth-cycle-owner-reanchor-first",
            "version": "main",
        },
        "evidence_refs": evidence_refs,
        "payload": payload,
    }


class MemoLiveReceiptBoundaryTestCase(MemoValidatorTestCase):
    def write_receipt(self, receipt: dict, log_path: Path) -> None:
        log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    def assert_receipt_validates(self, receipt: dict) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            self.write_receipt(receipt, log_path)
            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()

    def assert_receipt_fails(self, receipt: dict) -> SystemExit:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            self.write_receipt(receipt, log_path)
            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                return self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

    def test_live_receipt_log_accepts_cataloged_object_ref(self) -> None:
        self.assert_receipt_validates(runtime_receipt())

    def test_live_receipt_log_rejects_uncataloged_object_ref(self) -> None:
        object_id = "memo.decision.2099-01-01.missing"
        receipt = runtime_receipt(
            object_id=object_id,
            event_id="evt-memo-missing-object",
            evidence_refs=[
                {"kind": "memory_catalog_entry", "ref": catalog_ref(object_id), "role": "catalog"},
            ],
            payload={
                "target_kind": "decision",
                "writeback_class": "memo_surviving_event",
                "review_state": "confirmed",
            },
        )
        self.assert_receipt_fails(receipt)

    def test_live_receipt_log_rejects_repo_refs_that_escape_root(self) -> None:
        receipt = runtime_receipt()
        receipt["evidence_refs"][0]["ref"] = "repo:aoa-memo/../outside/examples/memory-objects/claim.example.json"
        ctx = self.assert_receipt_fails(receipt)
        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_rejects_event_kind_actor_drift(self) -> None:
        receipt = runtime_receipt(
            event_id="evt-memo-cataloged-object-actor-drift",
            actor_ref="aoa-memo:growth-refinery-writeback",
        )
        ctx = self.assert_receipt_fails(receipt)
        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_rejects_payload_kind_drift_from_catalog(self) -> None:
        receipt = runtime_receipt(
            event_id="evt-memo-payload-kind-drift",
            evidence_refs=[
                {"kind": "memory_catalog_entry", "ref": catalog_ref(CATALOGED_CLAIM_ID), "role": "catalog"},
            ],
            payload={
                "memory_object_ref": "examples/memory-objects/claim.example.json",
                "target_kind": "decision",
                "writeback_class": "memo_surviving_event",
                "review_state": "confirmed",
            },
        )
        self.assert_receipt_fails(receipt)

    def test_live_receipt_log_rejects_cataloged_object_without_capsule_hydration(self) -> None:
        capsules_path = validate_memo.GENERATED / "memory-objects" / "memory_object_capsules.json"
        capsules = copy.deepcopy(load_json(capsules_path))
        assert isinstance(capsules, dict)
        capsules["memory_objects"] = [
            item
            for item in capsules["memory_objects"]
            if isinstance(item, dict) and item.get("id") != CATALOGED_CLAIM_ID
        ]
        self.assert_receipt_fails_with_load_override(runtime_receipt(), capsules_path, capsules)

    def test_live_receipt_log_rejects_cataloged_object_without_expand_sections(self) -> None:
        sections_path = validate_memo.GENERATED / "memory-objects" / "memory_object_sections.full.json"
        sections = copy.deepcopy(load_json(sections_path))
        assert isinstance(sections, dict)
        for item in sections["memory_objects"]:
            if isinstance(item, dict) and item.get("id") == CATALOGED_CLAIM_ID:
                item["sections"] = []
                break
        self.assert_receipt_fails_with_load_override(runtime_receipt(), sections_path, sections)

    def assert_receipt_fails_with_load_override(self, receipt: dict, patched_path: Path, payload: dict) -> None:
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == patched_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            self.write_receipt(receipt, log_path)
            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with patch.object(validate_memo, "load_json", side_effect=side_effect):
                    ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)
        self.assertEqual(ctx.code, 1)

    def test_live_receipt_log_accepts_reviewed_candidate_receipt(self) -> None:
        self.assert_receipt_validates(reviewed_candidate_receipt())

    def test_live_receipt_log_rejects_reviewed_candidate_without_runtime_surface(self) -> None:
        self.assert_receipt_fails(reviewed_candidate_receipt(include_runtime_surface=False))

    def test_live_receipt_log_accepts_growth_refinery_receipt(self) -> None:
        self.assert_receipt_validates(growth_refinery_receipt())

    def test_live_receipt_log_rejects_growth_refinery_receipt_without_lane_ref(self) -> None:
        self.assert_receipt_fails(growth_refinery_receipt(include_lane_ref=False))
