# Agon Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Prebinding and candidate intake | [AGON_MEMORY_PREBINDING](./docs/AGON_MEMORY_PREBINDING.md), [AGON_DELTA_CHRONICLE_PREBINDING_MODEL](./docs/AGON_DELTA_CHRONICLE_PREBINDING_MODEL.md), [AGON_SCAR_CANDIDATE_INTAKE_MODEL](./docs/AGON_SCAR_CANDIDATE_INTAKE_MODEL.md), [AGON_SCAR_REQUEST_INTAKE_ALIGNMENT](./docs/AGON_SCAR_REQUEST_INTAKE_ALIGNMENT.md), [AGON_RETENTION_CANDIDATE_BOUNDARY](./docs/AGON_RETENTION_CANDIDATE_BOUNDARY.md), [AGON_RETENTION_CANDIDATE_INTAKE](./docs/AGON_RETENTION_CANDIDATE_INTAKE.md), [AGON_MEMO_RECURRENCE_REVIEW_BOUNDARY](./docs/AGON_MEMO_RECURRENCE_REVIEW_BOUNDARY.md), [AGON_RANK_MEMORY_BOUNDARY](./docs/AGON_RANK_MEMORY_BOUNDARY.md) | keeps candidate memory explicit before any stronger Agon write |
| Bridge and evidence seams | [AGON_EPISTEMIC_MEMORY_BOUNDARY](./docs/AGON_EPISTEMIC_MEMORY_BOUNDARY.md), [AGON_EPISTEMIC_MEMORY_BRIDGE](./docs/AGON_EPISTEMIC_MEMORY_BRIDGE.md), [AGON_KAG_MEMO_BOUNDARY](./docs/AGON_KAG_MEMO_BOUNDARY.md), [AGON_KAG_MEMO_EVIDENCE_PACKAGES](./docs/AGON_KAG_MEMO_EVIDENCE_PACKAGES.md), [AGON_MECHANICAL_TRIAL_MEMO_INTAKES](./docs/AGON_MECHANICAL_TRIAL_MEMO_INTAKES.md), [AGON_RETENTION_MEMORY_BRIDGE](./docs/AGON_RETENTION_MEMORY_BRIDGE.md), [AGON_SLC_MEMORY_BOUNDARY](./docs/AGON_SLC_MEMORY_BOUNDARY.md), [AGON_SLC_MEMORY_BRIDGE](./docs/AGON_SLC_MEMORY_BRIDGE.md), [AGON_SOPHIAN_MEMO_EVIDENCE](./docs/AGON_SOPHIAN_MEMO_EVIDENCE.md), [AGON_VDS_MEMO_BRIDGE](./docs/AGON_VDS_MEMO_BRIDGE.md) | keeps evidence and bridge memory source-linked without owning downstream truth |
| Quest follow-through | [root Agon quest lane](../../quests/agon/README.md) | keeps Agon-specific follow-through in the public Questbook item store with owner-routed memo stop-lines |
| Stage landing and stop-lines | [AGON_STAGE7_MEMO_LANDING](./docs/AGON_STAGE7_MEMO_LANDING.md), [AGON_STAGE11_MEMO_LANDING](./docs/AGON_STAGE11_MEMO_LANDING.md), [AGON_STAGE13_MEMO_LANDING](./docs/AGON_STAGE13_MEMO_LANDING.md), [AGON_STAGE13_MEMO_STOP_LINES](./docs/AGON_STAGE13_MEMO_STOP_LINES.md), [AGON_STAGE14_MEMO_LANDING](./docs/AGON_STAGE14_MEMO_LANDING.md), [AGON_STAGE15_MEMO_LANDING](./docs/AGON_STAGE15_MEMO_LANDING.md), [AGON_STAGE16_MEMO_LANDING](./docs/AGON_STAGE16_MEMO_LANDING.md), [AGON_STAGE17_MEMO_LANDING](./docs/AGON_STAGE17_MEMO_LANDING.md), [AGON_STAGE18_MEMO_LANDING](./docs/AGON_STAGE18_MEMO_LANDING.md) | keeps landing history reviewable without promoting it to source Agon law |

## Interface

Inputs are reviewed source refs, candidate Agon memory, owner-confirmed
handoff hints, and root Questbook follow-through notes. Outputs are bounded
memo docs, generated companion inputs, and clear stronger-owner routes.
