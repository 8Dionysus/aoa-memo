# One Owner per Validation Route

- Decision ID: AOA-MEM-D-0087

## Status

Accepted on 2026-08-31.

## Index Metadata

- Original date: 2026-08-31
- Surface classes: agents/mesh, validation guard, root/topology
- Mechanic parents: none
- Guard families: AGENTS/mesh, docs route, release/tooling
- Memory object classes: none
- Posture: accepted local-route topology; no proof, runtime, or release claim

## Context

`AOA-MEM-D-0086` moved executable procedure out of inherited `AGENTS.md`
context and into the nearest unambiguous `VALIDATION.md`. The first migration
preserved the commands but concatenated many would-be local files into
`docs/validation/VALIDATION.md`; several mechanic package routes recursively
contained their child routes as well.

That shape preserved text but not the intended loading boundary. A task that
needed one local procedure could be forced to load a repository-wide aggregate,
and a phrase such as "nearest `VALIDATION.md`" could resolve to a file owned by
another surface. Repeated copies also made command drift harder to distinguish
from an intentional local specialization.

## Decision

Every tracked `AGENTS.md` card has one physical same-directory
`VALIDATION.md` companion. Each companion contains only the focused procedure
for that card's owner surface. A validation file must not embed another route
file, concatenate child procedures, or contain repeated top-level documents.

Reusable machine sequences remain authoritative in
`config/validation_lanes.json`. A local companion may invoke a named lane and
may add a genuinely local focused check, but it must not fork a manifest-owned
sequence. Historical or legacy cards retain local companions only to preserve
their bounded route without reactivating the legacy surface.

The AGENTS mesh validator checks companion presence for the complete tracked
card corpus and rejects recursive aggregate markers or multiple level-one
headings. Generated indexes remain derived and are rebuilt after source
changes.

## Alternatives

- Keep the central aggregate and link to section anchors. Rejected because the
  on-demand hop would still load unrelated repository procedure and preserve a
  high-drift command catalog.
- Let a missing local route fall through to an ancestor `VALIDATION.md`.
  Rejected because "nearest" then changes meaning with directory topology and
  can silently bind a task to the wrong owner procedure.
- Keep aggregate package files but split only the repository-wide file.
  Rejected because recursive duplication and child-owner ambiguity would
  remain one level lower.

## Consequences

- The repository contains more small `VALIDATION.md` files, but an agent loads
  only the procedure for the selected owner surface.
- Command duplication becomes an explicit defect rather than a side effect of
  route aggregation; reusable sequence authority remains centralized.
- Moving or adding an `AGENTS.md` card now requires moving or adding its local
  companion in the same change.
- A green topology check proves local route shape and presence only. It does
  not prove command success, generated parity, CI, review, merge, runtime
  health, or Goal completion.

## Affected Surfaces

- every tracked `AGENTS.md` and same-directory `VALIDATION.md`
- `DESIGN.AGENTS.md`
- `docs/validation/COMMAND_AUTHORITY.md`
- `scripts/agents/validate_agents_mesh.py`
- `tests/agents/test_agents_mesh.py`
- decision indexes and generated AGENTS/KAG projections

## Verification

Run the decision-index builder and check, the AGENTS mesh validators and
focused tests, command-conservation and duplicate-route scans, then rebuild
affected generated projections. These checks do not cross the global merge
barrier established for the README/AGENTS migration.
