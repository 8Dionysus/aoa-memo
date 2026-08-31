# Validation Command Authority

`AOA-MEM-D-0086` fixes this split: inherited cards remain semantic deltas,
focused human procedure is on demand, and the lane manifest remains machine
command authority.

Validation commands use a split authority model:

- `config/validation_lanes.json` is the canonical storage surface for full
  repo-local lane command sequences and effective validator metadata.
- `docs/validation/validator_inventory.json` is the canonical inventory of
  validation-like entrypoints, lane-backed generated checks, compatibility
  wrappers, and manual validators.
- `scripts/validation_lanes.py` is a loader and compatibility API for Python
  callers. It must not grow a second copy of lane sequences.
- `scripts/ci_gate.py`, `scripts/release/release_check.py`, and workflow YAML
  should execute named lanes; they should not rebuild lane meaning inline.
- Active `AGENTS.md` cards may name focused owner checks, lane ids, and local
  next routes for the changed surface; they do not carry runnable command
  blocks or unconditional reading inventories.
- The nearest unambiguous `VALIDATION.md` preserves exact human-executable
  focused procedure after the touched surface is known.
- The active release procedure in `docs/root/RELEASING.md` may name its narrow
  operator flow. Spark scenario payloads under `.agents/spark/scenarios/` may
  name the scenario-local checks they execute.
- Decisions, changelogs, landing logs, reviewed memory objects, audit receipts,
  generated Markdown, and preserved reference docs keep outcomes and owner
  routes, not copied runnable command catalogs.

Use this balance when adding or moving validation:

1. Put full repeated lane sequences in `config/validation_lanes.json`.
2. Record validation-like entrypoints in `docs/validation/validator_inventory.json`.
3. Keep local focused commands in the nearest unambiguous `VALIDATION.md` only
   after the task has selected that owner surface.
4. Update `docs/testing/test_inventory.json` only for test files; do not make
   tests a second validator inventory.
5. Update topology tests when a new command store, workflow route, compatibility
   wrapper, or manual validator route is introduced.

Do not put runnable command blocks in active route, topology, audit, mechanic,
or scenario documentation when the same route can be expressed as a lane id
or a nearest `VALIDATION.md` pointer. README remains human/public semantic
navigation and never becomes command authority.
Do not put full validation command blocks in active `AGENTS.md` cards.
