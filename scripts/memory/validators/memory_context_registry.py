"""Memory/RAG/context validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403
from .questbook import validate_questbook_surface

def validate_registry() -> None:
    data = load_json(GENERATED / "memory" / "memo_registry.min.json")
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

    registry_version = data.get("version")
    readme_release = README_CURRENT_RELEASE.search(load_text(ROOT / "README.md"))
    changelog_release = CHANGELOG_RELEASE_HEADING.search(load_text(ROOT / "CHANGELOG.md"))
    roadmap = load_text(ROOT / "ROADMAP.md")
    if not isinstance(registry_version, str) or not registry_version:
        errors.append("generated/memory/memo_registry.min.json version must be a non-empty string")
    if readme_release is None:
        errors.append("README.md must publish a Current release line")
    if changelog_release is None:
        errors.append("CHANGELOG.md must publish at least one numeric release heading")
    if isinstance(registry_version, str) and readme_release is not None:
        readme_version = readme_release.group("version")
        if registry_version != readme_version:
            errors.append(
                "generated/memory/memo_registry.min.json version must match README.md current release "
                f"{readme_version!r}"
            )
        if f"`v{registry_version}`" not in roadmap:
            errors.append(
                "ROADMAP.md must mention the current memo registry release as "
                f"`v{registry_version}`"
            )
    if isinstance(registry_version, str) and changelog_release is not None:
        changelog_version = changelog_release.group("version")
        if registry_version != changelog_version:
            errors.append(
                "generated/memory/memo_registry.min.json version must match CHANGELOG.md latest release "
                f"{changelog_version!r}"
            )

    for key in ("core_docs", "schemas"):
        for index, ref in enumerate(data.get(key, [])):
            error = local_ref_error(ref, f"{key}[{index}]")
            if error:
                errors.append(error)

    expected_schemas = {
        "mechanics/antifragility/parts/failure-lesson-memory/schemas/failure_lesson_memory_v1.json",
        "schemas/generated-surfaces/artifact_identity.schema.json",
        "schemas/generated-surfaces/memory_object_surface_manifest.schema.json",
        "schemas/generated-surfaces/memory_object_catalog.schema.json",
        "schemas/generated-surfaces/memory_object_capsules.schema.json",
        "schemas/generated-surfaces/memory_object_sections.schema.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json",
    }
    for schema_ref in sorted(expected_schemas):
        if schema_ref not in data.get("schemas", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {schema_ref}")
    required_core_docs = (
        "mechanics/antifragility/docs/FAILURE_LESSON_MEMORY.md",
        "mechanics/antifragility/docs/FAILURE_LESSON_RECALL.md",
        "mechanics/antifragility/docs/RECOVERY_PATTERN_MEMORY.md",
        "mechanics/antifragility/docs/RECOVERY_PATTERN_RECALL.md",
        "mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md",
        "mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md",
        "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        "mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md",
        "mechanics/checkpoint/docs/CHECKPOINT_MEMORY_BOUNDARY.md",
        "mechanics/checkpoint/docs/CHECKPOINT_CARRY_CONTRACT.md",
        "mechanics/checkpoint/docs/CHECKPOINT_APPROVAL_HEALTH_MEMORY.md",
        "mechanics/checkpoint/docs/CHECKPOINT_TO_MEMORY_MAPPING.md",
        "mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md",
    )
    for doc_ref in required_core_docs:
        if doc_ref not in data.get("core_docs", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {doc_ref}")

    families = {
        item.get("family"): item
        for item in data.get("generated_surface_families", [])
        if isinstance(item, dict) and isinstance(item.get("family"), str)
    }
    if "doctrine" not in families:
        errors.append("generated/memory/memo_registry.min.json must publish doctrine generated_surface_families entry")
    if "memory_objects" not in families:
        errors.append("generated/memory/memo_registry.min.json must publish memory_objects generated_surface_families entry")
    if "kag_export" not in families:
        errors.append("generated/memory/memo_registry.min.json must publish kag_export generated_surface_families entry")

    doctrine = families.get("doctrine", {})
    doctrine_outputs = [
        "generated/memory/memory_catalog.json",
        "generated/memory/memory_catalog.min.json",
        "generated/memory/memory_capsules.json",
        "generated/memory/memory_sections.full.json",
    ]
    if doctrine.get("source_of_truth") != "aoa-memo-doctrine-route-surfaces-v1":
        errors.append("doctrine generated_surface_families entry must keep source_of_truth aoa-memo-doctrine-route-surfaces-v1")
    if doctrine.get("outputs") != doctrine_outputs:
        errors.append("doctrine generated_surface_families entry must list the doctrine output family")
    if doctrine.get("validator_command") != "python scripts/memory/validate_memory_surfaces.py":
        errors.append("doctrine generated_surface_families entry must keep validator_command python scripts/memory/validate_memory_surfaces.py")

    memory_objects = families.get("memory_objects", {})
    object_outputs = [
        "generated/memory-objects/memory_object_catalog.json",
        "generated/memory-objects/memory_object_catalog.min.json",
        "generated/memory-objects/memory_object_capsules.json",
        "generated/memory-objects/memory_object_sections.full.json",
    ]
    if memory_objects.get("source_of_truth") != "aoa-memo-object-example-surfaces-v1":
        errors.append("memory_objects generated_surface_families entry must keep source_of_truth aoa-memo-object-example-surfaces-v1")
    if memory_objects.get("manifest") != "examples/generated-surfaces/memory_object_surface_manifest.json":
        errors.append("memory_objects generated_surface_families entry must list examples/generated-surfaces/memory_object_surface_manifest.json as the manifest")
    if memory_objects.get("outputs") != object_outputs:
        errors.append("memory_objects generated_surface_families entry must list the object output family")
    if memory_objects.get("generator_command") != "python scripts/memory/generate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep generator_command python scripts/memory/generate_memory_object_surfaces.py")
    if memory_objects.get("validator_command") != "python scripts/memory/validate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep validator_command python scripts/memory/validate_memory_object_surfaces.py")

    kag_export = families.get("kag_export", {})
    if kag_export.get("source_of_truth") != "aoa-memo-kag-source-export-v1":
        errors.append("kag_export generated_surface_families entry must keep source_of_truth aoa-memo-kag-source-export-v1")
    if kag_export.get("outputs") != ["mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json"]:
        errors.append("kag_export generated_surface_families entry must list mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
    if kag_export.get("generator_command") != "python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py":
        errors.append("kag_export generated_surface_families entry must keep generator_command python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py")
    if kag_export.get("validator_command") != "python scripts/memory/validate_memo.py --profile handoff-boundary":
        errors.append(
            "kag_export generated_surface_families entry must keep validator_command "
            "python scripts/memory/validate_memo.py --profile handoff-boundary"
        )

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
        "python scripts/memory/validate_memo.py --profile schema",
        "python scripts/memory/validate_memo.py --profile memory-context",
        "python scripts/memory/validate_memo.py --profile runtime-boundary",
        "python scripts/memory/validate_memo.py --profile handoff-boundary",
        "python scripts/memory/validate_memo.py --profile eval-boundary",
        "python scripts/memory/validate_memory_surfaces.py",
        "python scripts/memory/validate_memory_object_surfaces.py",
        "python scripts/memory/validate_lifecycle_audit_examples.py",
    }
    missing_commands = sorted(required_validation_commands - set(data.get("validation_commands", [])))
    if missing_commands:
        errors.append("generated/memory/memo_registry.min.json missing validation commands: " + ", ".join(missing_commands))

    if errors:
        print("[FAIL] generated/memory/memo_registry.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   generated/memory/memo_registry.min.json")
