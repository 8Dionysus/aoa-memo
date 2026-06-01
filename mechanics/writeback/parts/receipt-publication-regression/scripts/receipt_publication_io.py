from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from receipt_publication_common import (
    GROWTH_REFINERY_LANES_PATH,
    MEMORY_OBJECT_CATALOG_PATH,
    RUNTIME_WRITEBACK_TARGETS_PATH,
    ReceiptPublishError,
    load_growth_refinery_writeback_lanes,
    load_memory_object_catalog,
    load_runtime_writeback_targets,
)
from receipt_publication_validation import validate_receipt


def load_receipts(
    paths: list[Path],
    *,
    memory_objects_by_id: dict[str, dict[str, Any]] | None = None,
    runtime_targets_by_surface: dict[str, dict[str, Any]] | None = None,
    growth_lanes_by_ref: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if memory_objects_by_id is None:
        memory_objects_by_id = load_memory_object_catalog(MEMORY_OBJECT_CATALOG_PATH)
    if runtime_targets_by_surface is None:
        runtime_targets_by_surface = load_runtime_writeback_targets(RUNTIME_WRITEBACK_TARGETS_PATH)
    if growth_lanes_by_ref is None:
        growth_lanes_by_ref = load_growth_refinery_writeback_lanes(GROWTH_REFINERY_LANES_PATH)
    receipts: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix == ".jsonl":
            for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                line = raw_line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ReceiptPublishError(f"{path}:{line_number}: receipt must be an object")
                validate_receipt(
                    item,
                    location=f"{path}:{line_number}",
                    memory_objects_by_id=memory_objects_by_id,
                    runtime_targets_by_surface=runtime_targets_by_surface,
                    growth_lanes_by_ref=growth_lanes_by_ref,
                )
                receipts.append(item)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            validate_receipt(
                payload,
                location=str(path),
                memory_objects_by_id=memory_objects_by_id,
                runtime_targets_by_surface=runtime_targets_by_surface,
                growth_lanes_by_ref=growth_lanes_by_ref,
            )
            receipts.append(payload)
            continue
        if not isinstance(payload, list):
            raise ReceiptPublishError(f"{path}: receipt payload must be an object or list")
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                raise ReceiptPublishError(f"{path}[{index}]: receipt must be an object")
            validate_receipt(
                item,
                location=f"{path}[{index}]",
                memory_objects_by_id=memory_objects_by_id,
                runtime_targets_by_surface=runtime_targets_by_surface,
                growth_lanes_by_ref=growth_lanes_by_ref,
            )
            receipts.append(item)
    return receipts


def load_existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    event_ids: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}:{line_number}: existing log line must be an object")
        event_id = item.get("event_id")
        if isinstance(event_id, str) and event_id:
            event_ids.add(event_id)
    return event_ids


def count_new_receipts(*, log_path: Path, receipts: list[dict[str, Any]]) -> tuple[int, int]:
    existing_ids = load_existing_ids(log_path)
    appended = 0
    skipped = 0
    for receipt in receipts:
        event_id = receipt["event_id"]
        if event_id in existing_ids:
            skipped += 1
            continue
        existing_ids.add(event_id)
        appended += 1
    return appended, skipped


def append_new_receipts(*, log_path: Path, receipts: list[dict[str, Any]]) -> tuple[int, int]:
    existing_ids = load_existing_ids(log_path)
    appended = 0
    skipped = 0
    needs_line_boundary = False
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists() and log_path.stat().st_size > 0:
        with log_path.open("rb") as existing_handle:
            existing_handle.seek(-1, 2)
            needs_line_boundary = existing_handle.read(1) != b"\n"
    with log_path.open("a", encoding="utf-8") as handle:
        for receipt in receipts:
            event_id = receipt["event_id"]
            if event_id in existing_ids:
                skipped += 1
                continue
            if needs_line_boundary:
                handle.write("\n")
                needs_line_boundary = False
            handle.write(json.dumps(receipt, sort_keys=True, ensure_ascii=False) + "\n")
            existing_ids.add(event_id)
            appended += 1
    return appended, skipped
