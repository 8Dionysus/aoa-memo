from __future__ import annotations

from pathlib import Path

import yaml

from decision_index_constants import (
    DECISIONS_DIR,
    FULL_ID_FILENAME_RE,
    GENERATED_INDEX_PATHS,
    INDEX_CONTRACT_PATH,
)
from decision_index_records import collect_decision_records
from decision_index_render import render_index_files


def load_index_contract(repo_root: Path) -> tuple[dict[str, object] | None, list[tuple[str, str]]]:
    path = repo_root / INDEX_CONTRACT_PATH
    if not path.is_file():
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract is missing")]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract must be a mapping")]
    return payload, []


def validate_decision_lane_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    decisions_root = repo_root / DECISIONS_DIR
    if not decisions_root.is_dir():
        return [(DECISIONS_DIR.as_posix(), "decision directory is missing")]

    allowed_paths = {
        (DECISIONS_DIR / "AGENTS.md").as_posix(),
        (DECISIONS_DIR / "README.md").as_posix(),
        (DECISIONS_DIR / "TEMPLATE.md").as_posix(),
        INDEX_CONTRACT_PATH.as_posix(),
        *(path.as_posix() for path in GENERATED_INDEX_PATHS),
    }
    issues: list[tuple[str, str]] = []
    for path in sorted(decisions_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(repo_root)
        relative_text = relative.as_posix()
        if relative_text in allowed_paths:
            continue
        decision_relative = path.relative_to(decisions_root)
        if len(decision_relative.parts) == 1 and FULL_ID_FILENAME_RE.match(path.name):
            continue
        issues.append(
            (
                relative_text,
                "unmodeled decision-lane surface; add it to the local decision surface contract or move it outside docs/decisions",
            )
        )
    return issues


def validate_decision_index_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    records, issues = collect_decision_records(repo_root)
    issues.extend(validate_decision_lane_surfaces(repo_root))
    contract, contract_issues = load_index_contract(repo_root)
    issues.extend(contract_issues)
    if contract is not None:
        expected = [path.as_posix() for path in GENERATED_INDEX_PATHS]
        if contract.get("generated_indexes") != expected:
            issues.append(
                (
                    INDEX_CONTRACT_PATH.as_posix(),
                    "generated_indexes must match the decision index read-model set",
                )
            )
        fields = contract.get("fields")
        if not isinstance(fields, dict) or "decision_id" not in fields:
            issues.append((INDEX_CONTRACT_PATH.as_posix(), "fields must name decision_id"))
        path_policy = contract.get("path_policy")
        if (
            isinstance(path_policy, dict)
            and path_policy.get("path_mode") == "full_canonical_id_filename"
        ):
            for record in records:
                filename_match = FULL_ID_FILENAME_RE.match(record.path.name)
                if not filename_match or filename_match.group(1) != record.decision_id:
                    issues.append(
                        (
                            record.repo_path,
                            "decision path must use the full canonical ID filename format",
                        )
                    )
    if issues:
        return issues

    rendered = render_index_files(records)
    for relative_path, expected_text in rendered.items():
        path = repo_root / relative_path
        if not path.is_file():
            issues.append((relative_path.as_posix(), "generated decision index is missing"))
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            issues.append(
                (
                    relative_path.as_posix(),
                    "generated decision index is stale; run python scripts/root-topology/build_decision_indexes.py",
                )
            )
    return issues
