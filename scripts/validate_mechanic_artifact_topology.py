#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_DISTRICTS_CONFIG = REPO_ROOT / "config" / "root_technical_districts.json"
ROOT_DISTRICTS_SCHEMA_VERSION = "aoa_memo_root_technical_districts_v8"
ROOT_TECHNICAL_DISTRICTS = (
    "config",
    "examples",
    "generated",
    "manifests",
    "schemas",
    "scripts",
    "tests",
)
GENERATED_SOURCE_KINDS = {
    "source-authored",
    "checked-in-derived",
    "generator-backed",
    "projection",
}
BUILDER_REQUIRED_GENERATED_SOURCE_KINDS = {"generator-backed", "projection"}
SCRIPT_FAMILY_ROLES = {
    "docs-and-agent-validator",
    "mechanic-artifact-validator",
    "mechanic-validator",
    "orchestrator",
    "route-card-validator",
    "validator-and-generator",
}
TEST_FAMILY_ROLES = {
    "agent-companion-regression",
    "downstream-contract-regression",
    "mechanic-contract-regression",
    "memory-object-regression",
    "route-and-topology-regression",
}
SCHEMA_FAMILY_ROLES = {
    "generated-surface-contract",
    "memory-object-contract",
    "recall-posture-contract",
    "support-object-contract",
}
EXAMPLE_FAMILY_ROLES = {
    "base-memory-object-example",
    "continuity-relay-example",
    "lifecycle-audit-example",
    "phase-alpha-thread-example",
    "recall-contract-example",
    "support-contract-example",
    "surface-manifest-example",
}
CONFIG_FAMILY_ROLES = {
    "mechanic-index-source-map",
    "route-card-source-map",
    "technical-district-source-map",
}
MANIFEST_POLICY_ROLE = "reserved-shared-recurrence-manifest-home"

FORBIDDEN_ROOT_PREFIXES = {
    "config": ("agon_",),
    "examples": (
        "adoption_",
        "agon_",
        "assistant_revision_",
        "bridge.kag-lift",
        "certification_",
        "checkpoint_",
        "checkpoint_to_memory_contract",
        "claim.tos-bridge-ready",
        "cross_repo_retention_",
        "deployment_",
        "decision.phase-alpha-self-agent-checkpoint",
        "episode.tos-interpretation",
        "failure_lesson_",
        "audit_event.phase-alpha-self-agent-checkpoint",
        "federation_",
        "first_office_",
        "governance_",
        "inquiry_checkpoint",
        "memo_to_kag_",
        "memory_readiness_boundary_contract",
        "memory_chunk_face",
        "memory_eval_guardrail",
        "memory_graph_face",
        "office_retention_",
        "pattern.antifragility",
        "pattern_lineage_",
        "phase_alpha_writeback_",
        "policy_precedent_",
        "post_release_",
        "provenance_thread.a2a",
        "provenance_thread.kag",
        "provenance_thread.self-agency",
        "quest_chronicle",
        "recovery_pattern_",
        "release_revision_",
        "revocation_",
        "rollback_",
        "service_",
        "shared_lesson_",
        "titan_",
        "train_release_",
        "witness_trace",
    ),
    "generated": (
        "agon_",
        "growth_refinery_",
        "kag_export",
        "phase_alpha_writeback_",
        "runtime_writeback_",
    ),
    "schemas": (
        "adoption_",
        "agon",
        "assistant_revision_",
        "certification_",
        "checkpoint-to-memory",
        "cross_repo_retention_",
        "deployment_",
        "failure_lesson_",
        "federation_",
        "first_office_",
        "governance_",
        "inquiry_checkpoint",
        "memo_to_kag_",
        "memory_readiness_boundary_contract",
        "memory_chunk_face",
        "memory_eval_guardrail",
        "memory_graph_face",
        "office_retention_",
        "pattern_lineage_",
        "policy_precedent_",
        "post_release_",
        "quest_chronicle",
        "recovery_pattern_",
        "release_revision_",
        "revocation_",
        "rollback_",
        "runtime-writeback",
        "service_",
        "shared_lesson_",
        "titan_",
        "train_release_",
        "witness-trace",
    ),
    "scripts": (
        "build_agon_",
        "generate_growth_refinery_",
        "generate_kag_export",
        "generate_phase_alpha_",
        "generate_runtime_writeback_",
        "publish_live_receipts",
        "validate_agon_",
    ),
    "tests": (
        "test_adoption_",
        "test_agon_",
        "test_antifragility_",
        "test_consumer_handoff_",
        "test_checkpoint_",
        "test_wave1_boundary_contract",
        "test_governance_mechanic",
        "test_growth_refinery_",
        "test_lineage_harvest_",
        "test_operational_gate_",
        "test_playbook_memory_scopes",
        "test_publish_live_receipts",
        "test_quest_chronicle_",
        "test_recurrence_support_",
        "test_shape_guard_",
        "test_titan_",
    ),
}


