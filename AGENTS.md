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

It does not own:

- techniques, skills, eval proof, routing, role contracts, playbook scenario meaning, KAG substrate semantics, stats summaries, or live quest sovereignty

## Start here

1. `README.md`
2. `CHARTER.md`
3. `DESIGN.md`
4. [`ROADMAP.md`](ROADMAP.md)
5. `docs/README.md`
6. `docs/BOUNDARIES.md`
7. `docs/MEMORY_MODEL.md`
8. `mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md` for readiness, retention, and memory-is-not-proof boundaries
9. the target memory surface and affected generated outputs
10. `docs/AGENTS_ROOT_REFERENCE.md` for preserved full root branches

For agent-facing topology, also read `DESIGN.AGENTS.md`.
For root or docs-root placement, read `docs/ROOT_SURFACE_LAW.md`.
For repeatable antifragility, adoption, governance, shape-guard, checkpoint,
readiness-boundary, consumer-handoff, operational-gate, recurrence-support,
lineage-harvest, writeback, or retention movement, read `mechanics/README.md`.

## Route modes

| Route mode | Use when | First surface |
|---|---|---|
| `first-reading` | you need the shortest public overview | `README.md` |
| `memory-doctrine` | memory meaning, object posture, trust, lifecycle, temperature, or provenance changes | `docs/MEMORY_MODEL.md` |
| `root-editing` | a root or docs-root surface is added, moved, deleted, or rewritten | `docs/ROOT_SURFACE_LAW.md` |
| `docs-placement` | a docs-root surface is classified, retired from flat placement, or checked for old district drift | `docs/README.md` -> `docs/ROOT_SURFACE_LAW.md` -> `scripts/validate_docs_districts.py` |
| `mechanic-change` | Antifragility, Agon, Titan, adoption, governance, shape-guard, checkpoint, readiness-boundary, consumer-handoff, operational-gate, recurrence-support, lineage-harvest, writeback, retention, owner split, legacy bridge, artifact placement, or mechanic-facing validation changes | `mechanics/README.md` -> target mechanic `AGENTS.md` -> `mechanics/ARTIFACT_TOPOLOGY.md` when artifacts move -> mechanics validators |
| `agent-surface-design` | agent-facing cards, lanes, or future mesh posture changes | `DESIGN.AGENTS.md` |
| `agents-mesh` | source-backed route-card coverage or generated mesh parity changes | `config/agents_mesh.json` -> `generated/agents_mesh.min.json` -> mesh validators |
| `generated-parity` | generated memory surfaces or their sources change | source surface -> builder -> generated output -> validator |
| `neighbor-seam` | a change touches proof, routing, role, playbook, KAG, or runtime boundaries | `docs/BOUNDARIES.md` |


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

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
- `docs/ROOT_SURFACE_LAW.md` when root or docs-root placement changes.
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

Core validation set:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_semantic_agents.py
python scripts/validate_docs_districts.py
python scripts/validate_memo_mechanics.py
python scripts/validate_memo_mechanic_parts.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python scripts/build_mechanic_artifact_inventory.py --check
python scripts/validate_mechanic_artifact_inventory.py
python -m pytest -q tests
```

Use branch docs in `docs/AGENTS_ROOT_REFERENCE.md` for object canon, trust posture, lifecycle, writeback, bridge, and guardrail work.

## Report

State which memory surface and class changed, whether provenance, temporal posture, writeback, chronicle, or recurrence seams changed, and what validation ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including memory-specific branch reading and hard boundaries.
