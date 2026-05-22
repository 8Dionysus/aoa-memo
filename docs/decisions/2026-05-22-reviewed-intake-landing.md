# Decision: Reviewed Intake Landing

## Status

Accepted.

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
schemas and guardrails, copies the accepted export into
`memo/intake/reviewed/`, creates a `memo/objects/<kind-dir>/<year>/<slug>/`
bundle, and writes a corpus-local landing receipt under
`memo/intake/receipts/`.

The landing receipt is schema-backed by
`schemas/support-objects/reviewed_intake_landing_receipt.schema.json`.

## Consequences

- `candidate_only` exports remain inspectable but cannot land as durable memory.
- Durable reviewed memory is created by an `aoa-memo` source change, not by MCP
  or by the origin port.
- Each landed object has a copied intake packet, origin candidate refs, origin
  receipt refs, object id, object path, and validation receipt.
- Generated object read models can consume the landed object through the normal
  corpus-backed builder.

## Validation

```bash
python scripts/memory/validate_memo_corpus.py
python -m pytest -q tests/memory/test_reviewed_intake_landing.py
python scripts/memory/generate_memory_object_surfaces.py --check
```
