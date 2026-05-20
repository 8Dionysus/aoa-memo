# Local Memo Port Standard

## Purpose

This standard lets other repositories add a small `memo/` port without turning
every repository into a second `aoa-memo`.

The local port holds near-field memory: candidates, receipts, review notes,
handoff packets, and source refs that are useful to that project. Cross-project
or durable memory moves to `aoa-memo` through reviewed intake.

## Minimal Pilot Shape

```text
memo/
  AGENTS.md
  README.md
  candidates/
  receipts/
  exports/
  local/
```

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

## Bridge To `aoa-memo`

Local memory enters `aoa-memo` as:

- a normal memory-object candidate
- a write-path guard record
- a reviewed runtime or host intake packet
- a consolidation or forgetting operation
- a consumer handoff bridge

The port may keep local detail after promotion. `aoa-memo` keeps the durable
cross-system object and its reviewable recall route.
