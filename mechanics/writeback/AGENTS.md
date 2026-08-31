# AGENTS.md

## Applies to

`mechanics/writeback/` and its active mechanic surfaces.

## Role

The writeback mechanic owns memo-side writeback posture: target maps, intake
contracts, chronicle writeback, revision writeback, rollback writeback,
growth-refinery writeback, A2A return writeback, and writeback temperature.

It does not run a live ledger, schedule workers, write runtime state, accept
owner-local truth, or grant promotion authority.

## Local delta

The `writeback` mechanic identity remains local; shared package, docs, parts, and
legacy hierarchy is inherited from `mechanics/AGENTS.md`. Its package card,
DIRECTION.md, PARTS.md, OWNER_MAP.md, and PROVENANCE.md remain the semantic
anchors for this operation.

## Boundaries

Keep the writeback package-specific owner boundaries in the mechanic card and OWNER_MAP.md.

## Verification

Use the nearest `VALIDATION.md` route for `writeback` work after the touched
surface is known; reusable lanes remain in `config/validation_lanes.json`.

## Closeout

Report the writeback part changed, whether generated targets or intake changed,
which owner route remains stronger, and whether any old flat writeback
docs-root reference remains.
