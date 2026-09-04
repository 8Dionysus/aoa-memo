# Contributing to aoa-memo

Thank you for contributing.

## What belongs here

Good contributions:
- memory objects and memory-layer schemas
- provenance threads and recall surfaces
- salience, freshness, and temporal-posture guidance
- generated memory-layer surfaces and their validators
- docs that clarify explicit memory boundaries without turning memory into proof

Bad contributions:
- reusable techniques that belong in `aoa-techniques`
- execution workflows that belong in `aoa-skills`
- bounded proof claims that belong in `aoa-evals`
- routing logic that belongs in `aoa-sdk`
- secret notes, private traces, or vague memory prose with no reviewable contract

## Before opening a PR

Start from:

1. [CHARTER](CHARTER.md) for the authority boundary.
2. [DESIGN](DESIGN.md) for system form.
3. [MEMORY_INDEX](MEMORY_INDEX.md) for memory-canon routing.
4. [AGENTS](AGENTS.md) for semantic scope, then the nearest `VALIDATION.md`
   after the touched surface is known for executable checks.

Please make sure the change keeps memory explicit and reviewable, keeps proof,
routing, runtime, role, and workflow authority outside this repository, keeps
provenance visible, names temporal posture where it matters, and keeps examples
and docs public-safe.

Executable validation routes live in `config/validation_lanes.json` and the
nearest `VALIDATION.md` after the touched surface is known. Do not duplicate the full command battery here; it drifts.
If generator-backed surfaces changed, regenerate only the touched families
first, then rerun the relevant AGENTS route and inspect the worktree state.

## Preferred PR scope

Prefer:
- 1 memory surface or memory-object change per PR
- or 1 focused validation improvement
- or 1 focused docs clarification for memory boundaries

## Review criteria

PRs are reviewed for:
- explicitness and reviewability
- provenance clarity
- temporal honesty
- public safety
- source-of-truth discipline

## Security

Do not use public issues or pull requests for leaks, credentials, or sensitive private traces.
Use the process in `SECURITY.md`.
