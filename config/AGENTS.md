# AGENTS.md

## Guidance for `config/`

`config/` holds build, publication, retention-adjacent, or guardrail-support inputs for memo surfaces.

Config can tune generated surfaces or validation, but it must not define memory truth by stealth. Memory truth belongs in docs, schemas, examples, and source-owned memory object surfaces.

Keep config explicit, public-safe, and reviewable. No private memories, personal data, hidden retention rules, secret tokens, or local-only paths.

When config changes generated surfaces, regenerate only the touched family and inspect the diff for recall or provenance drift.

Verify with:

```bash
python scripts/validate_memo.py
python scripts/validate_semantic_agents.py
```
