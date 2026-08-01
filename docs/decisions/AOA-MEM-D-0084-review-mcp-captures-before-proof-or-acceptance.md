# Decision: Review MCP captures before proof or acceptance

- Decision ID: AOA-MEM-D-0084

## Status

Accepted on 2026-08-01 for source-contract implementation. Live owner review,
central proof, acceptance, admission, and rollout remain separate later gates.

## Index Metadata

- Original date: 2026-08-01
- Surface classes: consumer handoff, mechanic part, boundary/runtime/sibling
- Mechanic parents: consumer-handoff
- Guard families: part and payload, source/projection parity, memory surface, sibling and boundary
- Memory object classes: decision
- Posture: owner review before proof or acceptance

## Context

The stack can authenticate a loopback MCP call and preserve its exact payload,
but transport success and a matched result contract cannot decide whether a
memory brief is grounded in current reviewed `aoa-memo` source. Conversely,
letting `abyss-stack` or a generic SDK control-plane helper interpret memo
objects would move semantic authority out of the memory owner.

The current root memory owner also intentionally reports a `route_only` local
memo-port posture. A generic check for a full writable repo-local port would
misclassify the canonical owner as unready. The owner review must understand
that distinction while still refusing to infer durable writes, proof, or
acceptance.

## Decision

Add one `consumer-handoff` part that:

- authenticates both the stack canary receipt and private result artifact
  against a source-pinned Ed25519 public key;
- binds every returned reviewed-memory row and central contract to one exact,
  clean, committed `aoa-memo` revision;
- requires byte parity for the compact reviewed-corpus catalog and source
  objects used by the runtime checkout;
- treats `route_only` as the correct local-port posture for the central memory
  owner rather than as a writable-port failure;
- emits the pinned `aoa-sdk` owner-result-review ABI with an exact catalog
  watermark and a lifetime no longer than five minutes or the earlier capture
  expiry.

The review explicitly sets owner acceptance, central proof, admission,
cross-organ proof, and rollback proof to false. `aoa-evals` receives the next
proof question. Only a later independent `aoa-memo` act may accept the exact
proof-bound contour.

## Alternatives

- Let `abyss-stack` declare memo grounding. Rejected because runtime capture
  ownership does not include memory semantics or lifecycle.
- Treat a matching MCP result schema as owner review. Rejected because schema
  compatibility does not establish current corpus parity.
- Reuse the KAG owner reviewer unchanged. Rejected because KAG source-index
  freshness and memo reviewed-corpus/current-recall semantics are different
  owner questions.
- Combine review and owner acceptance. Rejected because acceptance must follow
  central proof and bind the same exact evidence chain.

## Consequences

- Memo-specific grounding becomes machine-checkable without moving it into the
  runtime or control-plane owners.
- Runtime capture trust and SDK ABI pins become explicit reviewed source.
- Root `route_only` posture remains honest and cannot be "fixed" into a false
  writable local port.
- A valid review still leaves the registry in shadow until proof, acceptance,
  rollback, consumer, and admission gates close.

## Affected Surfaces

- `mechanics/consumer-handoff/parts/mcp-owner-evidence-review/`
- `mechanics/consumer-handoff/PARTS.md`
- `mechanics/consumer-handoff/OWNER_MAP.md`
- `aoa-sdk:schemas/organ-access/organ-owner-result-review.schema.json`
- `abyss-stack:mcp/services/abyss-stack-mcp/`

## Verification

Run the commands in
`mechanics/consumer-handoff/parts/mcp-owner-evidence-review/VALIDATION.md`, then
the consumer-handoff package and repository release lanes. Those source checks
do not prove a live review, central proof, owner acceptance, admission, or
benefit.
