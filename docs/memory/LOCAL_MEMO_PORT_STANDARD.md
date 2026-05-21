# Local Memo Port Standard

## Purpose

This standard lets other repositories add a small `memo/` port without turning
every repository into a second `aoa-memo`.

The local port holds near-field memory: candidates, receipts, check notes,
handoff packets, and source refs that are useful to that project. Cross-project
or durable memory moves to `aoa-memo` through reviewed intake.

## Minimal Pilot Shape

```text
memo/
  AGENTS.md
  README.md
  PORT.yaml
  INDEX.md
  index.min.json
  candidates/
  receipts/
  exports/
  local/
```

`PORT.yaml` stores the local port contract: owner, stronger memory owner,
default operation mode, allowed routes, directories, validators, and optional
local vocabulary extensions.

`INDEX.md` and `index.min.json` are generated read models over the local port.
They summarize counts, open items, routes, review states, and vocabulary use.
They are not authored memory.

`candidates/` stores proposed memory claims or intake packets.
`receipts/` stores validation, accept, reject, or forward traces.
`exports/` stores packets meant for reviewed `aoa-memo` intake.
`local/` stores project-local memory that should not become central yet.

Optional deeper ports may add `reviews/`, `handoffs/`, `generated/`, or
mechanic-specific subdirectories once a real workflow needs them. The useful
invariant is the route, not uniform bulk.

## Port Contract

Each local port should make these fields easy to find:

- local owner and stronger owner
- source refs
- candidate ids
- review state
- lifecycle posture
- export or intake packet refs
- target `aoa-memo` route when promotion is requested

The schema-backed port surfaces are:

- `schemas/memory-ports/local_memo_port.schema.json`
- `schemas/memory-ports/local_memo_candidate.schema.json`
- `schemas/memory-ports/local_memo_receipt.schema.json`
- `schemas/memory-ports/local_memo_export.schema.json`
- `schemas/memory-ports/local_memo_port_index.schema.json`

The controlled indexing vocabulary is:

- `docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md`
- `config/memory-ports/indexing_vocabulary.json`

## Bridge To `aoa-memo`

Local memory enters `aoa-memo` as:

- a normal memory-object candidate
- a write-path guard record
- a reviewed runtime or host intake packet
- a consolidation or forgetting operation
- a consumer handoff bridge

The port may keep local detail after promotion. `aoa-memo` keeps the durable
cross-system object and its reviewable recall route.

## Packet-First Rule

Local port state should be packet-first. Markdown companions may explain a
candidate for humans, but the reviewable state should live in JSON or YAML
packets so validators and MCP tools can read it.

Recommended file names:

```text
candidates/{stamp}.{slug}.candidate.json
receipts/{stamp}.{slug}.validation-receipt.json
receipts/{stamp}.{slug}.forwarding-receipt.json
exports/{stamp}.{slug}.aoa-memo-intake.json
local/{stamp}.{slug}.local.json
```

The useful invariant is still the route:

```text
candidate -> receipt -> export -> reviewed aoa-memo route
```