def root_files(directory: str) -> list[Path]:
    root = REPO_ROOT / directory
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name != "AGENTS.md"
        and "__pycache__" not in path.relative_to(REPO_ROOT).parts
    )


def load_root_districts_config() -> tuple[dict[str, object] | None, list[str]]:
    if not ROOT_DISTRICTS_CONFIG.exists():
        return None, ["config/root_technical_districts.json is missing"]
    try:
        payload = json.loads(ROOT_DISTRICTS_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"config/root_technical_districts.json is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, ["config/root_technical_districts.json must be a JSON object"]
    return payload, []


def as_string_list(value: object, label: str, issues: list[str]) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        issues.append(f"config/root_technical_districts.json: {label} must be a string array")
        return None
    return value


def validate_local_ref(path_text: object, label: str) -> list[str]:
    if not isinstance(path_text, str) or not path_text:
        return [f"config/root_technical_districts.json: {label} must be a local path"]
    path_without_anchor = path_text.split("#", 1)[0]
    path = Path(path_without_anchor)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        return [f"config/root_technical_districts.json: {label} must stay inside the repo: {path_text}"]
    target = (REPO_ROOT / path).resolve()
    try:
        target.relative_to(REPO_ROOT)
    except ValueError:
        return [f"config/root_technical_districts.json: {label} resolves outside repo: {path_text}"]
    if not target.exists():
        return [f"config/root_technical_districts.json: {label} points to missing path {path_text}"]
    return []


def validate_generated_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    generated_config = districts.get("generated")
    allowed_generated_files: set[str] = set()
    if isinstance(generated_config, dict):
        allowed_files = generated_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_generated_files = set(allowed_files)

    families = payload.get("generated_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: generated_families must be a list"]

    seen_family_ids: set[str] = set()
    output_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"generated_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate generated family id {family_id}")
        seen_family_ids.add(family_id)

        source_kind = family.get("source_kind")
        if source_kind not in GENERATED_SOURCE_KINDS:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.source_kind must be one of "
                f"{', '.join(sorted(GENERATED_SOURCE_KINDS))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        source_refs = as_string_list(family.get("source_refs"), f"{family_id}.source_refs", issues)
        outputs = as_string_list(family.get("outputs"), f"{family_id}.outputs", issues)
        validators = as_string_list(family.get("validators"), f"{family_id}.validators", issues)

        builders_value = family.get("builders", [])
        builders = as_string_list(builders_value, f"{family_id}.builders", issues)

        for field, refs in (
            ("source_refs", source_refs),
            ("builders", builders),
            ("validators", validators),
        ):
            if refs is None:
                continue
            for ref in refs:
                issues.extend(validate_local_ref(ref, f"{family_id}.{field}"))

        if source_refs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.source_refs must not be empty")
        if validators == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.validators must not be empty")
        if source_kind in BUILDER_REQUIRED_GENERATED_SOURCE_KINDS and builders == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.builders must not be empty")

        if outputs is None:
            continue
        if outputs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.outputs must not be empty")
        for output in outputs:
            output_path = Path(output)
            if output_path.parts[:1] != ("generated",):
                issues.append(f"config/root_technical_districts.json: {family_id}.outputs contains non-root generated path {output}")
            if output_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.outputs must not list route cards")
            if output in output_to_family:
                issues.append(
                    f"config/root_technical_districts.json: generated output {output} appears in both "
                    f"{output_to_family[output]} and {family_id}"
                )
            output_to_family[output] = family_id

    covered_outputs = set(output_to_family)
    for missing in sorted(allowed_generated_files - covered_outputs):
        issues.append(f"config/root_technical_districts.json: generated output {missing} lacks a generated_families contract")
    for extra in sorted(covered_outputs - allowed_generated_files):
        issues.append(f"config/root_technical_districts.json: generated_families covers non-allowed generated output {extra}")

    return issues


