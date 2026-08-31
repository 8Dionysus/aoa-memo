# Prompt-Light Agent Routes and On-Demand Validation

- Decision ID: AOA-MEM-D-0086

## Status

Accepted on 2026-08-31.

## Index Metadata

- Original date: 2026-08-31
- Surface classes: agents/mesh, validation guard, root/topology, generated/readout
- Mechanic parents: none
- Guard families: AGENTS/mesh, docs route, generated/read-model, source/projection parity, release/tooling
- Memory object classes: none
- Posture: accepted source-route rationale; no memory-object, runtime, proof, or lifecycle state change

## Context

`AOA-MEM-D-0044` correctly separated public orientation from active agent
guidance, but it placed executable validation procedure in root and nested
`AGENTS.md`. `AOA-MEM-D-0019` likewise required the nearest `AGENTS.md` or
`VALIDATION.md` to expose a package-local test route. The repository has since
grown to 118 tracked agent cards. Exact commands and unconditional reading
inventories in those cards are inherited even when a task touches an unrelated
memory surface.

That recurring context is expensive and obscures the small set of constraints
that must be known before acting: owner boundaries, source authority, memory-is-
not-proof limits, temporal and provenance posture, approval stop-lines, local
risk, and the route to verification. The repository already has a stronger
three-layer validation topology:

- `config/validation_lanes.json` owns reusable machine-executed lane sequences;
- `scripts/ci_gate.py` and the release runner execute those lanes;
- the nearest `VALIDATION.md` can preserve exact focused human procedure after
  the touched surface is known.

The decision must also preserve the distinction between reviewed corpus source
and generated memory read models. Reducing prompt context cannot make an
`AGENTS.md`, README, generated index, MCP result, or stale local-port projection
stronger than its authored owner source.

## Decision

Keep `AGENTS.md` as a prompt-light inherited semantic delta. Root and nested
cards may carry applies-to scope, local role, owner and source boundaries,
memory/proof/currentness limits, conditional source routes, approval or safety
stop-lines, a named validation lane or link, and closeout requirements. They do
not carry runnable command sequences, full release/merge procedure, or an
unconditional inventory of README and design files merely because an agent
entered a subtree.

Keep exact human-executable focused procedure in the nearest unambiguous
`VALIDATION.md`. Keep reusable machine command sequences authoritative in
`config/validation_lanes.json`; a human validation route may invoke a named
lane or add truly local focused procedure, but it must not claim to replace or
fork the manifest-owned sequence.

Keep README files as human and public semantic navigation. Root `README.md`
remains the public front door. A route card may point to a README when the
current task needs that surface's meaning, but README reading is conditional,
not an inherited entry tax. This decision does not authorize blanket README
deletion, renaming, or consolidation. Every non-root disposition still needs
link, public-consumer, semantic-source, fixture, and generator evidence.

Keep ordinary branch, pull-request, CI, merge-method, and post-merge procedure
in the repository's release/governance documentation. Root `AGENTS.md` keeps
only the landing route, evidence class, and stop-line when CI status or merge
authority cannot be observed.

Change authored source and builder inputs before generated AGENTS meshes,
decision indexes, memory read models, or local-port projections. A generated
surface with no safe owner builder is owner debt, not permission to hand-edit
the projection.

This decision supersedes only the executable-command placement and
unconditional-reading implications of `AOA-MEM-D-0044`. It preserves that
record's public README boundary, neighboring-document authority separation,
source-backed mesh, and stale-topology guards. It is compatible with
`AOA-MEM-D-0019`: a package-local test route remains discoverable through the
nearest `VALIDATION.md` rather than necessarily occupying inherited agent
context.

## Alternatives

- Keep exact commands in the nearest `AGENTS.md` and rely on chain-size limits.
  Rejected because unrelated procedure remains automatically inherited and
  repeated across a large route mesh.
- Move commands and agent procedure into README files. Rejected because README
  is the human/public semantic surface and must not become hidden executable
  authority or mandatory prompt context.
- Remove or consolidate README files mechanically while shrinking agent cards.
  Deferred because filename consumers, links, fixtures, generated sources,
  archives, and public entry routes require per-file disposition evidence.

## Consequences

- Inherited context becomes smaller without losing memory-owner, provenance,
  temporal, proof, generated/source, privacy, approval, or stronger-owner
  boundaries.
- Focused validation gains one explicit on-demand hop after the touched surface
  is known.
- Validators must inspect the applicable validation route instead of freezing
  command prose inside `AGENTS.md`.
- Generated read models remain weaker than their source and must be rebuilt by
  the declared builder; stale external projections remain explicit owner debt.
- A green documentation or source lane proves only its declared contract. It
  does not prove memory acceptance, current recall, proof, runtime health,
  external CI, review, merge, or Goal completion.

## Affected Surfaces

- `AGENTS.md`
- `DESIGN.AGENTS.md`
- nested `AGENTS.md`
- root and package-local `VALIDATION.md`
- `README.md` and non-root README disposition records
- `config/validation_lanes.json`
- `docs/validation/COMMAND_AUTHORITY.md`
- repository release/governance documentation
- `config/agents/agents_mesh.json` and generated AGENTS mesh
- generated memory/read-model builders and validators when their source route changes

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `VALIDATION.md`. Rebuild decision
indexes and every affected generated companion from source, validate the full
tracked README/AGENTS/VALIDATION corpus, measure inherited context before and
after, and keep merge blocked until all owner repositories have completed the
same evidence-bearing pass.
