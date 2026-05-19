# Lineage Harvest Landing Log

## 2026-05-19

- Renamed `parts/generated-companions/` to
  `parts/lineage-inspection-projections/` so the part names the lineage
  inspection operation rather than the generic generated-companion artifact
  family.
- Moved the pattern-lineage schema, example, and regression into
  `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/`.
- Removed the non-operational `mechanic-local-technical-contracts` active part;
  the pattern-lineage memory gate now owns its technical contract directly.

Validation route:

```bash
python -m pytest -q mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests
python scripts/release/release_check.py
```

## 2026-05-18

- Landed `mechanics/lineage-harvest/` as the memo-side package for
  pattern-lineage memory candidates.
- Moved the former flat docs-root `PATTERN_LINEAGE_MEMORY.md` into
  `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md`.
- Routed `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json` and
  `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json`
  through the lineage-harvest mechanic-local artifact lane.
- Added mechanics index coverage, AGENTS mesh coverage, doctrine recall
  surfaces, tests, and decision rationale.

## Validation anchors

Expected release-bound validation:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests/test_lineage_harvest_mechanic.py tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/mechanics/test_cross_mechanic_candidate_contracts.py
python scripts/release/release_check.py
```

## Stop-lines checked

- No direct proof or eval verdict moved into memo.
- No KAG promotion authority moved into memo.
- No ToS canon or direct write route moved into memo.
- No source-owner consent moved into memo.
- No runtime watchtower execution moved into memo.
- No stats certification authority moved into memo.
