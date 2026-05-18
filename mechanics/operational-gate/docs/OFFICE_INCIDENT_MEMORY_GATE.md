# Office Incident Memory Gate

This v1.1 surface belongs to the **AoA Experience Live Office Expansion and Multi-Release Train**.

## Purpose

Owner-local v1.1 surface for `aoa-memo`: office incident memory gate.

It decides whether an office or service incident becomes memo recall. It does
not approve office activation, grant assistant rights, prove service quality,
or write runtime state.

## Authority Source

Live office expansion law lives in [Agents-of-Abyss](https://github.com/8Dionysus/Agents-of-Abyss/blob/main/docs/EXPERIENCE_WAVE5_SOVEREIGN_OFFICE.md). The runtime write stop-line for Tree-of-Sophia lives in [Tree-of-Sophia](https://github.com/8Dionysus/Tree-of-Sophia/blob/main/docs/NO_RUNTIME_OFFICE_WRITE.md). This `aoa-memo` surface only defines owner-local contract behavior and consumes those upstream gates; it does not become release approval, assistant self-authority, or runtime ToS write authority.

## Shape

`notary.assistant` remains the first receipt-bearing anchor. `concierge.assistant`, `courier.assistant`, and `monitor.assistant` join through a governed train with compatibility checks, handoff graph, smoke gates, rollback, replay audit, and operator go/no-go.

## Admission Rule

An office incident may become memory only when it has:

- a stable office, service, train, or incident ref
- evidence refs to the receipt, train, smoke, replay, rollback, or owner
  review surface
- an owner route for the next stronger decision
- a review posture that explains whether the memory is allowed, rejected,
  retained for watch, or routed away
- a future effect such as a compatibility sentinel, release-train checklist
  item, retention watch, or writeback candidate

## Mechanic-Local Technical Contracts

Current public contracts live with the operational-gate mechanic:

- `mechanics/operational-gate/schemas/service_incident_memory_entry_v1.json`
- `mechanics/operational-gate/examples/service_incident_memory_entry_v1.example.json`
- `mechanics/operational-gate/schemas/train_release_memory_entry_v1.json`
- `mechanics/operational-gate/examples/train_release_memory_entry_v1.example.json`

The contracts are memo recall shapes. They are not live office state and do
not grant assistant rights.

## Stop-Line

Office incident memory cannot certify activation, prove smoke success, approve
rollback, or authorize ToS writes. Those decisions stay with the stronger
owners named in the mechanic owner map.
