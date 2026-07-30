from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker
import pytest


PART_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PART_ROOT / "scripts" / "aoa_memo_participation_hook.py"
SCHEMA_PATH = (
    PART_ROOT
    / "schemas"
    / "aoa_memo_participation_retention_report_v0.schema.json"
)

SPEC = importlib.util.spec_from_file_location(
    "aoa_memo_participation_retention",
    SCRIPT_PATH,
)
assert SPEC is not None and SPEC.loader is not None
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


def append_event(
    state_root: Path,
    *,
    session_id: str,
    event_name: str,
    observed_at: str,
) -> None:
    payload = {
        "session_id": session_id,
        "cwd": "/srv/AbyssOS/aoa-memo",
        "hook_event_name": event_name,
        "model": "gpt-5.6-sol",
        "permission_mode": "dontAsk",
        "turn_id": f"{session_id}-turn",
    }
    if event_name == "SessionStart":
        payload["source"] = "startup"
    if event_name == "SessionEnd":
        payload["reason"] = "other"
    receipt = HOOK.build_observation(payload)
    receipt["observed_at"] = observed_at
    HOOK.append_observation(state_root, receipt)


def load_schema() -> dict:
    payload = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_retention_is_plan_only_until_explicit_whole_session_erasure(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    for event_name in ("SessionStart", "SessionEnd"):
        append_event(
            state_root,
            session_id="old-closed",
            event_name=event_name,
            observed_at="2026-05-01T00:00:00Z",
        )
    append_event(
        state_root,
        session_id="old-open",
        event_name="SessionStart",
        observed_at="2026-05-01T00:00:00Z",
    )
    for event_name in ("SessionStart", "SessionEnd"):
        append_event(
            state_root,
            session_id="recent-closed",
            event_name=event_name,
            observed_at="2026-07-20T00:00:00Z",
        )

    reference_time = datetime(2026, 7, 30, tzinfo=timezone.utc)
    plan = HOOK.build_retention_report(
        state_root,
        retention_days=45,
        execute=False,
        reference_time=reference_time,
    )
    Draft202012Validator(
        load_schema(),
        format_checker=FormatChecker(),
    ).validate(plan)
    assert plan["mode"] == "plan"
    assert plan["counts"]["session_logs_scanned"] == 3
    assert plan["counts"]["eligible_session_logs"] == 1
    assert plan["counts"]["deleted_session_logs"] == 0
    assert plan["counts"]["skipped_not_closed"] == 1
    assert plan["counts"]["skipped_within_window"] == 1
    assert len(tuple((state_root / "sessions").glob("*.jsonl"))) == 3

    execution = HOOK.build_retention_report(
        state_root,
        retention_days=45,
        execute=True,
        acknowledge_whole_session_erasure=True,
        reference_time=reference_time,
    )
    Draft202012Validator(
        load_schema(),
        format_checker=FormatChecker(),
    ).validate(execution)
    assert execution["mode"] == "execute"
    assert execution["counts"]["deleted_session_logs"] == 1
    assert execution["counts"]["deleted_receipts"] == 2
    assert execution["authority"]["observation_receipt_erasure"] is True
    assert execution["content_persisted"] is False
    assert execution["session_refs_persisted"] is False
    assert len(tuple((state_root / "sessions").glob("*.jsonl"))) == 2
    assert len(tuple((state_root / "locks").glob("*.lock"))) == 2


def test_retention_skips_invalid_chain_and_never_deletes_partial_state(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    for event_name in ("SessionStart", "SessionEnd"):
        append_event(
            state_root,
            session_id="invalid-old-closed",
            event_name=event_name,
            observed_at="2026-05-01T00:00:00Z",
        )
    log_path = next((state_root / "sessions").glob("*.jsonl"))
    payloads = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
    ]
    payloads[-1]["receipt_digest"] = "sha256:" + ("0" * 64)
    log_path.write_text(
        "\n".join(HOOK.canonical_json(payload) for payload in payloads) + "\n",
        encoding="utf-8",
    )

    report = HOOK.build_retention_report(
        state_root,
        retention_days=45,
        execute=True,
        acknowledge_whole_session_erasure=True,
        reference_time=datetime(2026, 7, 30, tzinfo=timezone.utc),
    )
    assert report["counts"]["skipped_invalid"] == 1
    assert report["counts"]["deleted_session_logs"] == 0
    assert report["issues"]
    assert log_path.exists()


def test_retention_cli_requires_minimum_window_and_explicit_acknowledgement(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    with pytest.raises(ValueError, match="requires acknowledgement"):
        HOOK.build_retention_report(
            state_root,
            retention_days=45,
            execute=True,
        )

    too_short = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "retention",
            "--state-root",
            str(state_root),
            "--retention-days",
            "29",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert too_short.returncode == 2
    assert "at least 30" in too_short.stderr

    unacknowledged = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "retention",
            "--state-root",
            str(state_root),
            "--execute",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert unacknowledged.returncode == 2
    assert "--acknowledge-whole-session-erasure" in unacknowledged.stderr
