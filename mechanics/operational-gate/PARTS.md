# Operational Gate Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Deployment incident gate | [DEPLOYMENT_INCIDENT_MEMORY_GATE](./docs/DEPLOYMENT_INCIDENT_MEMORY_GATE.md) | admits deployment incident memory only with evidence, owner route, review posture, and future effect |
| Office incident gate | [OFFICE_INCIDENT_MEMORY_GATE](./docs/OFFICE_INCIDENT_MEMORY_GATE.md) | keeps office/service incident memory governed by upstream office law and local memo admission |
| Service revision ledger | [SERVICE_REVISION_LEDGER](./docs/SERVICE_REVISION_LEDGER.md) | preserves service revision recall without becoming live service state or release approval |
| Post-release boundaries | [POST_RELEASE_MEMORY_BOUNDARIES](./docs/POST_RELEASE_MEMORY_BOUNDARIES.md) | names what post-release material memo may preserve and what stays with release/runtime owners |

## Mechanic-Local Technical Contracts

The operational-gate schemas and examples live with the package because they
define the admission mechanic's own contract surface. Writeback revision
artifacts stay in the writeback package.

| Contract | Artifact Surface |
|---|---|
| Deployment incident gate | `mechanics/operational-gate/schemas/deployment_incident_memory_gate_v1.json`, `mechanics/operational-gate/examples/deployment_incident_memory_gate.example.json` |
| Deployment lesson candidate | `mechanics/operational-gate/schemas/deployment_lesson_candidate_v1.json`, `mechanics/operational-gate/examples/deployment_lesson_candidate.example.json` |
| Service incident memory entry | `mechanics/operational-gate/schemas/service_incident_memory_entry_v1.json`, `mechanics/operational-gate/examples/service_incident_memory_entry_v1.example.json` |
| Service revision ledger entry | `mechanics/operational-gate/schemas/service_revision_ledger_entry_v1.json`, `mechanics/operational-gate/examples/service_revision_ledger_entry_v1.example.json` |
| Release revision ledger entry | `mechanics/writeback/schemas/release_revision_ledger_entry_v1.json`, `mechanics/writeback/examples/release_revision_ledger_entry_v1.example.json` |
| Train release memory entry | `mechanics/operational-gate/schemas/train_release_memory_entry_v1.json`, `mechanics/operational-gate/examples/train_release_memory_entry_v1.example.json` |

## Interface

Inputs are operational event candidates, evidence refs, owner route refs,
verdict or review refs, retention posture, expiry/recheck posture, recurrence
signals, and proposed future effects.

Outputs are bounded memory admission decisions, service revision recall
records, post-release memory boundaries, and owner-routed next claims. Stronger
owners decide release quality, runtime remediation, proof, role rights,
dispatch, stats, and source meaning.
