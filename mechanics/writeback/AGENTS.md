# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/`.

## Role

The writeback mechanic owns memo-side writeback posture: target maps, intake
contracts, chronicle writeback, revision writeback, rollback writeback,
growth-refinery writeback, A2A return writeback, and writeback temperature.

It does not run a live ledger, schedule workers, write runtime state, accept
owner-local truth, or grant promotion authority.

## Route Stack

- Above: root `AGENTS.md` owns repo identity and release route;
  `mechanics/AGENTS.md` owns shared mechanic package law and validators.
- Here: `README.md` is the mechanic card, `DIRECTION.md` names current
  pressure, `PARTS.md` lists active function nodes, `OWNER_MAP.md` names
  stronger owners, and `PROVENANCE.md` plus `legacy/` preserve placement
  history.
- Below: `docs/` holds active source docs, `parts/` holds functioning
  contracts and artifact homes, and `legacy/` is historical evidence only.

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
- part-local examples, schemas, generated companions, scripts, and tests
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
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py --check
python -m pytest -q mechanics/writeback/parts/runtime-and-temperature/tests mechanics/writeback/parts/quest-and-chronicle/tests mechanics/writeback/parts/revision-ledgers/tests mechanics/writeback/parts/rollback-and-recovery/tests mechanics/writeback/parts/growth-and-continuity/tests mechanics/writeback/parts/receipt-publication-regression/tests mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_contracts.py tests/test_cross_mechanic_operational_contracts.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the writeback part changed, whether generated targets or intake changed,
which owner route remains stronger, and whether any old flat writeback
docs-root reference remains.
