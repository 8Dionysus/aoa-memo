# KAG Source Export

## Purpose

This document defines the source-owned memo export that `aoa-kag` may read as a
bounded donor surface.

It does not turn `aoa-memo` into a graph substrate and it does not activate the
memo export inside the live KAG federation spine by itself.

## Core Rule

Publish one reviewed bridge-bearing memo object as a source-owned tiny export.

The export should guide `aoa-kag` toward the memo-owned bridge object, its
capsule entry surface, and its bounded full-section handles without pretending
that the export is already normalized graph truth.

## Current Tiny Donor

The first source-owned memo donor stays intentionally narrow:

- `owner_repo`: `aoa-memo`
- `kind`: `bridge`
- `object_id`: `memo.bridge.2026-03-23.tos-lineage-kag-candidate`
- `object_bundle`: `memo/objects/bridges/2026/tos-lineage-kag-candidate/object.json`
- `entry_surface`: `generated/memory-objects/memory_object_capsules.json`
- `match_key`: `id`
- `source_kind`: `reviewed_corpus`

This keeps the export aligned with the current memo-side bridge candidate that
already preserves provenance, Tree-of-Sophia refs, and KAG lift posture.
The older bridge example remains a teaching and regression fixture, not the
durable donor object.

## What The Export Must Keep

The current tiny export keeps:

- one primary question for the bridge-bearing donor
- one short and one medium summary
- one primary source input from `aoa-memo`
- one supporting source input from `Tree-of-Sophia`
- the reviewed corpus object bundle for the current donor bridge
- the capsule entry surface for the current donor object
- the canonical four section handles from the bridge object
- a narrow direct-relation trio back to the reviewed claim, source episode, and
  ToS fragment
- provenance and non-identity notes that keep the export weaker than source
  truth

## Relationship To Bridge Faces

The source-owned export is complementary to the existing memo bridge faces:

- `memory_chunk_face` stays the compact inspection face
- `memory_graph_face` stays the downstream associative face
- `kag_export.min.json` stays the source-owned donor capsule for bounded KAG
  readiness

Those surfaces should agree on the donor object.
They should not duplicate ownership or replace one another.
Teaching fixtures may still demonstrate the bridge shape, but the source-owned
donor export should point at the reviewed corpus bundle.

## Non-Activation Boundary

Publishing the export does not yet mean:

- `aoa-kag` consumes it inside the live `federation_spine`
- `aoa-sdk` gets a new live `kag_view`
- memo becomes graph truth
- bridge candidates become normalized substrate facts

This tranche is publish-only plus consumer readiness.

## One-Line Rule

`aoa-memo` may publish one source-owned bridge export for `aoa-kag`, but the
export remains a guide to source rather than a live graph activation.
