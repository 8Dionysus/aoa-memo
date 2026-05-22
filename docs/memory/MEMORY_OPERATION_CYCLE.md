# Memory Operation Cycle

## Purpose

This document gives `aoa-memo` one compact operational map for memory movement.
It lets an agent see how a candidate becomes reviewed memory, how reviewed
memory becomes a read model, and how stale or unsafe memory leaves the active
path.

## Cycle

1. Candidate intake records a source-linked object, export, note, or evidence
   packet without claiming current truth.
2. Write-path guardrails mark trust, ingestion risk, derivation lineage, review
   route, and action-safety separation.
3. Review decides whether the candidate stays pending, becomes a reviewed
   `memo/objects/` bundle through an export with `allowed_result:
   reviewed_write`, is rejected, is quarantined, or is routed to a stronger
   owner.
4. Consolidation links duplicates, contradictions, supersessions, retractions,
   archives, and freezes.
5. Generated read models expose compact catalog, capsule, section, mechanic,
   and route-card surfaces. Object-facing read models are built from reviewed
   corpus bundles plus teaching fixtures and mark `source_kind` for consumers.
6. Consumer handoff gives evals, KAG, agents, playbooks, routing, runtime, or
   source owners bounded surfaces with provenance still visible.
7. Recurrence and retention checks return cooled, stale, contradicted, or
   newly useful memory to review.

## Minimal State Machine

| State | Meaning | Next route |
|---|---|---|
| captured | source-backed input exists, review not complete | write-path guard |
| candidate | shaped as a memory candidate | owner review |
| reviewed | accepted for memo-side recall and landed as corpus object | generated read models |
| current | preferred active recall posture | eval and consumer handoff |
| superseded | replaced by a newer or stronger object | consolidation record |
| retracted | withdrawn for safety, error, or source withdrawal | audit event |
| archived | retained for history, not active recall | retention route |
| frozen | intentionally stable and rarely changed | owner route |

## Operator Map

| Need | Route |
|---|---|
| Is this safe to write? | `mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md` |
| How should memory age or leave active recall? | `mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md` |
| Which access posture should a consumer use? | `docs/posture/MEMORY_OPERATION_MODES.md` |
| How should local project memory connect back? | `docs/memory/LOCAL_MEMO_PORT_STANDARD.md` |
| How does reviewed memory land inside aoa-memo? | `memo/OBJECT_SHAPE.md` and `scripts/memory/land_reviewed_memo_intake.py` |
| How do KAG or graph consumers preserve truth? | `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md` |
| How do runtime or host exports enter? | `mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md` |

## Calibration

Good memory operations are boringly inspectable. A later agent should be able to
open one object or packet and see source refs, review posture, lifecycle, owner
route, generated surface, and next validator without reconstructing the whole
system from scattered prose.
