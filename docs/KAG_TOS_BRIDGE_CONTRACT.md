# KAG ToS Bridge Contract

## Purpose

This document defines the memo-side bridge contract for KAG-oriented and ToS-linked memory exports.

It exists so `aoa-memo` can expose bounded bridge faces without becoming a graph engine or rewriting source-authored ToS meaning.

The current recall entrypoints for this surface are `examples/recall_contract.lineage.json` and `examples/recall_contract.router.lineage.json`.

## Core Rule

Write the memory event once.
Export bridge faces later.

The memory object remains the reviewable authored/core surface.
Chunk and graph faces remain bridge-oriented handoff surfaces rather than replacements for the source memory object.

## Chunk Face Contract

The chunk face is the bounded inspection surface for smaller models, routers, and human review.

It should preserve:

- the source memory id
- the recall mode that justified the export
- compact capsule text
- section refs for deeper opening
- source refs and fragment refs where available
- provenance thread linkage when known
- review state and temperature posture
- strongest next sources for deeper inspection

The current schema-backed chunk-face surface is:

- `schemas/memory_chunk_face.schema.json`
- `examples/memory_chunk_face.bridge.example.json`

## Graph Face Contract

The graph face is the downstream associative handoff surface for `aoa-kag` and related consumers.

It should preserve:

- the source memory id
- provenance thread ids
- entity and concept refs
- relation candidates rather than normalized graph truth
- ToS refs
- time window posture
- `kag_lift_status`
- strongest authored refs for backward inspection

The current schema-backed graph-face surface is:

- `schemas/memory_graph_face.schema.json`
- `examples/memory_graph_face.bridge.example.json`

## ToS Bridge Guidance

When a memo object points toward Tree of Sophia, it should do so by reference rather than by replacement.

Use the current bridge posture like this:

- `tos_refs` should point to nodes, fragments, concepts, or lineages
- `kag_lift_status` should say whether a lift is absent, candidate, lifted, or blocked
- source refs should preserve the authored surface that the bridge depends on
- provenance threads should preserve the bounded local chain that produced the bridge

A bridge may connect memo to ToS or KAG-facing work.
It should not become a silent substitute for either one.

## End-to-End Flow

The current end-to-end flow is:

1. an `episode` records the ToS inspection or interpretation event
2. a `claim` consolidates bounded meaning from that event and stronger source refs
3. a `bridge` connects the claim to ToS refs and KAG lift posture
4. a chunk face exposes bounded inspection material
5. a graph face exposes downstream relation candidates
6. `aoa-kag` decides whether and how to normalize the lift downstream

The current example bundle for this flow is:

- `examples/episode.tos-interpretation.example.json`
- `examples/claim.tos-bridge-ready.example.json`
- `examples/bridge.kag-lift.example.json`
- `examples/provenance_thread.kag-lift.example.json`
- `examples/memory_chunk_face.bridge.example.json`
- `examples/memory_graph_face.bridge.example.json`
- `examples/recall_contract.lineage.json`
- `examples/recall_contract.router.lineage.json`

## What This Contract Does Not Do

This contract does not:

- define the normalized KAG substrate
- rewrite ToS node meaning inside memo
- treat graph-facing candidates as proof
- turn provenance threads into a graph database
- authorize downstream lifts without explicit consumer review
