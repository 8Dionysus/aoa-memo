# AGENTS.md

## Guidance for `tests/`

`tests/` protects memory schemas, examples, generated catalogs, recall contracts, lifecycle audit examples, docs district migrations, and writeback boundaries.

Tests should expose provenance loss, recall overreach, stale context, schema mismatch, AGENTS mesh drift, and generated/source drift.

Do not update expected outputs without checking the source-owned memory docs, schemas, or examples that own the meaning.

Keep fixtures public-safe. No private memories, secrets, hidden telemetry, or unreduced personal data.

Verify with:

```bash
python -m pytest -q tests
python scripts/validate_semantic_agents.py
python scripts/validate_agents_mesh.py
python scripts/validate_agents_mesh_index.py
python scripts/validate_docs_districts.py
```
