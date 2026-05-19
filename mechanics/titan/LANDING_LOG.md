# Titan Landing Log

## 2026-05-18

- Landed Titan as a memo mechanic package.
- Moved active Titan source docs from the transitional `mechanics/titan/docs/` district
  into `mechanics/titan/docs/`.
- Preserved former flat docs-root and docs-district lineage through the legacy
  index.
- Added owner map, provenance bridge, package card, and mechanics validation.

Validation route:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

## 2026-05-19

- Renamed `parts/core-memory-posture/` to
  `parts/recall-and-remembrance-posture/` and
  `parts/specialized-policy/` to `parts/audit-personality-and-swarm-policy/`
  so Titan part names expose the memory operation they protect.
- Moved Titan schemas, examples, and tests from package-level artifact homes
  into the nearest functioning `parts/<part>/` homes.
- Split mixed candidate tests so recall/remembrance, closeout/digest, and
  audit/personality/swarm policy have their own part-local pytest routes.
- Kept Titan docs as source surfaces and moved only runnable contract artifacts.

Validation route:

```bash
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
python scripts/release/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
