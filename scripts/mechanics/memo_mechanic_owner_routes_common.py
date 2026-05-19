from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memo_mechanic_cards_common import GENERATED_PATH as CARD_INDEX_PATH
from memo_mechanic_cards_common import KNOWN_STRONGER_OWNER_REFS
from memo_mechanics_common import REPO_ROOT, load_config


GENERATED_PATH = REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_owner_routes.min.json"
SCHEMA_VERSION = "aoa_memo_mechanic_owner_routes_v1"
SOURCE_OF_TRUTH = "mechanics package OWNER_MAP.md and README mechanic cards"
CONFIG_REF = "config/mechanics/memo_mechanics.json"
CARD_INDEX_REF = "generated/mechanics/memo_mechanic_cards.min.json"
GENERATED_BY = "scripts/mechanics/build_memo_mechanic_owner_routes.py"

OWNER_REFS = ("aoa-memo", *KNOWN_STRONGER_OWNER_REFS)


def render_owner_routes(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _read(relative: str) -> str:
    path = REPO_ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _cells(line: str) -> list[str]:
    return [cell.strip().replace("`", "") for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(":", "").replace("-", "").strip()) <= set() for cell in cells)


def _normalize_owner_refs(text: str) -> list[str]:
    lower = text.casefold()
    refs = [owner_ref for owner_ref in OWNER_REFS if owner_ref.casefold() in lower]
    if (
        "source owner" in lower
        or "source repositories" in lower
        or "source repository" in lower
        or "owner repository" in lower
        or "owner repositories" in lower
        or "owning repository" in lower
        or "governing owner" in lower
    ) and "source owner" not in refs:
        refs.append("source owner")
    if "runtime owner" in lower and "abyss-stack" not in refs:
        refs.append("abyss-stack")
    return sorted(set(refs))


