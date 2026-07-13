# abyss-stack OS access-plane MCP services

## Memory

abyss-stack extended MCP access-plane services for memory, eval, and machine context while preserving sibling owner authority.

The durable memory is the owner split: `abyss-stack` owns the stdio MCP service
packages and runtime-adjacent adapters; `aoa-evals` owns proof meaning;
`abyss-machine` owns host-machine truth; `aoa-memo` owns reviewed memory.

## Source Route
- Reviewed intake: `memo/intake/reviewed/abyss-stack.20260526T003500Z.os-access-plane-mcp-services.reviewed-intake.json`
- `memo/intake/reviewed/abyss-stack.20260526T003500Z.os-access-plane-mcp-services.reviewed-intake.json`
- `repo:abyss-stack/memo/candidates/20260526T003500Z.os-access-plane-mcp-services-owner-split.candidate.json`
- `repo:abyss-stack/memo/receipts/20260526T003500Z.os-access-plane-mcp-services.forwarding-receipt.json`
- `repo:abyss-stack/memo/receipts/20260526T003646Z.export-abyss-stack-20260526t003500z-os-access-pl.forwarding-receipt.json`
- `repo:abyss-stack/mcp/AGENTS.md`
- `repo:abyss-stack/mcp/services/AGENTS.md`
- `repo:abyss-stack/docs/decisions/2026-05-25-aoa-evals-mcp-access-plane.md`
- `repo:abyss-stack/docs/decisions/2026-05-25-abyss-machine-mcp-access-plane.md`
- `repo:abyss-stack/mcp/services/aoa-evals-mcp/README.md`
- `repo:abyss-stack/mcp/services/abyss-machine-mcp/README.md`
- `repo:abyss-stack/mcp/services/aoa-evals-mcp/src/aoa_evals_mcp/core.py`
- `repo:abyss-stack/mcp/services/aoa-evals-mcp/tests/test_evals_mcp.py`

## Review Posture
This bundle landed from `abyss-stack` through the reviewed intake route. The local candidate packets remain source evidence; this object is the reviewed `aoa-memo` corpus memory.

## Candidate Claims
- abyss-stack extended the stack-owned MCP access-plane pattern from aoa-memo-mcp to aoa-evals and abyss-machine while keeping proof authority in aoa-evals, host authority in abyss-machine, and durable memory authority in aoa-memo.

## Next Routes
- Validate corpus and refresh read models through `memo/AGENTS.md` and the
  generated-memory owner route.
- Keep durable edits in `memo/objects/`; keep origin packet history in the source repo memo port.
