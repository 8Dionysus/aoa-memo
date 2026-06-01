from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from mechanic_artifact_topology_common import (
    BUILDER_REQUIRED_GENERATED_SOURCE_KINDS,
    CONFIG_FAMILY_ROLES,
    EXAMPLE_FAMILY_ROLES,
    GENERATED_SOURCE_KINDS,
    MANIFEST_POLICY_ROLE,
    SCHEMA_FAMILY_ROLES,
    SCRIPT_FAMILY_ROLES,
    TEST_FAMILY_ROLES,
    as_string_list,
    validate_local_ref,
)


@dataclass(frozen=True)
class ReferenceField:
    name: str
    required_non_empty: bool = True
    default: tuple[str, ...] | None = None
    required_when: Callable[[dict[str, object]], bool] | None = None


@dataclass(frozen=True)
class FamilySpec:
    collection: str
    district: str
    item_field: str
    allowed_label: str
    role_field: str | None = None
    allowed_roles: set[str] | None = None
    reference_fields: tuple[ReferenceField, ...] = ()


def _allowed_files(districts: dict[object, object], district: str) -> set[str]:
    district_config = districts.get(district)
    if not isinstance(district_config, dict):
        return set()
    allowed_files = district_config.get("allowed_files")
    if not isinstance(allowed_files, list) or not all(isinstance(item, str) for item in allowed_files):
        return set()
    return set(allowed_files)


def _validate_role(family: dict[str, object], family_id: str, spec: FamilySpec, issues: list[str]) -> None:
    if spec.role_field is None:
        return
    role = family.get(spec.role_field)
    if role not in (spec.allowed_roles or set()):
        issues.append(
            f"config/root-topology/root_technical_districts.json: {family_id}.{spec.role_field} must be one of "
            f"{', '.join(sorted(spec.allowed_roles or set()))}"
        )


def _string_refs(
    family: dict[str, object],
    family_id: str,
    field: ReferenceField,
    issues: list[str],
) -> list[str] | None:
    value = family.get(field.name, list(field.default) if field.default is not None else None)
    refs = as_string_list(value, f"{family_id}.{field.name}", issues)
    if refs == [] and (field.required_non_empty or (field.required_when and field.required_when(family))):
        issues.append(f"config/root-topology/root_technical_districts.json: {family_id}.{field.name} must not be empty")
    for ref in refs or []:
        issues.extend(validate_local_ref(ref, f"{family_id}.{field.name}"))
    return refs


def _validate_family_item(
    family_id: str,
    item: str,
    spec: FamilySpec,
    item_to_family: dict[str, str],
    issues: list[str],
) -> None:
    item_path = Path(item)
    if item_path.parts[:1] != (spec.district,):
        issues.append(
            f"config/root-topology/root_technical_districts.json: {family_id}.{spec.item_field} "
            f"contains non-root {spec.district} path {item}"
        )
    if item_path.name == "AGENTS.md":
        issues.append(
            f"config/root-topology/root_technical_districts.json: {family_id}.{spec.item_field} must not list route cards"
        )
    issues.extend(validate_local_ref(item, f"{family_id}.{spec.item_field}"))
    if item in item_to_family:
        issues.append(
            f"config/root-topology/root_technical_districts.json: root {spec.allowed_label} {item} appears in both "
            f"{item_to_family[item]} and {family_id}"
        )
    item_to_family[item] = family_id


def validate_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
    spec: FamilySpec,
) -> list[str]:
    issues: list[str] = []
    allowed_items = _allowed_files(districts, spec.district)
    families = payload.get(spec.collection)
    if not isinstance(families, list):
        return [f"config/root-topology/root_technical_districts.json: {spec.collection} must be a list"]

    seen_family_ids: set[str] = set()
    item_to_family: dict[str, str] = {}

    for index, family in enumerate(families):
        label = f"{spec.collection}[{index}]"
        if not isinstance(family, dict):
            issues.append(f"config/root-topology/root_technical_districts.json: {label} must be an object")
            continue

        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            issues.append(f"config/root-topology/root_technical_districts.json: {label}.id must be a non-empty string")
            family_id = f"<invalid-{spec.allowed_label}-{index}>"
        elif family_id in seen_family_ids:
            issues.append(f"config/root-topology/root_technical_districts.json: duplicate {spec.allowed_label} family id {family_id}")
        seen_family_ids.add(family_id)

        _validate_role(family, family_id, spec, issues)
        issues.extend(validate_local_ref(family.get("owner_surface"), f"{family_id}.owner_surface"))

        for field in spec.reference_fields:
            _string_refs(family, family_id, field, issues)

        items = as_string_list(family.get(spec.item_field), f"{family_id}.{spec.item_field}", issues)
        if items == []:
            issues.append(f"config/root-topology/root_technical_districts.json: {family_id}.{spec.item_field} must not be empty")
        for item in items or []:
            _validate_family_item(family_id, item, spec, item_to_family, issues)

    covered_items = set(item_to_family)
    for missing in sorted(allowed_items - covered_items):
        issues.append(f"config/root-topology/root_technical_districts.json: root {spec.allowed_label} {missing} lacks a {spec.collection} contract")
    for extra in sorted(covered_items - allowed_items):
        issues.append(f"config/root-topology/root_technical_districts.json: {spec.collection} covers non-allowed root {spec.allowed_label} {extra}")

    return issues


