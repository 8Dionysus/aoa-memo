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
    "aoa-sdk",
    "aoa-stats",
    "abyss-stack",
    "source owner",
)
VALIDATION_ROUTE_CONTRACT = (
    "at least one explicit repository-local VALIDATION.md owner link"
)
