# Decision: Add Memory Topology Spine Before Moving Flat Docs

- Decision ID: AOA-MEM-D-0023

Date: 2026-05-18

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-memory-topology-spine.md
- Surface classes: root/topology, memory doctrine
- Mechanic parents: none
- Guard families: docs route, memory surface
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` already has strong memory-layer doctrine, schemas, examples,
generated companions, validators, and green release validation. The current
weakness is topology: many active docs remain flat under `docs/`, and the repo
does not yet have the design, docs-map, root-surface-law, decision-lane, or
agent-surface design surfaces that recently made neighboring AoA repositories
easier to use.

The tempting move would be to start moving `AGON_*`, `TITAN_*`, adoption,
retention, rollback, and writeback docs into thematic directories immediately.
That would reduce visual noise, but it would also risk breaking links,
validators, generated refs, and owner boundaries before the repo has a local
placement law.

## Decision

Add a topology spine first:

- root `DESIGN.md`
- root `DESIGN.AGENTS.md`
- `docs/README.md`
- `docs/ROOT_SURFACE_LAW.md`
- `docs/decisions/`
- a regression test that pins these route surfaces and links

Do not move flat docs in this change.
Do not move root `Spark/` as part of this topology-spine decision.
Do not introduce a generated AGENTS mesh in this change.

## Alternatives Considered

### Move docs into districts immediately

Rejected for this slice. The target families are real memory seams, not trash.
Moving them before a docs map and placement law would hide risk under
cosmetic cleanup.

### Only add a docs README

Rejected as too weak. A map alone would not explain root placement,
agent-surface shape, or future decision placement.

### Copy the center repository topology wholesale

Rejected as too broad. `aoa-memo` is a memory layer, not the AoA center.
It needs the same discipline of owner boundaries, but with memory-specific
source classes and stop-lines.

## Consequences

Future cleanup now has a route:

- root and docs placement starts from `docs/ROOT_SURFACE_LAW.md`
- docs navigation starts from `docs/README.md`
- agent-surface changes start from `DESIGN.AGENTS.md`
- structural rationale goes to `docs/decisions/`

The diff intentionally leaves known follow-up work open:

- root `Spark/` remains a candidate move to `.agents/spark/` for a separate
  bounded follow-up decision
- flat `docs/` still needs thematic migration work
- a generated AGENTS mesh is not yet present
- validators still primarily protect contracts and route-surface presence, not
  full thematic topology

## Boundaries

This decision does not transfer authority from neighboring repositories into
`aoa-memo`.

Memory remains weaker than proof, routing, role policy, KAG substrate, runtime
state, and source-authored ToS meaning.

## Verification Route

Use:

```bash
python -m pytest -q tests
python scripts/release_check.py
```

The first command should include the topology-spine test. The second command
remains the broad release gate for the repository.
