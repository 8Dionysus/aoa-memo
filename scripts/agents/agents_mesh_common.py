from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


CONFIG_PATH = Path("config/agents/agents_mesh.json")
CONFIG_SCHEMA_VERSION = "aoa_memo_agents_mesh_v1"
INDEX_SCHEMA_VERSION = "aoa_memo_agents_mesh_index_v1"
SOURCE_OF_TRUTH = "agents-md-mesh-v1"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class AgentsMeshError(RuntimeError):
    pass


def repo_root_from_script(script_path: Path) -> Path:
    return script_path.resolve().parents[2]


def posix_rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def compact_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def load_mesh_config(repo_root: Path) -> dict[str, Any]:
    path = repo_root / CONFIG_PATH
    if not path.is_file():
        raise AgentsMeshError(f"{CONFIG_PATH.as_posix()}: file is missing")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AgentsMeshError(f"{CONFIG_PATH.as_posix()}: invalid JSON: {exc}") from exc
    if config.get("schema_version") != CONFIG_SCHEMA_VERSION:
        raise AgentsMeshError(
            f"{CONFIG_PATH.as_posix()}: schema_version must be {CONFIG_SCHEMA_VERSION!r}"
        )
    if config.get("source_of_truth") != SOURCE_OF_TRUTH:
        raise AgentsMeshError(
            f"{CONFIG_PATH.as_posix()}: source_of_truth must be {SOURCE_OF_TRUTH!r}"
        )
    return config


def ignored_directory_names(config: dict[str, Any]) -> set[str]:
    configured = config.get("ignored_directory_names", ())
    if not isinstance(configured, list):
        raise AgentsMeshError("ignored_directory_names must be a list")
    return {str(name) for name in configured}


def top_level_exemptions(config: dict[str, Any]) -> set[str]:
    configured = config.get("top_level_exemptions", ())
    if not isinstance(configured, list):
        raise AgentsMeshError("top_level_exemptions must be a list")
    return {str(name) for name in configured}


def card_contracts(config: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    cards = config.get("canonical_cards", ())
    if not isinstance(cards, list) or not cards:
        raise AgentsMeshError("canonical_cards must be a non-empty list")
    normalized: list[dict[str, Any]] = []
    for card in cards:
        if not isinstance(card, dict):
            raise AgentsMeshError("canonical_cards entries must be objects")
        path = card.get("path")
        if not isinstance(path, str) or not path:
            raise AgentsMeshError("canonical card path must be a non-empty string")
        snippets = card.get("required_snippets", ())
        if not isinstance(snippets, list) or not snippets:
            raise AgentsMeshError(f"{path}: required_snippets must be a non-empty list")
        normalized.append(
            {
                "path": path,
                "min_lines": int(card.get("min_lines", 1)),
                "required_snippets": tuple(str(snippet) for snippet in snippets),
            }
        )
    return tuple(normalized)


def canonical_card_paths(config: dict[str, Any]) -> tuple[str, ...]:
    return tuple(card["path"] for card in card_contracts(config))


def iter_agents_cards(repo_root: Path, config: dict[str, Any]) -> tuple[Path, ...]:
    ignored = ignored_directory_names(config)
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(
            dirname
            for dirname in dirnames
            if dirname not in ignored and not (Path(dirpath) / dirname).is_symlink()
        )
        if "AGENTS.md" in filenames:
            found.append(Path(dirpath) / "AGENTS.md")
    return tuple(sorted(found, key=lambda path: posix_rel(path, repo_root)))


def markdown_headings(text: str) -> tuple[str, ...]:
    headings: list[str] = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            headings.append(f"{match.group(1)} {match.group(2)}")
    return tuple(headings)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def card_summary(path: Path, repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    rel_path = posix_rel(path, repo_root)
    text = path.read_text(encoding="utf-8")
    headings = markdown_headings(text)
    contract_by_path = {card["path"]: card for card in card_contracts(config)}
    contract = contract_by_path.get(rel_path)
    required_snippets = tuple(contract["required_snippets"]) if contract else ()
    missing_snippets = [snippet for snippet in required_snippets if snippet not in text]
    shape_status = "canonical" if contract else "migration"
    first_heading = headings[0] if headings else ""
    return {
        "path": rel_path,
        "shape_status": shape_status,
        "sha256": sha256_text(text),
        "line_count": len(text.splitlines()),
        "first_heading": first_heading,
        "heading_count": len(headings),
        "headings": list(headings),
        "missing_required_snippets": missing_snippets,
    }


def build_agents_mesh_index(repo_root: Path) -> dict[str, Any]:
    config = load_mesh_config(repo_root)
    cards = [card_summary(path, repo_root, config) for path in iter_agents_cards(repo_root, config)]
    canonical_count = sum(1 for card in cards if card["shape_status"] == "canonical")
    migration_count = sum(1 for card in cards if card["shape_status"] == "migration")
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_PATH.as_posix(),
        "authority_ref": config["authority_ref"],
        "system_design_ref": config["system_design_ref"],
        "root_agents_ref": config["root_agents_ref"],
        "route_contract_ref": config["route_contract_ref"],
        "generated_ref": config["generated_ref"],
        "counts": {
            "cards": len(cards),
            "canonical": canonical_count,
            "migration": migration_count,
        },
        "cards": cards,
    }
