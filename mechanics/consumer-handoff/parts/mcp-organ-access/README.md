# MCP organ access

This active part belongs to `mechanics/consumer-handoff/` and materializes the
matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)
- `config/organ-access.v1.json`

## Function

Publish the owner-authored capability identities and primitive ceilings for
the stack-owned `aoa-memo-mcp` read and candidate processes. The manifest is
source truth for memory semantics; it is not runtime, credential, admission,
proof, or deployment truth.

## Next Route

`abyss-stack` binds these identities to exact MCP catalogs and process
credentials. `aoa-sdk` admits a contour only after source, deploy, consumer,
proof, acceptance, and rollback evidence close independently.
