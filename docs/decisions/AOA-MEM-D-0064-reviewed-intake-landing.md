# Decision: Reviewed Intake Landing

- Decision ID: AOA-MEM-D-0064

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-22
- Surface classes: reviewed corpus, local port/writeback
- Mechanic parents: none
- Guard families: reviewed corpus/intake
- Memory object classes: reviewed_intake
- Posture: active rationale

## Context

Local `repo/memo/` ports can now hold candidates, validation receipts, and
exports. `aoa-memo` also has a reviewed corpus under `memo/objects/`.

The remaining gap was the crossing itself: a candidate could be exported toward
`aoa-memo`, but there was no source-owned operation that checked the export and
made the durable object bundle without turning MCP, a local port, or a generated
read model into authority.

## Decision

Add `scripts/memory/land_reviewed_memo_intake.py` as the reviewed intake
landing route for `aoa-memo`.

The script only lands exports whose `allowed_result` is `reviewed_write`. It
loads candidate and receipt refs from inside the origin memo port, checks
schemas, guardrails, and local source/evidence refs, copies the accepted export
into `memo/intake/reviewed/`, creates a
`memo/objects/<kind-dir>/<year>/<slug>/` bundle, and writes a corpus-local
landing receipt under `memo/intake/receipts/`.

The landing receipt is schema-backed by
`schemas/support-objects/reviewed_intake_landing_receipt.schema.json`.

Local port receipt packets use
`schemas/memory-ports/local_memo_receipt.schema.json`. New producers emit
`aoa_local_memo_receipt_v2` with `checked_by`. The schema keeps the original
`aoa_local_memo_receipt_v1` shape with `reviewed_by` and `result: "reviewed"`
only as a legacy branch, so contract-breaking receipt field changes do not stay
hidden under the same schema token.

## Consequences

- `candidate_only` exports remain inspectable but cannot land as durable memory.
- Missing export or candidate source/evidence refs block landing before a corpus
  object is written.
- Durable reviewed memory is created by an `aoa-memo` source change, not by MCP
  or by the origin port.
- Each landed object has a copied intake packet, origin candidate refs, origin
  receipt refs, object id, object path, and validation receipt.
- Local receipt schema migration is explicit: old `reviewed_by` receipts remain
  readable as v1, while new `checked_by` receipts must identify themselves as
  v2.
- Generated object read models can consume the landed object through the normal
  corpus-backed builder.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
