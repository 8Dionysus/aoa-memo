# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/`.

## Role

The writeback mechanic owns memo-side writeback posture: target maps, intake
contracts, chronicle writeback, revision writeback, rollback writeback,
growth-refinery writeback, A2A return writeback, and writeback temperature.

It does not run a live ledger, schedule workers, write runtime state, accept
owner-local truth, or grant promotion authority.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

## Post-Change Review

After writeback changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `examples/`
- `legacy/INDEX.md`
- generated runtime writeback companions
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/generate_memory_object_surfaces.py
python scripts/validate_memory_object_surfaces.py
python -m pytest -q tests/test_downstream_feed_contracts.py mechanics/writeback/tests/test_quest_chronicle_writeback.py mechanics/writeback/tests/test_self_agency_continuity_writeback.py mechanics/writeback/tests/test_a2a_child_return_writeback.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the writeback part changed, whether generated targets or intake changed,
which owner route remains stronger, and whether any old flat writeback
docs-root reference remains.
