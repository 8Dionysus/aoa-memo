# Canonical Decision IDs and Generated Indexes

- Decision ID: AOA-MEM-D-0071

## Status

Accepted.

## Index Metadata

- Surface classes: root/topology, generated/readout, validation guard
- Mechanic parents: none
- Guard families: decision index/read-model, root technical district, release/tooling
- Memory object classes: decision
- Posture: active rationale

## Context

`aoa-memo` decision records were still date-path addressed and manually
indexed in `docs/decisions/README.md`. That worked while the lane was small,
but it made the decision surface expensive for agents: a contributor had to
read a long hand-maintained index before finding the right rationale.

The memory organ now needs a clearer operational map. A distant agent should be
able to ask by canonical handle, surface class, mechanic parent, guard family,
date, or affected memory-object class without treating generated lookup text as
the rationale itself.

The strategic risk is reference breakage. Renaming the existing date-path files
before a bridge exists would make older decisions, PRs, receipts, and route
cards harder to follow.

## Decision

Add a canonical decision ID to every decision note:

`AOA-MEM-D-####`

Each decision note owns an `## Index Metadata` block. Generated lookup indexes
under `docs/decisions/indexes/` are built from that metadata:

- `by-number.md`
- `by-date.md`
- `by-surface.md`
- `by-mechanic.md`
- `by-guard.md`
- `by-memory-object-class.md`
- `alias-map.md`
- `alias-map.min.json`

The current date-named files remain the live file paths for this migration
slice. The alias map bridges old/current paths to canonical IDs and reserves a
planned numbered path. A future rename may happen only after the alias/read
model layer protects dual-addressing.

## Alternatives

- Rename all decision files immediately. Rejected because it would make old
  refs brittle before the bridge existed.
- Keep the manual README index and only add IDs. Rejected because it would not
  make lookup cheaper for agents.
- Put the index metadata in a central manifest only. Rejected because each
  decision should carry the metadata that makes it findable.

## Consequences

- Decision lookup becomes cheaper without turning generated indexes into
  rationale authority.
- Future decisions must include a canonical ID and index metadata.
- The release gate can check generated index parity and missing metadata.
- Existing date-path refs remain valid during dual-addressing.
- A future numbered-file rename becomes a separate, lower-risk migration.

## Affected Surfaces

- `docs/decisions/`
- `docs/decisions/indexes/`
- `scripts/root-topology/build_decision_indexes.py`
- `scripts/root-topology/decision_index_common.py`
- `config/root-topology/root_technical_districts.json`
- `generated/root-topology/root_technical_districts.min.json`
- `scripts/release/release_check.py`

## Verification

Use:

```bash
python scripts/root-topology/build_decision_indexes.py --check
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/release/release_check.py
```
