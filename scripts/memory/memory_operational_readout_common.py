from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT.parent
OUTPUT_DIR = REPO_ROOT / "generated" / "memory"
ACCESS_OUTPUT = OUTPUT_DIR / "access_plane_currentness.min.json"
SOURCE_WAVE_OUTPUT = OUTPUT_DIR / "source_intake_wave.min.json"
PORT_STATUS_OUTPUT = OUTPUT_DIR / "workspace_memo_port_status.min.json"

OBJECT_CATALOG = REPO_ROOT / "generated" / "memory-objects" / "memory_object_catalog.min.json"
OBJECT_CAPSULES = REPO_ROOT / "generated" / "memory-objects" / "memory_object_capsules.json"
QUEST_CATALOG = REPO_ROOT / "generated" / "quests" / "quest_catalog.min.json"
QUEST_DISPATCH = REPO_ROOT / "generated" / "quests" / "quest_dispatch.min.json"
WORKSPACE_MAP = (
    Path(os.environ.get("AOA_WORKSPACE_ROUTE_ROOT", str(WORKSPACE_ROOT / "8Dionysus")))
    / "generated"
    / "workspace_memory_map.min.json"
)
MCP_ROOT = Path(
    os.environ.get(
        "AOA_MEMO_MCP_ROOT",
        str(Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-memo-mcp"),
    )
)
MCP_SOURCE_HINT = "repo:abyss-stack/mcp/services/aoa-memo-mcp"
WORKSPACE_MAP_REF = "repo:8Dionysus/generated/workspace_memory_map.min.json"

FORBIDDEN_ABSOLUTE_PREFIXES = ('"/srv/', '"/home/', '"/var/', '"/mnt/')
GENERATED_BY = "scripts/memory/build_memory_operational_readouts.py"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def object_index() -> dict[str, dict[str, Any]]:
    payload = load_json(OBJECT_CATALOG)
    return {
        item["id"]: item
        for item in payload.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def object_ref(objects: dict[str, dict[str, Any]], object_id: str) -> dict[str, Any]:
    item = objects.get(object_id)
    if not item:
        return {
            "id": object_id,
            "found": False,
            "source_kind": "",
            "current_recall_status": "",
            "source_path": "",
        }
    return {
        "id": object_id,
        "found": True,
        "kind": item.get("kind", ""),
        "title": item.get("title", ""),
        "source_kind": item.get("source_kind", ""),
        "current_recall_status": item.get("current_recall_status", ""),
        "source_path": item.get("source_path", ""),
    }


def validate_readout(path: Path, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "surface_kind", "owner_repo", "generated_by", "source_refs", "summary"):
        if key not in payload:
            errors.append(f"{path.name}: missing {key}")
    if payload.get("owner_repo") != "aoa-memo":
        errors.append(f"{path.name}: owner_repo must stay aoa-memo")
    if payload.get("generated_by") != GENERATED_BY:
        errors.append(f"{path.name}: generated_by must name the builder")
    if not isinstance(payload.get("source_refs"), list) or not payload.get("source_refs"):
        errors.append(f"{path.name}: source_refs must be a non-empty list")
    owner_split = {
        "owner_repo": payload.get("owner_repo"),
        "source_owner_split": payload.get("source_owner_split"),
        "authority_boundary": payload.get("authority_boundary"),
    }
    if "aoa-memo" not in json.dumps(owner_split, ensure_ascii=False):
        errors.append(f"{path.name}: owner split must mention aoa-memo")
    rendered = render_json(payload)
    if any(prefix in rendered for prefix in FORBIDDEN_ABSOLUTE_PREFIXES):
        errors.append(f"{path.name}: generated readout leaked an absolute path")
    return errors
