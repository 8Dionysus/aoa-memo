# AGENTS.md

## Applies to

`mechanics/antifragility/parts/` and every active part below it.

## Role

`mechanics/antifragility/parts/` holds functioning part contracts for the Antifragility memo mechanic.

## Local delta

The active `antifragility` part rows are selected by `PARTS.md`; each row is
materialized by its nearest part `README.md`, `CONTRACT.md`, and
`VALIDATION.md`. Single-part artifacts stay with that part when they are not
shared by the mechanic.

The `antifragility` part route narrows the package operation; it cannot widen memo
authority or replace the package `OWNER_MAP.md`. Source meaning remains in the
package docs, and former placement is documented in `PROVENANCE.md` and the immutable retirement decision`.

## Boundaries

Tie each `antifragility` part to one row in `mechanics/antifragility/PARTS.md`; keep its
contract and source-family references local. Stronger proof, runtime, role,
route, KAG, playbook, stats, ToS, or source-owner claims remain outside this
part and follow the package owner map.

## Verification

Use the nearest `VALIDATION.md` route for the affected `antifragility` part after its
contract or artifact surface is known.

## Closeout

Report active parts changed, whether source docs or artifacts moved, which
owner stop-lines stayed outside memo, and which package validation ran.
