# Writeback Landing Log

## 2026-05-19

- Moved writeback schemas, examples, generated companions, scripts, tests, and
  receipt fixtures into their nearest functioning `parts/` homes.
- Split runtime, quest, revision, rollback, growth/continuity, and receipt
  publication validation into part-local test routes while keeping the
  operational-contract regression as a registered cross-mechanic root test.

Validation route:

```bash
python -m pytest -q mechanics/writeback/parts/runtime-and-temperature/tests mechanics/writeback/parts/quest-and-chronicle/tests mechanics/writeback/parts/revision-ledgers/tests mechanics/writeback/parts/rollback-and-recovery/tests mechanics/writeback/parts/growth-and-continuity/tests mechanics/writeback/parts/receipt-publication-regression/tests tests/mechanics/test_cross_mechanic_operational_contracts.py
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, KAG, playbook,
  stats, or stronger-owner authority moved into memo.

## 2026-05-18

- Moved the tracked writeback receipt fixture from root `tests/fixtures/` into
  `mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/`.
- Kept receipt publication validation package-local while leaving only
  cross-mechanic regressions in root `tests/`.

Validation route:

```bash
python -m pytest -q mechanics/writeback/parts/receipt-publication-regression/tests
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.

## 2026-05-18

- Landed writeback as a memo mechanic package.
- Moved active writeback source docs from flat `docs/` paths into
  `mechanics/writeback/docs/`.
- Added owner map, provenance bridge, legacy index, and mechanics validation.

Validation route:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.

## 2026-05-18

- Moved self-agency continuity memory-object examples from root `examples/`
  into `mechanics/writeback/parts/growth-and-continuity/examples/`.
- Kept the root object-surface manifest as the repo-wide generated family
  input while routing writeback-owned examples to the writeback mechanic.

Validation route:

```bash
python scripts/memory/generate_memory_object_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_memo.py
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
