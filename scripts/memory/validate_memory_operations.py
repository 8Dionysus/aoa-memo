#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema", file=sys.stderr)
    raise SystemExit(2) from exc


ROOT = Path(__file__).resolve().parents[2]
FORMAT_CHECKER = FormatChecker()

WRITE_GUARD_PART = ROOT / "mechanics" / "operational-gate" / "parts" / "write-path-guardrails"
CONSOLIDATION_PART = ROOT / "mechanics" / "retention" / "parts" / "consolidation-and-forgetting"
KAG_TOS_PART = ROOT / "mechanics" / "consumer-handoff" / "parts" / "kag-tos-bridge-handoff"
RUNTIME_PART = ROOT / "mechanics" / "writeback" / "parts" / "runtime-and-temperature"
MODE_SCHEMA = ROOT / "schemas" / "recall-posture" / "memory_operation_mode.schema.json"
MODE_EXAMPLE = ROOT / "examples" / "recall" / "memory_operation_modes.example.json"

HIGH_RISK_MARKERS = {
    "indirect_prompt_injection",
    "sleeper_memory",
    "poisoned_experience",
    "source_spoofing",
    "private_data_bleed",
    "instruction_as_content",
}
EXPECTED_MODES = {
    "read_only",
    "write_candidate_only",
    "generate_without_read",
    "read_write_under_review",
    "frozen_read_mostly",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def schema_errors(schema_path: Path, payload_path: Path, payload: Any | None = None) -> list[str]:
    schema = load_json(schema_path)
    data = load_json(payload_path) if payload is None else payload
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    return [
        f"{rel(payload_path)}:{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]


def local_ref_target(ref: object) -> Path | None:
    if not isinstance(ref, str) or not ref:
        return None
    if ref.startswith(("http://", "https://", "web:", "operator:", "repo:", "aoa-", "abyss-", "state_capsule:", "audit_event:", "claim:", "bridge:", "episode:")):
        return None
    path_text = ref.split("#", 1)[0]
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        return None
    candidate = ROOT / path
    return candidate if candidate.exists() else None


def append_missing_local_refs(errors: list[str], label: str, refs: object) -> None:
    if not isinstance(refs, list):
        errors.append(f"{label} must be a list")
        return
    for index, ref in enumerate(refs):
        if not isinstance(ref, str) or not ref:
            errors.append(f"{label}[{index}] must be a non-empty string")
            continue
        if ref.startswith(("docs/", "mechanics/", "schemas/", "examples/", "generated/", "scripts/", "tests/")):
            path_text = ref.split("#", 1)[0]
            if not (ROOT / path_text).exists():
                errors.append(f"{label}[{index}] points to missing local ref {ref}")


def append_operation_mode_ref_error(errors: list[str], label: str, ref: object) -> None:
    if not isinstance(ref, str) or not ref:
        errors.append(f"{label} must be a non-empty string")
        return
    path_text, separator, mode = ref.partition("#")
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts or not path_text:
        errors.append(f"{label} must be a local operation mode ref")
        return
    target = ROOT / path_text
    if not target.exists():
        errors.append(f"{label} points to missing local ref {ref}")
        return
    if not target.is_file():
        errors.append(f"{label} points to non-file local ref {ref}")
        return
    if not separator or not mode:
        errors.append(f"{label} must include a #mode fragment")
        return
    if target.suffix.lower() != ".json":
        errors.append(f"{label} must point to a JSON operation mode catalog {ref}")
        return
    try:
        payload = load_json(target)
    except json.JSONDecodeError as exc:
        errors.append(f"{label} points to invalid JSON operation mode catalog {ref}: {exc.msg}")
        return
    modes = payload.get("modes") if isinstance(payload, dict) else None
    if not isinstance(modes, list):
        errors.append(f"{label} must point to an operation mode catalog with modes")
        return
    known_modes = {
        item.get("mode")
        for item in modes
        if isinstance(item, dict) and isinstance(item.get("mode"), str)
    }
    if mode not in known_modes:
        errors.append(f"{label} uses unknown mode {mode}")


def validate_required_text() -> list[str]:
    required_tokens = {
        "docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md": [
            "Untrusted text is data before it is memory.",
            "indirect instructions",
            "derivation lineage",
            "action-safety separation",
        ],
        "mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md": [
            "untrusted sources",
            "sleeper memory",
            "poisoned experience",
            "allowed result",
        ],
        "docs/memory/MEMORY_OPERATION_CYCLE.md": [
            "Candidate intake",
            "Consolidation",
            "Generated read models",
            "Consumer handoff",
            "MCP Access Plane",
            "`aoa_memo_brief`",
            "`aoa_memo_landing_plan`",
            "`run_dry_run: true`",
            "not memory truth",
        ],
        "mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md": [
            "demotion",
            "deduplication",
            "supersession",
            "archive",
            "freeze",
        ],
        "docs/posture/MEMORY_OPERATION_MODES.md": [
            "`read_only`",
            "`write_candidate_only`",
            "`generate_without_read`",
            "`read_write_under_review`",
            "`frozen_read_mostly`",
        ],
        "docs/memory/LIVING_MEMORY_TOPOLOGY.md": [
            "repo-local `memo/` port",
            "agent-local memory",
            "`aoa-memo`",
            "`aoa-kag`",
        ],
        "docs/memory/LOCAL_MEMO_PORT_STANDARD.md": [
            "memo/",
            "candidates/",
            "receipts/",
            "handoffs/",
            "MCP Support Boundary",
            "`aoa_memo_pending_exports`",
            "`aoa_memo_prepare_intake_packet`",
            "`aoa_memo_landing_plan`",
            "`run_dry_run: true`",
            "not central durable memory",
        ],
    }
    errors: list[str] = []
    for path_text, tokens in required_tokens.items():
        path = ROOT / path_text
        if not path.is_file():
            errors.append(f"{path_text} is missing")
            continue
        text = load_text(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{path_text} must mention {token!r}")
    return errors


def validate_operation_modes() -> list[str]:
    errors: list[str] = []
    payload = load_json(MODE_EXAMPLE)
    if not isinstance(payload, dict):
        return [f"{rel(MODE_EXAMPLE)} must be an object"]
    append_missing_local_refs(errors, "memory_operation_modes.source_refs", payload.get("source_refs"))
    modes = payload.get("modes")
    if not isinstance(modes, list):
        return errors + [f"{rel(MODE_EXAMPLE)} modes must be a list"]
    seen_modes: set[str] = set()
    for index, mode in enumerate(modes):
        errors.extend(schema_errors(MODE_SCHEMA, MODE_EXAMPLE, mode))
        if isinstance(mode, dict) and isinstance(mode.get("mode"), str):
            seen_modes.add(mode["mode"])
            if mode["mode"] == "generate_without_read" and mode.get("read_policy") != "none":
                errors.append("generate_without_read must keep read_policy none")
            if mode.get("write_policy") != "none" and mode.get("review_required") is not True:
                errors.append(f"{mode['mode']} write modes must require review")
        else:
            errors.append(f"{rel(MODE_EXAMPLE)} modes[{index}] must be an object")
    if seen_modes != EXPECTED_MODES:
        errors.append(
            f"{rel(MODE_EXAMPLE)} must expose modes {', '.join(sorted(EXPECTED_MODES))}"
        )
    return errors


def validate_write_path_guards() -> list[str]:
    errors: list[str] = []
    schema = WRITE_GUARD_PART / "schemas" / "memory_write_path_guard_v1.json"
    examples = sorted((WRITE_GUARD_PART / "examples").glob("memory_write_path_guard.*.example.json"))
    if len(examples) < 2:
        errors.append("write-path guardrails must keep at least two examples")
    for example in examples:
        errors.extend(schema_errors(schema, example))
        payload = load_json(example)
        append_missing_local_refs(errors, f"{rel(example)}.source_refs", payload.get("source_refs"))
        append_missing_local_refs(errors, f"{rel(example)}.review_route.evidence_refs", payload.get("review_route", {}).get("evidence_refs"))
        risks = set(payload.get("ingestion_risks", []))
        if risks & HIGH_RISK_MARKERS:
            if payload.get("allowed_write_result") == "reviewed_write":
                errors.append(f"{rel(example)} high-risk input must not allow reviewed_write")
            if payload.get("proposed_lifecycle") == "frozen":
                errors.append(f"{rel(example)} high-risk input must not propose frozen lifecycle")
        action = payload.get("action_safety_separation", {})
        if action.get("action_text_is_data") is not True:
            errors.append(f"{rel(example)} must keep action_text_is_data true")
        if payload.get("source_trust") in {"untrusted", "unknown"} and action.get("execution_owner") != "none":
            errors.append(f"{rel(example)} untrusted source must keep execution_owner none")
    return errors


def validate_consolidation_forgetting() -> list[str]:
    errors: list[str] = []
    schema = CONSOLIDATION_PART / "schemas" / "memory_consolidation_forgetting_operation_v1.json"
    examples = sorted((CONSOLIDATION_PART / "examples").glob("memory_consolidation_forgetting.*.example.json"))
    seen_types: set[str] = set()
    for example in examples:
        errors.extend(schema_errors(schema, example))
        payload = load_json(example)
        append_missing_local_refs(errors, f"{rel(example)}.source_refs", payload.get("source_refs"))
        seen_types.add(payload.get("operation_type", ""))
        transition = payload.get("lifecycle_transition", {})
        if transition.get("from") == transition.get("to"):
            errors.append(f"{rel(example)} lifecycle_transition must change posture")
        if payload.get("operation_type") == "supersede" and "replacement_memory_id" not in transition:
            errors.append(f"{rel(example)} supersede operation must name replacement_memory_id")
        if payload.get("operation_type") == "archive" and transition.get("to") != "archived":
            errors.append(f"{rel(example)} archive operation must transition to archived")
    if {"supersede", "archive"} - seen_types:
        errors.append("consolidation/forgetting examples must include supersede and archive")
    return errors


def validate_temporal_graph_edge() -> list[str]:
    errors: list[str] = []
    schema = KAG_TOS_PART / "schemas" / "memory_temporal_graph_edge_v1.json"
    example = KAG_TOS_PART / "examples" / "memory_temporal_graph_edge.bridge.example.json"
    errors.extend(schema_errors(schema, example))
    payload = load_json(example)
    append_missing_local_refs(errors, f"{rel(example)}.source_refs", payload.get("source_refs"))
    append_missing_local_refs(errors, f"{rel(example)}.provenance_thread_refs", payload.get("provenance_thread_refs"))
    if payload.get("lifecycle_state") in {"superseded", "retracted", "archived"} and payload.get("current_recall") == "preferred":
        errors.append(f"{rel(example)} inactive lifecycle must not be preferred recall")
    if not payload.get("stronger_owner_route"):
        errors.append(f"{rel(example)} must name stronger_owner_route")
    return errors


def validate_reviewed_intake_packets() -> list[str]:
    errors: list[str] = []
    schema = RUNTIME_PART / "schemas" / "reviewed_memory_intake_packet_v1.json"
    examples = sorted((RUNTIME_PART / "examples").glob("reviewed_memory_intake_packet.*.example.json"))
    producers: set[str] = set()
    for example in examples:
        errors.extend(schema_errors(schema, example))
        payload = load_json(example)
        producer = payload.get("producer", {})
        if isinstance(producer, dict) and isinstance(producer.get("repo"), str):
            producers.add(producer["repo"])
        append_missing_local_refs(errors, f"{rel(example)}.export_refs", payload.get("export_refs"))
        append_operation_mode_ref_error(errors, f"{rel(example)}.operation_mode_ref", payload.get("operation_mode_ref"))
        for key, value in payload.get("sanitization", {}).items():
            if value is not True:
                errors.append(f"{rel(example)} sanitization.{key} must be true")
        guard_ref = payload.get("write_path_guard_ref")
        if isinstance(guard_ref, str) and guard_ref.startswith("mechanics/") and not (ROOT / guard_ref).exists():
            errors.append(f"{rel(example)} write_path_guard_ref points to missing {guard_ref}")
    if {"abyss-stack", "abyss-machine"} - producers:
        errors.append("reviewed intake packets must cover abyss-stack and abyss-machine")
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    errors.extend(validate_required_text())
    errors.extend(validate_operation_modes())
    errors.extend(validate_write_path_guards())
    errors.extend(validate_consolidation_forgetting())
    errors.extend(validate_temporal_graph_edge())
    errors.extend(validate_reviewed_intake_packets())
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Memory operations validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("[ok] memory operations calibration surfaces are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
