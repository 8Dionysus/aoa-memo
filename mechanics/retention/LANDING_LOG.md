# Retention Landing Log

## 2026-05-19

- Moved retention schemas, examples, and local tests into their owning
  `parts/` homes.
- Split local validation across cross-repo/governance retention, office marker,
  and post-release retention parts.
- Removed the stale retention validation dependency on governance tests from
  the retention route; governance keeps its own package lane.

Validation route:

```bash
python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.

## 2026-05-18

- Added a package-local retention regression boundary for active docs,
  mechanic-owned schemas, public-safe examples, and stronger-owner stop-lines.
- Kept retention execution, proof, private traces, and runtime scheduling
  outside `aoa-memo`.

Validation route:

```bash
python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.

## 2026-05-18

- Landed retention as a memo mechanic package.
- Moved active retention source docs from flat `docs/` paths into
  `mechanics/retention/docs/`.
- Added owner map, provenance bridge, legacy index, and mechanics validation.

Validation route:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
