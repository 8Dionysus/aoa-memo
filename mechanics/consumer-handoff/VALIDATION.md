# VALIDATION.md

On-demand human procedure for `mechanics/consumer-handoff/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests mechanics/consumer-handoff/parts/mcp-organ-access/tests mechanics/consumer-handoff/parts/mcp-owner-evidence-review/tests mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests mechanics/consumer-handoff/parts/playbook-scope-handoff/tests tests/memory/test_memo_handoff_boundaries.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/consumer-handoff/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