def validate_script_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    scripts_config = districts.get("scripts")
    allowed_script_files: set[str] = set()
    if isinstance(scripts_config, dict):
        allowed_files = scripts_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_script_files = set(allowed_files)

    families = payload.get("script_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: script_families must be a list"]

    seen_family_ids: set[str] = set()
    script_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"script_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-script-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate script family id {family_id}")
        seen_family_ids.add(family_id)

        role = family.get("role")
        if role not in SCRIPT_FAMILY_ROLES:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.role must be one of "
                f"{', '.join(sorted(SCRIPT_FAMILY_ROLES))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        scripts = as_string_list(family.get("scripts"), f"{family_id}.scripts", issues)
        covered_by = as_string_list(family.get("covered_by"), f"{family_id}.covered_by", issues)

        if scripts == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.scripts must not be empty")
        if covered_by == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.covered_by must not be empty")

        for ref in covered_by or []:
            issues.extend(validate_local_ref(ref, f"{family_id}.covered_by"))

        if scripts is None:
            continue
        for script in scripts:
            script_path = Path(script)
            if script_path.parts[:1] != ("scripts",):
                issues.append(f"config/root_technical_districts.json: {family_id}.scripts contains non-root script path {script}")
            if script_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.scripts must not list route cards")
            issues.extend(validate_local_ref(script, f"{family_id}.scripts"))
            if script in script_to_family:
                issues.append(
                    f"config/root_technical_districts.json: root script {script} appears in both "
                    f"{script_to_family[script]} and {family_id}"
                )
            script_to_family[script] = family_id

    covered_scripts = set(script_to_family)
    for missing in sorted(allowed_script_files - covered_scripts):
        issues.append(f"config/root_technical_districts.json: root script {missing} lacks a script_families contract")
    for extra in sorted(covered_scripts - allowed_script_files):
        issues.append(f"config/root_technical_districts.json: script_families covers non-allowed root script {extra}")

    return issues


def validate_test_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    tests_config = districts.get("tests")
    allowed_test_files: set[str] = set()
    if isinstance(tests_config, dict):
        allowed_files = tests_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_test_files = set(allowed_files)

    families = payload.get("test_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: test_families must be a list"]

    seen_family_ids: set[str] = set()
    test_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"test_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-test-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate test family id {family_id}")
        seen_family_ids.add(family_id)

        role = family.get("role")
        if role not in TEST_FAMILY_ROLES:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.role must be one of "
                f"{', '.join(sorted(TEST_FAMILY_ROLES))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        tests = as_string_list(family.get("tests"), f"{family_id}.tests", issues)
        protects = as_string_list(family.get("protects"), f"{family_id}.protects", issues)

        if tests == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.tests must not be empty")
        if protects == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.protects must not be empty")

        for ref in protects or []:
            issues.extend(validate_local_ref(ref, f"{family_id}.protects"))

        if tests is None:
            continue
        for test in tests:
            test_path = Path(test)
            if test_path.parts[:1] != ("tests",):
                issues.append(f"config/root_technical_districts.json: {family_id}.tests contains non-root tests path {test}")
            if test_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.tests must not list route cards")
            issues.extend(validate_local_ref(test, f"{family_id}.tests"))
            if test in test_to_family:
                issues.append(
                    f"config/root_technical_districts.json: root test {test} appears in both "
                    f"{test_to_family[test]} and {family_id}"
                )
            test_to_family[test] = family_id

    covered_tests = set(test_to_family)
    for missing in sorted(allowed_test_files - covered_tests):
        issues.append(f"config/root_technical_districts.json: root test {missing} lacks a test_families contract")
    for extra in sorted(covered_tests - allowed_test_files):
        issues.append(f"config/root_technical_districts.json: test_families covers non-allowed root test {extra}")

    return issues


