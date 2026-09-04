from __future__ import annotations

import json
from typing import Any

from mechanic_readiness_build import (
    _has_runnable_local_test_routes,
    _local_test_dirs,
    _validation_owner_refs,
    build_package_readiness,
    build_readiness,
)
from mechanic_readiness_constants import (
    ARTIFACT_INVENTORY_REF,
    CARD_INDEX_REF,
    CONFIG_REF,
    CORE_OWNER_REFS,
    GENERATED_BY,
    GENERATED_PATH,
    LANDING_LOG_INDEX_REF,
    MECHANIC_INDEX_REF,
    OWNER_ROUTE_INDEX_REF,
    PACKAGE_SURFACES,
    READINESS_CHECKS,
    SCHEMA_VERSION,
    SOURCE_OF_TRUTH,
    VALIDATION_ROUTE_CONTRACT,
)
from mechanic_readiness_validate import validate_payload


def render_readiness(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


__all__ = [
    "ARTIFACT_INVENTORY_REF",
    "CARD_INDEX_REF",
    "CONFIG_REF",
    "CORE_OWNER_REFS",
    "GENERATED_BY",
    "GENERATED_PATH",
    "LANDING_LOG_INDEX_REF",
    "MECHANIC_INDEX_REF",
    "OWNER_ROUTE_INDEX_REF",
    "PACKAGE_SURFACES",
    "READINESS_CHECKS",
    "SCHEMA_VERSION",
    "SOURCE_OF_TRUTH",
    "VALIDATION_ROUTE_CONTRACT",
    "_has_runnable_local_test_routes",
    "_local_test_dirs",
    "_validation_owner_refs",
    "build_package_readiness",
    "build_readiness",
    "render_readiness",
    "validate_payload",
]
