# Canonical Decision IDs and Generated Indexes

- Decision ID: AOA-MEM-D-0071

## Status

Accepted.

Superseded in part on 2026-05-26 by
[AOA-MEM-D-0072 Numbered Decision Paths](0072-numbered-decision-paths.md):
active decision source files now use numbered paths.

Superseded in part again on 2026-05-26 by
[AOA-MEM-D-0073 Numbered Decision Route Completion](0073-numbered-decision-route-completion.md):
the previous date-path compatibility metadata and generated read models are
retired from the active repository surface.

## Index Metadata

- Original date: 2026-05-26
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

For this migration slice, the date-prefixed files remained the live paths while
the generated lookup indexes made future numbered paths possible. Later
decisions completed the migration and removed the compatibility layer.

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
