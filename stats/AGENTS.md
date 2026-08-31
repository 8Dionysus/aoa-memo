# AGENTS.md

## Applies to

Everything under `stats/` in `aoa-memo`.

## Role

This directory owns memo-local statistical questions, their embedded
measurement contracts, and evidence-linked reference packets. Shared
statistical grammar and cross-owner composition remain owned by `aoa-stats`.

## Conditional source route
Consult only the entries relevant to the current task:

1. Root `AGENTS.md`, `DESIGN.md`, and the memory boundary docs they route to.
2. `stats/README.md` and `stats/port.manifest.json`.
3. `memo/README.md`, `memo/OBJECT_SHAPE.md`, and the referenced corpus bundles.
4. The central measurement and packet contracts under `aoa-stats/stats/`.

## Boundaries

- `port.manifest.json` owns the memo-local question and measurement meaning.
- Reference packets are derived snapshots and remain weaker than reviewed
  corpus bundles and their object metadata.
- An object count describes the named corpus inventory only. It is not recall
  quality, truth, proof, freshness, or runtime availability.
- Keep packet refs repository-relative and keep memory content out of the
  packet.

## Validation

Inspect the owner evidence first:
Then validate the port and its referenced packets with the central owner:
## Closeout

Report the question or contract changed, the corpus evidence inspected,
whether the reference packet was refreshed, and which validation route ran.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
