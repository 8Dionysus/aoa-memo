#!/usr/bin/env python3
"""Compatibility CLI for layer-owned memo validators."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
from pathlib import Path
import sys
import types

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATORS_DIR = SCRIPT_DIR / "validators"
VALIDATORS_PACKAGE_NAME = "_aoa_memo_memory_validators"


def _ensure_script_dir_importable() -> None:
    script_dir = str(SCRIPT_DIR)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)


def _load_validators_package() -> types.ModuleType:
    existing = sys.modules.get(VALIDATORS_PACKAGE_NAME)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(
        VALIDATORS_PACKAGE_NAME,
        VALIDATORS_DIR / "__init__.py",
        submodule_search_locations=[str(VALIDATORS_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load validator package from {VALIDATORS_DIR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[VALIDATORS_PACKAGE_NAME] = module
    spec.loader.exec_module(module)
    return module


_ensure_script_dir_importable()
_load_validators_package()
profile_modules = importlib.import_module(f"{VALIDATORS_PACKAGE_NAME}.profile_modules")
profiles = importlib.import_module(f"{VALIDATORS_PACKAGE_NAME}.profiles")

_PROFILE_MODULES = profile_modules.PROFILE_MODULES


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
