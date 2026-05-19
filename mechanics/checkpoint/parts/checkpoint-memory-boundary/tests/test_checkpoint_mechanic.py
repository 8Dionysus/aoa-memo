from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_checkpoint_artifacts_live_in_functioning_parts() -> None:
    expected = [
        "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
        "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
        "mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.example.json",
        "mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.return.example.json",
        "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json",
        "mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_approval_record.example.json",
        "mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_health_check.example.json",
        "mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_improvement_thread.example.json",
        "mechanics/checkpoint/parts/approval-and-health-records/examples/decision.phase-alpha-self-agent-checkpoint.example.json",
        "mechanics/checkpoint/parts/approval-and-health-records/examples/audit_event.phase-alpha-self-agent-checkpoint.example.json",
    ]
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).is_file(), relative_path


def test_checkpoint_contract_keeps_existing_object_mapping() -> None:
    payload = load_json("mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json")
    assert payload["contract_type"] == "checkpoint_to_memory_contract"
    assert payload["checkpoint_artifact"]["schema_ref"] == (
        "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json"
    )

    pairs = {
        (item["runtime_surface"], item["target_kind"])
        for item in payload["mapping_rules"]
    }
    assert {
        ("checkpoint_export", "state_capsule"),
        ("approval_record", "decision"),
        ("transition_record", "decision"),
        ("execution_trace", "episode"),
        ("review_trace", "audit_event"),
        ("distillation_claim_candidate", "claim"),
        ("distillation_pattern_candidate", "pattern"),
        ("distillation_bridge_candidate", "bridge"),
    } <= pairs


def test_recurrence_and_writeback_consume_checkpoint_without_owning_it() -> None:
    recurrence_parts = (REPO_ROOT / "mechanics/recurrence-support/PARTS.md").read_text(
        encoding="utf-8"
    )
    writeback_seam = (REPO_ROOT / "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md").read_text(
        encoding="utf-8"
    )

    assert "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json" in recurrence_parts
    assert "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json" in writeback_seam


def test_registry_routes_checkpoint_docs_and_schemas() -> None:
    registry = load_json("generated/memory/memo_registry.min.json")
    for doc_ref in (
        "mechanics/checkpoint/docs/CHECKPOINT_MEMORY_BOUNDARY.md",
        "mechanics/checkpoint/docs/CHECKPOINT_CARRY_CONTRACT.md",
        "mechanics/checkpoint/docs/CHECKPOINT_APPROVAL_HEALTH_MEMORY.md",
        "mechanics/checkpoint/docs/CHECKPOINT_TO_MEMORY_MAPPING.md",
    ):
        assert doc_ref in registry["core_docs"]
    for schema_ref in (
        "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
        "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
    ):
        assert schema_ref in registry["schemas"]


def test_checkpoint_mechanic_validates() -> None:
    completed = subprocess.run(
        (sys.executable, "scripts/mechanics/validate_memo_mechanics.py"),
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
