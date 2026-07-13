# Validation Command Authority

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
- Nearest `AGENTS.md` cards may name focused owner checks, lane ids, and local
  next routes for the changed surface.
- The active release procedure in `docs/root/RELEASING.md` may name its narrow
  operator flow. Spark scenario payloads under `.agents/spark/scenarios/` may
  name the scenario-local checks they execute.
- Decisions, changelogs, landing logs, reviewed memory objects, audit receipts,
  generated Markdown, and preserved reference docs keep outcomes and owner
  routes, not copied runnable command catalogs.

Use this balance when adding or moving validation:

1. Put full repeated lane sequences in `config/validation_lanes.json`.
2. Record validation-like entrypoints in `docs/validation/validator_inventory.json`.
3. Keep local focused commands in the nearest `AGENTS.md` only when they help an
   agent iterate on that owner surface.
4. Update `docs/testing/test_inventory.json` only for test files; do not make
   tests a second validator inventory.
5. Update topology tests when a new command store, workflow route, compatibility
   wrapper, or manual validator route is introduced.

Do not put full validation command blocks in active route, topology, audit,
mechanic, or scenario documentation when the same route can be expressed as a
lane id, focused owner check, or nearest `AGENTS.md` pointer.
