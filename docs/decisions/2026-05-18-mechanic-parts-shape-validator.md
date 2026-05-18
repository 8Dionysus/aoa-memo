# Mechanic Parts Shape Validator

## Status

Accepted.

## Context

Mechanic packages use `PARTS.md` to name their functioning parts and local
interfaces.

Most packages already used an Active Parts table plus an Interface section, but
the shape was not enforced. Governance and lineage-harvest had drifted into
local variants. That made `PARTS.md` less machine-checkable and blurred the
difference between a semantic part map and a raw artifact inventory.

The artifact inventory now covers raw package-local files. `PARTS.md` should
stay operation-shaped.

## Decision

Add `scripts/validate_memo_mechanic_parts.py` and release-gate it.

The validator requires every package `PARTS.md` to keep:

- a package Parts title
- `## Active Parts`
- a three-column Active Parts table
- source links that resolve when they are Markdown links
- every configured active doc routed somewhere in the file
- `## Interface`

Governance and lineage-harvest `PARTS.md` are normalized into this shape.

## Consequences

- Functioning parts become reviewable across all memo mechanics.
- `PARTS.md` stays semantic rather than becoming an artifact dump.
- Raw artifact visibility stays in `generated/mechanic_artifacts.min.json`.
- Future mechanic growth has a sharper gate before it can claim to be
  operation-first.
