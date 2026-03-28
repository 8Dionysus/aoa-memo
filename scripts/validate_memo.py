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
    from referencing import Registry, Resource
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
CORE_KIND_SCHEMA_MAP = {
    "anchor": "schemas/anchor.schema.json",
    "state_capsule": "schemas/state_capsule.schema.json",
    "episode": "schemas/episode.schema.json",
    "claim": "schemas/claim.schema.json",
    "decision": "schemas/decision.schema.json",
    "pattern": "schemas/pattern.schema.json",
    "bridge": "schemas/bridge.schema.json",
    "audit_event": "schemas/audit_event.schema.json",
}
CORE_KIND_EXAMPLE_MAP = {
    "anchor": "anchor.example.json",
    "state_capsule": "state_capsule.example.json",
    "episode": "episode.example.json",
    "claim": "claim.example.json",
    "decision": "checkpoint_approval_record.example.json",
    "pattern": "pattern.example.json",
    "bridge": "bridge.kag-lift.example.json",
    "audit_event": "audit_event.supersession.example.json",
}


def validate_nested_agents_surface() -> None:
    try:
        from validate_nested_agents import validate_nested_agents_docs
    except Exception as exc:  # pragma: no cover - defensive wiring guard
        print("[FAIL] nested AGENTS docs")
        print(f"  - unable to load nested AGENTS validator: {exc}")
        raise SystemExit(1) from exc

    try:
        validate_nested_agents_docs()
    except RuntimeError as exc:
        print("[FAIL] nested AGENTS docs")
        print(f"  - {exc}")
        raise SystemExit(1) from exc

    print("[OK]   nested AGENTS docs")


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


def append_ref_errors(errors: list[str], ref_checks: list[tuple[str, object]]) -> None:
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))


@lru_cache(maxsize=None)
def schema_registry() -> Registry:
    resources: list[tuple[str, Resource]] = []
    for path in SCHEMAS.glob("*.json"):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER, registry=schema_registry())


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
        ("capsule_surface", data.get("capsule_surface")),
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
    return_pack = data.get("return_pack")
    if isinstance(return_pack, dict):
        for list_name in ("anchor_refs", "reentry_refs"):
            values = return_pack.get(list_name)
            if not isinstance(values, list):
                continue
            for index, value in enumerate(values):
                ref_checks.append((f"return_pack.{list_name}[{index}]", value))
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


def validate_memory_object_profiles() -> None:
    profile_validator = validator_for("memory_object_profile.schema.json")

    for kind, schema_path in CORE_KIND_SCHEMA_MAP.items():
        schema_name = Path(schema_path).name
        example_name = CORE_KIND_EXAMPLE_MAP[kind]
        validate_example(validator_for(schema_name), example_name)
        validate_example(profile_validator, example_name)

    extra_kind_examples = {
        "episode": [
            "checkpoint_health_check.example.json",
            "episode.tos-interpretation.example.json",
        ],
        "claim": [
            "claim.tos-bridge-ready.example.json",
            "claim.current-entrypoint.example.json",
            "claim.superseded.example.json",
            "claim.retracted.example.json",
        ],
        "audit_event": [
            "audit_event.retraction.example.json",
        ],
    }

    for kind, example_names in extra_kind_examples.items():
        schema_name = Path(CORE_KIND_SCHEMA_MAP[kind]).name
        for example_name in example_names:
            validate_example(validator_for(schema_name), example_name)
            validate_example(profile_validator, example_name)


