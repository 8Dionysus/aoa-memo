# Adoption Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Adoption boundary | [ADOPTION_MEMORY_BOUNDARIES](./docs/ADOPTION_MEMORY_BOUNDARIES.md), [ADOPTION_FORGETTING_LAW](./docs/ADOPTION_FORGETTING_LAW.md) | names what memory may preserve before adoption proof |
| Revision and retention pressure | [ADOPTION_REVISION_LEDGER](./docs/ADOPTION_REVISION_LEDGER.md), [ADOPTION_RETENTION_MEMORY](./docs/ADOPTION_RETENTION_MEMORY.md) | keeps adoption changes temporal and reviewable |
| Scar and routing adoption | [ADOPTION_SCAR_WRITEBACK](./docs/ADOPTION_SCAR_WRITEBACK.md), [ROUTING_MEMORY_ADOPTION](./docs/ROUTING_MEMORY_ADOPTION.md) | keeps scar and router-facing adoption candidate-only |

## Interface

Inputs are reviewed source refs and adoption candidates. Outputs are bounded
memo surfaces and owner handoff routes.
