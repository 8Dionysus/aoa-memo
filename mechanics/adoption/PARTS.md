# Adoption Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Adoption boundary | [ADOPTION_MEMORY_BOUNDARIES](./docs/ADOPTION_MEMORY_BOUNDARIES.md), [ADOPTION_FORGETTING_LAW](./docs/ADOPTION_FORGETTING_LAW.md) | names what memory may preserve before adoption proof |
| Revision and retention pressure | [ADOPTION_REVISION_LEDGER](./docs/ADOPTION_REVISION_LEDGER.md), [ADOPTION_RETENTION_MEMORY](./docs/ADOPTION_RETENTION_MEMORY.md) | keeps adoption changes temporal and reviewable |
| Scar and routing adoption | [ADOPTION_SCAR_WRITEBACK](./docs/ADOPTION_SCAR_WRITEBACK.md), [ROUTING_MEMORY_ADOPTION](./docs/ROUTING_MEMORY_ADOPTION.md) | keeps scar and router-facing adoption candidate-only |

## Part-Local Technical Contracts

Adoption schemas, examples, and regression tests live under the part that owns
their adoption pressure. They are candidate contracts, not proof of adoption or
writeback execution.

| Part | Contract | Artifact Surface |
|---|---|---|
| Adoption boundary | Duplicate memory cluster | `mechanics/adoption/parts/adoption-boundary/schemas/adoption_duplicate_memory_cluster_v1.json`, `mechanics/adoption/parts/adoption-boundary/examples/adoption_duplicate_memory_cluster.example.json` |
| Adoption boundary | Forgetting decision | `mechanics/adoption/parts/adoption-boundary/schemas/adoption_forgetting_decision_v1.json`, `mechanics/adoption/parts/adoption-boundary/examples/adoption_forgetting_decision.example.json` |
| Adoption boundary | Memory writeback candidate | `mechanics/adoption/parts/adoption-boundary/schemas/adoption_memory_writeback_v1.json`, `mechanics/adoption/parts/adoption-boundary/examples/adoption_memory_writeback.example.json` |
| Adoption boundary | Boundary contract tests | `mechanics/adoption/parts/adoption-boundary/tests/test_adoption_boundary_contracts.py` |
| Revision and retention pressure | Retention memory | `mechanics/adoption/parts/revision-and-retention-pressure/schemas/adoption_retention_memory_v1.json`, `mechanics/adoption/parts/revision-and-retention-pressure/examples/adoption_retention_memory.example.json` |
| Revision and retention pressure | Revision ledger entry | `mechanics/adoption/parts/revision-and-retention-pressure/schemas/adoption_revision_ledger_entry_v1.json`, `mechanics/adoption/parts/revision-and-retention-pressure/examples/adoption_revision_ledger_entry.example.json` |
| Revision and retention pressure | Revision/retention tests | `mechanics/adoption/parts/revision-and-retention-pressure/tests/test_revision_retention_contracts.py` |
| Scar and routing adoption | Scar writeback | `mechanics/adoption/parts/scar-and-routing-adoption/schemas/adoption_scar_writeback_v1.json`, `mechanics/adoption/parts/scar-and-routing-adoption/examples/adoption_scar_writeback.example.json` |
| Scar and routing adoption | Router-facing adoption tests | `mechanics/adoption/parts/scar-and-routing-adoption/tests/test_routing_memory_adoption.py` |

## Interface

Inputs are reviewed source refs and adoption candidates. Outputs are bounded
memo surfaces and owner handoff routes.
