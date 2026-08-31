# AGENTS.md

Root route card for `aoa-memo`.

## Purpose

`aoa-memo` is the explicit memory and recall layer of AoA.
It stores public, reviewable memory surfaces, memory-object structure, provenance threads, salience posture, and recall-oriented contracts for bounded agent memory behavior.
Memory is not proof, and continuity support is not proof of identity, agency, or current truth.

## Owner lane

This repository owns:

- memory-object structure, memory class distinctions, recall posture, salience, temporal relevance, and memory-temperature language
- memory-layer metadata, generated memory surfaces, witness trace, writeback, chronicle, recurrence-support, and lineage-harvest seams when defined here
- owner-local statistical questions and source-backed measurement declarations about memo-owned surfaces under `stats/`
- repository-specific callable procedures for bounded memory-owner work under `skills/`

It does not own:

- techniques, shared or cross-repository skills, eval proof, routing, role contracts, playbook scenario meaning, KAG substrate semantics, cross-owner statistical composition, or live quest sovereignty

## Conditional source route

Read only the route needed by the current task: `README.md` for public
orientation; `DESIGN.md` or `MEMORY_INDEX.md` for system or memory-canon
meaning; `memo/`, `stats/`, or `skills/` when that owner surface is touched;
`docs/README.md` and `docs/boundaries/BOUNDARIES.md` for placement or a
neighbor seam; and the target source plus affected generated outputs for a
concrete change. `docs/root/AGENTS_ROOT_REFERENCE.md` is conditional reference
material for preserved root branches, not an inherited inventory.
Consult [`ROADMAP.md`](ROADMAP.md) only when repository direction or future
triggers are part of the current task.
For readiness work, consult
`mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md` only when that
boundary is touched.

For agent-facing topology, also read `DESIGN.AGENTS.md`.
For root or docs-root placement, read `docs/root/ROOT_SURFACE_LAW.md`.
For repeatable antifragility, adoption, governance, shape-guard, checkpoint,
readiness-boundary, consumer-handoff, operational-gate, recurrence-support,
lineage-harvest, writeback, or retention movement, read `mechanics/AGENTS.md`
and the nearest package `AGENTS.md`. Read `mechanics/README.md` only for
public package atlas, placement, or provenance orientation.

## Route modes

| Route mode | Use when | First surface |
|---|---|---|
| `first-reading` | you need the shortest public overview | `README.md` |
| `memory-canon` | memory object kinds, support objects, recall modes, temperature vocabulary, source families, or generated companions are being inspected | `MEMORY_INDEX.md` -> `docs/memory/MEMORY_MODEL.md` -> target source |
| `memory-corpus` | reviewed durable memory object bundles, reviewed intake landing, landing receipts, or corpus support lanes change | `memo/AGENTS.md` -> `memo/OBJECT_SHAPE.md` -> target bundle |
| `local-stats` | a memo-owned statistical question, measurement contract, or reference packet changes | `stats/AGENTS.md` -> `stats/README.md` -> `stats/port.manifest.json` |
| `owner-skill` | the admitted `aoa-memo` procedure, its applicability, ABI, lifecycle, or OS-profile exposure changes | `skills/AGENTS.md` -> `skills/README.md` -> `skills/port.manifest.json` -> target `SKILL.md` |
| `memory-doctrine` | memory meaning, object posture, trust, lifecycle, temperature, or provenance changes | `docs/memory/MEMORY_MODEL.md` |
| `root-editing` | a root or docs-root surface is added, moved, deleted, or rewritten | `docs/root/ROOT_SURFACE_LAW.md` |
| `docs-placement` | a docs-root surface is classified, retired from flat placement, or checked for old district drift | `docs/README.md` -> `docs/root/ROOT_SURFACE_LAW.md` -> `scripts/root-topology/validate_docs_districts.py` |
| `mechanic-change` | Antifragility, Agon, Titan, adoption, governance, shape-guard, checkpoint, readiness-boundary, consumer-handoff, operational-gate, recurrence-support, lineage-harvest, writeback, retention, owner split, legacy bridge, artifact placement, or mechanic-facing validation changes | `mechanics/README.md` -> target mechanic `AGENTS.md` -> `mechanics/ARTIFACT_TOPOLOGY.md` when artifacts move -> mechanics validators |
| `agent-surface-design` | agent-facing cards, lanes, or future mesh posture changes | `DESIGN.AGENTS.md` |
| `agents-mesh` | source-backed route-card coverage or generated mesh parity changes | `config/agents/agents_mesh.json` -> `generated/agents/agents_mesh.min.json` -> mesh validators |
| `generated-parity` | generated memory surfaces or their sources change | source surface -> builder -> generated output -> validator |
| `neighbor-seam` | a change touches proof, routing, role, playbook, KAG, or runtime boundaries | `docs/boundaries/BOUNDARIES.md` |


