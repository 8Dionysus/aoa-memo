# AGENTS.md

Root route card for `aoa-memo`.

## Purpose

`aoa-memo` is the explicit memory and recall layer of AoA.
It stores public, reviewable memory surfaces, memory-object structure, provenance threads, salience posture, and recall-oriented contracts for bounded agent memory behavior.
Memory is not proof, and continuity support is not proof of identity, agency, or current truth.

## Owner lane

This repository owns:

- memory-object structure, memory class distinctions, recall posture, salience, temporal relevance, and memory-temperature language
- memory-layer metadata, generated memory surfaces, witness trace, writeback, chronicle, and recurrence-support seams when defined here

It does not own:

- techniques, skills, eval proof, routing, role contracts, playbook scenario meaning, KAG substrate semantics, stats summaries, or live quest sovereignty

## Start here

1. `README.md`
2. `ROADMAP.md`
3. `CHARTER.md`
4. `docs/BOUNDARIES.md`
5. `docs/MEMORY_MODEL.md`
6. `docs/MEMORY_READINESS_BOUNDARY.md` for readiness, retention, and memory-is-not-proof boundaries
7. the target memory surface and affected generated outputs
8. `docs/AGENTS_ROOT_REFERENCE.md` for preserved full root branches


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Route away when

- the task needs proof, execution logic, source meaning, routing logic, role authority, or scenario composition
- memory wording starts pretending to be current truth without explicit temporal and provenance framing

## Verify

Core validation set:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
python -m pytest -q tests
```

Use branch docs in `docs/AGENTS_ROOT_REFERENCE.md` for object canon, trust posture, lifecycle, writeback, bridge, and guardrail work.

## Report

State which memory surface and class changed, whether provenance, temporal posture, writeback, chronicle, or recurrence seams changed, and what validation ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including memory-specific branch reading and hard boundaries.
