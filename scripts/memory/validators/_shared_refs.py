from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

from ._shared_paths import ROOT
from ._shared_schema_constants import MARKDOWN_HEADING, SYMBOLIC_REF, WINDOWS_ABSOLUTE_PATH

def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")

@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors

def local_ref_error(ref_value: object, label: str) -> str | None:
    if not isinstance(ref_value, str) or not ref_value:
        return None
    if ref_value.startswith(("http://", "https://", "repo:")):
        return None
    if SYMBOLIC_REF.match(ref_value) and not WINDOWS_ABSOLUTE_PATH.match(ref_value):
        return None

    path_text, _, anchor = ref_value.partition("#")
    target = ROOT / path_text

    if not target.exists():
        return f"{label}: referenced path does not exist: {ref_value}"
    if anchor and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
        return f"{label}: referenced markdown anchor does not exist: {ref_value}"
    return None

def append_ref_errors(errors: list[str], ref_checks: list[tuple[str, object]]) -> None:
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))


LINEAGE_REF_CHAIN = ("cluster_ref", "candidate_ref", "source_ref", "object_ref")


def append_lineage_chain_errors(errors: list[str], lineage_refs: object) -> None:
    if not isinstance(lineage_refs, dict):
        return

    for index, field_name in enumerate(LINEAGE_REF_CHAIN):
        value = lineage_refs.get(field_name)
        if value is None:
            continue
        for required_name in LINEAGE_REF_CHAIN[:index]:
            if lineage_refs.get(required_name) is None:
                errors.append(
                    f"lineage_refs.{field_name} requires lineage_refs.{required_name} when later chain links are present"
                )
                break
