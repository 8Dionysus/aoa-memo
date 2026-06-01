#!/usr/bin/env python3
"""Compatibility CLI for layer-owned memo validators."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import types

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validators import (  # noqa: E402
    _shared,
    eval_boundary,
    handoff_boundary,
    memory_context,
    profiles,
    questbook,
    runtime_boundary,
    runtime_receipts,
    runtime_writeback,
    schema,
)

_PROFILE_MODULES = (
    _shared,
    schema,
    questbook,
    memory_context,
    runtime_writeback,
    runtime_receipts,
    runtime_boundary,
    handoff_boundary,
    eval_boundary,
)


def _export_public_names() -> None:
    for module in _PROFILE_MODULES:
        for name in dir(module):
            if name.startswith("__"):
                continue
            globals().setdefault(name, getattr(module, name))
    globals()["PROFILE_NAMES"] = profiles.PROFILE_NAMES
    globals()["run_profile"] = profiles.run_profile


_export_public_names()


class _CompatibilityModule(types.ModuleType):
    """Propagate old validate_memo monkeypatches into split validator modules."""

    def __setattr__(self, name: str, value: object) -> None:
        super().__setattr__(name, value)
        for module in _PROFILE_MODULES:
            if hasattr(module, name):
                setattr(module, name, value)


sys.modules[__name__].__class__ = _CompatibilityModule


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate aoa-memo memory contracts.")
    parser.add_argument(
        "--profile",
        choices=profiles.PROFILE_NAMES,
        default="all",
        help="Run one boundary profile instead of the historical broad gate.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    profiles.run_profile(args.profile)
    print(f"\nValidation profile {args.profile!r} completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
