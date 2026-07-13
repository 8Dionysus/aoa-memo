# Mechanics Subroutes and Artifact Topology

- Decision ID: AOA-MEM-D-0022

## Status

Accepted.

Superseded in part by
[2026-05-18-mechanic-artifact-lanes](AOA-MEM-D-0012-mechanic-artifact-lanes.md)
for active mechanic-owned schemas, examples, config, generated companions,
scripts, tests, manifests, and hook bindings.

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

The first adoption, writeback, and retention mechanics landing moved active
source docs out of flat `docs/` paths and added package cards, owner maps,
provenance bridges, landing logs, roadmaps, and legacy indexes.

That landing deliberately left many schemas, examples, generated companions,
scripts, tests, manifests, and quests in root technical districts because they
still serve repo-wide contracts and the release gate.

Without a second route layer, future edits could confuse active package docs
with legacy provenance, or move technical artifacts into mechanic packages as a
cosmetic cleanup instead of a source-owned artifact-placement decision.

## Decision

Add mechanic subroute cards for active docs and legacy provenance:

- `mechanics/adoption/docs/AGENTS.md`
- `mechanics/adoption/legacy/AGENTS.md`
- `mechanics/writeback/docs/AGENTS.md`
- `mechanics/writeback/legacy/AGENTS.md`
- `mechanics/retention/docs/AGENTS.md`
- `mechanics/retention/legacy/AGENTS.md`

Add `mechanics/ARTIFACT_TOPOLOGY.md` as the placement-law surface for deciding
when root technical artifacts may remain in repo-wide districts and when they
should move into mechanic-local homes.

Extend `config/agents_mesh.json`, `generated/agents_mesh.min.json`, and the
memo mechanics validator so the subroutes remain machine-checkable.

## Consequences

- Active mechanic docs and legacy provenance now have separate local route
  cards.
- Root technical artifacts are not automatically misplaced just because they
  mention adoption, writeback, or retention.
- Future artifact moves need a route argument, link updates, validators, and
  release-gate evidence.
- Legacy remains provenance, not an active alias layer.

## Alternatives Considered

- Move all mechanic-adjacent root artifacts into packages immediately.
  Rejected because many of those artifacts are shared public contracts or
  release-gate companions.
- Leave artifact placement as an informal note in `mechanics/README.md`.
  Rejected because future artifact moves need a stronger source surface.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
