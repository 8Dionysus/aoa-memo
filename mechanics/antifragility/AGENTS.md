# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/`.

## Role

The antifragility mechanic owns memo-side failure lesson and recovery pattern
memory: when to preserve a reviewed stress lesson, how to recall it, when a
drift-review or rollback-followthrough window should remain visible, and which
stronger owners must still be checked.

It does not own proof, route authority, stats conclusions, source receipts,
runtime repair, rollback execution, or current health claims.

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

For source docs, continue through `docs/AGENTS.md` and the target
`docs/*.md` surface.

## Post-Change Review

After antifragility changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- matching schemas, examples, generated object surfaces, tests, and writeback
  refs
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation
Before landing, also run:
## Closeout

Report the antifragility source family changed, whether legacy/provenance was
consulted, which stronger owner route remains outside `aoa-memo`, and whether
any old antifragility docs-root reference remains outside allowed provenance.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
