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
- routing logic that belongs in `aoa-routing`
- secret notes, private traces, or vague memory prose with no reviewable contract

## Before opening a PR

Please make sure:
- the change keeps memory explicit and reviewable
- memory remains distinct from proof, routing, and workflow execution
- provenance stays visible
- temporal posture and staleness risk stay explicit where they matter
- generated surfaces remain aligned with their source objects
- examples and docs stay public-safe

Run the read-only validation battery before opening a PR:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
python -m pytest -q tests
```

If you changed generator-backed surfaces, regenerate only the touched families first, then rerun the read-only validation battery above and inspect `git status -sb`.

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
