#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from local_memo_port_common import (
    INDEX_FILENAME,
    INDEX_MARKDOWN,
    build_index,
    render_json,
    render_markdown,
    resolve_port_path,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local memo port index.")
    parser.add_argument("--path", required=True, help="Path to a local memo port.")
    parser.add_argument("--check", action="store_true", help="Check generated files without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    port_path = resolve_port_path(args.path)
    index = build_index(port_path)
    json_text = render_json(index)
    markdown_text = render_markdown(index)
    json_path = port_path / INDEX_FILENAME
    markdown_path = port_path / INDEX_MARKDOWN

    if args.check:
        errors: list[str] = []
        if not json_path.exists():
            errors.append(f"{json_path} is missing")
        elif json_path.read_text(encoding="utf-8") != json_text:
            errors.append(f"{json_path} is not up to date")
        if not markdown_path.exists():
            errors.append(f"{markdown_path} is missing")
        elif markdown_path.read_text(encoding="utf-8") != markdown_text:
            errors.append(f"{markdown_path} is not up to date")
        if errors:
            print("Local memo port index check failed.", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"[ok] local memo port index is up to date: {port_path}")
        return 0

    json_path.write_text(json_text, encoding="utf-8")
    markdown_path.write_text(markdown_text, encoding="utf-8")
    print(f"[ok] wrote {json_path}")
    print(f"[ok] wrote {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

