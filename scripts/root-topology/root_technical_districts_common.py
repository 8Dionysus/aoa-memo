from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "root-topology" / "root_technical_districts.json"
GENERATED_PATH = REPO_ROOT / "generated" / "root-topology" / "root_technical_districts.min.json"

SCHEMA_VERSION = "aoa_memo_root_technical_districts_index_v1"
CONFIG_REF = "config/root-topology/root_technical_districts.json"
SOURCE_OF_TRUTH = "mechanics/ARTIFACT_TOPOLOGY.md"
GENERATED_BY = "scripts/root-topology/build_root_technical_districts_index.py"

DISTRICT_ORDER = (
    "config",
    "evals",
    "examples",
    "generated",
    "kag",
    "manifests",
    "schemas",
    "skills",
    "scripts",
    "tests",
)

FAMILY_FIELDS = {
    "config": ("config_families", "configs"),
    "examples": ("example_families", "examples"),
    "generated": ("generated_families", "outputs"),
    "schemas": ("schema_families", "schemas"),
    "scripts": ("script_families", "scripts"),
    "tests": ("test_families", "tests"),
}

DISTRICT_GUIDE = {
    "config": {
        "use_for": "repo-wide source maps that drive builders, validators, and route-card companions",
        "route_local_to": "mechanics/<slug>/parts/<part>/config/ when the input belongs to one mechanic operation",
        "check": "python scripts/mechanics/validate_mechanic_artifact_topology.py",
    },
    "evals": {
        "use_for": "repo-local eval pressure, intake packets, suites, reports, and memory guardrail evidence shape",
        "route_local_to": "aoa-evals when the pressure becomes proof doctrine, verdict, scoring, or regression authority",
        "check": "python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .",
    },
    "examples": {
        "use_for": "public-safe shared memory examples, recall contracts, and generated-surface manifests",
        "route_local_to": "mechanics/<slug>/parts/<part>/examples/ when the example teaches one mechanic contract",
        "check": "python scripts/memory/validate_memo.py --profile schema",
    },
    "generated": {
        "use_for": "compact companions consumed outside one package",
        "route_local_to": "mechanics/<slug>/parts/<part>/generated/ when the output mirrors one mechanic operation",
        "check": "python scripts/root-topology/validate_root_technical_districts_index.py",
    },
    "kag": {
        "use_for": "compact local KAG provider records for memo registry and reviewed memory corpus routes",
        "route_local_to": "aoa-kag when the change affects shared KAG schema, registry, composition, or provider validation",
        "check": "python ../aoa-kag/scripts/validate_kag.py",
    },
    "manifests": {
        "use_for": "future shared recurrence manifests",
        "route_local_to": "mechanics/<slug>/parts/<part>/manifests/ when the manifest binds one mechanic operation",
        "check": "python scripts/mechanics/validate_mechanic_artifact_topology.py",
    },
    "schemas": {
        "use_for": "public memory-object, recall, provenance, support-object, and generated-surface contracts",
        "route_local_to": "mechanics/<slug>/parts/<part>/schemas/ when the schema governs one mechanic operation",
        "check": "python scripts/memory/validate_memo.py --profile schema",
    },
    "skills": {
        "use_for": "admitted aoa-memo-specific callable procedures and their OS user-profile admission manifest",
        "route_local_to": "aoa-skills when the procedure is shared, cross-repository, or changes common portability and projection grammar",
        "check": "python ../aoa-skills/scripts/validate_home_skill_port.py --owner-root .",
    },
    "scripts": {
        "use_for": "repo-wide validators, builders, release gates, and shared helper modules",
        "route_local_to": "mechanics/<slug>/parts/<part>/scripts/ when the entrypoint belongs to one mechanic operation",
        "check": "python scripts/release/release_check.py",
    },
    "tests": {
        "use_for": "repo-wide regressions, route-card coverage, generated parity, and cross-mechanic contracts",
        "route_local_to": "mechanics/<slug>/parts/<part>/tests/ when the test protects one mechanic operation",
        "check": "python -m pytest -q tests",
    },
}


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _family_ids(payload: dict[str, Any], district: str) -> list[str]:
    if district == "manifests":
        policy = payload.get("manifest_policy", {})
        policy_id = policy.get("id") if isinstance(policy, dict) else None
        return [policy_id] if isinstance(policy_id, str) and policy_id else []
    if district not in FAMILY_FIELDS:
        return []

    family_key, path_key = FAMILY_FIELDS[district]
    allowed = set(payload["districts"][district]["allowed_files"])
    ids: list[str] = []
    for family in payload.get(family_key, []):
        if not isinstance(family, dict):
            continue
        family_id = family.get("id")
        paths = family.get(path_key, [])
        if isinstance(family_id, str) and isinstance(paths, list) and allowed.intersection(paths):
            ids.append(family_id)
    return sorted(ids)


def build_index() -> dict[str, Any]:
    payload = load_config()
    districts_config = payload["districts"]
    districts: dict[str, Any] = {}
    total_allowed = 0
    total_allowed_prefixes = 0
    total_families = 0

    for district in DISTRICT_ORDER:
        config = districts_config[district]
        allowed_count = len(config["allowed_files"])
        allowed_prefix_count = len(config.get("allowed_prefixes", []))
        family_ids = _family_ids(payload, district)
        total_allowed += allowed_count
        total_allowed_prefixes += allowed_prefix_count
        total_families += len(family_ids)
        districts[district] = {
            "path": f"{district}/",
            "route_card": f"{district}/AGENTS.md",
            "root_role": config["root_role"],
            "use_for": DISTRICT_GUIDE[district]["use_for"],
            "route_local_to": DISTRICT_GUIDE[district]["route_local_to"],
            "check": DISTRICT_GUIDE[district]["check"],
            "allowed_count": allowed_count,
            "allowed_prefix_count": allowed_prefix_count,
            "family_ids": family_ids,
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "generated_by": GENERATED_BY,
        "route_card_exception": payload["route_card_exception"],
        "district_order": list(DISTRICT_ORDER),
        "placement_rule": {
            "root": "shared, repo-wide, public contract, generated companion, or cross-mechanic artifact",
            "mechanic_local": "mechanics/<slug>/parts/<part>/",
            "bounded_allowlist": CONFIG_REF,
        },
        "counts": {
            "districts": len(DISTRICT_ORDER),
            "allowed_files": total_allowed,
            "allowed_prefixes": total_allowed_prefixes,
            "families": total_families,
        },
        "districts": districts,
    }


def render_index(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
