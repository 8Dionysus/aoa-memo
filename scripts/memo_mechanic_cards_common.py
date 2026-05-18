from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from memo_mechanics_common import README_HEADINGS, REPO_ROOT, load_config


GENERATED_PATH = REPO_ROOT / "generated" / "memo_mechanic_cards.min.json"
SCHEMA_VERSION = "aoa_memo_mechanic_cards_v1"
SOURCE_OF_TRUTH = "mechanics package README mechanic cards"
CONFIG_REF = "config/memo_mechanics.json"
GENERATED_BY = "scripts/build_memo_mechanic_cards.py"

SECTION_TO_KEY = {
    "### Operation": "operation",
    "### Trigger": "trigger",
    "### Memo owns": "memo_owns",
    "### Stronger owner split": "stronger_owner_split",
    "### Inputs": "inputs",
    "### Outputs": "outputs",
    "### Must not claim": "must_not_claim",
    "### Validation": "validation",
    "### Next route": "next_route",
}
LIST_SECTION_KEYS = {"stronger_owner_split", "must_not_claim"}
KNOWN_STRONGER_OWNER_REFS = (
    "Agents-of-Abyss",
    "Tree-of-Sophia",
    "aoa-agents",
    "aoa-evals",
    "aoa-kag",
    "aoa-playbooks",
    "aoa-routing",
    "aoa-stats",
    "abyss-stack",
    "source owner",
)
STOP_LINE_TERMS = ("proof", "runtime", "role", "route", "source owner", "authority", "owner acceptance")


