# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

It exists to make memory explicit, reviewable, and bounded.

This repository is not the main home of reusable techniques, agent workflows, or proof surfaces.
Its role is different: it should hold memory-oriented objects and contracts that help agents and humans recall, route, and reuse prior work without confusing memory with truth.

## Start here

If you are new to this repository, use this path:

1. Read [CHARTER](CHARTER.md) for the role and boundaries of the memory layer.
2. Read [docs/MEMORY_MODEL](docs/MEMORY_MODEL.md) for the conceptual model.
3. Read [docs/BOUNDARIES](docs/BOUNDARIES.md) for ownership rules.
4. Read [ROADMAP](ROADMAP.md) for the current direction.

## What this repository is for

`aoa-memo` should own memory-layer meaning about:
- memory objects
- recall surfaces
- provenance threads
- temporal relevance
- salience and memory-temperature surfaces
- memory-oriented retrieval contracts

It is the right place for:
- memory layer definitions
- recall and provenance guidance
- compact memory registries
- memory object schemas and validation
- boundaries between memory, proof, and execution

## What this repository is not for

This repository should not absorb primary meaning from neighboring AoA layers.

It should not become the main home for:
- reusable techniques
- skill bundles
- eval bundles
- routing surfaces as such
- infrastructure implementation details
- generic notes with no memory contract

Memory is valuable, but it is not the same as technique, workflow, or proof meaning.

## Relationship to the AoA federation

Within AoA:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns bounded proof meaning
- `aoa-routing` should own dispatch and navigation surfaces
- `aoa-memo` should own memory and recall meaning
- `aoa-agents` should eventually own role and persona meaning

## Local validation

This repository includes a compact machine-readable memory-layer registry at:
- `generated/memo_registry.min.json`

To validate the current memory-layer surface locally, run:

```bash
python scripts/validate_memo.py
```

## Current status

`aoa-memo` is in bootstrap.
The goal of this first public baseline is to define the role, boundaries, and first machine-readable memory-layer surface without overbuilding the repository too early.

## Principles

- memory should stay explicit and reviewable
- recall should preserve provenance where possible
- temporal and salience surfaces should stay bounded
- memory must not silently replace proof
- new memory power should become a clear layer, not a fog of context

## License

Apache-2.0
