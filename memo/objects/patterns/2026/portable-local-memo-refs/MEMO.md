# Local memo ports use portable refs before reviewed intake

## Memory
Local memo ports stay useful across agents and machines when candidates, receipts, and exports use repo-scoped refs rather than workstation absolute paths.

## Source Route
- `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`
- `repo:abyss-stack/memo/candidates/20260520T051034Z.aoa-memo-mcp-provides-the-first-stack-owned-mcp.candidate.json`
- `repo:abyss-stack/memo/exports/20260520T051034Z.aoa-memo-mcp.reviewed-intake.json`
- `commit:abyss-stack:9fef703dc016f8e5c59a5d9625748174def6b809`
- `commit:abyss-stack:4d4ddb003b362bcd37e2749ccc3cee27b88be998`

## Review Posture
This is a confirmed pattern from two stack-side corrections. It does not make local ports durable memory; it keeps them portable enough to feed reviewed intake.

## Next Routes
- Use `repo:` refs for cross-repo evidence.
- Keep absolute filesystem paths out of durable export payloads.
- Validate ports and landing plans before reviewed write.
