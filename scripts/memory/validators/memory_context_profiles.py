"""Memory/RAG/context validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403
from .questbook import validate_questbook_surface

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
            "audit_event.memory-retention-check.example.json",
            "audit_event.service-governed-fallback.example.json",
        ],
    }
    for kind, example_names in PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND.items():
        extra_kind_examples.setdefault(kind, []).extend(example_names)
    for kind, example_names in SELF_AGENCY_CONTINUITY_OBJECT_EXAMPLES_BY_KIND.items():
        extra_kind_examples.setdefault(kind, []).extend(example_names)

    for kind, example_names in extra_kind_examples.items():
        schema_name = Path(CORE_KIND_SCHEMA_MAP[kind]).name
        for example_name in example_names:
            validate_example(validator_for(schema_name), example_name)
            validate_example(profile_validator, example_name)

def validate_trust_lifecycle_contracts() -> None:
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")
    errors: list[str] = []

    for ref in (
        "docs/posture/MEMORY_TRUST_POSTURE.md",
        "docs/posture/LIFECYCLE.md",
        "schemas/recall-posture/trust_posture.schema.json",
        "schemas/recall-posture/lifecycle_posture.schema.json",
    ):
        if ref.endswith(".md") and ref not in registry.get("core_docs", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {ref}")
        if ref.endswith(".json") and ref not in registry.get("schemas", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {ref}")

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
    memory_examples.extend(PHASE_ALPHA_OBJECT_EXAMPLE_NAMES)
    memory_examples.extend(SELF_AGENCY_CONTINUITY_OBJECT_EXAMPLE_NAMES)

    for example_name in memory_examples:
        data = load_json(example_path_for(example_name))
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