def validate_trust_lifecycle_contracts() -> None:
    registry = load_json(GENERATED / "memo_registry.min.json")
    errors: list[str] = []

    for ref in (
        "docs/MEMORY_TRUST_POSTURE.md",
        "docs/LIFECYCLE.md",
        "schemas/trust_posture.schema.json",
        "schemas/lifecycle_posture.schema.json",
    ):
        if ref.endswith(".md") and ref not in registry.get("core_docs", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")
        if ref.endswith(".json") and ref not in registry.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")

    memory_examples = [
        "anchor.example.json",
        "state_capsule.example.json",
        "episode.example.json",
        "episode.tos-interpretation.example.json",
        "claim.example.json",
        "claim.current-entrypoint.example.json",
        "claim.superseded.example.json",
        "claim.retracted.example.json",
        "claim.tos-bridge-ready.example.json",
        "checkpoint_approval_record.example.json",
        "checkpoint_health_check.example.json",
        "pattern.example.json",
        "bridge.kag-lift.example.json",
        "audit_event.supersession.example.json",
        "audit_event.retraction.example.json",
    ]

    for example_name in memory_examples:
        data = load_json(EXAMPLES / example_name)
        trust = data.get("trust", {})
        lifecycle = data.get("lifecycle", {})
        current_recall = lifecycle.get("current_recall", {})

        if trust.get("temperature") == "frozen" and lifecycle.get("review_state") != "frozen":
            errors.append(f"{example_name} must keep lifecycle.review_state == 'frozen' when trust.temperature == 'frozen'")
        if current_recall.get("status") == "withdrawn" and lifecycle.get("review_state") != "retracted":
            errors.append(f"{example_name} withdrawn current_recall posture must stay tied to review_state 'retracted'")

    if errors:
        print("[FAIL] trust/lifecycle contract surfaces")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   trust/lifecycle contract surfaces")


def validate_memory_object_surface_manifest() -> None:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    data = load_json(EXAMPLES / "memory_object_surface_manifest.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    seen_paths: set[str] = set()
    for index, entry in enumerate(data.get("entries", [])):
        path = entry.get("example_path")
        if path in seen_paths:
            errors.append(f"entries[{index}].example_path duplicates {path}")
        if isinstance(path, str):
            seen_paths.add(path)
        error = local_ref_error(path, f"entries[{index}].example_path")
        if error:
            errors.append(error)

    if errors:
        print("[FAIL] memory_object_surface_manifest.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_object_surface_manifest.json")


def validate_recall_contract_example(
    example_name: str,
    *,
    expected_mode: str,
    expected_allowed_scopes: list[str],
    expected_preferred_kinds: list[str],
    expected_temperature_order: list[str],
    expected_inspect_surface: str,
    expected_expand_surface: str,
    expected_source_route_required: bool,
    expected_capsule_surface: str | None = None,
    expected_checkpoint_continuity_supported: bool | None = None,
    expected_return_ready: bool | None = None,
    expected_preferred_anchor_kinds: list[str] | None = None,
    expected_support_artifact_refs: list[str] | None = None,
) -> None:
    validator = validator_for("recall_contract.schema.json")
    data = load_json(EXAMPLES / example_name)

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    support_artifact_refs = data.get("support_artifact_refs")
    if not isinstance(support_artifact_refs, list):
        support_artifact_refs = []
    append_ref_errors(
        errors,
        [
            ("inspect_surface", data.get("inspect_surface")),
            ("capsule_surface", data.get("capsule_surface")),
            ("expand_surface", data.get("expand_surface")),
        ]
        + [
            (f"support_artifact_refs[{index}]", value)
            for index, value in enumerate(support_artifact_refs)
        ],
    )

    if data.get("mode") != expected_mode:
        errors.append(f"{example_name} mode must stay '{expected_mode}'")
    if data.get("allowed_scopes") != expected_allowed_scopes:
        errors.append(f"{example_name} allowed_scopes must stay {expected_allowed_scopes}")
    if data.get("preferred_kinds") != expected_preferred_kinds:
        errors.append(f"{example_name} preferred_kinds must stay {expected_preferred_kinds}")
    if data.get("temperature_order") != expected_temperature_order:
        errors.append(f"{example_name} temperature_order must stay {expected_temperature_order}")
    if data.get("inspect_surface") != expected_inspect_surface:
        errors.append(f"{example_name} inspect_surface must stay {expected_inspect_surface}")
    if expected_capsule_surface is not None and data.get("capsule_surface") != expected_capsule_surface:
        errors.append(f"{example_name} capsule_surface must stay {expected_capsule_surface}")
    if data.get("expand_surface") != expected_expand_surface:
        errors.append(f"{example_name} expand_surface must stay {expected_expand_surface}")
    if data.get("source_route_required") is not expected_source_route_required:
        errors.append(f"{example_name} source_route_required must stay {expected_source_route_required}")
    if expected_checkpoint_continuity_supported is not None and data.get("checkpoint_continuity_supported") is not expected_checkpoint_continuity_supported:
        errors.append(
            f"{example_name} checkpoint_continuity_supported must stay {expected_checkpoint_continuity_supported}"
        )
    if expected_return_ready is not None and data.get("return_ready") is not expected_return_ready:
        errors.append(f"{example_name} return_ready must stay {expected_return_ready}")
    if expected_preferred_anchor_kinds is not None and data.get("preferred_anchor_kinds") != expected_preferred_anchor_kinds:
        errors.append(f"{example_name} preferred_anchor_kinds must stay {expected_preferred_anchor_kinds}")
    if expected_support_artifact_refs is not None and data.get("support_artifact_refs") != expected_support_artifact_refs:
        errors.append(f"{example_name} support_artifact_refs must stay {expected_support_artifact_refs}")

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")


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
        "generated_surface_families",
        "validation_commands",
    ]
    missing = [key for key in required if key not in data]
    errors = [f"missing key: {key}" for key in missing]
    for key in ("core_docs", "schemas"):
        for index, ref in enumerate(data.get(key, [])):
            error = local_ref_error(ref, f"{key}[{index}]")
            if error:
                errors.append(error)

    expected_schemas = {
        "schemas/memory_object_surface_manifest.schema.json",
        "schemas/memory_object_catalog.schema.json",
        "schemas/memory_object_capsules.schema.json",
        "schemas/memory_object_sections.schema.json",
    }
    for schema_ref in sorted(expected_schemas):
        if schema_ref not in data.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {schema_ref}")

    families = {
        item.get("family"): item
        for item in data.get("generated_surface_families", [])
        if isinstance(item, dict) and isinstance(item.get("family"), str)
    }
    if "doctrine" not in families:
        errors.append("generated/memo_registry.min.json must publish doctrine generated_surface_families entry")
    if "memory_objects" not in families:
        errors.append("generated/memo_registry.min.json must publish memory_objects generated_surface_families entry")

    doctrine = families.get("doctrine", {})
    doctrine_outputs = [
        "generated/memory_catalog.json",
        "generated/memory_catalog.min.json",
        "generated/memory_capsules.json",
        "generated/memory_sections.full.json",
    ]
    if doctrine.get("source_of_truth") != "aoa-memo-doctrine-route-surfaces-v1":
        errors.append("doctrine generated_surface_families entry must keep source_of_truth aoa-memo-doctrine-route-surfaces-v1")
    if doctrine.get("outputs") != doctrine_outputs:
        errors.append("doctrine generated_surface_families entry must list the doctrine output family")
    if doctrine.get("validator_command") != "python scripts/validate_memory_surfaces.py":
        errors.append("doctrine generated_surface_families entry must keep validator_command python scripts/validate_memory_surfaces.py")

    memory_objects = families.get("memory_objects", {})
    object_outputs = [
        "generated/memory_object_catalog.json",
        "generated/memory_object_catalog.min.json",
        "generated/memory_object_capsules.json",
        "generated/memory_object_sections.full.json",
    ]
    if memory_objects.get("source_of_truth") != "aoa-memo-object-example-surfaces-v1":
        errors.append("memory_objects generated_surface_families entry must keep source_of_truth aoa-memo-object-example-surfaces-v1")
    if memory_objects.get("manifest") != "examples/memory_object_surface_manifest.json":
        errors.append("memory_objects generated_surface_families entry must list examples/memory_object_surface_manifest.json as the manifest")
    if memory_objects.get("outputs") != object_outputs:
        errors.append("memory_objects generated_surface_families entry must list the object output family")
    if memory_objects.get("generator_command") != "python scripts/generate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep generator_command python scripts/generate_memory_object_surfaces.py")
    if memory_objects.get("validator_command") != "python scripts/validate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep validator_command python scripts/validate_memory_object_surfaces.py")

    for family_name, family in families.items():
        manifest = family.get("manifest")
        if manifest is not None:
            error = local_ref_error(manifest, f"generated_surface_families.{family_name}.manifest")
            if error:
                errors.append(error)
        for index, ref in enumerate(family.get("outputs", [])):
            error = local_ref_error(ref, f"generated_surface_families.{family_name}.outputs[{index}]")
            if error:
                errors.append(error)

    required_validation_commands = {
        "python scripts/validate_memo.py",
        "python scripts/validate_memory_surfaces.py",
        "python scripts/validate_memory_object_surfaces.py",
        "python scripts/validate_lifecycle_audit_examples.py",
    }
    missing_commands = sorted(required_validation_commands - set(data.get("validation_commands", [])))
    if missing_commands:
        errors.append("generated/memo_registry.min.json missing validation commands: " + ", ".join(missing_commands))

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
    expected_profile_schema = "schemas/memory_object_profile.schema.json"
    expected_kind_schemas = CORE_KIND_SCHEMA_MAP

    append_ref_errors(
        errors,
        [("profile_schema", data.get("profile_schema"))]
        + [
            (f"kind_profile_schemas.{kind}", ref)
            for kind, ref in data.get("kind_profile_schemas", {}).items()
        ],
    )

    if sorted(data.get("core_memory_surfaces", [])) != sorted(expected_core):
        errors.append("core_memory_surfaces does not match generated/memo_registry.min.json memory_object_kinds")
    if sorted(data.get("supporting_objects", [])) != sorted(expected_supporting):
        errors.append("supporting_objects does not match generated/memo_registry.min.json supporting_objects")
    if data.get("profile_schema") != expected_profile_schema:
        errors.append("profile_schema must stay schemas/memory_object_profile.schema.json")
    if data.get("kind_profile_schemas") != expected_kind_schemas:
        errors.append("kind_profile_schemas does not match the shipped per-kind profile schema map")

    for ref in [expected_profile_schema, *expected_kind_schemas.values()]:
        if ref not in registry.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")
    if "docs/MEMORY_OBJECT_PROFILES.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/MEMORY_OBJECT_PROFILES.md")

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
    append_ref_errors(errors, ref_checks)

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

    runtime_surface_targets: dict[str, set[str]] = {}
    for rule in data.get("mapping_rules", []):
        if not isinstance(rule, dict):
            continue
        runtime_surface = rule.get("runtime_surface")
        target_kind = rule.get("target_kind")
        if not isinstance(runtime_surface, str) or not isinstance(target_kind, str):
            continue
        runtime_surface_targets.setdefault(runtime_surface, set()).add(target_kind)
    conflicting_runtime_mappings = {
        runtime_surface: sorted(target_kinds)
        for runtime_surface, target_kinds in runtime_surface_targets.items()
        if len(target_kinds) > 1
    }
    for runtime_surface, target_kinds in sorted(conflicting_runtime_mappings.items()):
        errors.append(
            "checkpoint_to_memory_contract.example.json has conflicting target kinds for "
            f"{runtime_surface}: {', '.join(target_kinds)}"
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


def validate_bridge_export_contracts() -> None:
    chunk_validator = validator_for("memory_chunk_face.schema.json")
    graph_validator = validator_for("memory_graph_face.schema.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    episode = load_json(EXAMPLES / "episode.tos-interpretation.example.json")
    claim = load_json(EXAMPLES / "claim.tos-bridge-ready.example.json")
    bridge = load_json(EXAMPLES / "bridge.kag-lift.example.json")
    thread = load_json(EXAMPLES / "provenance_thread.kag-lift.example.json")
    chunk = load_json(EXAMPLES / "memory_chunk_face.bridge.example.json")
    graph = load_json(EXAMPLES / "memory_graph_face.bridge.example.json")

    errors = [
        f"chunk.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(chunk_validator.iter_errors(chunk), key=lambda err: list(err.absolute_path))
    ]
    errors.extend(
        f"graph.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(graph_validator.iter_errors(graph), key=lambda err: list(err.absolute_path))
    )

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(thread.get("source_refs", [])):
        ref_checks.append((f"provenance_thread.kag-lift.source_refs[{index}]", value))
    for list_name in ("section_refs", "source_refs", "source_fragment_refs", "strongest_next_sources"):
        for index, value in enumerate(chunk.get(list_name, [])):
            ref_checks.append((f"memory_chunk_face.bridge.{list_name}[{index}]", value))
    for index, value in enumerate(graph.get("tos_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.tos_refs[{index}]", value))
    for index, value in enumerate(graph.get("strongest_authored_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.strongest_authored_refs[{index}]", value))
    for rel_index, relation in enumerate(graph.get("relation_candidates", [])):
        if not isinstance(relation, dict):
            continue
        for ref_index, value in enumerate(relation.get("evidence_refs", [])):
            ref_checks.append((f"memory_graph_face.bridge.relation_candidates[{rel_index}].evidence_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    episode_id = episode.get("id")
    claim_id = claim.get("id")
    bridge_id = bridge.get("id")
    thread_id = thread.get("id")

    if episode_id not in claim.get("provenance", {}).get("episode_refs", []):
        errors.append("claim.tos-bridge-ready.example.json must point back to the ToS interpretation episode")
    if claim.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("claim.tos-bridge-ready.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if bridge.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("bridge.kag-lift.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if sorted(thread.get("memory_object_ids", [])) != sorted([episode_id, claim_id, bridge_id]):
        errors.append("provenance_thread.kag-lift.example.json must track the episode, claim, and bridge example ids")

    if chunk.get("source_memory_id") != bridge_id:
        errors.append("memory_chunk_face.bridge.example.json must export the bridge.kag-lift example")
    if bridge_id not in chunk.get("bridge_refs", []):
        errors.append("memory_chunk_face.bridge.example.json must keep the bridge id in bridge_refs")
    if graph.get("source_memory_id") != bridge_id:
        errors.append("memory_graph_face.bridge.example.json must export the bridge.kag-lift example")
    if thread_id not in graph.get("provenance_thread_ids", []):
        errors.append("memory_graph_face.bridge.example.json must preserve the provenance thread id")

    relation_targets = {relation.get("target_ref") for relation in graph.get("relation_candidates", []) if isinstance(relation, dict)}
    if episode_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the source episode")
    if claim_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the reviewed claim")

    bridge_bridges = bridge.get("bridges", {})
    shared_envelope_ref = bridge_bridges.get("shared_envelope_ref")
    if shared_envelope_ref != "repo:aoa-kag/examples/aoa_tos_bridge_envelope.example.json":
        errors.append("bridge.kag-lift.example.json must keep shared_envelope_ref pointed at the canonical aoa-kag envelope example")
    append_ref_errors(
        errors,
        [("bridge.kag-lift.shared_envelope_ref", shared_envelope_ref)],
    )
    if bridge_bridges.get("kag_lift_status") != "candidate":
        errors.append("bridge.kag-lift.example.json must keep kag_lift_status as candidate")
    if not bridge_bridges.get("tos_refs"):
        errors.append("bridge.kag-lift.example.json must keep at least one ToS ref")
    if graph.get("kag_lift_status") != bridge_bridges.get("kag_lift_status"):
        errors.append("memory_graph_face.bridge.example.json must match the bridge kag_lift_status")

    if "schemas/memory_chunk_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_chunk_face.schema.json")
    if "schemas/memory_graph_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_graph_face.schema.json")
    if "docs/KAG_TOS_BRIDGE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/KAG_TOS_BRIDGE_CONTRACT.md")

    if errors:
        print("[FAIL] bridge export contract surfaces")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   bridge export contract surfaces")


def _guardrail_case_input_refs(case: dict[str, object]) -> set[str]:
    values = case.get("input_refs", [])
    if not isinstance(values, list):
        return set()
    return {value for value in values if isinstance(value, str)}


def _validate_guardrail_pilot_cases(
    case_by_focus: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    pilot_focuses = {"recall_precision", "provenance_fidelity", "staleness"}
    missing_pilot_focuses = sorted(pilot_focuses - set(case_by_focus))
    if missing_pilot_focuses:
        errors.append(
            "memory_eval_guardrail_pack.example.json must keep first-pilot focuses: "
            + ", ".join(missing_pilot_focuses)
        )

    precision_case = case_by_focus.get("recall_precision")
    if isinstance(precision_case, dict):
        refs = _guardrail_case_input_refs(precision_case)
        recall_contract_refs = [
            ref for ref in refs if ref.startswith("examples/recall_contract.")
        ]
        if not recall_contract_refs:
            errors.append(
                "recall_precision guardrail case must reference at least one recall contract example"
            )
        doctrine_surface_family = {
            "generated/memory_catalog.min.json",
            "generated/memory_capsules.json",
            "generated/memory_sections.full.json",
        }
        object_surface_family = {
            "generated/memory_object_catalog.min.json",
            "generated/memory_object_capsules.json",
            "generated/memory_object_sections.full.json",
        }
        if not (
            doctrine_surface_family.issubset(refs) or object_surface_family.issubset(refs)
        ):
            errors.append(
                "recall_precision guardrail case must reference one inspect/capsule/expand surface family"
            )

    provenance_case = case_by_focus.get("provenance_fidelity")
    if isinstance(provenance_case, dict):
        refs = _guardrail_case_input_refs(provenance_case)
        if not any(ref.startswith("examples/provenance_thread.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a provenance_thread example"
            )
        if not any(ref.startswith("examples/claim.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a claim example"
            )
        if not any(ref.startswith("examples/bridge.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a bridge example"
            )

    staleness_case = case_by_focus.get("staleness")
    if isinstance(staleness_case, dict):
        refs = _guardrail_case_input_refs(staleness_case)
        required_docs = {
            "docs/LIFECYCLE.md",
            "docs/MEMORY_TRUST_POSTURE.md",
        }
        missing_docs = sorted(required_docs - refs)
        if missing_docs:
            errors.append(
                "staleness guardrail case must reference lifecycle/trust docs: "
                + ", ".join(missing_docs)
            )
        required_examples = {
            "examples/claim.current-entrypoint.example.json",
            "examples/claim.superseded.example.json",
            "examples/claim.retracted.example.json",
        }
        missing_examples = sorted(required_examples - refs)
        if missing_examples:
            errors.append(
                "staleness guardrail case must reference current/superseded/retracted examples: "
                + ", ".join(missing_examples)
            )


def validate_memory_eval_guardrail_pack() -> None:
    validator = validator_for("memory_eval_guardrail_pack.schema.json")
    data = load_json(EXAMPLES / "memory_eval_guardrail_pack.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(data.get("source_refs", [])):
        ref_checks.append((f"memory_eval_guardrail_pack.source_refs[{index}]", value))
    for case_index, case in enumerate(data.get("cases", [])):
        if not isinstance(case, dict):
            continue
        for ref_index, value in enumerate(case.get("input_refs", [])):
            ref_checks.append((f"memory_eval_guardrail_pack.cases[{case_index}].input_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    seen_case_ids: set[str] = set()
    seen_focuses: set[str] = set()
    case_by_focus: dict[str, dict[str, object]] = {}
    for case in data.get("cases", []):
        if not isinstance(case, dict):
            continue
        case_id = case.get("case_id")
        focus = case.get("focus")
        if isinstance(case_id, str):
            if case_id in seen_case_ids:
                errors.append(f"duplicate guardrail case id: {case_id}")
            seen_case_ids.add(case_id)
        if isinstance(focus, str):
            seen_focuses.add(focus)
            case_by_focus[focus] = case

    required_focuses = {
        "recall_precision",
        "provenance_fidelity",
        "staleness",
        "contradiction_handling",
        "permission_leakage",
        "over_promotion",
        "hallucinated_merge",
    }
    missing_focuses = sorted(required_focuses - seen_focuses)
    if missing_focuses:
        errors.append("memory_eval_guardrail_pack.example.json is missing required focuses: " + ", ".join(missing_focuses))

    _validate_guardrail_pilot_cases(case_by_focus, errors)

    if data.get("handoff_target") != "aoa-evals":
        errors.append("memory_eval_guardrail_pack.example.json must hand off to aoa-evals")
    if "schemas/memory_eval_guardrail_pack.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_eval_guardrail_pack.schema.json")
    if "docs/MEMORY_EVAL_GUARDRAILS.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/MEMORY_EVAL_GUARDRAILS.md")

    if errors:
        print("[FAIL] memory_eval_guardrail_pack.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_eval_guardrail_pack.example.json")


def main() -> int:
    validate_nested_agents_surface()
    validate_support_schema("memory_object_profile.schema.json")
    validate_support_schema("trust_posture.schema.json")
    validate_support_schema("lifecycle_posture.schema.json")
    validate_support_schema("anchor.schema.json")
    validate_support_schema("state_capsule.schema.json")
    validate_support_schema("episode.schema.json")
    validate_support_schema("claim.schema.json")
    validate_support_schema("decision.schema.json")
    validate_support_schema("pattern.schema.json")
    validate_support_schema("bridge.schema.json")
    validate_support_schema("audit_event.schema.json")
    validate_support_schema("memory_object_surface_manifest.schema.json")
    validate_support_schema("memory_object_catalog.schema.json")
    validate_support_schema("memory_object_capsules.schema.json")
    validate_support_schema("memory_object_sections.schema.json")
    validate_support_schema("decay_policy.schema.json")
    validate_support_schema("inquiry_checkpoint.schema.json")
    validate_support_schema("checkpoint-to-memory-contract.schema.json")
    validate_support_schema("memory_chunk_face.schema.json")
    validate_support_schema("memory_graph_face.schema.json")
    validate_support_schema("memory_eval_guardrail_pack.schema.json")
    validate_memory_object_surface_manifest()
    validate_example(validator_for("memory_object.schema.json"), "episode.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_approval_record.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_health_check.example.json")
    validate_example(validator_for("memory_object.schema.json"), "episode.tos-interpretation.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.tos-bridge-ready.example.json")
    validate_example(validator_for("memory_object.schema.json"), "bridge.kag-lift.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.return.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "checkpoint_improvement_thread.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.kag-lift.example.json")
    validate_recall_contract_example(
        "recall_contract.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memo_registry.min.json",
        expected_expand_surface="docs/MEMORY_MODEL.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_capsule_surface="generated/memory_capsules.json",
        expected_expand_surface="generated/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_expand_surface="docs/RUNTIME_WRITEBACK_SEAM.md",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_expand_surface="docs/KAG_TOS_BRIDGE_CONTRACT.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_capsule_surface="generated/memory_capsules.json",
        expected_expand_surface="generated/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.return.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=False,
        expected_checkpoint_continuity_supported=True,
        expected_return_ready=True,
        expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
        expected_support_artifact_refs=[
            "schemas/inquiry_checkpoint.schema.json",
            "schemas/checkpoint-to-memory-contract.schema.json",
            "docs/RUNTIME_WRITEBACK_SEAM.md",
            "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        ],
    )
    validate_recall_contract_example(
        "recall_contract.object.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
    validate_memory_object_profiles()
    validate_trust_lifecycle_contracts()
    validate_registry()
    validate_core_memory_contract()
    validate_checkpoint_to_memory_contract()
    validate_witness_trace_contract()
    validate_bridge_export_contracts()
    validate_memory_eval_guardrail_pack()
    print("\nValidation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
