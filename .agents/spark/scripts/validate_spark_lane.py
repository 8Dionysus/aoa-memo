#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spark_lane_registry import validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the aoa-memo Spark lane.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()

    problems = validate(root)
    if problems:
        print("Spark lane validation failed:")
        for problem in problems:
            print(f" - {problem}")
        return 1
    print("Spark lane validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
