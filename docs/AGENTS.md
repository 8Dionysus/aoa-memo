# AGENTS.md

## Guidance for `docs/`

`docs/` explains memory models, boundaries, lifecycle, trust posture, writeback, recall, KAG bridge, and neighboring-layer seams.

Docs may define doctrine for memo surfaces, but they must preserve the boundary: memory is not proof, not execution, not routing authority, and not runtime infrastructure.

Keep provenance, temporal relevance, salience, temperature, and recall pressure explicit. Avoid making durable-consequence claims without matching schemas, examples, and validators.

When docs change proof, routing, KAG, role, or playbook seams, name the downstream owner repo and what remains outside memo authority.

Verify with:

```bash
python scripts/validate_memo.py
python scripts/validate_semantic_agents.py
```
