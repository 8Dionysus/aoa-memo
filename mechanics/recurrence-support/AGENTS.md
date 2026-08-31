# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence-support/`.

## Role

The recurrence-support mechanic owns memo-side support for bounded relaunch
anchors, witness trace exports, and reviewed closeout recall landings.

It keeps route-return memory public, source-linked, and reviewable. It does not
own recurrence doctrine, dispatch behavior, runtime retry policy, actor rights,
proof verdicts, scenario choreography, or owner acceptance.

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
that reference recurrence-support docs, read the nearest local `AGENTS.md`
before editing that district.

## Boundaries

- Keep recurrence-support docs memory-only, evidence-linked, and
  operation-first.
- Do not claim route dispatch, tier escalation, runtime retry budgets, live
  scratchpad storage, role rights, identity continuity, eval proof, playbook
  acceptance, source truth, or owner acceptance.
- Do not introduce `return_memory` or another return-only memory-object family.
- Keep old flat docs-root paths out of active references except in provenance,
  legacy, decisions, and former-path source maps.
- Do not move checkpoint schemas or examples back into this package; use
  `mechanics/checkpoint/` for checkpoint artifacts and this package for
  route-return support that consumes them.
- Keep writeback return lanes with writeback and consumer scope posture with
  consumer-handoff unless this package is only preserving relaunch support.

## Post-Change Review

After recurrence-support changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- recurrence-support package contract refs in
  `mechanics/recurrence-support/{schemas,examples,tests}/` plus shared recall
  and quest refs
- generated mechanics or AGENTS mesh companions
- docs-root maps, root route cards, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation
Before landing, also run:
## Closeout

Report recurrence-support docs changed, whether package-local artifacts and
shared recall/quest refs stayed owner-routed, whether old flat docs-root
references remain only as allowed provenance, and which stronger owner
boundaries stayed outside `aoa-memo`.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
