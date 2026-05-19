# Retention Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Cross-repo and governance retention | [CROSS_REPO_RETENTION_MEMORY](./docs/CROSS_REPO_RETENTION_MEMORY.md), [GOVERNANCE_RETENTION_CHECKS](./docs/GOVERNANCE_RETENTION_CHECKS.md) | keeps retention review owner-routed |
| Office markers | [FIRST_OFFICE_RETENTION_MARKERS](./docs/FIRST_OFFICE_RETENTION_MARKERS.md), [MULTI_OFFICE_RETENTION_MARKERS](./docs/MULTI_OFFICE_RETENTION_MARKERS.md) | keeps office retention markers public-safe |
| Post-release retention | [POST_RELEASE_RETENTION_WATCH](./docs/POST_RELEASE_RETENTION_WATCH.md), [POST_RELEASE_RETENTION_OUTCOME](./docs/POST_RELEASE_RETENTION_OUTCOME.md) | keeps post-release retention visible without execution claims |

## Mechanic-Local Technical Contracts

Retention schemas, examples, and regression tests live with this package
because they define retention review posture without claiming runtime
execution.

| Contract | Artifact Surface |
|---|---|
| Cross-repo retention result | `mechanics/retention/schemas/cross_repo_retention_result_v1.json`, `mechanics/retention/examples/cross_repo_retention_result.example.json` |
| First office retention marker | `mechanics/retention/schemas/first_office_retention_marker_v1.json`, `mechanics/retention/examples/first_office_retention_marker_v1.example.json` |
| Governance retention check | `mechanics/retention/schemas/governance_retention_check_v1.json`, `mechanics/retention/examples/governance_retention_check.example.json` |
| Office retention marker | `mechanics/retention/schemas/office_retention_marker_v1.json`, `mechanics/retention/examples/office_retention_marker_v1.example.json` |
| Post-release retention memory | `mechanics/retention/schemas/post_release_retention_memory_v1.json`, `mechanics/retention/examples/post_release_retention_memory.example.json` |
| Post-release retention watch | `mechanics/retention/schemas/post_release_retention_watch_v1.json`, `mechanics/retention/examples/post_release_retention_watch.example.json` |
| Retention regression boundary | `mechanics/retention/tests/test_retention_mechanic.py` |

## Interface

Inputs are public-safe retention signals and owner confirmations. Outputs are
bounded memo docs and owner handoff routes.
