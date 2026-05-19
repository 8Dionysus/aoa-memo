from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
AGON_PARTS = ROOT / "mechanics" / "agon" / "parts"
OLD_PACKAGE_ARTIFACT_PATHS = (
    "mechanics/agon/config/",
    "mechanics/agon/examples/",
    "mechanics/agon/generated/",
    "mechanics/agon/manifests/",
    "mechanics/agon/schemas/",
    "mechanics/agon/scripts/",
    "mechanics/agon/tests/",
)


def _walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)


def _path_refs(value: str) -> list[str]:
    refs: list[str] = []
    if value.startswith("mechanics/"):
        refs.append(value)
    elif value.startswith("python mechanics/"):
        refs.append(value.split(" ", 1)[1])
    return refs


def test_agon_part_manifests_route_to_existing_part_or_doc_surfaces() -> None:
    manifest_files = sorted((AGON_PARTS).glob("*/manifests/**/*.json"))
    assert manifest_files

    for manifest_path in manifest_files:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        strings = list(_walk_strings(payload))
        for old_prefix in OLD_PACKAGE_ARTIFACT_PATHS:
            assert all(old_prefix not in item for item in strings), manifest_path
        for item in strings:
            for ref in _path_refs(item):
                if "*" in ref:
                    assert list(ROOT.glob(ref)), f"{manifest_path}: unresolved glob {ref}"
                else:
                    assert (ROOT / ref).exists(), f"{manifest_path}: missing ref {ref}"
