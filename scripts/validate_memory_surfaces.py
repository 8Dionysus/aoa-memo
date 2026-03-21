#!/usr/bin/env python3
"""Validate router-facing aoa-memo doctrine surfaces."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"


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


def main() -> int:
    validate_catalog(GENERATED / "memory_catalog.json", require_relations=True)
    validate_catalog(GENERATED / "memory_catalog.min.json", require_relations=False)
    validate_capsules(GENERATED / "memory_capsules.json")
    validate_sections(GENERATED / "memory_sections.full.json")
    print("Router-facing memo doctrine surfaces validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
