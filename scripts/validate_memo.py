#!/usr/bin/env python3
"""Validate bootstrap aoa-memo artifacts.

This script is intentionally small and honest. It validates the current example
objects against the local JSON schemas, checks the local artifact refs they
expose, and performs a light structural check on `generated/memo_registry.min.json`.
"""

from __future__ import annotations

import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"
FORMAT_CHECKER = FormatChecker()
RFC3339_DATETIME = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SYMBOLIC_REF = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:")
WINDOWS_ABSOLUTE_PATH = re.compile(r"^[A-Za-z]:[\\\\/]")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@FORMAT_CHECKER.checks("date-time")
def is_rfc3339_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if not RFC3339_DATETIME.fullmatch(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def local_ref_error(ref_value: object, label: str) -> str | None:
    if not isinstance(ref_value, str) or not ref_value:
        return None
    if ref_value.startswith(("http://", "https://", "repo:")):
        return None
    if SYMBOLIC_REF.match(ref_value) and not WINDOWS_ABSOLUTE_PATH.match(ref_value):
        return None

    path_text, _, anchor = ref_value.partition("#")
    target = ROOT / path_text

    if not target.exists():
        return f"{label}: referenced path does not exist: {ref_value}"
    if anchor and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
        return f"{label}: referenced markdown anchor does not exist: {ref_value}"
    return None


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def validate_example(validator: Draft202012Validator, example_name: str) -> None:
    data = load_json(EXAMPLES / example_name)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks = [
        ("payload_ref", data.get("payload_ref")),
        ("bridges.route_capsule_ref", data.get("bridges", {}).get("route_capsule_ref")),
        ("inspect_surface", data.get("inspect_surface")),
        ("expand_surface", data.get("expand_surface")),
    ]
    for list_name in (
        "evidence_pack_refs",
        "contradiction_pack_refs",
        "witness_refs",
        "memory_delta_refs",
        "canon_delta_refs",
    ):
        values = data.get(list_name)
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            ref_checks.append((f"{list_name}[{index}]", value))
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")


def validate_support_schema(schema_name: str) -> None:
    validator_for(schema_name)
    print(f"[OK]   {schema_name}")


def validate_registry() -> None:
    data = load_json(GENERATED / "memo_registry.min.json")
    required = [
        "layer",
        "version",
        "status",
        "memory_object_kinds",
        "supporting_objects",
        "recall_modes",
        "temperature_scale",
        "core_docs",
        "schemas",
    ]
    missing = [key for key in required if key not in data]
    errors = [f"missing key: {key}" for key in missing]
    for key in ("core_docs", "schemas"):
        for index, ref in enumerate(data.get(key, [])):
            error = local_ref_error(ref, f"{key}[{index}]")
            if error:
                errors.append(error)
    if errors:
        print("[FAIL] generated/memo_registry.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   generated/memo_registry.min.json")


def validate_core_memory_contract() -> None:
    validator = validator_for("core-memory-contract.schema.json")
    data = load_json(EXAMPLES / "core_memory_contract.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    expected_core = registry.get("memory_object_kinds", [])
    expected_supporting = registry.get("supporting_objects", [])

    if sorted(data.get("core_memory_surfaces", [])) != sorted(expected_core):
        errors.append("core_memory_surfaces does not match generated/memo_registry.min.json memory_object_kinds")
    if sorted(data.get("supporting_objects", [])) != sorted(expected_supporting):
        errors.append("supporting_objects does not match generated/memo_registry.min.json supporting_objects")

    if errors:
        print("[FAIL] core_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   core_memory_contract.example.json")


def validate_witness_trace_contract() -> None:
    validator = validator_for("witness-trace.schema.json")
    data = load_json(EXAMPLES / "witness_trace.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "witness_trace" in registry.get("memory_object_kinds", []):
        errors.append("witness_trace must not appear in generated/memo_registry.min.json memory_object_kinds")
    if "witness_trace" in registry.get("supporting_objects", []):
        errors.append("witness_trace must not appear in generated/memo_registry.min.json supporting_objects")
    if "schemas/witness-trace.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/witness-trace.schema.json")
    if "docs/WITNESS_TRACE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/WITNESS_TRACE_CONTRACT.md")

    if not any(step.get("kind") == "tool" for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one tool-visible step")
    if not any("state_delta" in step for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one state_delta example")
    summary_output = data.get("summary_output", {})
    if summary_output.get("format") != "markdown":
        errors.append("witness_trace.example.json summary_output.format must stay 'markdown'")

    if errors:
        print("[FAIL] witness_trace.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   witness_trace.example.json")


def validate_checkpoint_to_memory_contract() -> None:
    validator = validator_for("checkpoint-to-memory-contract.schema.json")
    data = load_json(EXAMPLES / "checkpoint_to_memory_contract.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks = [("source_seed_ref", data.get("source_seed_ref"))]
    checkpoint_artifact = data.get("checkpoint_artifact", {})
    if isinstance(checkpoint_artifact, dict):
        ref_checks.append(("checkpoint_artifact.schema_ref", checkpoint_artifact.get("schema_ref")))
    runtime_boundary = data.get("runtime_boundary", {})
    if isinstance(runtime_boundary, dict):
        for index, value in enumerate(runtime_boundary.get("review_boundary_refs", [])):
            ref_checks.append((f"runtime_boundary.review_boundary_refs[{index}]", value))
    for index, rule in enumerate(data.get("mapping_rules", [])):
        if not isinstance(rule, dict):
            continue
        for ref_index, value in enumerate(rule.get("runtime_refs", [])):
            ref_checks.append((f"mapping_rules[{index}].runtime_refs[{ref_index}]", value))
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))

    if data.get("contract_type") != "checkpoint_to_memory_contract":
        errors.append("checkpoint_to_memory_contract.example.json contract_type must stay 'checkpoint_to_memory_contract'")
    if checkpoint_artifact.get("artifact_name") != "inquiry_checkpoint":
        errors.append("checkpoint_to_memory_contract.example.json must keep inquiry_checkpoint as the checkpoint artifact")
    if runtime_boundary.get("scratchpad_posture") != "runtime_local_only":
        errors.append("runtime scratchpad posture must stay runtime_local_only")
    if runtime_boundary.get("checkpoint_export_kind") != "state_capsule":
        errors.append("checkpoint export kind must stay state_capsule")
    if runtime_boundary.get("distillation_review_posture") != "review_required":
        errors.append("distillation review posture must stay review_required")

    expected_pairs = {
        ("checkpoint_export", "state_capsule"),
        ("approval_record", "decision"),
        ("transition_record", "decision"),
        ("execution_trace", "episode"),
        ("review_trace", "audit_event"),
        ("distillation_claim_candidate", "claim"),
        ("distillation_pattern_candidate", "pattern"),
        ("distillation_bridge_candidate", "bridge"),
    }
    seen_pairs = {
        (rule.get("runtime_surface"), rule.get("target_kind"))
        for rule in data.get("mapping_rules", [])
        if isinstance(rule, dict)
    }
    missing_pairs = sorted(expected_pairs - seen_pairs)
    if missing_pairs:
        errors.append(
            "checkpoint_to_memory_contract.example.json is missing required runtime-to-memo mappings: "
            + ", ".join(f"{surface}->{kind}" for surface, kind in missing_pairs)
        )

    for target_kind in ("claim", "pattern", "bridge"):
        matching_rules = [
            rule
            for rule in data.get("mapping_rules", [])
            if isinstance(rule, dict) and rule.get("target_kind") == target_kind
        ]
        if not matching_rules:
            continue
        for rule in matching_rules:
            if rule.get("writeback_class") != "reviewed_candidate":
                errors.append(f"{target_kind} mappings must stay reviewed_candidate writeback")
            if rule.get("requires_human_review") is not True:
                errors.append(f"{target_kind} mappings must require human review")

    if "schemas/checkpoint-to-memory-contract.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/checkpoint-to-memory-contract.schema.json")
    if "docs/RUNTIME_WRITEBACK_SEAM.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/RUNTIME_WRITEBACK_SEAM.md")

    if errors:
        print("[FAIL] checkpoint_to_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   checkpoint_to_memory_contract.example.json")


def main() -> int:
    validate_support_schema("decay_policy.schema.json")
    validate_support_schema("inquiry_checkpoint.schema.json")
    validate_support_schema("checkpoint-to-memory-contract.schema.json")
    validate_example(validator_for("memory_object.schema.json"), "episode.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_approval_record.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_health_check.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "checkpoint_improvement_thread.example.json")
    validate_example(validator_for("recall_contract.schema.json"), "recall_contract.semantic.json")
    validate_registry()
    validate_core_memory_contract()
    validate_checkpoint_to_memory_contract()
    validate_witness_trace_contract()
    print("\nValidation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
