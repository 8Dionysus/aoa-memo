# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/`.

## Role

The writeback mechanic owns memo-side writeback posture: target maps, intake
contracts, chronicle writeback, revision writeback, rollback writeback,
growth-refinery writeback, A2A return writeback, and writeback temperature.

It does not run a live ledger, schedule workers, write runtime state, accept
owner-local truth, or grant promotion authority.

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

## Post-Change Review

After writeback changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- part-local examples, schemas, generated companions, scripts, and tests
- `legacy/INDEX.md`
- generated runtime writeback companions
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation
Use the nearest mechanic `VALIDATION.md` route before closeout; reusable lanes remain in `config/validation_lanes.json`.
## Closeout

Report the writeback part changed, whether generated targets or intake changed,
which owner route remains stronger, and whether any old flat writeback
docs-root reference remains.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
