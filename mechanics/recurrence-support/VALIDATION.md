# VALIDATION.md

On-demand human procedure for `mechanics/recurrence-support/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/root-topology/test_roadmap_parity.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/recurrence-support/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
