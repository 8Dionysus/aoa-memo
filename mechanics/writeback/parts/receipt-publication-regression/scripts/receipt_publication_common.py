from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_LOG_PATH = REPO_ROOT / ".aoa" / "live_receipts" / "memo-writeback-receipts.jsonl"
MEMORY_OBJECT_CATALOG_PATH = (
    REPO_ROOT
    / "generated"
    / "memory-objects"
    / "memory_object_catalog.min.json"
)
RUNTIME_WRITEBACK_TARGETS_PATH = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "runtime-and-temperature"
    / "generated"
    / "runtime_writeback_targets.min.json"
)
GROWTH_REFINERY_LANES_PATH = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "growth-and-continuity"
    / "generated"
    / "growth_refinery_writeback_lanes.min.json"
)
RECALL_SURFACE_PREFIX = "repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#"
GROWTH_LANE_REF_PREFIX = (
    "repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/"
    "growth_refinery_writeback_lanes.min.json#"
)
ALLOWED_EVENT_KINDS = {"memo_writeback_receipt", "memo_growth_writeback_receipt"}
EXPECTED_ACTOR_BY_EVENT_KIND = {
    "memo_writeback_receipt": "aoa-memo:runtime-writeback",
    "memo_growth_writeback_receipt": "aoa-memo:growth-refinery-writeback",
}


class ReceiptPublishError(ValueError):
    pass


def load_memory_object_catalog(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: memory-object catalog must be an object")
    items = payload.get("memory_objects")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: memory-object catalog must expose memory_objects")
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.memory_objects[{index}]: must be an object")
        object_id = item.get("id")
        if not isinstance(object_id, str) or not object_id:
            raise ReceiptPublishError(f"{path}.memory_objects[{index}].id: must be a non-empty string")
        by_id[object_id] = item
    return by_id


def load_runtime_writeback_targets(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: runtime writeback targets must be an object")
    items = payload.get("targets")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: runtime writeback targets must expose targets")
    by_surface: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.targets[{index}]: must be an object")
        runtime_surface = item.get("runtime_surface")
        if not isinstance(runtime_surface, str) or not runtime_surface:
            raise ReceiptPublishError(
                f"{path}.targets[{index}].runtime_surface: must be a non-empty string"
            )
        by_surface[runtime_surface] = item
    return by_surface


def load_growth_refinery_writeback_lanes(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: growth refinery writeback lanes must be an object")
    items = payload.get("lanes")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: growth refinery writeback lanes must expose lanes")
    by_ref: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.lanes[{index}]: must be an object")
        lane_ref = item.get("lane_ref")
        if not isinstance(lane_ref, str) or not lane_ref:
            raise ReceiptPublishError(f"{path}.lanes[{index}].lane_ref: must be a non-empty string")
        by_ref[lane_ref] = item
    return by_ref
