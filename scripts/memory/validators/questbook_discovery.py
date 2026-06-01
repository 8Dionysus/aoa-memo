"""Quest source and projection checks for the memory-context profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def quest_sort_key(quest_id: str) -> tuple[int, str]:
    suffix = quest_id.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_id)
    except ValueError:
        return (sys.maxsize, quest_id)

def discover_questbook_file_paths() -> list[Path]:
    return sorted(
        (
            path
            for path in (ROOT / "quests" / "memo").glob("*/AOA-MEM-Q-*.yaml")
            if path.is_file()
        ),
        key=lambda path: (quest_sort_key(path.stem), path.as_posix()),
    )

def duplicate_questbook_file_issues(paths: list[Path] | None = None) -> list[str]:
    by_quest_id: dict[str, list[Path]] = {}
    for path in paths if paths is not None else discover_questbook_file_paths():
        by_quest_id.setdefault(path.stem, []).append(path)

    issues: list[str] = []
    for quest_id in sorted(by_quest_id, key=quest_sort_key):
        duplicates = by_quest_id[quest_id]
        if len(duplicates) < 2:
            continue
        locations = ", ".join(path.relative_to(ROOT).as_posix() for path in duplicates)
        issues.append(f"duplicate quest id {quest_id}: {locations}")
    return issues

def discover_questbook_files(paths: list[Path] | None = None) -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    for path in paths if paths is not None else discover_questbook_file_paths():
        discovered.setdefault(path.stem, path)
    if not discovered:
        return dict(FOUNDATION_QUESTBOOK_FILES)
    return {
        quest_id: discovered[quest_id]
        for quest_id in sorted(discovered, key=quest_sort_key)
    }

def quest_path_state(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT / "quests")
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) < 3:
        return None
    lane, state = parts[0], parts[1]
    if lane != "memo" or state not in QUEST_LIFECYCLE_STATES:
        return None
    return state

def quest_anchor_doc_ref(data: dict[str, object]) -> str | None:
    anchor_ref = data.get("anchor_ref")
    if isinstance(anchor_ref, str):
        return anchor_ref
    if isinstance(anchor_ref, dict):
        ref_value = anchor_ref.get("ref")
        if isinstance(ref_value, str):
            return ref_value
    return None