def parse_owner_map(slug: str) -> list[dict[str, Any]]:
    relative = f"mechanics/{slug}/OWNER_MAP.md"
    text = _read(relative)
    entries: list[dict[str, Any]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        table_lines: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            table_lines.append(lines[index])
            index += 1
        if len(table_lines) < 3:
            continue
        header = _cells(table_lines[0])
        body = [_cells(line) for line in table_lines[1:]]
        body = [row for row in body if not _is_separator(row)]
        if len(header) < 2:
            continue
        header_lower = [cell.casefold() for cell in header]
        for row in body:
            if len(row) < 2:
                continue
            if "owner" in header_lower[0] and ("owns" in header_lower[1] or "concern" not in header_lower[0]):
                owner_text = row[0]
                concern = row[1]
            elif "owner" in header_lower[1]:
                concern = row[0]
                owner_text = row[1]
            else:
                continue
            owner_refs = _normalize_owner_refs(f"{owner_text} {concern}")
            entries.append(
                {
                    "concern": concern,
                    "owner_text": owner_text,
                    "owner_refs": owner_refs,
                    "route_kind": "memo-owner" if "aoa-memo" in owner_refs else "stronger-owner",
                }
            )
    return entries


def _load_cards() -> dict[str, dict[str, Any]]:
    payload = json.loads(CARD_INDEX_PATH.read_text(encoding="utf-8"))
    return {package["slug"]: package for package in payload.get("packages", [])}


def _owner_index(packages: list[dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    owner_index: dict[str, list[dict[str, str]]] = {}
    for package in packages:
        slug = package["slug"]
        for route in package["owner_routes"]:
            for owner_ref in route["owner_refs"]:
                owner_index.setdefault(owner_ref, []).append(
                    {
                        "package": slug,
                        "concern": route["concern"],
                        "route_kind": route["route_kind"],
                    }
                )
    return {owner_ref: owner_index[owner_ref] for owner_ref in sorted(owner_index)}


def _checks(card: dict[str, Any], owner_routes: list[dict[str, Any]]) -> dict[str, bool]:
    card_owner_refs = set(card.get("owner_refs", []))
    owner_map_refs = {
        owner_ref
        for route in owner_routes
        for owner_ref in route.get("owner_refs", [])
    }
    stronger_routes = [route for route in owner_routes if route["route_kind"] == "stronger-owner"]
    return {
        "owner-map-present": bool(owner_routes),
        "memo-owner-route": any(route["route_kind"] == "memo-owner" for route in owner_routes),
        "stronger-owner-routes": len(stronger_routes) >= 3,
        "card-owner-coverage": card_owner_refs.issubset(owner_map_refs),
        "no-generated-authority": True,
    }


def build_owner_routes() -> dict[str, Any]:
    config = load_config()
    cards = _load_cards()
    packages = []
    for package in config["packages"]:
        slug = package["slug"]
        card = cards.get(slug, {})
        owner_routes = parse_owner_map(slug)
        if not any(route["route_kind"] == "memo-owner" for route in owner_routes):
            memo_owns = str((card.get("card") or {}).get("memo_owns", "")).strip()
            if memo_owns:
                owner_routes.insert(
                    0,
                    {
                        "concern": memo_owns,
                        "owner_text": "aoa-memo",
                        "owner_refs": ["aoa-memo"],
                        "route_kind": "memo-owner",
                    },
                )
        package_payload = {
            "slug": slug,
            "title": package["title"],
            "status": package["status"],
            "operation": package["operation"],
            "owner_map_ref": f"mechanics/{slug}/OWNER_MAP.md",
            "card_ref": f"mechanics/{slug}/README.md#mechanic-card",
            "card_owner_refs": card.get("owner_refs", []),
            "owner_map_refs": sorted(
                {
                    owner_ref
                    for route in owner_routes
                    for owner_ref in route.get("owner_refs", [])
                }
            ),
            "owner_routes": owner_routes,
            "checks": _checks(card, owner_routes),
        }
        packages.append(package_payload)

    owner_index = _owner_index(packages)
    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "card_index_ref": CARD_INDEX_REF,
        "generated_by": GENERATED_BY,
        "counts": {
            "packages": len(packages),
            "route_entries": sum(len(package["owner_routes"]) for package in packages),
            "stronger_owner_entries": sum(
                1
                for package in packages
                for route in package["owner_routes"]
                if route["route_kind"] == "stronger-owner"
            ),
            "owners": len(owner_index),
        },
        "packages": packages,
        "owners": owner_index,
        "generated_note": "This route matrix mirrors package OWNER_MAP and README card surfaces. It is not owner acceptance, proof, runtime authority, route dispatch, role authority, KAG truth, playbook choreography, stats truth, or source doctrine.",
    }


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    expected = build_owner_routes()
    if payload != expected:
        issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json is stale; run scripts/mechanics/build_memo_mechanic_owner_routes.py")
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"generated/mechanics/memo_mechanic_owner_routes.min.json must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json must keep OWNER_MAP.md and README cards as source_of_truth")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"generated/mechanics/memo_mechanic_owner_routes.min.json must route config_ref to {CONFIG_REF}")
    if payload.get("card_index_ref") != CARD_INDEX_REF:
        issues.append(f"generated/mechanics/memo_mechanic_owner_routes.min.json must route card_index_ref to {CARD_INDEX_REF}")
    if payload.get("generated_by") != GENERATED_BY:
        issues.append(f"generated/mechanics/memo_mechanic_owner_routes.min.json must name {GENERATED_BY}")

    packages = payload.get("packages")
    if not isinstance(packages, list):
        issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json packages must be a list")
        return issues

    for package in packages:
        if not isinstance(package, dict):
            issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json package entries must be objects")
            continue
        slug = package.get("slug", "<missing>")
        checks = package.get("checks")
        if not isinstance(checks, dict):
            issues.append(f"mechanics/{slug}: owner-route checks must be an object")
            continue
        for check, passed in checks.items():
            if passed is not True:
                issues.append(f"mechanics/{slug}: owner-route check failed: {check}")
        owner_routes = package.get("owner_routes")
        if not isinstance(owner_routes, list) or not owner_routes:
            issues.append(f"mechanics/{slug}: owner_routes must be a non-empty list")
            continue
        for route in owner_routes:
            if not isinstance(route, dict):
                issues.append(f"mechanics/{slug}: owner route entries must be objects")
                continue
            if not route.get("concern") or not route.get("owner_text"):
                issues.append(f"mechanics/{slug}: owner route entries must name concern and owner_text")
            if not route.get("owner_refs"):
                issues.append(f"mechanics/{slug}: owner route entry lacks normalized owner_refs: {route.get('owner_text')}")

    owners = payload.get("owners")
    if not isinstance(owners, dict) or not owners:
        issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json owners index must be a non-empty object")
    counts = payload.get("counts")
    if isinstance(counts, dict):
        if counts.get("packages") != len(packages):
            issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json package count mismatch")
        if int(counts.get("owners", 0)) < 8:
            issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json must expose broad stronger-owner coverage")
        if int(counts.get("stronger_owner_entries", 0)) < int(counts.get("packages", 0)) * 3:
            issues.append("generated/mechanics/memo_mechanic_owner_routes.min.json must keep at least three stronger-owner entries per package on average")

    note = str(payload.get("generated_note", ""))
    for stop_line in ("not owner acceptance", "proof", "runtime authority", "route dispatch", "role authority"):
        if stop_line not in note:
            issues.append(f"generated/mechanics/memo_mechanic_owner_routes.min.json generated_note must mention {stop_line!r}")
    return issues
