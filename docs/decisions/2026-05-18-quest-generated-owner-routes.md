# Quest Generated Owner Routes

## Status

Accepted on 2026-05-18.

## Context

`generated/quest_catalog.min*.json` and `generated/quest_dispatch.min*.json`
are root-level public companions for the memo quest store. They are useful to
neighboring consumers, but they must not become a second quest ledger or a
place where stale owner names survive after mechanics move.

The mechanics topology now gives witness trace to recurrence-support and quest
chronicle writeback to writeback. The previous quest projection still carried
the old `memo/quest-chronicle` route and kept the witness trace quest under
writeback even though the contract and example live in recurrence-support.

## Decision

Keep the quest generated companions in root `generated/` because they project a
cross-mechanic public quest store.

Make the memo quest YAML sources the source for those generated companions and
add a deterministic builder. A later Questbook topology pass moved those
sources to `quests/memo/<state>/AOA-MEM-Q-*.yaml` and the builder to
`mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`. The release gate checks
the builder output before the broader memo validator.

Require current `AOA-MEM-Q-*` owner routes to resolve into concrete memo docs
or mechanic docs. Q2 closes through
`mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md`; Q3 routes to
`mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md`.

## Consequences

- Root quest generated files stay as public projections, not hand-authored
  authority.
- Mechanics keep ownership of their operation surfaces while `quests/` keeps
  the public obligation store.
- Future quest moves must update `QUESTBOOK.md`, the quest YAML, the owning
  mechanic docs, generated projections, and tests together.
- Stale symbolic owner routes such as `memo/quest-chronicle` are no longer
  valid.

## Validation

- `python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check`
- `python scripts/validate_memo.py`
- `python -m pytest -q tests/test_memo_validators.py`
- `python scripts/release_check.py`
