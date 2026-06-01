#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from memory_operational_access import build_access_plane_currentness
from memory_operational_readout_common import (
    ACCESS_OUTPUT,
    OUTPUT_DIR,
    PORT_STATUS_OUTPUT,
    REPO_ROOT,
    SOURCE_WAVE_OUTPUT,
    load_json,
    render_json,
    validate_readout,
)
from memory_operational_source_wave import build_source_intake_wave
from memory_operational_workspace import build_workspace_port_status


def build_all(*, live: bool) -> dict[Path, dict[str, Any] | None]:
    return {
        ACCESS_OUTPUT: build_access_plane_currentness(live=live),
        SOURCE_WAVE_OUTPUT: build_source_intake_wave(),
        PORT_STATUS_OUTPUT: build_workspace_port_status(),
    }


def write_outputs(outputs: dict[Path, dict[str, Any] | None]) -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    missing = [path for path, payload in outputs.items() if payload is None]
    if missing:
        for path in missing:
            print(f"[error] cannot build {path.relative_to(REPO_ROOT)}; source input is missing", file=sys.stderr)
        return 1
    for path, payload in outputs.items():
        assert payload is not None
        path.write_text(render_json(payload), encoding="utf-8")
        print(f"[ok] wrote {path.relative_to(REPO_ROOT)}")
    return 0


def check_outputs(outputs: dict[Path, dict[str, Any] | None], *, live: bool) -> int:
    errors: list[str] = []
    for path in (ACCESS_OUTPUT, SOURCE_WAVE_OUTPUT, PORT_STATUS_OUTPUT):
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT)} is missing")
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(REPO_ROOT)} is invalid JSON: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{path.relative_to(REPO_ROOT)} must be a JSON object")
            continue
        errors.extend(validate_readout(path, payload))
        expected = outputs.get(path)
        if expected is not None:
            if path == ACCESS_OUTPUT and not live:
                continue
            if render_json(payload) != render_json(expected):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)} is stale; run "
                    "scripts/memory/build_memory_operational_readouts.py --write"
                    + (" --live" if live else "")
                )
    if errors:
        print("Memory operational readout validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    skipped = []
    if outputs.get(PORT_STATUS_OUTPUT) is None:
        skipped.append("workspace port status rebuild skipped because 8Dionysus workspace map was unavailable")
    if not live:
        skipped.append("live MCP currentness comparison skipped; use --check --live in a workspace")
    for item in skipped:
        print(f"[note] {item}")
    print("[ok] memory operational readouts are valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build aoa-memo operational readouts.")
    parser.add_argument("--write", action="store_true", help="write generated readout files")
    parser.add_argument("--check", action="store_true", help="validate generated readout files")
    parser.add_argument("--live", action="store_true", help="run live aoa_memo MCP probes")
    args = parser.parse_args()
    if args.write and args.check:
        parser.error("--write and --check are mutually exclusive")
    if not args.write and not args.check:
        parser.error("choose --write or --check")

    outputs = build_all(live=args.live)
    if args.write:
        return write_outputs(outputs)
    return check_outputs(outputs, live=args.live)


if __name__ == "__main__":
    raise SystemExit(main())
