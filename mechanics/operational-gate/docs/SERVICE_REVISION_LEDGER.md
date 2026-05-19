# Service Revision Ledger

This v1.1 surface belongs to the **AoA Experience Live Office Expansion and Multi-Release Train**.

## Purpose

Owner-local v1.1 surface for `aoa-memo`: service revision ledger.

It preserves reviewable service revision recall. It does not become live
service state, release approval, runtime storage, or proof verdict logic.

## Authority Source

Live office expansion law lives in [Agents-of-Abyss](https://github.com/8Dionysus/Agents-of-Abyss/blob/main/docs/EXPERIENCE_WAVE5_SOVEREIGN_OFFICE.md). The runtime write stop-line for Tree-of-Sophia lives in [Tree-of-Sophia](https://github.com/8Dionysus/Tree-of-Sophia/blob/main/docs/NO_RUNTIME_OFFICE_WRITE.md). This `aoa-memo` surface only defines owner-local contract behavior and consumes those upstream gates; it does not become release approval, assistant self-authority, or runtime ToS write authority.

## Shape

`notary.assistant` remains the first receipt-bearing anchor. `concierge.assistant`, `courier.assistant`, and `monitor.assistant` join through a governed train with compatibility checks, handoff graph, smoke gates, rollback, replay audit, and operator go/no-go.

## Ledger Entry Rule

A service revision ledger entry may be durable memo when it names:

- the service or office ref
- the revision or train ref
- the entry type
- evidence refs for the reviewed change
- status posture such as draft, reviewed, retained, superseded, or rejected
- the owner route for activation, rollback, proof, or remediation

Memo records the revision as recallable context. It does not say the service
is running, healthy, deployed, or accepted.

## Mechanic-Local Technical Contracts

Current public contracts live with their owning mechanics:

- `mechanics/operational-gate/schemas/service_revision_ledger_entry_v1.json`
- `mechanics/operational-gate/examples/service_revision_ledger_entry_v1.example.json`
- `mechanics/writeback/parts/revision-ledgers/schemas/release_revision_ledger_entry_v1.json`
- `mechanics/writeback/parts/revision-ledgers/examples/release_revision_ledger_entry_v1.example.json`

The schemas and examples validate public-safe entry shape. They do not become
live ledgers.

## Next Route

Activation and release train decisions route to `Agents-of-Abyss` and the
release owner. Runtime state routes to `abyss-stack` or the runtime owner.
Proof routes to `aoa-evals`. Assistant rights route to `aoa-agents`.
