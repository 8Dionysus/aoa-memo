# AGENTS.md

Route card for `scripts/memory/`.

## Purpose

This district owns memory-object, recall, lifecycle, operation-cycle, local
memo port, reviewed corpus, and generated memory surface validators and
builders. The broad memo validator CLI is a compatibility router; boundary
logic lives under `scripts/memory/validators/`.

## Source

Scripts here execute checks; they do not author doctrine. Source routes to
`docs/memory/`, `docs/posture/`, `schemas/`, and `examples/`.
Reviewed corpus checks route to `memo/`.
Reviewed intake landing from a local memo port route uses
`land_reviewed_memo_intake.py`; the script prepares object bundles and landing
receipts, but only after an export packet explicitly allows `reviewed_write`.
Its implementation is split into path/schema input checks, landing-plan
synthesis, and write/summary helpers so the CLI remains an entrypoint rather
than a hidden policy body.
`reject_reviewed_intake_candidate.py` owns the complementary explicit
non-landing route. It may issue schema-valid local and landing rejection
receipts from an owner-reviewed candidate and evaluation result, but it must
not copy intake or create a durable memory object.

Object-surface and operational-readout builders follow the same boundary:
source loading, projection rendering, live probing, and CLI check/write
orchestration stay in separate helper modules. Generated builders may check
projection parity, but they must not become the source of memory meaning.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/memory/`.
- Downstream: generated outputs in `generated/memory/` and
  `generated/memory-objects/`.
- Landing and rejection usage is preserved in this directory's on-demand
  `VALIDATION.md` route. Keep dry-run, review acceptance, explicit references,
  and receipt-only rejection semantics intact; rejection never creates corpus
  state.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
