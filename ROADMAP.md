# AoA Memo Roadmap

This roadmap tracks the bootstrap and early shaping of the AoA memory layer.

## Current phase

`aoa-memo` is in bootstrap.
The current goal is not to build a giant memory engine immediately.
The goal is to define what the memory layer is for, what it owns, and what it must not silently absorb.

## Phase 1: memory layer definition

Goals:
- define `aoa-memo` as the canonical memory and recall layer within AoA
- make the difference between memory, proof, execution, and routing explicit
- establish a compact memory registry and a minimal validator

Exit signals:
- the repository role is clear
- memory-layer boundaries are documented
- a compact machine-readable registry exists

## Phase 2: first memory object discipline

Goals:
- define the first public shape for memory objects
- distinguish at least basic classes such as episodic memory, semantic memory, and provenance thread surfaces
- keep object forms compact enough to review

## Phase 3: recall and provenance surfaces

Goals:
- make recall pathways explicit
- preserve provenance surfaces where possible
- support bounded retrieval and historical traceability without pretending to be proof

## Phase 4: salience and temporal shaping

Goals:
- introduce bounded notions of salience, freshness, and temporal relevance
- make memory prioritization more legible to humans and smaller models

## Phase 5: federation integration

Goals:
- connect `aoa-memo` cleanly to `aoa-routing`
- connect memory surfaces to `aoa-agents`
- preserve clear boundaries relative to `aoa-techniques`, `aoa-skills`, and `aoa-evals`

## Standing discipline

Across all phases:
- keep memory explicit
- preserve provenance where possible
- do not confuse memory with proof
- do not let the memory layer turn into a dump of untyped context
