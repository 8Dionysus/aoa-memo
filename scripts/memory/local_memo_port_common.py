from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML. Install it with: pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[2]
VOCABULARY_PATH = ROOT / "config" / "memory-ports" / "indexing_vocabulary.json"
INDEX_FILENAME = "index.min.json"
INDEX_MARKDOWN = "INDEX.md"
PORT_FILENAME = "PORT.yaml"
PACKET_DIRS = ("candidates", "receipts", "exports", "local")
PACKET_SUFFIX = ".json"
INDEX_SCHEMA = "aoa_local_memo_port_index_v1"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def resolve_port_path(path: str | Path) -> Path:
    port_path = Path(path).expanduser()
    if not port_path.is_absolute():
        port_path = (Path.cwd() / port_path).resolve()
    else:
        port_path = port_path.resolve()
    return port_path


def repo_root_for_port(port_path: Path) -> Path:
    if port_path.name == "memo":
        return port_path.parent
    if port_path.is_relative_to(ROOT):
        return ROOT
    return port_path.parent


def relative_to_port(port_path: Path, path: Path) -> str:
    try:
        return path.relative_to(port_path).as_posix()
    except ValueError:
        return path.as_posix()


def packet_files(port_path: Path, directory: str) -> list[Path]:
    packet_dir = port_path / directory
    if not packet_dir.exists():
        return []
    return sorted(path for path in packet_dir.glob(f"*{PACKET_SUFFIX}") if path.is_file())


def all_packet_files(port_path: Path) -> list[Path]:
    files: list[Path] = []
    for directory in PACKET_DIRS:
        files.extend(packet_files(port_path, directory))
    return sorted(files)


def load_port(port_path: Path) -> dict[str, Any]:
    payload = load_yaml(port_path / PORT_FILENAME)
    if not isinstance(payload, dict):
        raise ValueError(f"{port_path / PORT_FILENAME} must be a YAML mapping")
    return payload


def load_vocabulary() -> dict[str, Any]:
    payload = load_json(VOCABULARY_PATH)
    if not isinstance(payload, dict):
        raise ValueError(f"{VOCABULARY_PATH} must be a JSON object")
    return payload


def vocabulary_terms(port_payload: dict[str, Any] | None = None) -> dict[str, set[str]]:
    payload = load_vocabulary()
    terms_payload = payload.get("terms")
    if not isinstance(terms_payload, dict):
        raise ValueError("memory-port vocabulary must expose terms")
    terms: dict[str, set[str]] = {}
    for key, values in terms_payload.items():
        if not isinstance(values, list):
            raise ValueError(f"memory-port vocabulary terms.{key} must be a list")
        terms[key] = {str(value) for value in values}

    if port_payload:
        local_terms = port_payload.get("local_terms") or {}
        if isinstance(local_terms, dict):
            for key, values in local_terms.items():
                if not isinstance(values, list):
                    continue
                terms.setdefault(str(key), set()).update(str(value) for value in values)
    return terms


def _latest_created_at(port_path: Path) -> str:
    timestamps: list[str] = []
    for path in all_packet_files(port_path):
        try:
            payload = load_json(path)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and isinstance(payload.get("created_at"), str):
            timestamps.append(payload["created_at"])
    return max(timestamps) if timestamps else "1970-01-01T00:00:00Z"


def build_index(port_path: str | Path) -> dict[str, Any]:
    port = resolve_port_path(port_path)
    port_payload = load_port(port)
    candidates = []
    by_kind: Counter[str] = Counter()
    by_family: Counter[str] = Counter()
    by_route: Counter[str] = Counter()
    open_items: list[dict[str, str]] = []

    for path in packet_files(port, str(port_payload.get("candidate_dir", "candidates"))):
        payload = load_json(path)
        if not isinstance(payload, dict):
            continue
        candidates.append(payload)
        for field, counter in (("kind", by_kind), ("family", by_family), ("route", by_route)):
            value = payload.get(field)
            if isinstance(value, str) and value:
                counter[value] += 1
        review_state = payload.get("review_state")
        if review_state not in {"rejected", "landed", "superseded", "archived"}:
            open_items.append(
                {
                    "id": str(payload.get("id") or payload.get("candidate_id") or path.stem),
                    "path": relative_to_port(port, path),
                    "review_state": str(review_state or "candidate"),
                    "route": str(payload.get("route") or payload.get("desired_route") or "reviewed_intake"),
                }
            )

    counts = {
        "candidates": len(packet_files(port, str(port_payload.get("candidate_dir", "candidates")))),
        "receipts": len(packet_files(port, str(port_payload.get("receipt_dir", "receipts")))),
        "exports": len(packet_files(port, str(port_payload.get("export_dir", "exports")))),
        "local": len(packet_files(port, str(port_payload.get("local_dir", "local")))),
    }
    source_refs = [PORT_FILENAME]
    source_refs.extend(relative_to_port(port, path) for path in all_packet_files(port))

    return {
        "schema": INDEX_SCHEMA,
        "repo": str(port_payload["repo"]),
        "port": port.name,
        "default_mode": str(port_payload["default_mode"]),
        "counts": counts,
        "by_kind": dict(sorted(by_kind.items())),
        "by_family": dict(sorted(by_family.items())),
        "by_route": dict(sorted(by_route.items())),
        "open_items": sorted(open_items, key=lambda item: item["path"]),
        "generated_at": _latest_created_at(port),
        "source_refs": source_refs,
    }


def render_markdown(index: dict[str, Any]) -> str:
    counts = index["counts"]
    lines = [
        f"# {index['repo']} memo port index",
        "",
        "Generated from `PORT.yaml` and local memo packets.",
        "",
        "## Counts",
        "",
        "| District | Count |",
        "|---|---:|",
        f"| candidates | {counts['candidates']} |",
        f"| receipts | {counts['receipts']} |",
        f"| exports | {counts['exports']} |",
        f"| local | {counts['local']} |",
        "",
        "## Routes",
        "",
    ]
    if index["by_route"]:
        lines.extend(["| Route | Count |", "|---|---:|"])
        for route, count in index["by_route"].items():
            lines.append(f"| `{route}` | {count} |")
    else:
        lines.append("No routed candidates yet.")
    lines.extend(["", "## Open Items", ""])
    if index["open_items"]:
        lines.extend(["| ID | State | Route | Path |", "|---|---|---|---|"])
        for item in index["open_items"]:
            lines.append(
                f"| `{item['id']}` | `{item['review_state']}` | `{item['route']}` | `{item['path']}` |"
            )
    else:
        lines.append("No open candidate items.")
    lines.extend(
        [
            "",
            "## Agent Route",
            "",
            "Executable validation and rebuild commands live in the nearest unambiguous `VALIDATION.md` after the port surface is known.",
            "This generated index is a read model; it does not own the operational route.",
            "",
        ]
    )
    return "\n".join(lines)
