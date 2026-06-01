from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoRuntimeBoundaryTestCase(MemoValidatorTestCase):
    def test_runtime_writeback_targets_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_targets()
    def test_runtime_writeback_targets_surface_rejects_review_state_drift(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["review_state_default"] = "captured"
                break

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)
    def test_runtime_writeback_targets_surface_rejects_duplicate_runtime_surface(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["targets"][1]["runtime_surface"] = "checkpoint_export"

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)
    def test_runtime_writeback_targets_surface_rejects_incomplete_runtime_boundary(self) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(target_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["runtime_boundary"] = {}

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)
    def test_runtime_writeback_intake_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_intake()
    def test_runtime_writeback_intake_surface_rejects_owner_review_ref_drift(self) -> None:
        intake_path = validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(intake_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["targets"][0]["owner_review_refs"] = ["mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md"]

        def side_effect(path: Path) -> dict:
            if Path(path) == intake_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_intake)
    def test_runtime_writeback_intake_surface_rejects_reviewed_candidate_posture_drift(self) -> None:
        intake_path = validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH
        original_load_json = validate_memo.load_json
        payload = load_json(intake_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["intake_posture"] = "capturable_runtime_export"
                break

        def side_effect(path: Path) -> dict:
            if Path(path) == intake_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_intake)
    def test_live_receipt_log_rejects_uncataloged_object_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-missing-object",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-missing-object",
                "session_ref": "session:memo-missing-object",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": "memo.decision.2099-01-01.missing",
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_catalog_entry",
                        "ref": "repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#memo.decision.2099-01-01.missing",
                        "role": "catalog",
                    }
                ],
                "payload": {
                    "target_kind": "decision",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)
    def test_live_receipt_log_accepts_cataloged_object_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object",
                "session_ref": "session:memo-cataloged-object",
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
                        "ref": "repo:aoa-memo/examples/memory-objects/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()
    def test_live_receipt_log_rejects_repo_refs_that_escape_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-escaped-evidence-ref",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-escaped-evidence-ref",
                "session_ref": "session:memo-escaped-evidence-ref",
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
                        "ref": "repo:aoa-memo/../outside/examples/memory-objects/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)
    def test_live_receipt_log_rejects_cataloged_object_without_capsule_hydration(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-missing-capsule",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-missing-capsule",
                "session_ref": "session:memo-cataloged-object-missing-capsule",
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
                        "ref": "repo:aoa-memo/examples/memory-objects/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
            capsules_path = (
                validate_memo.GENERATED
                / "memory-objects"
                / "memory_object_capsules.json"
            )
            capsules = load_json(capsules_path)
            assert isinstance(capsules, dict)
            capsules = copy.deepcopy(capsules)
            capsules["memory_objects"] = [
                item
                for item in capsules["memory_objects"]
                if isinstance(item, dict) and item.get("id") != object_id
            ]
            original_load_json = validate_memo.load_json

            def side_effect(path: Path) -> dict:
                if Path(path) == capsules_path:
                    return copy.deepcopy(capsules)
                return original_load_json(path)

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with patch.object(validate_memo, "load_json", side_effect=side_effect):
                    ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)
    def test_live_receipt_log_rejects_event_kind_actor_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-actor-drift",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-actor-drift",
                "session_ref": "session:memo-cataloged-object-actor-drift",
                "actor_ref": "aoa-memo:growth-refinery-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_object",
                        "ref": "repo:aoa-memo/examples/memory-objects/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)
    def test_live_receipt_log_rejects_cataloged_object_without_expand_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-cataloged-object-empty-sections",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-cataloged-object-empty-sections",
                "session_ref": "session:memo-cataloged-object-empty-sections",
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
                        "ref": "repo:aoa-memo/examples/memory-objects/claim.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "claim",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
            sections_path = (
                validate_memo.GENERATED
                / "memory-objects"
                / "memory_object_sections.full.json"
            )
            sections = load_json(sections_path)
            assert isinstance(sections, dict)
            sections = copy.deepcopy(sections)
            for item in sections["memory_objects"]:
                if isinstance(item, dict) and item.get("id") == object_id:
                    item["sections"] = []
                    break
            original_load_json = validate_memo.load_json

            def side_effect(path: Path) -> dict:
                if Path(path) == sections_path:
                    return copy.deepcopy(sections)
                return original_load_json(path)

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with patch.object(validate_memo, "load_json", side_effect=side_effect):
                    ctx = self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)

        self.assertEqual(ctx.code, 1)
    def test_live_receipt_log_rejects_payload_kind_drift_from_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.claim.2026-03-20.temperature-not-truth"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-payload-kind-drift",
                "observed_at": "2026-04-13T19:00:00Z",
                "run_ref": "run-memo-payload-kind-drift",
                "session_ref": "session:memo-payload-kind-drift",
                "actor_ref": "aoa-memo:runtime-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "memory_object",
                    "id": object_id,
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/memory-objects/claim.example.json",
                    "target_kind": "decision",
                    "writeback_class": "memo_surviving_event",
                    "review_state": "confirmed",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)
    def test_live_receipt_log_accepts_reviewed_candidate_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.bridge.2026-03-23.tos-lineage-kag-candidate"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-reviewed-bridge",
                "observed_at": "2026-04-13T22:00:00Z",
                "run_ref": "run-memo-reviewed-bridge",
                "session_ref": "session:memo-reviewed-bridge",
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
                        "ref": "repo:aoa-memo/mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
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
                "payload": {
                    "memory_object_ref": "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
                    "runtime_surface": "distillation_bridge_candidate",
                    "target_kind": "bridge",
                    "writeback_class": "reviewed_candidate",
                    "review_state": "proposed",
                    "writeback_anchor_ref": "repo:aoa-memo/mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()
    def test_live_receipt_log_rejects_reviewed_candidate_without_runtime_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            object_id = "memo.pattern.2026-04-02.alpha-remediation-recurrence"
            receipt = {
                "event_kind": "memo_writeback_receipt",
                "event_id": "evt-memo-reviewed-pattern-missing-runtime-surface",
                "observed_at": "2026-04-13T22:00:00Z",
                "run_ref": "run-memo-reviewed-pattern-missing-runtime-surface",
                "session_ref": "session:memo-reviewed-pattern-missing-runtime-surface",
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
                        "ref": "repo:aoa-memo/examples/phase-alpha/pattern.phase-alpha-remediation-recurrence.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "memory_catalog_entry",
                        "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                        "role": "catalog",
                    },
                    {
                        "kind": "review_anchor",
                        "ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
                        "role": "writeback-anchor",
                    },
                ],
                "payload": {
                    "memory_object_ref": "examples/phase-alpha/pattern.phase-alpha-remediation-recurrence.example.json",
                    "target_kind": "pattern",
                    "writeback_class": "reviewed_candidate",
                    "review_state": "confirmed",
                    "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)
    def test_live_receipt_log_accepts_growth_refinery_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            lane_ref = "growth_refinery_failure_lesson"
            receipt = {
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
                "evidence_refs": [
                    {
                        "kind": "support_memory",
                        "ref": "repo:aoa-memo/mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory.lineage.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "growth_lane_entry",
                        "ref": f"repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                        "role": "lane",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-playbooks:review_note_v1#AOA-P-0025:owner-reanchor",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-sdk:closeout_context_lineage_v1#session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
                        "role": "required-evidence",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "Agents-of-Abyss:reviewable_growth_refinery_v1#owner-boundaries",
                        "role": "required-evidence",
                    },
                ],
                "payload": {
                    "growth_lane_ref": lane_ref,
                    "source_example_ref": "mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory.lineage.example.json",
                    "target_kind": "failure_lesson",
                    "review_status": "reviewed",
                    "writeback_class": "growth_refinery_memory",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                with io.StringIO() as stdout, io.StringIO() as stderr:
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        validate_memo.validate_live_receipt_log()
    def test_live_receipt_log_rejects_growth_refinery_receipt_without_lane_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "memo-writeback-receipts.jsonl"
            receipt = {
                "event_kind": "memo_growth_writeback_receipt",
                "event_id": "evt-memo-growth-recovery-pattern",
                "observed_at": "2026-04-14T00:05:00Z",
                "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
                "session_ref": "session:memo-growth-refinery-writeback",
                "actor_ref": "aoa-memo:growth-refinery-writeback",
                "object_ref": {
                    "repo": "aoa-memo",
                    "kind": "support_memory",
                    "id": "memo:session-growth-cycle-playbook-reanchor",
                    "version": "main",
                },
                "evidence_refs": [
                    {
                        "kind": "support_memory",
                        "ref": "repo:aoa-memo/mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.lineage.example.json",
                        "role": "primary",
                    },
                    {
                        "kind": "growth_evidence",
                        "ref": "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
                        "role": "required-evidence",
                    },
                ],
                "payload": {
                    "source_example_ref": "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.lineage.example.json",
                    "target_kind": "recovery_pattern",
                    "review_status": "reviewed",
                    "writeback_class": "growth_refinery_memory",
                },
            }
            log_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

            with patch.object(validate_memo, "LIVE_RECEIPT_LOG_PATH", log_path):
                self.assert_system_exit_quietly(validate_memo.validate_live_receipt_log)
    def test_self_agency_continuity_writeback_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_self_agency_continuity_writeback_surface()
    def test_self_agency_continuity_writeback_rejects_unhydrated_memory_object_id(self) -> None:
        thread_path = validate_memo.example_path_for(
            "provenance_thread.self-agency-continuity.example.json"
        )
        original_load_json = validate_memo.load_json
        payload = load_json(thread_path)
        assert isinstance(payload, dict)
        payload = copy.deepcopy(payload)
        payload["memory_object_ids"].append("memo.state.2099-01-01.missing-continuity-relay")

        def side_effect(path: Path) -> object:
            if Path(path) == thread_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_self_agency_continuity_writeback_surface
            )