def validate_schema_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    schemas_config = districts.get("schemas")
    allowed_schema_files: set[str] = set()
    if isinstance(schemas_config, dict):
        allowed_files = schemas_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_schema_files = set(allowed_files)

    families = payload.get("schema_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: schema_families must be a list"]

    seen_family_ids: set[str] = set()
    schema_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"schema_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-schema-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate schema family id {family_id}")
        seen_family_ids.add(family_id)

        role = family.get("role")
        if role not in SCHEMA_FAMILY_ROLES:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.role must be one of "
                f"{', '.join(sorted(SCHEMA_FAMILY_ROLES))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        schemas = as_string_list(family.get("schemas"), f"{family_id}.schemas", issues)
        source_refs = as_string_list(family.get("source_refs"), f"{family_id}.source_refs", issues)
        validators = as_string_list(family.get("validators"), f"{family_id}.validators", issues)

        if schemas == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.schemas must not be empty")
        if source_refs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.source_refs must not be empty")
        if validators == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.validators must not be empty")

        for field, refs in (("source_refs", source_refs), ("validators", validators)):
            if refs is None:
                continue
            for ref in refs:
                issues.extend(validate_local_ref(ref, f"{family_id}.{field}"))

        if schemas is None:
            continue
        for schema in schemas:
            schema_path = Path(schema)
            if schema_path.parts[:1] != ("schemas",):
                issues.append(f"config/root_technical_districts.json: {family_id}.schemas contains non-root schema path {schema}")
            if schema_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.schemas must not list route cards")
            issues.extend(validate_local_ref(schema, f"{family_id}.schemas"))
            if schema in schema_to_family:
                issues.append(
                    f"config/root_technical_districts.json: root schema {schema} appears in both "
                    f"{schema_to_family[schema]} and {family_id}"
                )
            schema_to_family[schema] = family_id

    covered_schemas = set(schema_to_family)
    for missing in sorted(allowed_schema_files - covered_schemas):
        issues.append(f"config/root_technical_districts.json: root schema {missing} lacks a schema_families contract")
    for extra in sorted(covered_schemas - allowed_schema_files):
        issues.append(f"config/root_technical_districts.json: schema_families covers non-allowed root schema {extra}")

    return issues


def validate_example_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    examples_config = districts.get("examples")
    allowed_example_files: set[str] = set()
    if isinstance(examples_config, dict):
        allowed_files = examples_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_example_files = set(allowed_files)

    families = payload.get("example_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: example_families must be a list"]

    seen_family_ids: set[str] = set()
    example_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"example_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-example-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate example family id {family_id}")
        seen_family_ids.add(family_id)

        role = family.get("role")
        if role not in EXAMPLE_FAMILY_ROLES:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.role must be one of "
                f"{', '.join(sorted(EXAMPLE_FAMILY_ROLES))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        examples = as_string_list(family.get("examples"), f"{family_id}.examples", issues)
        source_refs = as_string_list(family.get("source_refs"), f"{family_id}.source_refs", issues)
        validators = as_string_list(family.get("validators"), f"{family_id}.validators", issues)

        if examples == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.examples must not be empty")
        if source_refs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.source_refs must not be empty")
        if validators == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.validators must not be empty")

        for field, refs in (("source_refs", source_refs), ("validators", validators)):
            if refs is None:
                continue
            for ref in refs:
                issues.extend(validate_local_ref(ref, f"{family_id}.{field}"))

        if examples is None:
            continue
        for example in examples:
            example_path = Path(example)
            if example_path.parts[:1] != ("examples",):
                issues.append(f"config/root_technical_districts.json: {family_id}.examples contains non-root example path {example}")
            if example_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.examples must not list route cards")
            issues.extend(validate_local_ref(example, f"{family_id}.examples"))
            if example in example_to_family:
                issues.append(
                    f"config/root_technical_districts.json: root example {example} appears in both "
                    f"{example_to_family[example]} and {family_id}"
                )
            example_to_family[example] = family_id

    covered_examples = set(example_to_family)
    for missing in sorted(allowed_example_files - covered_examples):
        issues.append(f"config/root_technical_districts.json: root example {missing} lacks an example_families contract")
    for extra in sorted(covered_examples - allowed_example_files):
        issues.append(f"config/root_technical_districts.json: example_families covers non-allowed root example {extra}")

    return issues


