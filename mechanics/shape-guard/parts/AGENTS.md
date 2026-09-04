# AGENTS.md

## Applies to

`mechanics/shape-guard/parts/` and every active part below it.

## Role

`mechanics/shape-guard/parts/` holds functioning part contracts for the Shape Guard memo mechanic.

## Local delta

The active `shape-guard` part rows are selected by `PARTS.md`; each row is
materialized by its nearest part `README.md`, `CONTRACT.md`, and
`VALIDATION.md`. Single-part artifacts stay with that part when they are not
shared by the mechanic.

The `shape-guard` part route narrows the package operation; it cannot widen memo
authority or replace the package `OWNER_MAP.md`. Source meaning remains in the
package docs, and former placement is documented in `PROVENANCE.md` and the immutable retirement decision`.

## Boundaries

Tie each `shape-guard` part to one row in `mechanics/shape-guard/PARTS.md`; keep its
contract and source-family references local. Stronger proof, runtime, role,
route, KAG, playbook, stats, ToS, or source-owner claims remain outside this
part and follow the package owner map.

## Verification

Use the nearest `VALIDATION.md` route for the affected `shape-guard` part after its
contract or artifact surface is known.

## Closeout

Report active parts changed, whether source docs or artifacts moved, which
owner stop-lines stayed outside memo, and which package validation ran.
