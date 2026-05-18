# Recurrence Support Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Recurrence support surfaces | [RECURRENCE_MEMORY_SUPPORT_SURFACES](./docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md) | preserves checkpoint continuity, relaunch anchors, return packs, and anti-`return_memory` stop-lines |
| Witness trace contract | [WITNESS_TRACE_CONTRACT](./docs/WITNESS_TRACE_CONTRACT.md) | keeps witness trace exports reviewable and maps later writeback into existing memo object kinds |
| Reviewed closeout recall landing | [REVIEWED_CLOSEOUT_RECALL_LANDING](./docs/REVIEWED_CLOSEOUT_RECALL_LANDING.md) | preserves owner-local recall survivors without becoming proof, playbook authority, or a second route ledger |

## Root Technical Contracts

The current schemas, examples, manifests, quests, and generated companions
remain in root technical districts because they are public memory/support
contracts, not package-local implementation files:

| Contract | Root Surface |
|---|---|
| Inquiry checkpoint | `schemas/inquiry_checkpoint.schema.json`, `examples/inquiry_checkpoint.example.json`, `examples/inquiry_checkpoint.return.example.json` |
| Checkpoint to memory contract | `schemas/checkpoint-to-memory-contract.schema.json`, `examples/checkpoint_to_memory_contract.example.json` |
| Witness trace | `schemas/witness-trace.schema.json`, `examples/witness_trace.example.json` |
| Working return recall | `examples/recall_contract.object.working.return.json`, `examples/recall_contract.object.working.phase-alpha.json` |
| Reviewed closeout quest | `quests/AOA-MEM-Q-0009.yaml`, `generated/quest_catalog.min.json`, `generated/quest_catalog.min.example.json` |

## Interface

Inputs are checkpoint refs, working recall contracts, return packs, witness
trace exports, closeout reviewed evidence refs, owner-local recall candidates,
and memory delta refs.

Outputs are bounded relaunch support notes, existing-object writeback mappings,
reviewed closeout recall landings, and owner-routed next claims. Stronger
owners decide recurrence doctrine, route dispatch, runtime retry, actor rights,
scenario choreography, proof, and source acceptance.
