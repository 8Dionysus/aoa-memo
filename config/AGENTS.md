# AGENTS.md

## Guidance for `config/`

`config/` holds build, publication, retention-adjacent, or guardrail-support inputs for memo surfaces.

Config can tune generated surfaces or validation, but it must not define memory truth by stealth. Memory truth belongs in docs, schemas, examples, and source-owned memory object surfaces.

`config/agents_mesh.json` is the source-backed map for current route cards. It
may require local card snippets and generated mesh parity, but it still routes
to authored `AGENTS.md` cards rather than replacing them.

`config/memo_mechanics.json` is the source-backed map for current mechanic
packages. It drives `generated/memo_mechanics.min.json`, but package cards and
mechanic docs remain the active authored surfaces.

Keep config explicit, public-safe, and reviewable. No private memories, personal data, hidden retention rules, secret tokens, or local-only paths.

When config changes generated surfaces, regenerate only the touched family and inspect the diff for recall or provenance drift.

Verify with:

```bash
python scripts/validate_memo.py
python scripts/validate_semantic_agents.py
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
```
