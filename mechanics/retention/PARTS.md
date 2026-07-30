# Retention Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Consolidation and forgetting | [CONSOLIDATION_FORGETTING_OPERATION](./docs/CONSOLIDATION_FORGETTING_OPERATION.md) | keeps demotion, deduplication, supersession, retraction, archive, and freeze as explicit reviewed memory operations |
| Cross-repo and governance retention | [CROSS_REPO_RETENTION_MEMORY](./docs/CROSS_REPO_RETENTION_MEMORY.md), [GOVERNANCE_RETENTION_CHECKS](./docs/GOVERNANCE_RETENTION_CHECKS.md) | keeps retention review owner-routed |
| Office markers | [FIRST_OFFICE_RETENTION_MARKERS](./docs/FIRST_OFFICE_RETENTION_MARKERS.md), [MULTI_OFFICE_RETENTION_MARKERS](./docs/MULTI_OFFICE_RETENTION_MARKERS.md) | keeps office retention markers public-safe |
| Post-release retention | [POST_RELEASE_RETENTION_WATCH](./docs/POST_RELEASE_RETENTION_WATCH.md), [POST_RELEASE_RETENTION_OUTCOME](./docs/POST_RELEASE_RETENTION_OUTCOME.md) | keeps post-release retention visible without execution claims |

## Part-Local Technical Contracts

Retention schemas, examples, and regression tests live with the part that owns
their retention pressure because they define retention review posture without
claiming runtime execution.

| Part | Contract | Artifact Surface |
|---|---|---|
| Consolidation and forgetting | Memory consolidation/forgetting operation | `mechanics/retention/parts/consolidation-and-forgetting/schemas/memory_consolidation_forgetting_operation_v1.json`, `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.supersede.example.json`, `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.archive.example.json` |
| Consolidation and forgetting | C06-compatible mechanical lifecycle plan, semantic proposal, and reference receipt | `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_mechanical_lifecycle_plan_v0.schema.json`, `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_semantic_lifecycle_proposal_v0.schema.json`, `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_lifecycle_execution_receipt_v0.schema.json`, `mechanics/retention/parts/consolidation-and-forgetting/scripts/active_organ_lifecycle.py` |
| Consolidation and forgetting | C14-C17 distributed-erasure closure, content-minimized recovery probe, and memo-owned ER0/ER9 owner extension | `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_erasure_recovery_probe_v0.schema.json`, `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_memo_erasure_owner_extension_v0.schema.json`, `mechanics/retention/parts/consolidation-and-forgetting/scripts/distributed_erasure.py` |
| Consolidation and forgetting | Consolidation/forgetting tests | `mechanics/retention/parts/consolidation-and-forgetting/tests/test_consolidation_forgetting.py`, `mechanics/retention/parts/consolidation-and-forgetting/tests/test_active_organ_lifecycle.py`, `mechanics/retention/parts/consolidation-and-forgetting/tests/test_distributed_erasure.py` |
| Cross-repo and governance retention | Cross-repo retention result | `mechanics/retention/parts/cross-repo-and-governance-retention/schemas/cross_repo_retention_result_v1.json`, `mechanics/retention/parts/cross-repo-and-governance-retention/examples/cross_repo_retention_result.example.json` |
| Cross-repo and governance retention | Governance retention check | `mechanics/retention/parts/cross-repo-and-governance-retention/schemas/governance_retention_check_v1.json`, `mechanics/retention/parts/cross-repo-and-governance-retention/examples/governance_retention_check.example.json` |
| Cross-repo and governance retention | Cross-repo/governance tests | `mechanics/retention/parts/cross-repo-and-governance-retention/tests/test_cross_repo_governance_retention.py` |
| Office markers | First office retention marker | `mechanics/retention/parts/office-markers/schemas/first_office_retention_marker_v1.json`, `mechanics/retention/parts/office-markers/examples/first_office_retention_marker_v1.example.json` |
| Office markers | Office retention marker | `mechanics/retention/parts/office-markers/schemas/office_retention_marker_v1.json`, `mechanics/retention/parts/office-markers/examples/office_retention_marker_v1.example.json` |
| Office markers | Office marker tests | `mechanics/retention/parts/office-markers/tests/test_office_marker_contracts.py` |
| Post-release retention | Post-release retention memory | `mechanics/retention/parts/post-release-retention/schemas/post_release_retention_memory_v1.json`, `mechanics/retention/parts/post-release-retention/examples/post_release_retention_memory.example.json` |
| Post-release retention | Post-release retention watch | `mechanics/retention/parts/post-release-retention/schemas/post_release_retention_watch_v1.json`, `mechanics/retention/parts/post-release-retention/examples/post_release_retention_watch.example.json` |
| Post-release retention | Post-release retention tests | `mechanics/retention/parts/post-release-retention/tests/test_post_release_retention_contracts.py` |

## Interface

Inputs are public-safe retention signals, lifecycle triggers, target memory
ids, owner confirmations, and audit refs. Outputs are bounded memo docs,
reviewed lifecycle operations, generated read-model updates, and owner handoff
routes.
