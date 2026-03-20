# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-memo`.

## Purpose

`aoa-memo` is the explicit memory and recall layer of AoA.

It stores public, reviewable memory surfaces, memory-object structure, provenance threads, salience posture, and recall-oriented contracts for bounded agent memory behavior.

This repository is for explicit memory meaning, not for proof, routing, or workflow execution.

## Owns

This repository is the source of truth for:

- memory-object structure
- episodic / semantic / provenance memory distinctions
- recall posture and retrieval-oriented memory wording
- temporal relevance and salience language at the memory layer
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
- derived knowledge substrate semantics in `aoa-kag`

Memory may reference other layers. It does not replace them.

## Core rule

Memory is not proof.

A memory object may preserve a past event, judgment, or trace.
It does not automatically make that content authoritative, current, or sufficient.

If the task requires source meaning, proof, or execution logic, route to the canonical neighboring repository instead of recreating it here.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. any memory object schema or registry docs referenced by the README
3. the target source file you plan to edit
4. any generated memory catalogs, capsules, or registry outputs affected by the task
5. adjacent README surfaces if the task touches provenance, routing, or agents

## Primary objects

The most important objects in this repository are:

- memory object definitions
- provenance-thread definitions
- recall / retrieval-oriented docs
- generated memory catalogs or capsules
- docs that define salience, freshness, temporal posture, and registry shape

## Allowed changes

Safe, normal contributions include:

- refining memory-object wording
- tightening distinctions between memory classes
- improving provenance phrasing
- improving temporal or salience caveats
- fixing metadata drift between source files and generated outputs
- adding a new bounded memory-object type when it clearly belongs to the explicit memory layer

## Changes requiring extra care

Use extra caution when:

- changing memory object classes
- changing registry or generated-surface shape
- changing wording that may affect how memory is interpreted as evidence
- changing provenance semantics
- changing temporal or freshness posture
- adding fields that imply stronger truth, confidence, or authority than the layer can honestly support

## Hard NO

Do not:

- treat memory as proof
- store secret notes, tokens, or private infrastructure details
- turn memory objects into workflow definitions
- turn memory objects into role contracts
- turn memory into routing or dispatch logic
- turn memory into a hidden knowledge graph platform
- silently collapse episodic, semantic, and provenance distinctions

Do not write memory objects that pretend to be current truth without clear temporal and provenance framing.

## Memory doctrine

A good memory change should make it easier to answer:

- what happened
- when it happened
- where it came from
- how reliable the trace is
- whether the memory is still salient or stale
- what canonical source should be inspected next if stronger grounding is needed

A bad memory change usually makes memory more absolute, less temporal, less reviewable, or more authoritative than it should be.

## Public hygiene

Assume everything here is public, inspectable, and challengeable.

Write for portability:

- keep time references explicit
- keep provenance explicit
- distinguish memory from proof
- avoid private identifiers where possible
- sanitize examples
- prefer bounded reviewable objects over vague memory prose

## Default editing posture

Prefer the smallest reviewable change.

Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.

## Contribution doctrine

Use this flow:

`PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what memory surface is changing
- which memory class is affected
- what provenance or temporal risk exists
- whether neighboring repos may be affected

### DIFF

Keep the change focused.

Do not mix unrelated cleanup into a memory change unless it is necessary for repository integrity.

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

If catalogs, capsules, or other generated memory surfaces changed, regenerate and validate them before finishing.

Do not claim checks you did not run.

## Cross-repo neighbors

Use these neighboring repositories when the task crosses boundaries:

- `aoa-routing` for routing and dispatch
- `aoa-agents` for role and memory posture at the agent layer
- `aoa-skills` for execution workflows
- `aoa-evals` for proof surfaces
- `aoa-kag` for derived knowledge substrate surfaces
- `Agents-of-Abyss` for ecosystem-level map and boundary doctrine

## Output expectations

When reporting back after a change, include:

- which memory surfaces changed
- whether semantics changed or only metadata changed
- whether provenance, salience, or temporal posture changed
- whether generated outputs changed
- what validation was run
- any neighboring repo follow-up likely needed

## Default editing posture

Prefer the smallest reviewable change.
Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.