def validate_config_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    config_config = districts.get("config")
    allowed_config_files: set[str] = set()
    if isinstance(config_config, dict):
        allowed_files = config_config.get("allowed_files")
        if isinstance(allowed_files, list) and all(isinstance(item, str) for item in allowed_files):
            allowed_config_files = set(allowed_files)

    families = payload.get("config_families")
    if not isinstance(families, list):
        return ["config/root_technical_districts.json: config_families must be a list"]

    seen_family_ids: set[str] = set()
    config_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"config_families[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-config-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root_technical_districts.json: duplicate config family id {family_id}")
        seen_family_ids.add(family_id)

        role = family.get("role")
        if role not in CONFIG_FAMILY_ROLES:
            issues.append(
                f"config/root_technical_districts.json: {family_id}.role must be one of "
                f"{', '.join(sorted(CONFIG_FAMILY_ROLES))}"
            )

        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        configs = as_string_list(family.get("configs"), f"{family_id}.configs", issues)
        source_refs = as_string_list(family.get("source_refs"), f"{family_id}.source_refs", issues)
        validators = as_string_list(family.get("validators"), f"{family_id}.validators", issues)

        if configs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.configs must not be empty")
        if source_refs == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.source_refs must not be empty")
        if validators == []:
            issues.append(f"config/root_technical_districts.json: {family_id}.validators must not be empty")

        for field, refs in (("source_refs", source_refs), ("validators", validators)):
            if refs is None:
                continue
            for ref in refs:
                issues.extend(validate_local_ref(ref, f"{family_id}.{field}"))

        if configs is None:
            continue
        for config_path_text in configs:
            config_path = Path(config_path_text)
            if config_path.parts[:1] != ("config",):
                issues.append(
                    f"config/root_technical_districts.json: {family_id}.configs contains non-root config path {config_path_text}"
                )
            if config_path.name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {family_id}.configs must not list route cards")
            issues.extend(validate_local_ref(config_path_text, f"{family_id}.configs"))
            if config_path_text in config_to_family:
                issues.append(
                    f"config/root_technical_districts.json: root config {config_path_text} appears in both "
                    f"{config_to_family[config_path_text]} and {family_id}"
                )
            config_to_family[config_path_text] = family_id

    covered_configs = set(config_to_family)
    for missing in sorted(allowed_config_files - covered_configs):
        issues.append(f"config/root_technical_districts.json: root config {missing} lacks a config_families contract")
    for extra in sorted(covered_configs - allowed_config_files):
        issues.append(f"config/root_technical_districts.json: config_families covers non-allowed root config {extra}")

    return issues