## AGENTS stack law

- Read the root card only for repository-wide scope; follow a nearest nested card when the task touches that path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Memory route

`aoa-memo` is the reviewed memory owner for OS Abyss. Use this repository when
local candidates, session evidence, or MCP recalls need durable memory objects,
lifecycle, provenance, guardrails, consolidation, or reviewed handoff contracts.

- Need session evidence: route to `.aoa` rehydrate, retrieve, or review packets.
- Need local preservation before review: write through the owning place's
  `repo/memo/` port when present.
- Need reviewed durable memory inside this repo: use `memo/` object bundles
  with `object.json` plus `MEMO.md`; when coming from a local port export,
  land only `reviewed_write` packets through
  `scripts/memory/land_reviewed_memo_intake.py`, then validate the corpus.
- Need live access: use `aoa_memo` MCP as an access plane while keeping reviewed
  memory truth in this repository.

## Decision review

After structural, ownership, workflow, route-law, validator-authority,
public-contract, or topology changes, check whether future agents will need a
decision record to understand why the path was chosen.

Use `docs/decisions/AGENTS.md` and `docs/decisions/README.md` for the local
decision lane. If no record is needed, say so in closeout.

## Route away when

- the task needs proof, execution logic, source meaning, routing logic, role authority, or scenario composition
- memory wording starts pretending to be current truth without explicit temporal and provenance framing

## Post-change route review

Before closeout, check whether the change actually affects these surfaces.
Update only the ones that moved; otherwise say no update was needed.

- `ROADMAP.md` when repo-level direction, topology posture, consumer adoption,
  or future triggers changed.
- `CHANGELOG.md` when public docs, validation, repository structure, generated
  surfaces, or release-visible behavior changed.
- `DESIGN.md` when the memory-layer system form changed.
- `DESIGN.AGENTS.md` when agent-facing form, local route cards, or future mesh
  posture changed.
- `MEMORY_INDEX.md` when public memory object, support object, recall-mode,
  source-family, or generated-companion routing changes.
- `stats/` when the owner-local statistical question, evidence route,
  measurement contract, or exported reference packet changes.
- `skills/` when the admitted owner procedure, lifecycle, portability, or
  OS-profile exposure changes.
- `docs/root/ROOT_SURFACE_LAW.md` when root or docs-root placement changes.
- `docs/decisions/` when future agents need rationale for a route, topology,
  validator, source-of-truth, or ownership choice.
- generated surfaces, builders, validators, and tests when a source-backed
  machine companion changed.
- neighboring owner repositories when the change routes or constrains their
  truth.

## Release route

The ordinary branch, pull-request, CI, merge-method, and post-merge procedure
lives in [`docs/root/RELEASING.md`](docs/root/RELEASING.md). This card only
provides the landing pointer and the fail-closed boundary: if CI status,
review, merge authority, or post-merge state cannot be observed, stop and
report the exact blocker rather than inferring success.

## Verify

Use focused lanes for broad verification; the full command sequences live in
`config/validation_lanes.json`, with the route policy in
`docs/validation/COMMAND_AUTHORITY.md` and the validator map in
`docs/validation/validator_inventory.json`.

The `source-fast` lane includes central stats-contract validation. Provide a
compatible `aoa-stats` checkout through `AOA_STATS_ROOT`, `.deps/aoa-stats`, or
the sibling `../aoa-stats` path; CI supplies its pinned checkout explicitly.
An unavailable central validator is a failed check, not a skipped one.
Use the named `release_check` lane and the nearest `VALIDATION.md` route for
the frozen release gate.

Use branch docs in `docs/root/AGENTS_ROOT_REFERENCE.md` for object canon, trust posture, lifecycle, writeback, bridge, and guardrail work.

## Report

State which memory surface and class changed, whether provenance, temporal posture, writeback, chronicle, recurrence, or owner-local stats seams changed, and what validation ran.

## Full reference

`docs/root/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including memory-specific branch reading and hard boundaries.

## Validation route

For executable focused procedure, read the nearest `VALIDATION.md` after the touched surface is known.