def render_cards(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _section_block(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    next_heading = re.search(r"^#{2,3} .+$", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def _parse_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current:
                bullets.append(_normalize(" ".join(current)))
            current = [stripped[2:].strip()]
            continue
        if current:
            current.append(stripped)
    if current:
        bullets.append(_normalize(" ".join(current)))
    return bullets


def _extract_status(text: str) -> str:
    block = _section_block(text, "## Mechanic card")
    match = re.search(r"^-\s*Status:\s*`?([^`\n]+)`?\s*$", block, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _find_owner_refs(*texts: object) -> list[str]:
    combined = "\n".join(
        "\n".join(value) if isinstance(value, list) else str(value)
        for value in texts
        if value
    )
    return [
        owner_ref
        for owner_ref in KNOWN_STRONGER_OWNER_REFS
        if owner_ref.casefold() in combined.casefold()
    ]


def _find_stop_line_terms(*texts: object) -> list[str]:
    combined = "\n".join(
        "\n".join(value) if isinstance(value, list) else str(value)
        for value in texts
        if value
    ).casefold()
    return [term for term in STOP_LINE_TERMS if term in combined]


def extract_card(slug: str) -> dict[str, Any]:
    readme_path = REPO_ROOT / "mechanics" / slug / "README.md"
    text = readme_path.read_text(encoding="utf-8")
    card: dict[str, Any] = {}
    for heading, key in SECTION_TO_KEY.items():
        block = _section_block(text, heading)
        card[key] = _parse_bullets(block) if key in LIST_SECTION_KEYS else _normalize(block)
    return {
        "status": _extract_status(text),
        "card": card,
        "owner_refs": _find_owner_refs(
            card.get("stronger_owner_split", []),
            card.get("next_route", ""),
        ),
        "stop_line_terms": _find_stop_line_terms(
            card.get("must_not_claim", []),
            card.get("next_route", ""),
        ),
    }


def build_cards() -> dict[str, Any]:
    config = load_config()
    packages = []
    for package in config["packages"]:
        slug = package["slug"]
        extracted = extract_card(slug)
        card = extracted["card"]
        packages.append(
            {
                "slug": slug,
                "title": package["title"],
                "status": extracted["status"],
                "configured_status": package["status"],
                "operation": card["operation"],
                "configured_operation": package["operation"],
                "card_ref": f"mechanics/{slug}/README.md#mechanic-card",
                "source_refs": [
                    f"mechanics/{slug}/README.md",
                    f"mechanics/{slug}/AGENTS.md",
                    f"mechanics/{slug}/OWNER_MAP.md",
                    f"mechanics/{slug}/PARTS.md",
                ],
                "card": card,
                "owner_refs": extracted["owner_refs"],
                "stop_line_terms": extracted["stop_line_terms"],
                "checks": _checks_for_package(package, extracted),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "generated_by": GENERATED_BY,
        "contract": {
            "required_headings": list(README_HEADINGS),
            "list_sections": sorted(LIST_SECTION_KEYS),
            "known_stronger_owner_refs": list(KNOWN_STRONGER_OWNER_REFS),
            "stop_line_terms": list(STOP_LINE_TERMS),
        },
        "counts": {
            "packages": len(packages),
            "landed_packages": sum(1 for package in packages if package["status"] == "landed"),
            "must_not_claims": sum(len(package["card"]["must_not_claim"]) for package in packages),
        },
        "packages": packages,
    }


def _checks_for_package(package: dict[str, Any], extracted: dict[str, Any]) -> dict[str, bool]:
    card = extracted["card"]
    source_refs = [
        REPO_ROOT / "mechanics" / package["slug"] / "README.md",
        REPO_ROOT / "mechanics" / package["slug"] / "AGENTS.md",
        REPO_ROOT / "mechanics" / package["slug"] / "OWNER_MAP.md",
        REPO_ROOT / "mechanics" / package["slug"] / "PARTS.md",
    ]
    return {
        "source-surfaces": all(path.is_file() for path in source_refs),
        "status-match": extracted["status"] == package["status"],
        "operation-match": card.get("operation") == package["operation"],
        "sections-present": all(bool(card.get(key)) for key in SECTION_TO_KEY.values()),
        "owner-split-list": len(card.get("stronger_owner_split", [])) >= 3,
        "must-not-claim-list": len(card.get("must_not_claim", [])) >= 3,
        "owner-refs": len(extracted["owner_refs"]) >= 3,
        "stop-lines": (
            {"proof", "runtime"}.issubset(set(extracted["stop_line_terms"]))
            and bool({"role", "route", "source owner", "authority", "owner acceptance"} & set(extracted["stop_line_terms"]))
        ),
        "validation-route": "AGENTS" in str(card.get("validation", "")) and "validation" in str(card.get("validation", "")).casefold(),
        "next-route": bool(extracted["owner_refs"]) and "Route " in str(card.get("next_route", "")),
    }


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    expected = build_cards()
    if payload != expected:
        issues.append("generated/memo_mechanic_cards.min.json is stale; run scripts/build_memo_mechanic_cards.py")
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"generated/memo_mechanic_cards.min.json must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append("generated/memo_mechanic_cards.min.json must keep mechanic README cards as source_of_truth")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"generated/memo_mechanic_cards.min.json must route config_ref to {CONFIG_REF}")
    if payload.get("generated_by") != GENERATED_BY:
        issues.append(f"generated/memo_mechanic_cards.min.json must name {GENERATED_BY}")

    packages = payload.get("packages")
    if not isinstance(packages, list):
        issues.append("generated/memo_mechanic_cards.min.json packages must be a list")
        return issues
    for package in packages:
        if not isinstance(package, dict):
            issues.append("generated/memo_mechanic_cards.min.json package entries must be objects")
            continue
        slug = package.get("slug", "<missing>")
        checks = package.get("checks")
        if not isinstance(checks, dict):
            issues.append(f"mechanics/{slug}: card checks must be an object")
            continue
        for check, passed in checks.items():
            if passed is not True:
                issues.append(f"mechanics/{slug}: route-card check failed: {check}")
        card = package.get("card")
        if not isinstance(card, dict):
            issues.append(f"mechanics/{slug}: card must be an object")
            continue
        for key in SECTION_TO_KEY.values():
            if not card.get(key):
                issues.append(f"mechanics/{slug}: card.{key} is empty")

    counts = payload.get("counts")
    if isinstance(counts, dict):
        if counts.get("landed_packages") != counts.get("packages"):
            issues.append("generated/memo_mechanic_cards.min.json landed_packages must equal packages")
        if int(counts.get("must_not_claims", 0)) < int(counts.get("packages", 0)) * 3:
            issues.append("generated/memo_mechanic_cards.min.json must keep at least three stop-lines per package")

    return issues
