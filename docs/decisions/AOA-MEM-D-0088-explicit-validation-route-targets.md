# Explicit Validation Route Targets

- Decision ID: AOA-MEM-D-0088

## Status

Accepted on 2026-09-04.

## Index Metadata

- Original date: 2026-09-04
- Surface classes: validation guard, agents/mesh, root/topology
- Mechanic parents: none
- Guard families: AGENTS/mesh, docs route, release/tooling
- Memory object classes: none
- Posture: accepted clarification of AOA-MEM-D-0086 and AOA-MEM-D-0087; no proof, runtime, or release claim

## Context

`AOA-MEM-D-0086` moved runnable procedure out of inherited agent context and
`AOA-MEM-D-0087` gave every tracked card a same-directory on-demand companion.
The first complete migration exposed a second ambiguity: some companions still
told readers to obtain commands from an `AGENTS.md#validation` section, used a
bare `VALIDATION.md` name from a nested directory, or retained a command
lead-in after the command had moved. Exact command uniqueness alone could not
detect those broken routes.

Some package-wide commands also enumerate child test directories already
represented by narrower part routes. Such a command can be a legitimate
composite scope, but only when the package owns that aggregate and its
membership is stable or checked against an authored topology. Otherwise it is
a second manually maintained roster, even though its argv is not textually
identical to the child commands.

## Decision

Keep the same-directory companion law from `AOA-MEM-D-0087`, but make every
handoff explicit.

- `AGENTS.md` owns semantic selection, risk, and stop-lines. A validation file
  must not route executable procedure back to `AGENTS.md#validation`.
- A nested companion that delegates procedure names the repository-relative
  owner path, linked from its own location, or names an exact validated lane or
  runner key. A bare `VALIDATION.md` label is not enough when it could mean the
  current file, a parent, or the repository root.
- A route-only companion says that the local surface owns no distinct
  executable procedure and points to the actual parent, root, or manifest
  owner. It does not keep empty command headings or dangling run lead-ins.
- A companion with a local procedure owns only that focused invocation. Wider
  checks are reached through an explicit owner link or named machine lane.
- A package-wide aggregate may remain distinct from child-focused procedures
  only when the package really owns the aggregate and a validator derives or
  checks its membership against authored topology. Otherwise composition moves
  to `config/validation_lanes.json` or an owner runner and the human file names
  that lane instead of copying membership.
- Fence language does not change ownership. Executable-looking invocations in
  text, terminal, unlabelled, or shell fences are measured alike.

The guard remains repository-local. It does not make `aoa-memo` the owner of
sibling validation procedure, CI state, release admission, or proof verdicts.

## Alternatives

- Treat every same-directory filename as unambiguous. Rejected because nested
  prose can silently refer to itself or the wrong ancestor.
- Restore commands to AGENTS validation sections. Rejected because it defeats
  the inherited-context split.
- Reject every overlapping test scope. Rejected because a package composite
  and a leaf-focused check can be different procedures when composition
  ownership and membership are explicit.

## Consequences

- Same-directory discovery remains stable while procedure ownership becomes
  traversable without guessing.
- Route residue and ambiguous targets become validator failures.
- Exact duplicate counts remain a lower bound; package aggregate membership
  still receives semantic and topology review.
- Existing companions require a bounded cleanup, but no unique executable
  procedure may disappear during it.

## Affected Surfaces

- every tracked same-directory `VALIDATION.md` companion
- `docs/validation/COMMAND_AUTHORITY.md`
- `scripts/agents/validate_agents_mesh.py`
- `tests/agents/test_agents_mesh.py`
- decision indexes and generated AGENTS projections

## Verification

Run the validation-route topology and ownership guards, focused AGENTS mesh
tests, decision index parity, generated projection checks, and a before/after
unique-command census. Review package-wide aggregates separately from exact
duplicate groups.
