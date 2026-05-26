# Numbered Decision Route Completion

- Decision ID: AOA-MEM-D-0073

## Status

Accepted on 2026-05-26.

## Index Metadata

- Original date: 2026-05-26
- Surface classes: root/topology, generated/readout, validation guard
- Mechanic parents: none
- Guard families: decision index/read-model, docs route, generated/read-model, release/tooling
- Memory object classes: decision
- Posture: accepted canonical cleanup

## Context

AOA-MEM-D-0071 gave every decision a canonical ID and generated lookup indexes.
AOA-MEM-D-0072 moved the source files to numbered paths. After that landing,
keeping the transitional date-path compatibility layer would turn a migration
scaffold into a second active route.

For `aoa-memo` as a memory organ, that is the wrong signal. A distant agent
should see one current decision route: canonical `AOA-MEM-D-####` handle plus
the numbered source file. Historical path archaeology belongs to git history,
PRs, and release notes rather than a live repository lookup surface.

## Decision

Complete the decision-lane migration by keeping only the numbered canonical
route:

- source files are `docs/decisions/####-*.md`;
- `Decision ID: AOA-MEM-D-####` is the stable handle;
- `Original date` stays as semantic metadata for `by-date` lookup;
- generated indexes cover number, date, surface, mechanic, guard, and memory
  object class only;
- previous date-prefixed names are not preserved as active repo metadata or
  generated read models.

## Alternatives

Keeping the compatibility layer would make old references easier to follow, but
it would also teach agents that the migration is still incomplete.

Creating stub files for previous names would make duplicate edit targets and
weaken the numbered source route.

Keeping a central historical path table would be cheaper than stubs, but it
would still be a second lookup route for a lane that now has a canonical handle.

## Consequences

Decision lookup is simpler: agents use `AOA-MEM-D-####`, numbered filenames,
and generated classification indexes.

Old date-prefixed references are not active repository affordances. If they
need to be investigated, use git history, PRs, release notes, or the decision ID
visible in surrounding text.

The builder, index contract, lane route card, README, template, generated
indexes, and topology tests now enforce the numbered-only route.

## Affected Surfaces

- `docs/decisions/*.md`
- `docs/decisions/AGENTS.md`
- `docs/decisions/README.md`
- `docs/decisions/TEMPLATE.md`
- `docs/decisions/indexes/*`
- `docs/decisions/indexes/index_contract.yaml`
- `scripts/root-topology/decision_index_common.py`
- `tests/root-topology/test_topology_spine.py`

## Verification

Use:

```bash
python scripts/root-topology/build_decision_indexes.py --check
python -m pytest -q tests/root-topology/test_topology_spine.py
python scripts/release/release_check.py
```
