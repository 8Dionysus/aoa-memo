# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/`.

## Role

The checkpoint mechanic owns memo-side checkpoint memory: bounded checkpoint
gates, carry packets, approval records, health records, improvement threads,
and checkpoint-to-memory mappings.

It keeps checkpoint artifacts public, source-linked, and reviewable. It does
not own checkpoint execution, runtime stores, retry policy, actor rights,
proof verdicts, route dispatch, playbook choreography, or owner acceptance.

## Conditional route scope

- Above: root `AGENTS.md` owns repo identity and release route;
  `mechanics/AGENTS.md` owns shared mechanic package law and validators.
- Here: `README.md` is the mechanic card, `DIRECTION.md` names current
  pressure, `PARTS.md` lists active function nodes, `OWNER_MAP.md` names
  stronger owners, and `PROVENANCE.md` plus `legacy/` preserve placement
  history.
- Below: `docs/` holds active source docs, `parts/` holds functioning
  contracts and artifact homes, and `legacy/` is historical evidence only.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target `docs/*.md`
surface.

For schemas, examples, generated outputs, scripts, tests, quests, or manifests
that reference checkpoint memory, read the nearest local `AGENTS.md` before
editing that district.

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

## Post-Change Review

After checkpoint changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- checkpoint package docs plus part-local schemas, examples, and tests
- recurrence-support and writeback consumer refs
- generated mechanics, AGENTS mesh, memory object surfaces, and writeback
  companions
- docs-root maps, root route cards, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation
Before landing, also run:
## Closeout

Report checkpoint docs changed, whether part-local artifacts and consumer refs
stayed owner-routed, whether old root or package-level examples/schema refs
remain, and which stronger owner boundaries stayed outside `aoa-memo`.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
