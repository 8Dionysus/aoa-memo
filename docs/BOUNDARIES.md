# Memory Layer Boundaries

This document records the most important ownership boundaries for `aoa-memo`.

## Rule 1: memory owns recall, not everything remembered

`aoa-memo` should own memory-layer meaning such as:
- memory objects
- recall handles
- provenance threads
- temporal relevance surfaces
- salience-oriented memory surfaces

It should not become the default dumping ground for any information that does not yet have a home.

## Rule 2: memory is not proof

A recalled event, trace, or memory object may be useful.
It is not automatically proof.

Bounded proof still belongs to eval surfaces.

## Rule 3: memory is not reusable practice canon

A remembered success or failure may inspire a technique.
That does not make the memory object itself a technique.

Reusable practice still belongs to `aoa-techniques`.

## Rule 4: memory is not execution

A remembered workflow or prior agent run may inform action.
It does not replace the bounded workflow surface.

Execution still belongs to `aoa-skills`.

## Rule 5: memory is not routing

Memory can support navigation, but dispatch decisions should remain routing-layer work.

Cross-repo navigation belongs to `aoa-routing`.

## Rule 6: provenance matters

A memory object should preserve where it came from as clearly as possible.
That does not require perfect completeness, but it should not silently erase origin context.

## Rule 7: keep memory object shapes reviewable

If memory surfaces become too vague, too implicit, or too magical, the layer will stop being trustworthy.
Compactness and explicitness matter.

## Compact rule

`aoa-memo` should help AoA remember without becoming a fog that blurs every other layer.
