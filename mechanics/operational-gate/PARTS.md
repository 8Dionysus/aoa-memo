# Operational Gate Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Deployment incident gate | [DEPLOYMENT_INCIDENT_MEMORY_GATE](./docs/DEPLOYMENT_INCIDENT_MEMORY_GATE.md) | admits deployment incident memory only with evidence, owner route, review posture, and future effect |
| Office incident gate | [OFFICE_INCIDENT_MEMORY_GATE](./docs/OFFICE_INCIDENT_MEMORY_GATE.md) | keeps office/service incident memory governed by upstream office law and local memo admission |
| Service revision ledger | [SERVICE_REVISION_LEDGER](./docs/SERVICE_REVISION_LEDGER.md) | preserves service revision recall without becoming live service state or release approval |
| Post-release boundaries | [POST_RELEASE_MEMORY_BOUNDARIES](./docs/POST_RELEASE_MEMORY_BOUNDARIES.md) | names what post-release material memo may preserve and what stays with release/runtime owners |

## Part-Local Artifacts

Operational-gate schemas, examples, and regressions live with the nearest
functioning part. Writeback revision artifacts stay in the writeback package.

| Part | Artifact Homes |
|---|---|
| Deployment incident gate | `parts/deployment-incident-gate/schemas/`, `parts/deployment-incident-gate/examples/`, `parts/deployment-incident-gate/tests/` |
| Office incident gate | `parts/office-incident-gate/schemas/`, `parts/office-incident-gate/examples/` |
| Service revision ledger | `parts/service-revision-ledger/schemas/`, `parts/service-revision-ledger/examples/` |
| Post-release boundaries | `parts/post-release-boundaries/schemas/`, `parts/post-release-boundaries/examples/`, `parts/post-release-boundaries/tests/` |

### Part Artifact Contracts

Deployment incident gate:

- `mechanics/operational-gate/parts/deployment-incident-gate/schemas/deployment_incident_memory_gate_v1.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/examples/deployment_incident_memory_gate.example.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/schemas/deployment_lesson_candidate_v1.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/examples/deployment_lesson_candidate.example.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/tests/test_operational_gate_mechanic.py`

Office incident gate:

- `mechanics/operational-gate/parts/office-incident-gate/schemas/service_incident_memory_entry_v1.json`
- `mechanics/operational-gate/parts/office-incident-gate/examples/service_incident_memory_entry_v1.example.json`

Service revision ledger:

- `mechanics/operational-gate/parts/service-revision-ledger/schemas/service_revision_ledger_entry_v1.json`
- `mechanics/operational-gate/parts/service-revision-ledger/examples/service_revision_ledger_entry_v1.example.json`

Post-release boundaries:

- `mechanics/operational-gate/parts/post-release-boundaries/schemas/train_release_memory_entry_v1.json`
- `mechanics/operational-gate/parts/post-release-boundaries/examples/train_release_memory_entry_v1.example.json`
- `mechanics/operational-gate/parts/post-release-boundaries/tests/test_post_release_boundary_contracts.py`

## Neighbor Technical Contracts

| Neighbor Contract | Artifact Surface |
|---|---|
| Release revision ledger entry | `mechanics/writeback/parts/revision-ledgers/schemas/release_revision_ledger_entry_v1.json`, `mechanics/writeback/parts/revision-ledgers/examples/release_revision_ledger_entry_v1.example.json` |

## Interface

Inputs are operational event candidates, evidence refs, owner route refs,
verdict or review refs, retention posture, expiry/recheck posture, recurrence
signals, and proposed future effects.

Outputs are bounded memory admission decisions, service revision recall
records, post-release memory boundaries, and owner-routed next claims. Stronger
owners decide release quality, runtime remediation, proof, role rights,
dispatch, stats, and source meaning.
