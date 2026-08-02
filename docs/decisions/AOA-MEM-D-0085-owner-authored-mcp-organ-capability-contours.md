# Decision: Owner-authored MCP organ capability contours

- Decision ID: AOA-MEM-D-0085

## Status

Accepted on 2026-08-01 for source-contract implementation. Runtime binding,
proof, acceptance, admission, deployment, and rollback remain separate gates.

## Index Metadata

- Original date: 2026-08-01
- Surface classes: consumer handoff, mechanic part, boundary/runtime/sibling
- Mechanic parents: consumer-handoff
- Guard families: part and payload, memory surface, sibling and boundary
- Memory object classes: decision
- Posture: owner capability source before runtime binding

## Context

`abyss-stack` already runs separate read and candidate `aoa-memo-mcp`
processes, but their complete catalogs are wider than the capability that
should be admitted into the agent OS. If runtime discovery alone defines the
capability, the stack can accidentally become the owner of memory semantics,
and legacy helpers can enter admission merely because they exist.

The read contour also mixes reviewed corpus memory with local-port orientation
and unaccepted intake inspection. The candidate contour contains maintenance
helpers beyond the bounded memory-candidate handoff. Process separation is
necessary but does not itself define a least-privilege organ contract.

## Decision

Publish one owner-authored manifest under
`mechanics/consumer-handoff/parts/mcp-organ-access/` with two disjoint
capabilities:

- `durable-memory-read` returns only reviewed corpus memory and explicit
  lifecycle, temporal, provenance, current-recall, and stronger-owner posture;
- `memory-candidate-prepare` creates only allowlisted local candidate,
  candidate-only intake, and forwarding-check packets.

The manifest owns exact capability IDs, primitive IDs, MCP names, credential
classes, effect classes, idempotency, blast-radius statements, and rollback
routes. `abyss-stack` binds those identities to exact process catalogs and
credentials. `aoa-sdk` handles admission. `aoa-evals` owns proof.

The complete legacy MCP surfaces may remain available outside the admitted
profiles during migration, but they are not implicitly part of either organ
capability.

## Alternatives

- Derive capability identity from every discovered tool. Rejected because
  implementation inventory is not owner semantics.
- Admit the complete read and candidate catalogs. Rejected because local-port
  maintenance and diagnostic helpers exceed the bounded consumer need.
- Put the manifest only in `abyss-stack`. Rejected because runtime owns binding
  and lifecycle, not durable-memory meaning or candidate authority ceilings.
- Combine read and candidate behind one credential. Rejected because a read
  principal must not reach local packet writes.

## Consequences

- Agents can discover a small stable memo capability instead of the complete
  implementation inventory.
- Candidate preparation remains a local, reversible, unaccepted write and
  cannot become durable corpus mutation.
- Runtime/source parity becomes explicitly checkable across two owners.
- Existing broad surfaces remain dual-era until the exact profiles are landed,
  deployed, and admitted.

## Affected Surfaces

- `mechanics/consumer-handoff/parts/mcp-organ-access/`
- `mechanics/consumer-handoff/PARTS.md`
- `mechanics/consumer-handoff/OWNER_MAP.md`
- `abyss-stack:mcp/services/aoa-memo-mcp/`
- `aoa-sdk:organ admission`

## Verification

Run the commands in the part `VALIDATION.md`, the consumer-handoff mechanic
topology checks, the decision-index check, and the repository source-fast
lane. These source checks do not prove runtime binding, consumer use, proof,
acceptance, admission, deployment parity, or rollback.
