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

It does not own:

- techniques, skills, eval proof, routing, role contracts, playbook scenario meaning, KAG substrate semantics, cross-owner statistical composition, or live quest sovereignty

## Start here

1. `README.md`
2. `CHARTER.md`
3. `DESIGN.md`
4. `MEMORY_INDEX.md`
5. `memo/README.md` when reviewed memory objects or corpus intake are touched
6. `stats/README.md` when memo-owned statistical questions, contracts, or reference packets are touched
7. [`ROADMAP.md`](ROADMAP.md)
8. `docs/README.md`
9. `docs/boundaries/BOUNDARIES.md`
10. `docs/memory/MEMORY_MODEL.md`
11. `mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md` for readiness, retention, and memory-is-not-proof boundaries
12. the target memory surface and affected generated outputs
13. `docs/root/AGENTS_ROOT_REFERENCE.md` for preserved full root branches

For agent-facing topology, also read `DESIGN.AGENTS.md`.
For root or docs-root placement, read `docs/root/ROOT_SURFACE_LAW.md`.
For repeatable antifragility, adoption, governance, shape-guard, checkpoint,
readiness-boundary, consumer-handoff, operational-gate, recurrence-support,
lineage-harvest, writeback, or retention movement, read `mechanics/README.md`.

## Route modes

| Route mode | Use when | First surface |
|---|---|---|
| `first-reading` | you need the shortest public overview | `README.md` |
| `memory-canon` | memory object kinds, support objects, recall modes, temperature vocabulary, source families, or generated companions are being inspected | `MEMORY_INDEX.md` -> `docs/memory/MEMORY_MODEL.md` -> target source |
| `memory-corpus` | reviewed durable memory object bundles, reviewed intake landing, landing receipts, or corpus support lanes change | `memo/AGENTS.md` -> `memo/OBJECT_SHAPE.md` -> target bundle |
| `local-stats` | a memo-owned statistical question, measurement contract, or reference packet changes | `stats/AGENTS.md` -> `stats/README.md` -> `stats/port.manifest.json` |
| `memory-doctrine` | memory meaning, object posture, trust, lifecycle, temperature, or provenance changes | `docs/memory/MEMORY_MODEL.md` |
| `root-editing` | a root or docs-root surface is added, moved, deleted, or rewritten | `docs/root/ROOT_SURFACE_LAW.md` |
| `docs-placement` | a docs-root surface is classified, retired from flat placement, or checked for old district drift | `docs/README.md` -> `docs/root/ROOT_SURFACE_LAW.md` -> `scripts/root-topology/validate_docs_districts.py` |
| `mechanic-change` | Antifragility, Agon, Titan, adoption, governance, shape-guard, checkpoint, readiness-boundary, consumer-handoff, operational-gate, recurrence-support, lineage-harvest, writeback, retention, owner split, legacy bridge, artifact placement, or mechanic-facing validation changes | `mechanics/README.md` -> target mechanic `AGENTS.md` -> `mechanics/ARTIFACT_TOPOLOGY.md` when artifacts move -> mechanics validators |
| `agent-surface-design` | agent-facing cards, lanes, or future mesh posture changes | `DESIGN.AGENTS.md` |
| `agents-mesh` | source-backed route-card coverage or generated mesh parity changes | `config/agents/agents_mesh.json` -> `generated/agents/agents_mesh.min.json` -> mesh validators |
| `generated-parity` | generated memory surfaces or their sources change | source surface -> builder -> generated output -> validator |
| `neighbor-seam` | a change touches proof, routing, role, playbook, KAG, or runtime boundaries | `docs/boundaries/BOUNDARIES.md` |


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
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
- `docs/root/ROOT_SURFACE_LAW.md` when root or docs-root placement changes.
- `docs/decisions/` when future agents need rationale for a route, topology,
  validator, source-of-truth, or ownership choice.
- generated surfaces, builders, validators, and tests when a source-backed
  machine companion changed.
- neighboring owner repositories when the change routes or constrains their
  truth.

## GitHub landing workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this route:

1. Start from a branch based on the current `origin/main`. If the worktree is already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces, validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing route and report the exact blocker instead of guessing.

## Verify

Use focused lanes for broad verification; the full command sequences live in
`config/validation_lanes.json`, with the route policy in
`docs/validation/COMMAND_AUTHORITY.md` and the validator map in
`docs/validation/validator_inventory.json`.

The `source-fast` lane includes central stats-contract validation. Provide a
compatible `aoa-stats` checkout through `AOA_STATS_ROOT`, `.deps/aoa-stats`, or
the sibling `../aoa-stats` path; CI supplies its pinned checkout explicitly.
An unavailable central validator is a failed check, not a skipped one.

```bash
python scripts/ci_gate.py --mode source-fast
python scripts/ci_gate.py --mode generated
python scripts/ci_gate.py --mode memory
python scripts/ci_gate.py --mode tests
```

Use `python scripts/release/release_check.py` for the frozen release gate.

Use branch docs in `docs/root/AGENTS_ROOT_REFERENCE.md` for object canon, trust posture, lifecycle, writeback, bridge, and guardrail work.

## Report

State which memory surface and class changed, whether provenance, temporal posture, writeback, chronicle, recurrence, or owner-local stats seams changed, and what validation ran.

## Full reference

`docs/root/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including memory-specific branch reading and hard boundaries.
