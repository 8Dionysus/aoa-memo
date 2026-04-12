# SELF_AGENCY_CONTINUITY_WRITEBACK

## Purpose

This note defines how `aoa-memo` supports self-agency continuity without
becoming the policy owner, the runtime body, or the proof layer.

Wave 9 continuity writeback stays memo-side support for bounded relaunch and
cross-window legibility.
It does not turn memory into identity proof, route authority, or silent retry
sovereignty.

## Rule

Do not add a new memory object family for continuity or return.

Use the existing canon:

- `anchor`
- `decision`
- `audit_event`
- `episode`
- `state_capsule`
- `provenance_thread`

## Recommended landing

- stable continuity reference point -> `anchor`
- explicit reflective revision or reanchor choice -> `decision`
- bounded review or continuity failure note -> `audit_event`
- meaningful continuity passage across one reviewed window -> `episode`
- exported bounded working state for relaunch -> `state_capsule`
- cross-window continuity chain -> `provenance_thread`

## Boundary

Memo can help a route return.
Memo can preserve one inspectable continuity chain.
Memo cannot decide whether return is legitimate.
Memo cannot define the active revision window.
Memo cannot replace owner truth, playbook truth, or proof truth.

## Suggested source chain

When continuity writeback is worth keeping, prefer the strongest public chain
that already exists:

- `aoa-agents` continuity window example or reviewed continuity artifact
- `aoa-sdk` continuity carry only as hint support
- `aoa-playbooks` recurring continuity route
- `aoa-evals` bounded continuity proof anchors

If a provenance thread is the right memo object, keep the thread inspectable and
make the return target explicit as `anchor_artifact_ref`.

## Negative rules

Do not:

- mint a new `self_agency_memory` or `return_memory` family
- use memo writeback as the first proof that self-agency exists
- let memory replace the active continuity window or reanchor decision
- let continuity survive only as vague chat residue

## Canonical neighbors

- `docs/RUNTIME_WRITEBACK_SEAM.md` owns the runtime-to-memo boundary
- `docs/GROWTH_REFINERY_WRITEBACK.md` owns lineage-aware refinery writeback
- `docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md` owns recurring memory support posture
