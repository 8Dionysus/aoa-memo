# KAG ToS Bridge Contract

## Purpose

This document defines the memo-side bridge contract for KAG-oriented and ToS-linked memory exports.

It exists so `aoa-memo` can expose bounded bridge faces without becoming a graph engine or rewriting source-authored ToS meaning.

The current recall entrypoints for this surface are `examples/recall_contract.lineage.json` and `examples/recall_contract.router.lineage.json`.

## Companion surfaces

This memo-side contract works beside:

- `aoa-kag/docs/BRIDGE_CONTRACTS.md` for derived bridge coordination
- `docs/KAG_SOURCE_EXPORT.md` for the source-owned memo donor export that stays
  narrower than the current bridge faces
- `aoa-kag/schemas/bridge-envelope.schema.json` and `aoa-kag/examples/aoa_tos_bridge_envelope.example.json` for the shared cross-repo linkage object
- `schemas/bridge.schema.json` for the memo-side bridge object
- `schemas/memory_chunk_face.schema.json` and `schemas/memory_graph_face.schema.json` for downstream export faces

## Core Rule

Write the memory event once.
Export bridge faces later.

The memory object remains the reviewable authored/core surface.
Chunk and graph faces remain bridge-oriented handoff surfaces rather than replacements for the source memory object.
The source-owned memo KAG export remains a separate tiny donor capsule and does
not replace those faces.

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

## Shared bridge envelope

Strict first-wave closure now also points to one shared envelope at the KAG layer.

That envelope keeps only shared linkage:

- which stronger source class leads
- which supporting source joins the bridge
- which ToS refs and memo refs the bridge depends on
- which retrieval, chunk-face, and graph-face surfaces are the current bounded faces

The envelope is not a second memo object and not a second graph payload.
It exists so memo-side and KAG-side bridge faces can be inspected together without duplicating their bodies.

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

The bridge example keeps an explicit `shared_envelope_ref` back to the KAG-owned linkage surface.
The current source-owned memo export points at the same donor bridge object, but
it remains publish-only until a later federation activation package widens the
live spine deliberately.

## What This Contract Does Not Do

This contract does not:

- define the normalized KAG substrate
- rewrite ToS node meaning inside memo
- treat graph-facing candidates as proof
- turn provenance threads into a graph database
- authorize downstream lifts without explicit consumer review
