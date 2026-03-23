# MEMORY TRUST POSTURE

## Purpose

This document hardens the trust posture contract of `aoa-memo`.

The goal is to keep trust multi-axial without turning it into a hidden proof score.
`aoa-memo` should say how a memory object should be interpreted, not pretend to settle whether the world is true.

## Core rule

Trust posture stays split across separate signals:

- `temperature` for recall activity
- `confidence` for bounded plausibility
- `authority_kind` plus `authority` for source posture
- `freshness` for currentness
- `salience` plus `salience_components` for recall pressure

These signals should not collapse into one number.

## Ordinal fields

The shipped public contract now treats these fields as ordinal numeric posture signals in the `0..1` range:

- `confidence`
- `freshness`
- `salience`

They are not proof scores.
They are bounded memo-side posture signals.

Useful reading posture:

- `0.00 - 0.24`: weak or low-pressure
- `0.25 - 0.49`: tentative
- `0.50 - 0.74`: usable but review-sensitive
- `0.75 - 0.89`: strong for the named scope
- `0.90 - 1.00`: very strong for the named scope

These bands are interpretive guidance, not automatic verdict logic.

## Authority posture

Authority remains descriptive.

The contract separates:

- `authority_kind` for a compact machine-readable class
- `authority` for a human-legible phrase that preserves nuance

The current public `authority_kind` values are:

- `human_reviewed`
- `repo_maintained`
- `source_inspection`
- `operational_observation`
- `candidate_under_review`

This is intentionally small.
It gives downstream consumers a stable class without pretending the class is the whole story.

## Freshness posture

Freshness answers:

- how current is this memory for the present question?

Freshness may fall even when the historical event remains true.
That is why freshness must stay distinct from confidence and authority.

## Salience posture

Salience answers:

- how much should this object compete for recall right now?

Salience is not truth.
It is relevance pressure.

When `salience_components` are present, they should explain why the item deserves current recall pressure.

The current component surface is:

- `novelty`
- `impact`
- `recurrence`
- `risk`

These are also ordinal `0..1` signals.

## Freeze posture

`frozen` should be harder than `confirmed`.

When an object is `frozen`, the memory object should now carry `lifecycle.freeze_basis`.
This is the explicit reason the layer considers the object stabilized.

The current public freeze bases are:

- `human_review`
- `source_boundary`
- `constitutional_seam`

This keeps frozen posture inspectable instead of magical.

## Current recall posture

Lifecycle state alone is not enough to tell a consumer how current recall should treat an object.

The shipped contract therefore keeps `lifecycle.current_recall.status` explicit:

- `preferred`
- `allowed`
- `historical`
- `withdrawn`

When contradiction must remain visible, use `lifecycle.current_recall.contradiction_refs`.

## What this document does not do

This document does not:

- create a proof verdict
- assign role rights
- define routing heuristics
- replace eval scoring in `aoa-evals`
- claim that any single trust field settles correctness

## Anti-patterns

Treat these as warnings:

- using `temperature` as a synonym for truth
- using `confidence` as if it were source authority
- using `freshness` as if it erased history
- using `salience` as if it proved correctness
- freezing an object with no visible basis

## One-line doctrine

Trust posture tells a reader how to interpret a memory object without pretending memory has become proof.
