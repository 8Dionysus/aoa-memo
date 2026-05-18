# Lineage Harvest Landing Log

## 2026-05-18

- Landed `mechanics/lineage-harvest/` as the memo-side package for
  pattern-lineage memory candidates.
- Moved the former flat docs-root `PATTERN_LINEAGE_MEMORY.md` into
  `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md`.
- Routed `mechanics/lineage-harvest/schemas/pattern_lineage_memory_entry_v1.json` and
  `mechanics/lineage-harvest/examples/pattern_lineage_memory_entry.example.json`
  through the lineage-harvest mechanic-local artifact lane.
- Added mechanics index coverage, AGENTS mesh coverage, doctrine recall
  surfaces, tests, and decision rationale.

## Validation anchors

Expected release-bound validation:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memo.py
python -m pytest -q mechanics/lineage-harvest/tests/test_lineage_harvest_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py mechanics/recurrence-support/tests/test_recurrence_support_mechanic.py tests/test_experience_wave3_seed_contracts.py
python scripts/release_check.py
```

## Stop-lines checked

- No direct proof or eval verdict moved into memo.
- No KAG promotion authority moved into memo.
- No ToS canon or direct write route moved into memo.
- No source-owner consent moved into memo.
- No runtime watchtower execution moved into memo.
- No stats certification authority moved into memo.
