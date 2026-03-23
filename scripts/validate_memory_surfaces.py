#!/usr/bin/env python3
"""Validate router-facing aoa-memo doctrine surfaces and recall entrypoints."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from validate_memo import local_ref_error, validator_for

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
EXAMPLES = ROOT / "examples"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_exists(path_text: str, label: str) -> None:
    if not isinstance(path_text, str) or not path_text:
        raise SystemExit(f"{label}: invalid path")
    if not (ROOT / path_text).exists():
        raise SystemExit(f"{label}: missing path {path_text}")


def validate_catalog(path: Path, require_relations: bool) -> None:
    data = load_json(path)
    for key in ("catalog_version", "source_of_truth", "memo_surfaces"):
        if key not in data:
            raise SystemExit(f"{path}: missing key {key}")
    if not isinstance(data["memo_surfaces"], list) or not data["memo_surfaces"]:
        raise SystemExit(f"{path}: memo_surfaces must be a non-empty list")
    seen = set()
    for item in data["memo_surfaces"]:
        for key in ("id", "name", "surface_kind", "summary", "primary_focus", "recall_modes", "status", "temperature", "inspect_surface", "expand_surface", "source_path"):
            if key not in item:
                raise SystemExit(f"{path}: surface missing key {key}")
        if item["id"] in seen:
            raise SystemExit(f"{path}: duplicate id {item['id']}")
        seen.add(item["id"])
        ensure_exists(item["source_path"], f"{path}:{item['id']}:source_path")
        ensure_exists(item["inspect_surface"], f"{path}:{item['id']}:inspect_surface")
        ensure_exists(item["expand_surface"], f"{path}:{item['id']}:expand_surface")
        if require_relations:
            for key in ("related_surface_ids", "strongest_next_sources", "focus_tags"):
                if key not in item:
                    raise SystemExit(f"{path}: surface {item['id']} missing key {key}")


def validate_capsules(path: Path) -> None:
    data = load_json(path)
    for key in ("capsule_version", "source_of_truth", "memo_surfaces"):
        if key not in data:
            raise SystemExit(f"{path}: missing key {key}")
    if not isinstance(data["memo_surfaces"], list) or not data["memo_surfaces"]:
        raise SystemExit(f"{path}: memo_surfaces must be a non-empty list")
    for item in data["memo_surfaces"]:
        for key in ("id", "name", "summary", "one_line_intent", "use_when_short", "do_not_use_short", "inputs_short", "outputs_short", "core_contract_short", "main_risk_short", "validation_short", "source_path"):
            if key not in item:
                raise SystemExit(f"{path}: capsule {item.get('id', '<unknown>')} missing key {key}")
        ensure_exists(item["source_path"], f"{path}:{item['id']}:source_path")


def validate_sections(path: Path) -> None:
    data = load_json(path)
    for key in ("sections_version", "source_of_truth", "memo_surfaces"):
        if key not in data:
            raise SystemExit(f"{path}: missing key {key}")
    if not isinstance(data["memo_surfaces"], list) or not data["memo_surfaces"]:
        raise SystemExit(f"{path}: memo_surfaces must be a non-empty list")
    seen = set()
    for item in data["memo_surfaces"]:
        for key in ("id", "name", "source_path", "sections"):
            if key not in item:
                raise SystemExit(f"{path}: section surface missing key {key}")
        ensure_exists(item["source_path"], f"{path}:{item['id']}:source_path")
        if not isinstance(item["sections"], list) or not item["sections"]:
            raise SystemExit(f"{path}: {item['id']} must contain at least one section")
        for section in item["sections"]:
            for key in ("section_id", "heading", "ordinal", "summary", "body"):
                if key not in section:
                    raise SystemExit(f"{path}: section in {item['id']} missing key {key}")
            if section["section_id"] in seen:
                raise SystemExit(f"{path}: duplicate section id {section['section_id']}")
            seen.add(section["section_id"])


def validate_router_recall_contract(path: Path) -> None:
    validator = validator_for("recall_contract.schema.json")
    data = load_json(path)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    for label in ("inspect_surface", "expand_surface"):
        error = local_ref_error(data.get(label), label)
        if error:
            errors.append(error)
    if errors:
        raise SystemExit(f"{path}: " + "; ".join(errors))


def validate_surface_alignment() -> None:
    catalog = load_json(GENERATED / "memory_catalog.json")
    catalog_min = load_json(GENERATED / "memory_catalog.min.json")
    capsules = load_json(GENERATED / "memory_capsules.json")
    sections = load_json(GENERATED / "memory_sections.full.json")

    surfaces = {
        "memory_catalog.json": catalog["memo_surfaces"],
        "memory_catalog.min.json": catalog_min["memo_surfaces"],
        "memory_capsules.json": capsules["memo_surfaces"],
        "memory_sections.full.json": sections["memo_surfaces"],
    }

    expected_ids = {item["id"] for item in catalog["memo_surfaces"]}
    expected_paths = {item["id"]: item["source_path"] for item in catalog["memo_surfaces"]}

    for label, items in surfaces.items():
        ids = {item["id"] for item in items}
        if ids != expected_ids:
            missing = sorted(expected_ids - ids)
            extra = sorted(ids - expected_ids)
            details = []
            if missing:
                details.append("missing ids: " + ", ".join(missing))
            if extra:
                details.append("extra ids: " + ", ".join(extra))
            raise SystemExit(f"{label}: surface ids out of alignment ({'; '.join(details)})")

        for item in items:
            expected_path = expected_paths[item["id"]]
            if item["source_path"] != expected_path:
                raise SystemExit(
                    f"{label}: {item['id']} source_path mismatch: "
                    f"expected {expected_path}, got {item['source_path']}"
                )


def main() -> int:
    validate_catalog(GENERATED / "memory_catalog.json", require_relations=True)
    validate_catalog(GENERATED / "memory_catalog.min.json", require_relations=False)
    validate_capsules(GENERATED / "memory_capsules.json")
    validate_sections(GENERATED / "memory_sections.full.json")
    validate_router_recall_contract(EXAMPLES / "recall_contract.router.semantic.json")
    validate_surface_alignment()
    print("Router-facing memo doctrine surfaces validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
