# Routing Memory Adoption

## Purpose

This document defines the first router-facing neighbor-adoption package for
`aoa-memo`.

It makes the memo-side consumption flow explicit for `aoa-routing` without
moving dispatch logic, ranking policy, or truth authority into this repository.

## Core Rule

Inspect first.
Hydrate through capsules second.
Expand only when the capsule step is insufficient.

The capsule step is the compact posture layer between inspect and full section
expansion.
It is not a new recall family and not a new routing policy surface.

## Router Entry Flows

### Doctrine-first questions

Use the router-ready doctrine contracts when the router needs layer meaning,
boundary interpretation, or memo doctrine orientation:

- `examples/recall_contract.router.semantic.json`
- `examples/recall_contract.router.lineage.json`

Those contracts use this additive flow:

1. inspect ids in `generated/memory_catalog.min.json`
2. hydrate selected ids through `generated/memory_capsules.json`
3. open `generated/memory_sections.full.json` only when the capsule step is not enough

### Curated object-first lookup

Use the existing object-facing semantic or lineage contracts when the router
should inspect actual curated memory objects before leaving the memo layer:

- `examples/recall_contract.object.semantic.json`
- `examples/recall_contract.object.lineage.json`

Those contracts use the parallel additive flow:

1. inspect ids in `generated/memory_object_catalog.min.json`
2. hydrate selected ids through `generated/memory_object_capsules.json`
3. open `generated/memory_object_sections.full.json` only when the capsule step is not enough

## Join Rule

The inspect id is the join key across all three steps.

- the `id` returned by inspect is the same id used in the capsule family
- the same `id` is also the expansion key for the full section family
- no extra hydrate key or router-only lookup key is introduced here

This keeps the adoption package additive and reviewable.

## Capsule Step Expectations

The capsule step is required before full expansion when the consumer needs:

- compact recall posture
- compact trust posture
- strongest-next-source hints
- a bounded answer about whether deeper opening is necessary

If the capsule already resolves the next route safely, the router may stop
there.
If the capsule is insufficient, the router should open the matching full
sections.

## Stronger Source Escalation

Memo capsules and sections remain bounded memory surfaces.

If a route still needs stronger grounding after the capsule or section step,
the router should escalate to the strongest cited source rather than infer
proof, rights, or current truth from memo fields alone.

Typical stronger-source escalation points include:

- cited docs in `aoa-memo`
- outward refs such as `repo:aoa-routing`, `repo:aoa-agents`, `repo:aoa-kag`, or `repo:Tree-of-Sophia`
- object-level `strongest_next_source` or section-level strongest source refs

## What This Adoption Package Does Not Do

This package does not:

- add routing policy to `aoa-memo`
- define scoring or ranking inside the memo layer
- create a router-specific object-family duplicate
- replace inspect or expand surfaces with capsules
- let memo posture fields stand in for proof, rights, or runtime state

## One-line Rule

`aoa-memo` now publishes an explicit inspect -> capsule -> expand consumption
path for router-facing doctrine and curated object recall, while keeping routing
authority outside the memory layer.
