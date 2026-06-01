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

def validate_memory_readiness_boundary_materialization() -> None:
    boundary_doc = MEMORY_READINESS_BOUNDARY_DOC_PATH.read_text(encoding="utf-8")
    checkpoint = load_json(example_path_for("inquiry_checkpoint.return.example.json"))
    contradiction = load_json(example_path_for("claim.phase-alpha-runtime-history-later-infra-track.example.json"))
    bridge = load_json(example_path_for("bridge.kag-lift.example.json"))
    retention = load_json(example_path_for("audit_event.memory-retention-check.example.json"))
    service = load_json(example_path_for("audit_event.service-governed-fallback.example.json"))
    catalog = load_json(GENERATED / "memory-objects" / "memory_object_catalog.min.json")
    errors: list[str] = []

    for phrase in (
        "memory delta",
        "canon delta reference",
        "retention check",
        "unresolved contradiction",
        "survivor or bridge candidate",
        "civil/service assistant trace",
    ):
        if phrase not in boundary_doc:
            errors.append(f"{MEMORY_READINESS_BOUNDARY_DOC_REF} must keep pressure row {phrase!r}")

    memory_delta_refs = checkpoint.get("memory_delta_refs")
    canon_delta_refs = checkpoint.get("canon_delta_refs")
    if not isinstance(memory_delta_refs, list) or not memory_delta_refs:
        errors.append("inquiry_checkpoint.return.example.json must keep non-empty memory_delta_refs")
    if not isinstance(canon_delta_refs, list) or not canon_delta_refs:
        errors.append("inquiry_checkpoint.return.example.json must keep non-empty canon_delta_refs")
    if isinstance(memory_delta_refs, list) and isinstance(canon_delta_refs, list):
        overlap = sorted(set(memory_delta_refs) & set(canon_delta_refs))
        if overlap:
            errors.append(
                "inquiry_checkpoint.return.example.json must keep memory_delta_refs distinct from canon_delta_refs "
                f"(overlap={overlap})"
            )

    contradiction_refs = contradiction.get("lifecycle", {}).get("current_recall", {}).get("contradiction_refs")
    if not isinstance(contradiction_refs, list) or not contradiction_refs:
        errors.append(
            "claim.phase-alpha-runtime-history-later-infra-track.example.json must keep explicit contradiction_refs"
        )

    bridge_lifecycle = bridge.get("lifecycle", {})
    if bridge_lifecycle.get("review_state") != "proposed":
        errors.append("bridge.kag-lift.example.json must keep lifecycle.review_state == 'proposed'")
    if bridge_lifecycle.get("retention_class") != "bridge-candidate":
        errors.append("bridge.kag-lift.example.json must keep lifecycle.retention_class == 'bridge-candidate'")

    retention_sources = retention.get("provenance", {}).get("source_refs")
    if retention.get("kind") != "audit_event":
        errors.append("audit_event.memory-retention-check.example.json must stay an audit_event")
    if retention.get("lifecycle", {}).get("retention_class") != "audit-trace":
        errors.append("audit_event.memory-retention-check.example.json must keep lifecycle.retention_class == 'audit-trace'")
    if not isinstance(retention_sources, list) or (
        MEMORY_READINESS_BOUNDARY_PRESSURE_REF not in retention_sources
    ):
        errors.append(
            f"audit_event.memory-retention-check.example.json must cite {MEMORY_READINESS_BOUNDARY_PRESSURE_REF}"
        )

    service_sources = service.get("provenance", {}).get("source_refs")
    if service.get("kind") != "audit_event":
        errors.append("audit_event.service-governed-fallback.example.json must stay an audit_event")
    if service.get("lifecycle", {}).get("retention_class") != "audit-trace":
        errors.append(
            "audit_event.service-governed-fallback.example.json must keep lifecycle.retention_class == 'audit-trace'"
        )
    if not isinstance(service_sources, list) or not any(
        "service_degradation_receipt" in ref for ref in service_sources
    ):
        errors.append(
            "audit_event.service-governed-fallback.example.json must preserve a source receipt ref"
        )
    if not isinstance(service_sources, list) or "repo:aoa-agents/docs/AGENT_RUNTIME_SEAM.md" not in service_sources:
        errors.append(
            "audit_event.service-governed-fallback.example.json must preserve the aoa-agents owner boundary ref"
        )

    catalog_objects = catalog.get("memory_objects")
    catalog_ids: set[str] = set()
    if isinstance(catalog_objects, list):
        catalog_ids = {
            item.get("id")
            for item in catalog_objects
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    for object_id in (
        "memo.audit.2026-04-13.memo-entrypoint-retention-check",
        "memo.audit.2026-04-07.hybrid-query-service-fallback",
    ):
        if object_id not in catalog_ids:
            errors.append(
                "generated/memory-objects/memory_object_catalog.min.json must surface memory readiness example "
                f"{object_id}"
            )

    if errors:
        print("[FAIL] memory readiness boundary materialization")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory readiness boundary materialization")

def validate_memory_readiness_boundary_contract() -> None:
    doc = MEMORY_READINESS_BOUNDARY_DOC_PATH.read_text(encoding="utf-8")
    schema = validator_for(MEMORY_READINESS_BOUNDARY_CONTRACT_SCHEMA)
    payload = load_json(MEMORY_READINESS_BOUNDARY_CONTRACT_PATH)
    errors: list[str] = []

    for token in (
        "mechanics/readiness-boundary/parts/memory-readiness-boundary/schemas/memory_readiness_boundary_contract.schema.json",
        "mechanics/readiness-boundary/parts/memory-readiness-boundary/examples/memory_readiness_boundary_contract.example.json",
        "memory_gate",
        "retention_boundary",
        "writeback_boundary",
    ):
        if token not in doc:
            errors.append(f"{MEMORY_READINESS_BOUNDARY_DOC_REF} must mention {token}")

    if payload.get("contract_id") != "aoa-memo.memory-readiness-boundary.v1":
        errors.append(
            "memory_readiness_boundary_contract.example.json must keep contract_id aoa-memo.memory-readiness-boundary.v1"
        )
    if payload.get("owner_repo") != "aoa-memo":
        errors.append("memory_readiness_boundary_contract.example.json must keep owner_repo aoa-memo")

    errors.extend(
        f"memory_readiness_boundary_contract.example.json schema violation: {error.message}"
        for error in schema.iter_errors(payload)
    )

    gate = payload.get("memory_gate", {})
    retention = payload.get("retention_boundary", {})
    writeback = payload.get("writeback_boundary", {})
    if not isinstance(gate, dict) or "live scratchpad residue" not in gate.get("rejected_inputs", []):
        errors.append("memory_readiness_boundary_contract.example.json must reject live scratchpad residue")
    if not isinstance(retention, dict) or retention.get("owned_by") != "abyss-stack":
        errors.append("memory_readiness_boundary_contract.example.json must keep retention owned by abyss-stack")
    if not isinstance(writeback, dict) or "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" not in writeback.get("export_surfaces", []):
        errors.append(
            "memory_readiness_boundary_contract.example.json must point writeback at mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md"
        )

    if errors:
        print("[FAIL] memory readiness boundary contract")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory readiness boundary contract")

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

def validate_core_memory_contract() -> None:
    validator = validator_for("core-memory-contract.schema.json")
    data = load_json(example_path_for("core_memory_contract.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    expected_core = registry.get("memory_object_kinds", [])
    expected_supporting = registry.get("supporting_objects", [])
    expected_profile_schema = "schemas/memory-objects/memory_object_profile.schema.json"
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
        errors.append("core_memory_surfaces does not match generated/memory/memo_registry.min.json memory_object_kinds")
    if sorted(data.get("supporting_objects", [])) != sorted(expected_supporting):
        errors.append("supporting_objects does not match generated/memory/memo_registry.min.json supporting_objects")
    if data.get("profile_schema") != expected_profile_schema:
        errors.append("profile_schema must stay schemas/memory-objects/memory_object_profile.schema.json")
    if data.get("kind_profile_schemas") != expected_kind_schemas:
        errors.append("kind_profile_schemas does not match the shipped per-kind profile schema map")

    for ref in [expected_profile_schema, *expected_kind_schemas.values()]:
        if ref not in registry.get("schemas", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {ref}")
    if "docs/memory/MEMORY_OBJECT_PROFILES.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list docs/memory/MEMORY_OBJECT_PROFILES.md")

    if errors:
        print("[FAIL] core_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   core_memory_contract.example.json")

def validate_witness_trace_contract() -> None:
    validator = validator_for("witness-trace.schema.json")
    data = load_json(example_path_for("witness_trace.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "witness_trace" in registry.get("memory_object_kinds", []):
        errors.append("witness_trace must not appear in generated/memory/memo_registry.min.json memory_object_kinds")
    if "witness_trace" in registry.get("supporting_objects", []):
        errors.append("witness_trace must not appear in generated/memory/memo_registry.min.json supporting_objects")
    if "mechanics/recurrence-support/parts/witness-trace-contract/schemas/witness-trace.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/recurrence-support/parts/witness-trace-contract/schemas/witness-trace.schema.json")
    if "mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md")

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

def validate_quest_chronicle_surface() -> None:
    validator = validator_for("quest_chronicle.schema.json")
    data = load_json(example_path_for("quest_chronicle.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "quest_chronicle" in registry.get("memory_object_kinds", []):
        errors.append("quest_chronicle must not appear in generated/memory/memo_registry.min.json memory_object_kinds")
    if "quest_chronicle" in registry.get("supporting_objects", []):
        errors.append("quest_chronicle must not appear in generated/memory/memo_registry.min.json supporting_objects")
    if "mechanics/writeback/parts/quest-and-chronicle/schemas/quest_chronicle.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/parts/quest-and-chronicle/schemas/quest_chronicle.schema.json")
    if "mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md")

    if data.get("public_safe") is not True:
        errors.append("quest_chronicle.example.json must stay public_safe")
    if data.get("temperature") == "hot":
        errors.append("quest_chronicle.example.json must not default to hot temperature")

    allowed_anchor_refs: set[str] = set()
    for field_name in ("campaign_ref", "recall_anchor_ref"):
        value = data.get(field_name)
        if isinstance(value, str) and value:
            allowed_anchor_refs.add(value)
    for field_name in ("quest_refs", "evidence_refs"):
        values = data.get(field_name)
        if isinstance(values, list):
            allowed_anchor_refs.update(value for value in values if isinstance(value, str) and value)

    for index, stage in enumerate(data.get("stage_witness", [])):
        if not isinstance(stage, dict):
            continue
        anchor_ref = stage.get("anchor_ref")
        if isinstance(anchor_ref, str) and anchor_ref not in allowed_anchor_refs:
            errors.append(
                f"quest_chronicle.example.json stage_witness[{index}].anchor_ref must resolve through quest_refs, evidence_refs, campaign_ref, or recall_anchor_ref"
            )
        next_recall_cue = stage.get("next_recall_cue")
        if not isinstance(next_recall_cue, str) or not next_recall_cue.strip():
            errors.append(f"quest_chronicle.example.json stage_witness[{index}] must include next_recall_cue")

    notes = data.get("notes")
    if not isinstance(notes, str) or "witness" not in notes.lower() or "not quest authority" not in notes.lower():
        errors.append("quest_chronicle.example.json notes must keep witness-only, non-authority posture explicit")

    if errors:
        print("[FAIL] quest_chronicle.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   quest_chronicle.example.json")

def validate_checkpoint_to_memory_contract() -> None:
    validator = validator_for("checkpoint-to-memory-contract.schema.json")
    data = load_json(example_path_for("checkpoint_to_memory_contract.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks = [("source_event_ref", data.get("source_event_ref"))]
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

    if "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json")
    if "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md")

    if errors:
        print("[FAIL] checkpoint_to_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   checkpoint_to_memory_contract.example.json")

def run() -> None:
    validate_memory_object_profiles()
    validate_trust_lifecycle_contracts()
    validate_memory_readiness_boundary_materialization()
    validate_memory_readiness_boundary_contract()
    validate_registry()
    validate_core_memory_contract()
    validate_checkpoint_to_memory_contract()
    validate_witness_trace_contract()
    validate_quest_chronicle_surface()
    validate_questbook_surface()
