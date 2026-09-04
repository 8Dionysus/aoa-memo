# AGENTS.md

## Applies to

`mechanics/questbook/parts/` and every active part below it.

## Role

Questbook parts hold compact functioning contracts for the memo-side public
obligation mechanic.

They do not own root quest source files, root generated read models, proof,
route dispatch, runtime state, playbook choreography, role authority, or owner
acceptance.

## Local delta

The active `questbook` part rows are selected by `PARTS.md`; each row is
materialized by its nearest part `README.md`, `CONTRACT.md`, and
`VALIDATION.md`. Single-part artifacts stay with that part when they are not
shared by the mechanic.

The `questbook` part route narrows the package operation; it cannot widen memo
authority or replace the package `OWNER_MAP.md`. Source meaning remains in the
package docs, and former placement remains in `PROVENANCE.md` or `legacy/`.

For quest projections, retain root `quests/` as source and
`generated/quests/quest_*.json` as read models; the
`quest-read-model-projections` part owns that boundary.

## Boundaries

Tie each `questbook` part to one row in `mechanics/questbook/PARTS.md`; keep its
contract and source-family references local. Stronger proof, runtime, role,
route, KAG, playbook, stats, ToS, or source-owner claims remain outside this
part and follow the package owner map.

## Verification

Use the nearest `VALIDATION.md` route for the affected `questbook` part after its
contract or artifact surface is known.

## Closeout

Report active questbook parts and the package validation route.
