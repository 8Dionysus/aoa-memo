# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-memo`.

## Purpose

`aoa-memo` is the explicit memory and recall layer of AoA. It stores public, reviewable memory surfaces, memory-object structure, provenance threads, salience posture, and recall-oriented contracts for bounded agent memory behavior.

This repository is for explicit memory meaning, not for proof, routing, or workflow execution.

## Owns

This repository is the source of truth for:

- memory-object structure
- episodic, semantic, and provenance memory distinctions
- recall posture and retrieval-oriented memory wording
- temporal relevance, salience, and memory-temperature language
- memory-layer metadata and generated memory surfaces
- doctrine about what explicit memory is and is not

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- bounded execution workflows in `aoa-skills`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- scenario composition in `aoa-playbooks`
- derived substrate semantics in `aoa-kag`

Memory may reference other layers. It does not replace them.

## Core rule

Memory is not proof.

A memory object may preserve a past event, judgment, or trace. It does not automatically make that content authoritative, current, or sufficient. If the task requires source meaning, proof, or execution logic, route to the canonical neighboring repository instead of recreating it here.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. the relevant memory model or object/profile docs referenced there
3. the target source file you plan to edit
4. any affected generated memory catalogs, capsules, registry outputs, or examples
5. adjacent docs if the task touches provenance, routing, agents, playbooks, or KAG export posture

If you are working inside `schemas/`, `examples/`, `generated/`, or `scripts/`, also read the nested `AGENTS.md` in that directory.

## Primary objects

The most important objects in this repository are:

- memory object definitions
- provenance-thread and witness-trace support surfaces
- recall / retrieval-oriented docs and examples
- generated memory catalogs, capsules, sections, and registry outputs
- docs that define salience, freshness, temporal posture, and bridge/export shape

## Hard NO

Do not:

- treat memory as proof
- store secret notes, tokens, or private infrastructure details
- turn memory objects into workflow definitions or role contracts
- turn memory into routing logic or a hidden graph platform
- silently collapse episodic, semantic, and provenance distinctions
- write memory objects that pretend to be current truth without explicit temporal and provenance framing

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what memory surface is changing
- which memory class is affected
- what provenance or temporal risk exists
- whether neighboring repositories may be affected

### DIFF

Keep the change focused. Do not mix unrelated cleanup into a memory change unless it is necessary for repository integrity.

### VERIFY

Confirm that:

- the memory object remains explicit and reviewable
- provenance is still visible
- temporal posture is still coherent
- no wording overclaims proof, current truth, or authority
- generated outputs remain aligned if the task touches metadata surfaces

### REPORT

Summarize:

- what memory surfaces changed
- whether semantics changed or only metadata changed
- whether provenance or temporal posture changed
- what validation was run
- any neighboring repo follow-up likely needed

## Validation

Run the validation commands documented in `README.md`.

If catalogs, capsules, or other generated memory surfaces changed, regenerate and validate them before finishing. `python scripts/validate_memo.py` also checks the local guidance surfaces in `schemas/`, `examples/`, `generated/`, and `scripts/`.

Do not claim checks you did not run.
