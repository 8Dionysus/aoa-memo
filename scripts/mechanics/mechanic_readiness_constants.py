from __future__ import annotations

from mechanic_artifact_inventory_common import ARTIFACT_DIRS
from memo_mechanics_common import PACKAGE_REQUIRED_FILES, README_HEADINGS, REPO_ROOT


GENERATED_PATH = REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_readiness.min.json"
SCHEMA_VERSION = "aoa_memo_mechanic_readiness_v1"
SOURCE_OF_TRUTH = "mechanics/README.md"
CONFIG_REF = "config/mechanics/memo_mechanics.json"
MECHANIC_INDEX_REF = "generated/mechanics/memo_mechanics.min.json"
ARTIFACT_INVENTORY_REF = "generated/mechanics/mechanic_artifacts.min.json"
CARD_INDEX_REF = "generated/mechanics/memo_mechanic_cards.min.json"
OWNER_ROUTE_INDEX_REF = "generated/mechanics/memo_mechanic_owner_routes.min.json"
LANDING_LOG_INDEX_REF = "generated/mechanics/memo_mechanic_landing_logs.min.json"
GENERATED_BY = "scripts/mechanics/build_memo_mechanic_readiness.py"

PACKAGE_SURFACES = tuple(PACKAGE_REQUIRED_FILES)
READINESS_CHECKS = (
    "package-surfaces",
    "readme-card",
    "docs-index",
    "parts-interface",
    "owner-map",
    "legacy-bridge",
    "provenance",
    "landing-log",
    "validation-route",
    "artifact-test-coverage",
    "local-test-route",
    "stronger-owner-stop-lines",
)
NON_TEST_ARTIFACT_DIRS = tuple(district for district in ARTIFACT_DIRS if district != "tests")
CORE_OWNER_REFS = ("aoa-memo", "aoa-evals", "abyss-stack")
KNOWN_STRONGER_OWNER_REFS = (
    "Agents-of-Abyss",
    "Tree-of-Sophia",
    "aoa-agents",
    "aoa-evals",
    "aoa-kag",
    "aoa-playbooks",
    "aoa-routing",
    "aoa-stats",
    "abyss-stack",
    "source owner",
)
REQUIRED_VALIDATION_REFS = (
    "python scripts/release/release_check.py",
)
SUPPORTING_VALIDATION_REFS = (
    "python scripts/mechanics/validate_memo_mechanics.py",
    "python scripts/mechanics/build_memo_mechanics_index.py --check",
    "python scripts/mechanics/validate_memo_mechanics_index.py",
    "python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py",
    "python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check",
    "python scripts/memory/validate_memo.py",
)