def validate_generated_family_contracts(
    payload: dict[str, object],
    districts: dict[object, object],
) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="generated_families",
            district="generated",
            item_field="outputs",
            allowed_label="generated output",
            role_field="source_kind",
            allowed_roles=GENERATED_SOURCE_KINDS,
            reference_fields=(
                ReferenceField("source_refs"),
                ReferenceField("builders", required_non_empty=False, default=(), required_when=_builder_required),
                ReferenceField("validators"),
            ),
        ),
    )


def _builder_required(family: dict[str, object]) -> bool:
    return family.get("source_kind") in BUILDER_REQUIRED_GENERATED_SOURCE_KINDS


def validate_script_family_contracts(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="script_families",
            district="scripts",
            item_field="scripts",
            allowed_label="script",
            role_field="role",
            allowed_roles=SCRIPT_FAMILY_ROLES,
            reference_fields=(ReferenceField("covered_by"),),
        ),
    )


def validate_test_family_contracts(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="test_families",
            district="tests",
            item_field="tests",
            allowed_label="test",
            role_field="role",
            allowed_roles=TEST_FAMILY_ROLES,
            reference_fields=(ReferenceField("protects"),),
        ),
    )


def validate_schema_family_contracts(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="schema_families",
            district="schemas",
            item_field="schemas",
            allowed_label="schema",
            role_field="role",
            allowed_roles=SCHEMA_FAMILY_ROLES,
            reference_fields=(ReferenceField("source_refs"), ReferenceField("validators")),
        ),
    )


def validate_example_family_contracts(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="example_families",
            district="examples",
            item_field="examples",
            allowed_label="example",
            role_field="role",
            allowed_roles=EXAMPLE_FAMILY_ROLES,
            reference_fields=(ReferenceField("source_refs"), ReferenceField("validators")),
        ),
    )


def validate_config_family_contracts(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    return validate_family_contracts(
        payload,
        districts,
        FamilySpec(
            collection="config_families",
            district="config",
            item_field="configs",
            allowed_label="config",
            role_field="role",
            allowed_roles=CONFIG_FAMILY_ROLES,
            reference_fields=(ReferenceField("source_refs"), ReferenceField("validators")),
        ),
    )


def validate_manifest_policy_contract(payload: dict[str, object], districts: dict[object, object]) -> list[str]:
    issues: list[str] = []
    manifest_policy = payload.get("manifest_policy")
    if not isinstance(manifest_policy, dict):
        return ["config/root-topology/root_technical_districts.json: manifest_policy must be an object"]

    if manifest_policy.get("id") != "root_manifests_reserved":
        issues.append("config/root-topology/root_technical_districts.json: manifest_policy.id must be root_manifests_reserved")
    if manifest_policy.get("role") != MANIFEST_POLICY_ROLE:
        issues.append(
            f"config/root-topology/root_technical_districts.json: manifest_policy.role must be {MANIFEST_POLICY_ROLE}"
        )

    issues.extend(validate_local_ref(manifest_policy.get("owner_surface"), "manifest_policy.owner_surface"))
    source_refs = _string_refs(manifest_policy, "manifest_policy", ReferenceField("source_refs"), issues)
    validators = _string_refs(manifest_policy, "manifest_policy", ReferenceField("validators"), issues)
    allowed_files = as_string_list(manifest_policy.get("allowed_files"), "manifest_policy.allowed_files", issues)

    manifests_config = districts.get("manifests")
    district_allowed_files: list[str] | None = None
    if isinstance(manifests_config, dict):
        value = manifests_config.get("allowed_files")
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            district_allowed_files = value
    if allowed_files is not None and district_allowed_files is not None and allowed_files != district_allowed_files:
        issues.append("config/root-topology/root_technical_districts.json: manifest_policy.allowed_files must match manifests.allowed_files")

    for manifest_path_text in allowed_files or []:
        manifest_path = Path(manifest_path_text)
        if manifest_path.parts[:1] != ("manifests",):
            issues.append(
                f"config/root-topology/root_technical_districts.json: manifest_policy.allowed_files contains non-root manifest path {manifest_path_text}"
            )
        if manifest_path.name == "AGENTS.md":
            issues.append("config/root-topology/root_technical_districts.json: manifest_policy.allowed_files must not list route cards")
        issues.extend(validate_local_ref(manifest_path_text, "manifest_policy.allowed_files"))

    if source_refs is None or validators is None:
        return issues
    return issues
