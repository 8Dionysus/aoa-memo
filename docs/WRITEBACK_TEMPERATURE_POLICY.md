# WRITEBACK TEMPERATURE POLICY

## Purpose

This document defines how temperature affects memo-layer writeback and downstream bridge behavior.

It does not define ToS canon law.
It defines the memo-side gate that decides what kind of memory is ready to survive a route.

## Core rule

Not every memory object should survive as writeback.

`aoa-memo` should preserve bounded, provenance-aware memory.
It should not push every live task artifact into durable memory or downstream knowledge surfaces.

## Writeback classes

### Session-only operational memory

Typical examples:

- scratch planning notes
- ephemeral routing decisions
- unstable hypotheses
- transient retries

Default writeback posture:

- do not preserve by default
- only export as a bounded `state_capsule` when another layer must inspect the state

### Memo-surviving operational memory

Typical examples:

- episodes worth recalling later
- decisions that shape future work
- repeated failure patterns
- explicit contradiction markers

Default writeback posture:

- preserve inside `aoa-memo`
- require provenance and review posture
- do not treat this as ToS-ready canon automatically

### Bridge-ready memory

Typical examples:

- reviewed claims with clear source refs
- durable decision surfaces
- stable bridge candidates tied to a named route

Default writeback posture:

- may survive as memo objects
- may be referenced by ToS-facing or KAG-facing bridge contracts
- still require explicit provenance and current limits

## Temperature guidance

### `hot`

Default writeback:

- avoid durable writeback unless the item records a meaningful event or task checkpoint
- prefer `state_capsule` or no durable writeback

### `warm`

Default writeback:

- strongest candidate zone for episodes, decisions, and contradiction markers
- preserve when the item changes future routing, review, or handoff behavior

### `cool`

Default writeback:

- good zone for durable claims, stable summaries, and reviewed patterns
- suitable for bounded downstream bridge candidacy

### `cold`

Default writeback:

- preserve selectively for audit, lineage, or delayed recall
- do not surface by default in lightweight recall flows

### `frozen`

Default writeback:

- stable reference use only
- require explicit review before supersession

## `core` overlay guidance

If an item is `core`, it should be preserved more conservatively.

That does **not** mean it must become ToS canon.
It means the item should remain available as a stable operating axis inside AoA memory posture.

## What may bridge outward

Bridge-ready memory should usually satisfy all of these:

- clear provenance
- explicit temporal posture
- explicit review state
- bounded claim or decision shape
- route-level reason to survive beyond the originating run

Good outward candidates:

- reviewed `decision`
- stabilized `claim`
- `bridge` object with named source refs

Weak outward candidates:

- raw scratch notes
- unresolved plan fragments
- unreviewed summaries with no source boundary

## Inquiry checkpoint packs

`inquiry_checkpoint` artifacts are writeback candidates when a long-horizon route must survive a pause or relaunch.

They should preserve:

- current axis
- open contradictions
- evidence references
- memory delta
- canon delta

They should not pretend to be ToS canon or a new memory-object kind by themselves.

## Anti-patterns

- writing back every tool step as durable memo
- treating `frozen` as automatic canon
- pushing unresolved contradictions outward as settled truth
- mixing memo writeback with runtime logging doctrine
- turning ToS bridge readiness into a hidden score

## Practical rule

Before preserving writeback, ask:

1. what future route needs this memory?
2. what provenance survives?
3. what temperature is it leaving from?
4. is it only memo-facing, or actually bridge-ready?
5. what should still remain operational-only?
