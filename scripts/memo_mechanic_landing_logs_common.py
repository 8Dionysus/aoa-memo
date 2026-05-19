from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from memo_mechanics_common import REPO_ROOT, load_config


GENERATED_PATH = REPO_ROOT / "generated" / "memo_mechanic_landing_logs.min.json"
SCHEMA_VERSION = "aoa_memo_mechanic_landing_logs_v1"
SOURCE_OF_TRUTH = "mechanics package LANDING_LOG.md receipts"
CONFIG_REF = "config/memo_mechanics.json"
CARD_INDEX_REF = "generated/memo_mechanic_cards.min.json"
OWNER_ROUTE_INDEX_REF = "generated/memo_mechanic_owner_routes.min.json"
GENERATED_BY = "scripts/build_memo_mechanic_landing_logs.py"

REQUIRED_VALIDATION_REFS = ("python scripts/release_check.py",)
SUPPORTING_VALIDATION_REFS = (
    "python scripts/validate_memo_mechanics.py",
    "python scripts/build_memo_mechanics_index.py --check",
    "python scripts/validate_memo_mechanics_index.py",
    "python scripts/build_memo_mechanic_cards.py --check",
    "python scripts/validate_memo_mechanic_cards.py",
    "python scripts/build_memo_mechanic_owner_routes.py --check",
    "python scripts/validate_memo_mechanic_owner_routes.py",
    "python scripts/build_memo_mechanic_readiness.py --check",
    "python scripts/validate_memo_mechanic_readiness.py",
    "python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py",
    "python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check",
)
LANDING_EVIDENCE_TERMS = (
    "landed",
    "moved",
    "added",
    "corrected",
    "became",
    "refreshed",
    "routed",
    "updated",
)
STOP_LINE_TERMS = (
    "proof",
    "runtime",
    "role",
    "route",
    "source owner",
    "authority",
    "owner acceptance",
    "KAG",
    "playbook",
    "stats",
)


