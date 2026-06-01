from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: PyYAML. Install it with: pip install PyYAML")
    raise SystemExit(2) from exc

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def load_yaml(path: Path) -> object:
    return yaml.safe_load(load_text(path))

def format_schema_path(path_parts: list[object]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)
