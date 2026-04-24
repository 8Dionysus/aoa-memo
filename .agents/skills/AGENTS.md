# AGENTS.md

## Guidance for `.agents/skills/`

`.agents/skills/` is an agent-facing companion surface for memory-layer maintenance.

It may help an agent inspect memory objects, recall contracts, writeback seams, and guardrail surfaces, but it must not create memory authority beyond source docs, schemas, examples, and generated catalogs.

Memory is valuable. It is not proof, not runtime retention, and not a replacement for source-owned meaning in sibling repositories.

Do not hand-edit exported companion files before changing the source memory, recall, or writeback surface that owns meaning.

Keep everything public-safe: no private memories, secrets, hidden telemetry, or unreduced personal data.

Verify with:

```bash
python scripts/validate_memo.py
python scripts/validate_semantic_agents.py
```
