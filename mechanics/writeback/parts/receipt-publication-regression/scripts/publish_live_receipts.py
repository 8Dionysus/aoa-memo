#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from receipt_publication_common import (  # noqa: E402
    DEFAULT_LOG_PATH,
    GROWTH_REFINERY_LANES_PATH,
    MEMORY_OBJECT_CATALOG_PATH,
    RUNTIME_WRITEBACK_TARGETS_PATH,
    ReceiptPublishError,
    load_growth_refinery_writeback_lanes,
    load_memory_object_catalog,
    load_runtime_writeback_targets,
)
from receipt_publication_io import (  # noqa: E402
    append_new_receipts,
    count_new_receipts,
    load_receipts,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append bounded memo-layer receipts to the owner-local live JSONL log."
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Path to a JSON or JSONL file containing one receipt, an array of receipts, or one receipt per line.",
    )
    parser.add_argument(
        "--log-path",
        default=str(DEFAULT_LOG_PATH),
        help="Owner-local JSONL log that should receive newly published memo receipts.",
    )
    parser.add_argument(
        "--catalog-path",
        default=str(MEMORY_OBJECT_CATALOG_PATH),
        help="Generated memory-object recall catalog used to verify receipt adoption.",
    )
    parser.add_argument(
        "--runtime-targets-path",
        default=str(RUNTIME_WRITEBACK_TARGETS_PATH),
        help="Generated runtime writeback targets used to verify reviewed-candidate receipts.",
    )
    parser.add_argument(
        "--growth-lanes-path",
        default=str(GROWTH_REFINERY_LANES_PATH),
        help="Generated growth-refinery writeback lanes used to verify support-memory receipts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and report append/duplicate counts without mutating the live receipt log.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_paths = [Path(path).expanduser().resolve() for path in args.input]
    if not input_paths:
        raise SystemExit("no receipt input files were provided")
    log_path = Path(args.log_path).expanduser().resolve()
    catalog_path = Path(args.catalog_path).expanduser().resolve()
    runtime_targets_path = Path(args.runtime_targets_path).expanduser().resolve()
    growth_lanes_path = Path(args.growth_lanes_path).expanduser().resolve()
    memory_objects_by_id = load_memory_object_catalog(catalog_path)
    runtime_targets_by_surface = load_runtime_writeback_targets(runtime_targets_path)
    growth_lanes_by_ref = load_growth_refinery_writeback_lanes(growth_lanes_path)
    receipts = load_receipts(
        input_paths,
        memory_objects_by_id=memory_objects_by_id,
        runtime_targets_by_surface=runtime_targets_by_surface,
        growth_lanes_by_ref=growth_lanes_by_ref,
    )
    if args.dry_run:
        appended, skipped = count_new_receipts(log_path=log_path, receipts=receipts)
        print(f"[dry-run] would append {appended} memo receipts to {log_path}")
        print(f"[dry-run] duplicate event ids skipped: {skipped}")
        return 0
    appended, skipped = append_new_receipts(log_path=log_path, receipts=receipts)
    print(f"[ok] appended {appended} memo receipts to {log_path}")
    print(f"[skip] duplicate event ids skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