def validate_manifest_policy_contract(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    issues: list[str] = []
    manifest_policy = payload.get("manifest_policy")
    if not isinstance(manifest_policy, dict):
        return ["config/root_technical_districts.json: manifest_policy must be an object"]

    if manifest_policy.get("id") != "root_manifests_reserved":
        issues.append("config/root_technical_districts.json: manifest_policy.id must be root_manifests_reserved")
    if manifest_policy.get("role") != MANIFEST_POLICY_ROLE:
        issues.append(
            f"config/root_technical_districts.json: manifest_policy.role must be {MANIFEST_POLICY_ROLE}"
        )

    issues.extend(validate_local_ref(manifest_policy.get("owner_surface"), "manifest_policy.owner_surface"))
    source_refs = as_string_list(manifest_policy.get("source_refs"), "manifest_policy.source_refs", issues)
    validators = as_string_list(manifest_policy.get("validators"), "manifest_policy.validators", issues)
    allowed_files = as_string_list(manifest_policy.get("allowed_files"), "manifest_policy.allowed_files", issues)

    if source_refs == []:
        issues.append("config/root_technical_districts.json: manifest_policy.source_refs must not be empty")
    if validators == []:
        issues.append("config/root_technical_districts.json: manifest_policy.validators must not be empty")

    for field, refs in (("source_refs", source_refs), ("validators", validators)):
        if refs is None:
            continue
        for ref in refs:
            issues.extend(validate_local_ref(ref, f"manifest_policy.{field}"))

    manifests_config = districts.get("manifests")
    district_allowed_files: list[str] | None = None
    if isinstance(manifests_config, dict):
        value = manifests_config.get("allowed_files")
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            district_allowed_files = value
    if allowed_files is not None and district_allowed_files is not None and allowed_files != district_allowed_files:
        issues.append("config/root_technical_districts.json: manifest_policy.allowed_files must match manifests.allowed_files")

    for manifest_path_text in allowed_files or []:
        manifest_path = Path(manifest_path_text)
        if manifest_path.parts[:1] != ("manifests",):
            issues.append(
                f"config/root_technical_districts.json: manifest_policy.allowed_files contains non-root manifest path {manifest_path_text}"
            )
        if manifest_path.name == "AGENTS.md":
            issues.append("config/root_technical_districts.json: manifest_policy.allowed_files must not list route cards")
        issues.extend(validate_local_ref(manifest_path_text, "manifest_policy.allowed_files"))

    return issues


def validate_root_district_allowlist() -> list[str]:
    issues: list[str] = []
    payload, config_errors = load_root_districts_config()
    issues.extend(config_errors)
    if payload is None:
        return issues

    if payload.get("schema_version") != ROOT_DISTRICTS_SCHEMA_VERSION:
        issues.append(f"config/root_technical_districts.json must keep schema_version {ROOT_DISTRICTS_SCHEMA_VERSION}")
    if payload.get("source_of_truth") != "mechanics/ARTIFACT_TOPOLOGY.md":
        issues.append("config/root_technical_districts.json must route source_of_truth to mechanics/ARTIFACT_TOPOLOGY.md")

    districts = payload.get("districts")
    if not isinstance(districts, dict):
        issues.append("config/root_technical_districts.json: districts must be an object")
        return issues

    missing_districts = sorted(set(ROOT_TECHNICAL_DISTRICTS) - set(districts))
    extra_districts = sorted(set(districts) - set(ROOT_TECHNICAL_DISTRICTS))
    for district in missing_districts:
        issues.append(f"config/root_technical_districts.json: missing district {district}")
    for district in extra_districts:
        issues.append(f"config/root_technical_districts.json: unsupported district {district}")

    for district in ROOT_TECHNICAL_DISTRICTS:
        config = districts.get(district)
        if not isinstance(config, dict):
            if district in districts:
                issues.append(f"config/root_technical_districts.json: {district} must be an object")
            continue
        if not isinstance(config.get("root_role"), str) or not config.get("root_role"):
            issues.append(f"config/root_technical_districts.json: {district} must name root_role")
        allowed_files = config.get("allowed_files")
        if not isinstance(allowed_files, list) or not all(isinstance(item, str) for item in allowed_files):
            issues.append(f"config/root_technical_districts.json: {district}.allowed_files must be a string array")
            continue

        duplicate_paths = sorted({item for item in allowed_files if allowed_files.count(item) > 1})
        for duplicate_path in duplicate_paths:
            issues.append(f"config/root_technical_districts.json: duplicate allowed path {duplicate_path}")

        allowed = set(allowed_files)
        for allowed_path in allowed:
            parts = Path(allowed_path).parts
            if not parts or parts[0] != district:
                issues.append(f"config/root_technical_districts.json: {allowed_path} is outside district {district}")
            if Path(allowed_path).name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {allowed_path} should rely on the route-card exception, not allowed_files")

        actual = {path.relative_to(REPO_ROOT).as_posix() for path in root_files(district)}
        for missing in sorted(allowed - actual):
            issues.append(f"{missing}: allowed root technical artifact is missing")
        for unexpected in sorted(actual - allowed):
            issues.append(
                f"{unexpected}: root technical artifact must be listed in config/root_technical_districts.json or moved under mechanics/<slug>/"
            )

    issues.extend(validate_generated_family_contracts(payload, districts))
    issues.extend(validate_script_family_contracts(payload, districts))
    issues.extend(validate_test_family_contracts(payload, districts))
    issues.extend(validate_schema_family_contracts(payload, districts))
    issues.extend(validate_example_family_contracts(payload, districts))
    issues.extend(validate_config_family_contracts(payload, districts))
    issues.extend(validate_manifest_policy_contract(payload, districts))

    return issues


def validate() -> list[str]:
    issues: list[str] = []
    issues.extend(validate_root_district_allowlist())

    for directory, prefixes in FORBIDDEN_ROOT_PREFIXES.items():
        for path in root_files(directory):
            if path.name.startswith(prefixes):
                relative = path.relative_to(REPO_ROOT).as_posix()
                issues.append(
                    f"{relative}: single-mechanic artifact must live under mechanics/<slug>/"
                )

    for path in root_files("manifests"):
        relative = path.relative_to(REPO_ROOT).as_posix()
        issues.append(f"{relative}: root manifests are reserved for shared manifests only")

    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Mechanic artifact topology validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] mechanic artifact topology is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
