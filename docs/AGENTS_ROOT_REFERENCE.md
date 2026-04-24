# AGENTS root reference

This file preserves the previous full root guidance for `aoa-memo`.
The live root route card is `../AGENTS.md`.

Use this reference when:

- auditing a legacy rule from before Pack 5
- resolving a task branch that the short route card intentionally summarized
- checking whether a slimming move should become a nested `AGENTS.md`, owner doc, or validator rule

Do not treat this file as a competing root. If a preserved rule still actively governs a local directory, move or restate it at the smallest owner surface rather than re-bloating the root.

## Preserved root AGENTS.md from before Pack 5

# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-memo`.

## Purpose

`aoa-memo` is the explicit memory and recall layer of AoA.
It stores public, reviewable memory surfaces, memory-object structure,
provenance threads, salience posture, and recall-oriented contracts for bounded
agent memory behavior.

Memory matters here, but memory is not proof.
Continuity support matters here, but memory alone is not proof of identity,
agency, or current truth.

## Owns

This repository is the source of truth for:

- memory-object structure
- episodic, semantic, and provenance memory distinctions
- recall posture and retrieval-oriented memory wording
- temporal relevance, salience, and memory-temperature language
- memory-layer metadata and generated memory surfaces
- doctrine about what explicit memory is and is not
- writeback, chronicle, and recurrence-support seams when those are explicitly defined in repo-owned docs

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- bounded execution workflows in `aoa-skills`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- role contracts, progression doctrine, or self-agent checkpoint policy in `aoa-agents`
- scenario composition or questline sovereignty in `aoa-playbooks`
- derived substrate semantics in `aoa-kag`
- derived observability or movement summaries in `aoa-stats`

Memory may reference other layers.
It does not replace them.

## Core rules

Memory is not proof.

A memory object may preserve a past event, judgment, or trace.
It does not automatically make that content authoritative, current, or
sufficient.

If the task requires source meaning, proof, or execution logic, route to the
canonical neighboring repository instead of recreating it here.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `ROADMAP.md`
3. `CHARTER.md`
4. `docs/BOUNDARIES.md`
5. `docs/MEMORY_MODEL.md`
6. the target source file you plan to edit
7. any affected generated memory catalogs, capsules, registry outputs, or examples

Then branch by task:

- object canon, trust posture, lifecycle, or temperatures:
  `docs/MEMORY_OBJECT_PROFILES.md`,
  `docs/MEMORY_TRUST_POSTURE.md`,
  `docs/MEMORY_TEMPERATURES.md`,
  `docs/LIFECYCLE.md`, and
  `docs/NARRATIVE_CORE_CONTRACT.md`
- failure-lesson or recovery-pattern surfaces:
  `docs/FAILURE_LESSON_MEMORY.md`,
  `docs/FAILURE_LESSON_RECALL.md`,
  `docs/RECOVERY_PATTERN_MEMORY.md`, and
  `docs/RECOVERY_PATTERN_RECALL.md`
- writeback, quest chronicle, runtime support, or recurrence seams:
  `docs/WITNESS_TRACE_CONTRACT.md`,
  `docs/WRITEBACK_TEMPERATURE_POLICY.md`,
  `docs/QUEST_CHRONICLE_WRITEBACK.md`,
  `docs/RUNTIME_WRITEBACK_SEAM.md`,
  `docs/MEMORY_READINESS_BOUNDARY.md`,
  `docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md`,
  `docs/AGENT_MEMORY_POSTURE_SEAM.md`, and
  `docs/PLAYBOOK_MEMORY_SCOPES.md`
- bridge, export, or guardrail surfaces:
  `docs/KAG_TOS_BRIDGE_CONTRACT.md`,
  `docs/KAG_SOURCE_EXPORT.md`,
  `docs/MEMORY_EVAL_GUARDRAILS.md`,
  `docs/OPERATIONAL_BOUNDARY.md`, and
  `docs/ROUTING_MEMORY_ADOPTION.md`

If you are working inside `schemas/`, `examples/`, `generated/`, or `scripts/`,
also read the nested `AGENTS.md` in that directory.

## Primary objects

The most important objects in this repository are:

- memory object definitions
- provenance-thread and witness-trace support surfaces
- recall / retrieval-oriented docs and examples
- generated memory catalogs, capsules, sections, and registry outputs
- writeback, chronicle, and runtime-support docs and generated surfaces
- docs that define salience, freshness, temporal posture, and bridge/export shape

## Hard NO

Do not:

- treat memory as proof
- store secret notes, tokens, or private infrastructure details
- turn memory objects into workflow definitions or role contracts
- turn memory into routing logic or a hidden graph platform
- silently collapse episodic, semantic, and provenance distinctions
- write memory objects that pretend to be current truth without explicit temporal and provenance framing
- let quest-chronicle or writeback surfaces become live quest sovereignty or hidden ledgers
- use memory wording to imply self-agent identity without explicit evidence and temporal framing

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what memory surface is changing
- which memory class is affected
- what provenance or temporal risk exists
- whether writeback, chronicle, or recurrence support seams are changing
- whether neighboring repositories may be affected

### DIFF

Keep the change focused.
Do not mix unrelated cleanup into a memory change unless it is necessary for
repository integrity.

### VERIFY

Run the validation commands documented in `README.md`.

Use the core validation set when source or generated surfaces change:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
python -m pytest -q tests
```

Confirm that:

- the memory object or support surface remains explicit and reviewable
- provenance is still visible
- temporal posture is still coherent
- no wording overclaims proof, current truth, or authority
- writeback and chronicle surfaces remain bounded and non-sovereign
- generated outputs remain aligned if the task touches metadata or registry surfaces

### REPORT

Summarize:

- what memory surfaces changed
- whether semantics changed or only metadata changed
- whether provenance, temporal posture, or writeback posture changed
- what validation was run
- any neighboring repo follow-up likely needed

## Validation

Do not claim checks you did not run.
