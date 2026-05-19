# Recurrence Support Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Recurrence support surfaces | [RECURRENCE_MEMORY_SUPPORT_SURFACES](./docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md) | preserves checkpoint continuity, relaunch anchors, return packs, and anti-`return_memory` stop-lines |
| Witness trace contract | [WITNESS_TRACE_CONTRACT](./docs/WITNESS_TRACE_CONTRACT.md) | keeps witness trace exports reviewable and maps later writeback into existing memo object kinds |
| Reviewed closeout recall landing | [REVIEWED_CLOSEOUT_RECALL_LANDING](./docs/REVIEWED_CLOSEOUT_RECALL_LANDING.md) | preserves owner-local recall survivors without becoming proof, playbook authority, or a second route ledger |

## Mechanic-Local Technical Contracts

Witness trace schemas and examples live with this package because they define
route-return support. Checkpoint schemas and examples live with
`mechanics/checkpoint/` because checkpoint is the artifact owner. Shared recall
contracts and reviewed closeout quest surfaces remain root-owned only when
they serve more than this one mechanic:

| Contract | Artifact Surface |
|---|---|
| Checkpoint artifact consumer refs | `mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json`, `mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.example.json`, `mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.return.example.json` |
| Checkpoint to memory consumer refs | `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json`, `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json` |
| Witness trace | `mechanics/recurrence-support/schemas/witness-trace.schema.json`, `mechanics/recurrence-support/examples/witness_trace.example.json` |
| Working return recall | `examples/recall_contract.object.working.return.json`, `examples/recall_contract.object.working.phase-alpha.json` |
| Witness trace quest closeout | `quests/memo/done/AOA-MEM-Q-0002.yaml`, `generated/quest_catalog.min.json`, `generated/quest_catalog.min.example.json` |
| Reviewed closeout quest | `quests/memo/reanchor/AOA-MEM-Q-0009.yaml`, `generated/quest_catalog.min.json`, `generated/quest_catalog.min.example.json` |

## Interface

Inputs are checkpoint refs, working recall contracts, return packs, witness
trace exports, closeout reviewed evidence refs, owner-local recall candidates,
and memory delta refs.

Outputs are bounded relaunch support notes, existing-object writeback mappings,
reviewed closeout recall landings, and owner-routed next claims. Stronger
owners decide recurrence doctrine, route dispatch, runtime retry, actor rights,
scenario choreography, proof, and source acceptance.
