# aoa_memo search starts from reviewed corpus read models

## Memory
`aoa_memo_search` should inspect generated reviewed-corpus read models before falling back to supporting file snippets. Retrieval accelerates recall; it does not replace authored reviewed memory objects.

## Source Route
- `repo:abyss-stack/mcp/services/aoa-memo-mcp/DESIGN.md`
- `repo:abyss-stack/mcp/services/aoa-memo-mcp/README.md`
- `repo:abyss-stack/mcp/services/aoa-memo-mcp/src/aoa_memo_mcp/core.py`
- `repo:abyss-stack/mcp/services/aoa-memo-mcp/tests/test_memo_mcp.py`
- `generated/memory-objects/memory_object_catalog.min.json`
- `commit:abyss-stack:afbd28b6fd14d7e6aead78716ec1dc274f15aed0`

## Review Posture
This is a confirmed access-plane memory. `abyss-stack` owns the MCP implementation, while `aoa-memo` owns the reviewed corpus and generated read models.

## Next Routes
- Validate corpus/read-model parity through `memo/AGENTS.md` and the
  generated-memory owner route.
- Validate MCP search behavior in `abyss-stack` with the service tests.
- Keep future RAG/KAG/vector layers weaker than the reviewed object catalog.
