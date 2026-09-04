# AGENTS.md

## Applies to

`mechanics/checkpoint/` and its active mechanic surfaces.

## Role

The checkpoint mechanic owns memo-side checkpoint memory: bounded checkpoint
gates, carry packets, approval records, health records, improvement threads,
and checkpoint-to-memory mappings.

It keeps checkpoint artifacts public, source-linked, and reviewable. It does
not own checkpoint execution, runtime stores, retry policy, actor rights,
proof verdicts, route dispatch, playbook choreography, or owner acceptance.

## Local delta

The `checkpoint` mechanic identity remains local; shared package, docs, parts, and
legacy hierarchy is inherited from `mechanics/AGENTS.md`. Its package card,
DIRECTION.md, PARTS.md, OWNER_MAP.md, and PROVENANCE.md remain the semantic
anchors for this operation.

## Boundaries

- Keep checkpoint surfaces memory-only, evidence-linked, and operation-first.
- Do not claim checkpoint execution, runtime persistence, retry scheduling,
  role rights, route dispatch, proof, playbook acceptance, or source-owner
  acceptance.
- Do not create a new durable memory-object kind for checkpoints. Map
  checkpoint artifacts into existing object kinds such as `state_capsule`,
  `decision`, `episode`, `audit_event`, `claim`, `pattern`, `bridge`, and
  `provenance_thread`.
- Keep recurrence return posture with `mechanics/recurrence-support/` unless
  the surface is the checkpoint artifact itself.
- Keep generic writeback governance with `mechanics/writeback/`; this package
  owns only the checkpoint-specific source contract that writeback consumes.
- Keep old root examples or root schemas out of active references once the
  checkpoint package owns the artifact.

## Verification

Use the nearest `VALIDATION.md` route for `checkpoint` work after the touched
surface is known; reusable lanes remain in `config/validation_lanes.json`.

## Closeout

Report checkpoint docs changed, whether part-local artifacts and consumer refs
stayed owner-routed, whether old root or package-level examples/schema refs
remain, and which stronger owner boundaries stayed outside `aoa-memo`.
