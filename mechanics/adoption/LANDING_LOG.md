# Adoption Landing Log

## 2026-05-19

- Moved adoption schemas, examples, and local tests into their owning
  `parts/` homes.
- Split validation between adoption boundary, revision/retention pressure, and
  scar/routing adoption so the mechanic is runnable by part.
- Kept adoption writeback as a candidate memory contract, not proof, runtime
  write execution, route authority, or owner acceptance.

Validation route:

```bash
python -m pytest -q mechanics/adoption/parts/adoption-boundary/tests mechanics/adoption/parts/revision-and-retention-pressure/tests mechanics/adoption/parts/scar-and-routing-adoption/tests
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.

## 2026-05-18

- Landed adoption as a memo mechanic package.
- Moved active adoption source docs from flat `docs/` paths into
  `mechanics/adoption/docs/`.
- Added owner map, provenance bridge, legacy index, and mechanics validation.

Validation route:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
