# Retention Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Cross-repo and governance retention | [CROSS_REPO_RETENTION_MEMORY](./docs/CROSS_REPO_RETENTION_MEMORY.md), [GOVERNANCE_RETENTION_CHECKS](./docs/GOVERNANCE_RETENTION_CHECKS.md) | keeps retention review owner-routed |
| Office markers | [FIRST_OFFICE_RETENTION_MARKERS](./docs/FIRST_OFFICE_RETENTION_MARKERS.md), [MULTI_OFFICE_RETENTION_MARKERS](./docs/MULTI_OFFICE_RETENTION_MARKERS.md) | keeps office retention markers public-safe |
| Post-release retention | [POST_RELEASE_RETENTION_WATCH](./docs/POST_RELEASE_RETENTION_WATCH.md), [POST_RELEASE_RETENTION_OUTCOME](./docs/POST_RELEASE_RETENTION_OUTCOME.md) | keeps post-release retention visible without execution claims |

## Interface

Inputs are public-safe retention signals and owner confirmations. Outputs are
bounded memo docs and owner handoff routes.