def render_landing_logs(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _read(relative: str) -> str:
    path = REPO_ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _dates(text: str) -> list[str]:
    found = set(re.findall(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", text, flags=re.MULTILINE))
    found.update(re.findall(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|", text, flags=re.MULTILINE))
    return sorted(found)


def _known_validation_refs(text: str) -> list[str]:
    refs = (*REQUIRED_VALIDATION_REFS, *SUPPORTING_VALIDATION_REFS)
    return [ref for ref in refs if ref in text]


def _python_commands(text: str) -> list[str]:
    commands = []
    for line in text.splitlines():
        stripped = line.strip().strip("`")
        if stripped.startswith("python "):
            commands.append(stripped)
        elif "| `python " in line:
            for match in re.findall(r"`(python [^`]+)`", line):
                commands.append(match.strip())
    return sorted(set(commands))


def _terms(text: str, terms: tuple[str, ...]) -> list[str]:
    folded = text.casefold()
    return [term for term in terms if term.casefold() in folded]


def _has_stop_line_section(text: str) -> bool:
    return "stop-line" in text.casefold() or "stop line" in text.casefold()


def build_package_landing_log(package: dict[str, Any]) -> dict[str, Any]:
    slug = package["slug"]
    relative = f"mechanics/{slug}/LANDING_LOG.md"
    path = REPO_ROOT / relative
    text = _read(relative)
    validation_refs = _known_validation_refs(text)
    stop_line_terms = _terms(text, STOP_LINE_TERMS)
    checks = {
        "landing-log-present": path.is_file(),
        "dated-entry": bool(_dates(text)),
        "landing-evidence": bool(_terms(text, LANDING_EVIDENCE_TERMS)),
        "validation-route": all(ref in validation_refs for ref in REQUIRED_VALIDATION_REFS),
        "stop-line-section": _has_stop_line_section(text),
        "stop-line-terms": (
            {"proof", "runtime"}.issubset(set(stop_line_terms))
            and bool({"role", "route", "source owner", "authority", "owner acceptance"} & set(stop_line_terms))
        ),
    }
    return {
        "slug": slug,
        "title": package["title"],
        "status": package["status"],
        "operation": package["operation"],
        "landing_log_ref": relative,
        "card_ref": f"mechanics/{slug}/README.md#mechanic-card",
        "owner_map_ref": f"mechanics/{slug}/OWNER_MAP.md",
        "dates": _dates(text),
        "landing_terms": _terms(text, LANDING_EVIDENCE_TERMS),
        "validation_refs": validation_refs,
        "python_commands": _python_commands(text),
        "stop_line_terms": stop_line_terms,
        "checks": checks,
        "ready": all(checks.values()),
    }


def build_landing_logs() -> dict[str, Any]:
    config = load_config()
    packages = [build_package_landing_log(package) for package in config["packages"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "card_index_ref": CARD_INDEX_REF,
        "owner_route_index_ref": OWNER_ROUTE_INDEX_REF,
        "generated_by": GENERATED_BY,
        "contract": {
            "required_validation_refs": list(REQUIRED_VALIDATION_REFS),
            "supporting_validation_refs": list(SUPPORTING_VALIDATION_REFS),
            "landing_evidence_terms": list(LANDING_EVIDENCE_TERMS),
            "stop_line_terms": list(STOP_LINE_TERMS),
        },
        "counts": {
            "packages": len(packages),
            "ready_logs": sum(1 for package in packages if package["ready"]),
            "dated_logs": sum(1 for package in packages if package["dates"]),
            "release_check_logs": sum(
                1
                for package in packages
                if "python scripts/release_check.py" in package["validation_refs"]
            ),
            "stop_line_logs": sum(1 for package in packages if package["checks"]["stop-line-section"]),
        },
        "packages": packages,
        "generated_note": "This receipt index mirrors package LANDING_LOG.md files. It is not proof, owner acceptance, runtime authority, route dispatch, role authority, KAG truth, playbook choreography, stats truth, or source doctrine.",
    }


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    expected = build_landing_logs()
    if payload != expected:
        issues.append("generated/memo_mechanic_landing_logs.min.json is stale; run scripts/build_memo_mechanic_landing_logs.py")
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"generated/memo_mechanic_landing_logs.min.json must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append("generated/memo_mechanic_landing_logs.min.json must keep package LANDING_LOG.md receipts as source_of_truth")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"generated/memo_mechanic_landing_logs.min.json must route config_ref to {CONFIG_REF}")
    if payload.get("card_index_ref") != CARD_INDEX_REF:
        issues.append(f"generated/memo_mechanic_landing_logs.min.json must route card_index_ref to {CARD_INDEX_REF}")
    if payload.get("owner_route_index_ref") != OWNER_ROUTE_INDEX_REF:
        issues.append(f"generated/memo_mechanic_landing_logs.min.json must route owner_route_index_ref to {OWNER_ROUTE_INDEX_REF}")
    if payload.get("generated_by") != GENERATED_BY:
        issues.append(f"generated/memo_mechanic_landing_logs.min.json must name {GENERATED_BY}")

    packages = payload.get("packages")
    if not isinstance(packages, list):
        issues.append("generated/memo_mechanic_landing_logs.min.json packages must be a list")
        return issues

    for package in packages:
        if not isinstance(package, dict):
            issues.append("generated/memo_mechanic_landing_logs.min.json package entries must be objects")
            continue
        slug = package.get("slug", "<missing>")
        if package.get("ready") is not True:
            issues.append(f"mechanics/{slug}: landing-log contract is not complete")
        checks = package.get("checks")
        if not isinstance(checks, dict):
            issues.append(f"mechanics/{slug}: landing-log checks must be an object")
            continue
        for check, passed in checks.items():
            if passed is not True:
                issues.append(f"mechanics/{slug}: landing-log check failed: {check}")
        validation_refs = package.get("validation_refs")
        if not isinstance(validation_refs, list) or not all(ref in validation_refs for ref in REQUIRED_VALIDATION_REFS):
            issues.append(f"mechanics/{slug}: landing log must name python scripts/release_check.py")
        stop_line_terms = package.get("stop_line_terms")
        if (
            not isinstance(stop_line_terms, list)
            or not {"proof", "runtime"}.issubset(set(stop_line_terms))
            or not bool({"role", "route", "source owner", "authority", "owner acceptance"} & set(stop_line_terms))
        ):
            issues.append(
                f"mechanics/{slug}: landing log stop-lines must name proof, runtime, and one authority boundary"
            )

    counts = payload.get("counts")
    if isinstance(counts, dict):
        for field in ("ready_logs", "dated_logs", "release_check_logs", "stop_line_logs"):
            if counts.get(field) != counts.get("packages"):
                issues.append(f"generated/memo_mechanic_landing_logs.min.json {field} must equal packages")

    note = str(payload.get("generated_note", ""))
    for stop_line in ("not proof", "owner acceptance", "runtime authority", "route dispatch", "role authority"):
        if stop_line not in note:
            issues.append(f"generated/memo_mechanic_landing_logs.min.json generated_note must mention {stop_line!r}")
    return issues
