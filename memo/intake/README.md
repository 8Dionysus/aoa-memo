# Corpus Intake

This directory holds reviewed intake material for the `aoa-memo` corpus.

- `reviewed/` stores accepted intake packets before or alongside object
  landing.
- `quarantine/` stores bounded material that needs more review.
- `receipts/` stores corpus-local validation and landing receipts. Only
  `result: landed` is an active successful landing; `rejected` and
  `quarantined` receipts remain inspectable outcome history and do not count as
  current landing authority.

The durable memory object lives under `memo/objects/` after review.

Landing from an origin local memo port is routed through `memo/AGENTS.md`.
The command prints a dry-run plan by default; `--write` is only for accepted
reviewed-write packets.
