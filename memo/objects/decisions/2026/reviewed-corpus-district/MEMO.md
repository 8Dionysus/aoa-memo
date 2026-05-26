# Reviewed Corpus District

## Memory

`aoa-memo` now keeps reviewed durable memory objects in `memo/` as a corpus
district. The district is the repo's own memory body: object bundles live under
`memo/objects/`, while intake receipts and support surfaces stay nearby.

## Source Route

- System form: `DESIGN.md`
- Memory canon: `MEMORY_INDEX.md`
- Memory model: `docs/memory/MEMORY_MODEL.md`
- Living topology: `docs/memory/LIVING_MEMORY_TOPOLOGY.md`
- Local port contrast: `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`
- Decision rationale: `docs/decisions/AOA-MEM-D-0063-reviewed-memory-corpus-district.md`

## Review Posture

This object is a confirmed repo-topology decision. It does not make local
repo ports durable memory authorities; it gives reviewed intake a source-owned
landing corpus inside `aoa-memo`.

## Next Routes

- Validate with `python scripts/memory/validate_memo_corpus.py`.
- Keep generated read models under `generated/`.
- Keep MCP access in `abyss-stack/mcp/services/aoa-memo-mcp`.
- Route future graph lift through object ids, source refs, lifecycle posture,
  and provenance threads.
