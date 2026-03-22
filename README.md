# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

It exists to make memory explicit, reviewable, and bounded.

This repository is not the main home of reusable techniques, agent workflows, or proof surfaces.
Its role is different: it should hold memory-oriented objects and contracts that help agents and humans recall, route, and reuse prior work without confusing memory with truth.

## Start here

If you are new to this repository, use this path:

1. Read [CHARTER](CHARTER.md) for the role and boundaries of the memory layer.
2. Read [docs/MEMORY_MODEL](docs/MEMORY_MODEL.md) for the conceptual model.
3. Read [docs/NARRATIVE_CORE_CONTRACT](docs/NARRATIVE_CORE_CONTRACT.md) for the authored/core-memory versus derived-memory split.
4. Read [docs/BOUNDARIES](docs/BOUNDARIES.md) for ownership rules.
5. Read [ROADMAP](ROADMAP.md) for the current direction.

For the shortest next route by intent:
- if you need the ecosystem center and layer map, go to [`Agents-of-Abyss`](https://github.com/8Dionysus/Agents-of-Abyss)
- if you need navigation and dispatch rather than memory-layer meaning, go to [`aoa-routing`](https://github.com/8Dionysus/aoa-routing)
- if you need authored practice, execution, or proof meaning, go to [`aoa-techniques`](https://github.com/8Dionysus/aoa-techniques), [`aoa-skills`](https://github.com/8Dionysus/aoa-skills), or [`aoa-evals`](https://github.com/8Dionysus/aoa-evals)
- if you need explicit role contracts and handoff posture, go to [`aoa-agents`](https://github.com/8Dionysus/aoa-agents)

## Quick route table

| repository | owns | go here when |
|---|---|---|
| `aoa-memo` | memory objects, recall surfaces, provenance threads, temporal relevance, salience, retrieval contracts | you need explicit memory-layer meaning rather than proof or execution meaning |
| `Agents-of-Abyss` | ecosystem identity, layer map, federation rules, program-level direction | you need the center and the constitutional view of AoA |
| `aoa-routing` | navigation and dispatch surfaces | you need the smallest next object rather than memory-layer semantics |
| `aoa-techniques` / `aoa-skills` / `aoa-evals` | authored practice, execution, and proof meaning | you need source-owned meaning rather than memory-layer objects |
| `aoa-agents` | role contracts, persona boundaries, handoff posture | you need actor-level contracts rather than memory surfaces |

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

This repository includes compact machine-readable memory-layer surfaces at:
- `generated/memo_registry.min.json`
- `generated/memory_catalog.min.json`
- `generated/memory_capsules.json`
- `generated/memory_sections.full.json`

To validate the current memory-layer surface locally, run:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

`validate_memo.py` checks the core memory objects, schemas, examples, and registry.
`validate_memory_surfaces.py` checks the router-facing generated doctrine surfaces and the router semantic recall contract.
`validate_lifecycle_audit_examples.py` checks lifecycle, provenance-thread, and audit-event example integrity.

## Current status

`aoa-memo` is in bootstrap.
The goal of this first public baseline is to define the role, boundaries, and first machine-readable memory-layer surface without overbuilding the repository too early.

## Principles

- memory should stay explicit and reviewable
- authored/core memory should stay distinct from derived retrieval substrate
- recall should preserve provenance where possible
- temporal and salience surfaces should stay bounded
- memory must not silently replace proof
- new memory power should become a clear layer, not a fog of context

## License

Apache-2.0
