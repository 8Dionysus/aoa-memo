#!/usr/bin/env python3
"""Content-minimized, fail-open observation for aoa-memo participation.

The ``observe`` command is suitable for Codex command hooks. It intentionally
writes nothing to stdout or stderr in normal operation, never returns model
context, and never blocks or continues a turn. The ``summary`` and ``verify``
commands are operator/lab surfaces and are not referenced by the hook fragment.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable


SCHEMA_VERSION = "aoa_memo_participation_receipt_v0"
SUMMARY_SCHEMA_VERSION = "aoa_memo_participation_summary_v0"
RETENTION_SCHEMA_VERSION = "aoa_memo_participation_retention_report_v0"
CLASSIFIER_VERSION = "aoa_memo_participation_classifier_v0"
DEFAULT_RETENTION_DAYS = 45
MINIMUM_RETENTION_DAYS = 30
SUPPORTED_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PostToolUse",
    "PreCompact",
    "PostCompact",
    "Stop",
    "SessionEnd",
}
PERMISSION_MODES = {
    "default",
    "acceptEdits",
    "plan",
    "dontAsk",
    "bypassPermissions",
}
MODEL_PATTERN = re.compile(r"^[A-Za-z0-9._:+/-]{1,96}$")
SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
SYNTHETIC_MARKERS = (
    '<codex_internal_context source="goal">',
    "<codex_internal_context source='goal'>",
)
RAW_SESSION_SIGNALS = (
    ".aoa",
    "aoa-session-memory",
    "session memory",
    "session-memory",
    "codex transcript",
    "raw transcript",
    "rollout.jsonl",
    "rehydrat",
    "compaction",
    "сесси",
    "транскрипт",
    "компак",
    "сжат",
)
WRITEBACK_SIGNALS = (
    "memo candidate",
    "memory candidate",
    "first candidate",
    "writeback",
    "reusable lesson",
    "durable lesson",
    "кандидат памяти",
    "сохрани урок",
    "запиши урок",
    "повторяемый урок",
)
DEEP_SIGNALS = (
    "memory object",
    "memo object",
    "corpus identity",
    "quarantine packet",
    "read-model drift",
    "read model drift",
    "lifecycle target",
    "semantic lifecycle",
    "superseded",
    "retracted",
    "quarantined",
    "forgetting",
    "erasure",
    "объект памяти",
    "семантическ",
    "жизненн",
    "забыван",
    "стирани",
    "отозван",
    "карантин",
)
CONTINUITY_SIGNALS = (
    "continue",
    "continuing",
    "resume",
    "resuming",
    "prior",
    "previous",
    "earlier",
    "histor",
    "rationale",
    "why we chose",
    "owner boundary",
    "owner truth",
    "cross-repo",
    "cross repo",
    "durable decision",
    "reviewed decision",
    "provenance",
    "продолж",
    "возобнов",
    "раньше",
    "ранее",
    "прошл",
    "истори",
    "почему выбрал",
    "решени",
    "границ",
    "владел",
    "источник истины",
    "межреп",
    "происхожд",
)
ECOSYSTEM_SIGNALS = (
    "aoa",
    "abyss",
    "tree of sophia",
    "tree-of-sophia",
    "agents of abyss",
)


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def contains_any(value: str, needles: Iterable[str]) -> bool:
    return any(needle in value for needle in needles)


def length_bucket(value: str) -> str:
    length = len(value)
    if length == 0:
        return "empty"
    if length <= 128:
        return "short"
    if length <= 512:
        return "medium"
    if length <= 2048:
        return "long"
    return "very_long"


def classify_workspace(cwd: Any) -> str:
    if not isinstance(cwd, str):
        return "unknown"
    lowered = cwd.lower()
    known = (
        ("aoa-session-memory", "aoa-session-memory"),
        ("aoa-memo", "aoa-memo"),
        ("aoa-evals", "aoa-evals"),
        ("aoa-sdk", "aoa-sdk"),
        ("aoa-skills", "aoa-skills"),
        ("abyss-stack", "abyss-stack"),
        ("abyss-machine", "abyss-machine"),
        ("tree-of-sophia", "tree-of-sophia"),
    )
    for marker, workspace_class in known:
        if marker in lowered:
            return workspace_class
    if "/srv/abyssos/" in lowered or "/.aoa/" in lowered:
        return "other-aoa"
    return "other"


def classify_prompt(prompt: str, workspace_class: str) -> dict[str, Any]:
    lowered = prompt.casefold()
    synthetic = contains_any(lowered, SYNTHETIC_MARKERS)
    if synthetic:
        return {
            "route_class": "none",
            "opportunity_class": "synthetic_continuation",
            "opportunity_state": "excluded",
            "prompt_length_bucket": length_bucket(prompt),
            "synthetic_continuation_excluded": True,
        }

    raw_session = contains_any(lowered, RAW_SESSION_SIGNALS)
    writeback = contains_any(lowered, WRITEBACK_SIGNALS)
    deep = contains_any(lowered, DEEP_SIGNALS)
    continuity = contains_any(lowered, CONTINUITY_SIGNALS)
    ecosystem = contains_any(lowered, ECOSYSTEM_SIGNALS)
    aoa_workspace = workspace_class not in {"other", "unknown"}

    if raw_session:
        route_class = "aoa-session-memory"
        opportunity_class = "raw_session_handoff"
        opportunity_state = "handoff"
    elif writeback:
        route_class = "aoa-memo-writeback"
        opportunity_class = "first_writeback_handoff"
        opportunity_state = "handoff"
    elif deep:
        route_class = "aoa-memo-deep"
        opportunity_class = "existing_memory_deep"
        opportunity_state = "eligible"
    elif continuity and (ecosystem or aoa_workspace):
        route_class = "aoa-memo-orient"
        opportunity_class = "reviewed_context_orientation"
        opportunity_state = "eligible"
    else:
        route_class = "none"
        opportunity_class = "none"
        opportunity_state = "not_applicable"

    return {
        "route_class": route_class,
        "opportunity_class": opportunity_class,
        "opportunity_state": opportunity_state,
        "prompt_length_bucket": length_bucket(prompt),
        "synthetic_continuation_excluded": False,
    }


def classify_tool(tool_name: Any) -> str:
    if not isinstance(tool_name, str):
        return "unknown"
    lowered = tool_name.casefold()
    if "aoa_memo_brief" in lowered:
        return "brief"
    if "aoa_memo_search" in lowered:
        return "search"
    if "aoa_memo_owner_orientation" in lowered:
        return "owner_orientation"
    if "aoa_memo" in lowered:
        return "other_memo_read"
    return "unknown"


def classify_tool_result(response: Any) -> str:
    if not isinstance(response, dict):
        return "returned"
    if response.get("isError") is True or response.get("is_error") is True:
        return "reported_error"
    error = response.get("error")
    if error not in (None, False, "", [], {}):
        return "reported_error"
    return "returned"


def safe_model(value: Any) -> str:
    if isinstance(value, str) and MODEL_PATTERN.fullmatch(value):
        return value
    return "unknown"


def safe_permission_mode(value: Any) -> str:
    if isinstance(value, str) and value in PERMISSION_MODES:
        return value
    return "unknown"


def digest_optional_ref(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return sha256_text(value)


def event_detail(event_name: str, payload: dict[str, Any]) -> str:
    if event_name == "SessionStart":
        value = payload.get("source")
        return value if value in {"startup", "resume", "clear", "compact"} else "unknown"
    if event_name in {"PreCompact", "PostCompact"}:
        value = payload.get("trigger")
        return value if value in {"manual", "auto"} else "unknown"
    if event_name == "SessionEnd":
        return "other" if payload.get("reason") == "other" else "unknown"
    if event_name == "Stop":
        return "already_active" if payload.get("stop_hook_active") is True else "normal"
    if event_name == "PostToolUse":
        return "tool_result"
    if event_name == "UserPromptSubmit":
        return "prompt_observed"
    return "unknown"


def build_observation(payload: dict[str, Any]) -> dict[str, Any]:
    event_name = payload.get("hook_event_name")
    if event_name not in SUPPORTED_EVENTS:
        raise ValueError("unsupported hook event")
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("session_id is required")

    workspace_class = classify_workspace(payload.get("cwd"))
    prompt_result = {
        "route_class": "none",
        "opportunity_class": "none",
        "opportunity_state": "unknown",
        "prompt_length_bucket": None,
        "synthetic_continuation_excluded": False,
    }
    if event_name == "UserPromptSubmit":
        prompt = payload.get("prompt")
        if not isinstance(prompt, str):
            raise ValueError("prompt is required for UserPromptSubmit")
        prompt_result = classify_prompt(prompt, workspace_class)

    tool_class = None
    tool_result_state = None
    invocation_state = "unknown"
    result_returned_state = "unknown"
    if event_name == "PostToolUse":
        tool_class = classify_tool(payload.get("tool_name"))
        if tool_class == "unknown":
            raise ValueError("PostToolUse is outside the aoa_memo contour")
        tool_result_state = classify_tool_result(payload.get("tool_response"))
        invocation_state = "observed"
        result_returned_state = (
            "error_observed"
            if tool_result_state == "reported_error"
            else "observed"
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "classifier_version": CLASSIFIER_VERSION,
        "observed_at": now_utc(),
        "sequence": 0,
        "event_name": event_name,
        "event_detail": event_detail(event_name, payload),
        "session_ref": sha256_text(session_id),
        "turn_ref": digest_optional_ref(payload.get("turn_id")),
        "tool_use_ref": (
            digest_optional_ref(payload.get("tool_use_id"))
            if event_name == "PostToolUse"
            else None
        ),
        "workspace_class": workspace_class,
        "model": safe_model(payload.get("model")),
        "permission_mode": safe_permission_mode(payload.get("permission_mode")),
        "observation": {
            **prompt_result,
            "tool_class": tool_class,
            "tool_result_state": tool_result_state,
        },
        "evidence_ladder": {
            "opportunity": prompt_result["opportunity_state"],
            "noticed": "unknown",
            "invocation": invocation_state,
            "result_returned": result_returned_state,
            "used_or_rejected": "unknown",
            "action_change": "unknown",
            "outcome": "unknown",
        },
        "authority": {
            "context_injection": False,
            "blocking": False,
            "turn_continuation": False,
            "memory_write": False,
            "semantic_transition": False,
            "policy_change": False,
            "effect": False,
        },
        "previous_receipt_digest": None,
        "receipt_digest": "",
    }


def receipt_digest(receipt: dict[str, Any]) -> str:
    payload = dict(receipt)
    payload.pop("receipt_digest", None)
    return sha256_text(canonical_json(payload))


def ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)


@contextmanager
def state_lock(state_root: Path, *, exclusive: bool) -> Iterable[None]:
    """Coordinate observation appenders with explicit whole-session erasure."""

    ensure_private_directory(state_root)
    lock_path = state_root / "retention.lock"
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    os.chmod(lock_path, 0o600)
    with os.fdopen(lock_fd, "r+", encoding="utf-8") as lock_handle:
        lock_mode = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        fcntl.flock(lock_handle.fileno(), lock_mode)
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def last_receipt(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    last: dict[str, Any] | None = None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                candidate = json.loads(line)
                if not isinstance(candidate, dict):
                    raise ValueError("receipt log contains a non-object")
                last = candidate
    return last


def append_observation(state_root: Path, receipt: dict[str, Any]) -> Path:
    ensure_private_directory(state_root)
    session_dir = state_root / "sessions"
    lock_dir = state_root / "locks"
    ensure_private_directory(session_dir)
    ensure_private_directory(lock_dir)

    session_hex = receipt["session_ref"].removeprefix("sha256:")
    log_path = session_dir / f"{session_hex}.jsonl"
    lock_path = lock_dir / f"{session_hex}.lock"
    with state_lock(state_root, exclusive=False):
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        os.chmod(lock_path, 0o600)
        with os.fdopen(lock_fd, "r+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            previous = last_receipt(log_path)
            if previous is None:
                receipt["sequence"] = 1
                receipt["previous_receipt_digest"] = None
            else:
                expected = receipt_digest(previous)
                if previous.get("receipt_digest") != expected:
                    raise ValueError("existing receipt chain is invalid")
                sequence = previous.get("sequence")
                if not isinstance(sequence, int) or sequence < 1:
                    raise ValueError("existing receipt sequence is invalid")
                receipt["sequence"] = sequence + 1
                receipt["previous_receipt_digest"] = previous["receipt_digest"]
            receipt["receipt_digest"] = receipt_digest(receipt)
            line = canonical_json(receipt) + "\n"
            file_fd = os.open(
                log_path,
                os.O_CREAT | os.O_APPEND | os.O_WRONLY,
                0o600,
            )
            os.chmod(log_path, 0o600)
            with os.fdopen(file_fd, "a", encoding="utf-8") as handle:
                handle.write(line)
                handle.flush()
                os.fsync(handle.fileno())
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
    return log_path


def record_failure(state_root: Path, event_name: Any, failure: BaseException) -> None:
    """Best-effort content-free health signal; never expose exception text."""

    try:
        ensure_private_directory(state_root)
        failure_path = state_root / "hook-failures.jsonl"
        payload = {
            "schema_version": "aoa_memo_participation_hook_failure_v0",
            "observed_at": now_utc(),
            "event_name": (
                event_name if event_name in SUPPORTED_EVENTS else "unknown"
            ),
            "failure_class": type(failure).__name__,
            "content_persisted": False,
        }
        file_fd = os.open(
            failure_path,
            os.O_CREAT | os.O_APPEND | os.O_WRONLY,
            0o600,
        )
        with os.fdopen(file_fd, "a", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            os.chmod(failure_path, 0o600)
            handle.write(canonical_json(payload) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except BaseException:
        return


def load_receipts(path: Path) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            receipts.append(payload)
    return receipts


def verify_chain(receipts: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    previous_digest: str | None = None
    for index, receipt in enumerate(receipts, start=1):
        if receipt.get("schema_version") != SCHEMA_VERSION:
            issues.append(f"receipt {index}: unsupported schema_version")
        if receipt.get("sequence") != index:
            issues.append(f"receipt {index}: sequence mismatch")
        if receipt.get("previous_receipt_digest") != previous_digest:
            issues.append(f"receipt {index}: previous digest mismatch")
        observed = receipt.get("receipt_digest")
        expected = receipt_digest(receipt)
        if not isinstance(observed, str) or not SHA256_PATTERN.fullmatch(observed):
            issues.append(f"receipt {index}: invalid receipt digest")
        elif observed != expected:
            issues.append(f"receipt {index}: receipt digest mismatch")
        authority = receipt.get("authority")
        if not isinstance(authority, dict) or any(authority.values()):
            issues.append(f"receipt {index}: authority must remain false")
        ladder = receipt.get("evidence_ladder")
        if not isinstance(ladder, dict):
            issues.append(f"receipt {index}: evidence ladder missing")
        else:
            for field in (
                "noticed",
                "used_or_rejected",
                "action_change",
                "outcome",
            ):
                if ladder.get(field) != "unknown":
                    issues.append(
                        f"receipt {index}: {field} requires external review"
                    )
        previous_digest = observed if isinstance(observed, str) else None
    return issues


def iter_session_logs(state_root: Path) -> Iterable[Path]:
    session_dir = state_root / "sessions"
    if not session_dir.exists():
        return ()
    return tuple(sorted(session_dir.glob("*.jsonl")))


def parse_utc_timestamp(value: Any) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must use UTC Z form")
    parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone aware")
    return parsed.astimezone(timezone.utc)


def build_retention_report(
    state_root: Path,
    *,
    retention_days: int,
    execute: bool,
    acknowledge_whole_session_erasure: bool = False,
    reference_time: datetime | None = None,
) -> dict[str, Any]:
    """Plan or execute bounded erasure of old, closed receipt chains."""

    if execute and not acknowledge_whole_session_erasure:
        raise ValueError(
            "execution requires acknowledgement of whole-session erasure"
        )
    if retention_days < MINIMUM_RETENTION_DAYS:
        raise ValueError(
            f"retention_days must be at least {MINIMUM_RETENTION_DAYS}"
        )
    observed_now = reference_time or datetime.now(timezone.utc)
    if observed_now.tzinfo is None:
        raise ValueError("reference_time must be timezone aware")
    observed_now = observed_now.astimezone(timezone.utc)
    cutoff = observed_now - timedelta(days=retention_days)

    counts: Counter[str] = Counter()
    issues: set[str] = set()
    with state_lock(state_root, exclusive=True):
        for path in iter_session_logs(state_root):
            counts["session_logs_scanned"] += 1
            try:
                receipts = load_receipts(path)
                chain_issues = verify_chain(receipts)
                if not receipts or chain_issues:
                    raise ValueError("invalid receipt chain")
                last = receipts[-1]
                last_observed = parse_utc_timestamp(last.get("observed_at"))
            except (OSError, ValueError, json.JSONDecodeError):
                counts["skipped_invalid"] += 1
                issues.add("one or more session logs failed retention validation")
                continue

            if last.get("event_name") != "SessionEnd":
                counts["skipped_not_closed"] += 1
                continue
            if last_observed > cutoff:
                counts["skipped_within_window"] += 1
                continue

            counts["eligible_session_logs"] += 1
            counts["eligible_receipts"] += len(receipts)
            try:
                log_bytes = path.stat().st_size
            except OSError:
                counts["skipped_invalid"] += 1
                counts["eligible_session_logs"] -= 1
                counts["eligible_receipts"] -= len(receipts)
                issues.add("one or more eligible session logs became unreadable")
                continue
            counts["eligible_bytes"] += log_bytes

            if not execute:
                continue

            lock_path = state_root / "locks" / f"{path.stem}.lock"
            try:
                lock_path.unlink(missing_ok=True)
                path.unlink()
            except OSError:
                counts["deletion_failures"] += 1
                issues.add("one or more eligible session logs could not be erased")
                continue
            counts["deleted_session_logs"] += 1
            counts["deleted_receipts"] += len(receipts)
            counts["deleted_bytes"] += log_bytes

    count_fields = (
        "session_logs_scanned",
        "eligible_session_logs",
        "eligible_receipts",
        "eligible_bytes",
        "deleted_session_logs",
        "deleted_receipts",
        "deleted_bytes",
        "skipped_not_closed",
        "skipped_within_window",
        "skipped_invalid",
        "deletion_failures",
    )
    return {
        "schema_version": RETENTION_SCHEMA_VERSION,
        "generated_at": observed_now.isoformat().replace("+00:00", "Z"),
        "mode": "execute" if execute else "plan",
        "retention_days": retention_days,
        "cutoff_at": cutoff.isoformat().replace("+00:00", "Z"),
        "state_root_ref": sha256_text(str(state_root.resolve())),
        "counts": {field: counts[field] for field in count_fields},
        "issues": sorted(issues),
        "content_persisted": False,
        "session_refs_persisted": False,
        "authority": {
            "automatic_execution": False,
            "semantic_memory_delete": False,
            "shared_memory_write": False,
            "observation_receipt_erasure": execute,
        },
    }


def build_summary(state_root: Path) -> dict[str, Any]:
    event_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    opportunity_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    result_counts: Counter[str] = Counter()
    issues: list[str] = []
    receipt_count = 0
    session_count = 0

    for path in iter_session_logs(state_root):
        session_count += 1
        try:
            receipts = load_receipts(path)
        except (OSError, ValueError, json.JSONDecodeError):
            issues.append(f"{path.name}: unreadable receipt log")
            continue
        receipt_count += len(receipts)
        issues.extend(f"{path.name}: {issue}" for issue in verify_chain(receipts))
        for receipt in receipts:
            event_counts[str(receipt.get("event_name", "unknown"))] += 1
            observation = receipt.get("observation")
            if not isinstance(observation, dict):
                continue
            route_counts[str(observation.get("route_class", "unknown"))] += 1
            opportunity_counts[
                str(observation.get("opportunity_class", "unknown"))
            ] += 1
            tool_class = observation.get("tool_class")
            if tool_class is not None:
                tool_counts[str(tool_class)] += 1
            result_state = observation.get("tool_result_state")
            if result_state is not None:
                result_counts[str(result_state)] += 1

    failure_count = 0
    failure_path = state_root / "hook-failures.jsonl"
    if failure_path.exists():
        try:
            failure_count = sum(
                1
                for line in failure_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        except OSError:
            issues.append("hook-failures.jsonl: unreadable")

    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "generated_at": now_utc(),
        "state_root_ref": sha256_text(str(state_root.resolve())),
        "receipt_logs_valid": not issues,
        "issues": issues,
        "counts": {
            "sessions": session_count,
            "receipts": receipt_count,
            "hook_failures": failure_count,
            "events": dict(sorted(event_counts.items())),
            "routes": dict(sorted(route_counts.items())),
            "opportunities": dict(sorted(opportunity_counts.items())),
            "memo_tools": dict(sorted(tool_counts.items())),
            "tool_results": dict(sorted(result_counts.items())),
        },
        "claims": {
            "noticed": "unknown",
            "used_or_rejected": "unknown",
            "action_change": "unknown",
            "outcome": "unknown",
            "benefit_claim_allowed": False,
            "reason": (
                "shadow receipts prove only opportunity classification and "
                "observed aoa_memo tool-result stages"
            ),
        },
    }


def write_json_private(path: Path, payload: dict[str, Any]) -> None:
    ensure_private_directory(path.parent)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    file_fd = os.open(
        temporary,
        os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        0o600,
    )
    try:
        with os.fdopen(file_fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, indent=2))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    except BaseException:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise


def observe_command(args: argparse.Namespace) -> int:
    event_name: Any = "unknown"
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("hook input must be a JSON object")
        event_name = payload.get("hook_event_name")
        receipt = build_observation(payload)
        append_observation(args.state_root, receipt)
        return 0
    except BaseException as failure:
        record_failure(args.state_root, event_name, failure)
        if args.strict:
            print("aoa-memo participation hook validation failed", file=sys.stderr)
            return 1
        return 0


def summary_command(args: argparse.Namespace) -> int:
    summary = build_summary(args.state_root)
    if args.output is not None:
        write_json_private(args.output, summary)
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["receipt_logs_valid"] else 1


def verify_command(args: argparse.Namespace) -> int:
    receipts = load_receipts(args.receipt_log)
    issues = verify_chain(receipts)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print(f"[ok] {len(receipts)} aoa-memo participation receipts")
    return 0


def retention_command(args: argparse.Namespace) -> int:
    if args.execute and not args.acknowledge_whole_session_erasure:
        print(
            "--execute requires --acknowledge-whole-session-erasure",
            file=sys.stderr,
        )
        return 2
    try:
        report = build_retention_report(
            args.state_root,
            retention_days=args.retention_days,
            execute=args.execute,
            acknowledge_whole_session_erasure=(
                args.acknowledge_whole_session_erasure
            ),
        )
    except ValueError as failure:
        print(str(failure), file=sys.stderr)
        return 2
    if args.output is not None:
        write_json_private(args.output, report)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["issues"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Observe or review aoa-memo participation without content.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    observe = subparsers.add_parser("observe")
    observe.add_argument("--state-root", type=Path, required=True)
    observe.add_argument(
        "--strict",
        action="store_true",
        help="lab-only: report invalid input instead of silently failing open",
    )
    observe.set_defaults(handler=observe_command)

    summary = subparsers.add_parser("summary")
    summary.add_argument("--state-root", type=Path, required=True)
    summary.add_argument("--output", type=Path)
    summary.set_defaults(handler=summary_command)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--receipt-log", type=Path, required=True)
    verify.set_defaults(handler=verify_command)

    retention = subparsers.add_parser(
        "retention",
        help="plan or explicitly erase old, closed observation receipt chains",
    )
    retention.add_argument("--state-root", type=Path, required=True)
    retention.add_argument(
        "--retention-days",
        type=int,
        default=DEFAULT_RETENTION_DAYS,
    )
    retention.add_argument(
        "--execute",
        action="store_true",
        help="erase eligible whole-session chains; otherwise plan only",
    )
    retention.add_argument(
        "--acknowledge-whole-session-erasure",
        action="store_true",
        help="required acknowledgement for irreversible receipt erasure",
    )
    retention.add_argument("--output", type=Path)
    retention.set_defaults(handler=retention_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
