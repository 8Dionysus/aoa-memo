from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "memo_mechanics.json"
GENERATED_PATH = REPO_ROOT / "generated" / "memo_mechanics.min.json"

PACKAGE_REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "DIRECTION.md",
    "PARTS.md",
    "OWNER_MAP.md",
    "PROVENANCE.md",
    "LANDING_LOG.md",
    "ROADMAP.md",
    "docs/AGENTS.md",
    "legacy/AGENTS.md",
    "legacy/README.md",
    "legacy/INDEX.md",
)

README_HEADINGS = (
    "## Mechanic card",
    "### Trigger",
    "### Memo owns",
    "### Stronger owner split",
    "### Inputs",
    "### Outputs",
    "### Must not claim",
    "### Validation",
    "### Next route",
)


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def build_index() -> dict[str, Any]:
    config = load_config()
    packages = []
    for package in config["packages"]:
        slug = package["slug"]
        docs = sorted(package["docs"])
        packages.append(
            {
                "slug": slug,
                "title": package["title"],
                "status": package["status"],
                "path": f"mechanics/{slug}/README.md",
                "docs_path": f"mechanics/{slug}/docs",
                "legacy_path": f"mechanics/{slug}/legacy/INDEX.md",
                "doc_count": len(docs),
                "docs": [f"mechanics/{slug}/docs/{doc}" for doc in docs],
            }
        )

    return {
        "schema_version": "aoa_memo_mechanics_index_v1",
        "source_of_truth": config["source_of_truth"],
        "config_ref": "config/memo_mechanics.json",
        "authority_ref": config["authority_ref"],
        "counts": {
            "packages": len(packages),
            "docs": sum(package["doc_count"] for package in packages),
        },
        "packages": packages,
    }
