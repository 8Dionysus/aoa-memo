# Readiness Boundary Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Memory readiness boundary | [MEMORY_READINESS_BOUNDARY](./docs/MEMORY_READINESS_BOUNDARY.md) | maps high-pressure memory readiness into existing objects and stronger owner routes |

## Mechanic-Local Technical Contracts

The readiness-boundary schema, example, and tests live with the package because
they define this mechanic:

| Contract | Artifact Surface |
|---|---|
| Readiness boundary contract | `mechanics/readiness-boundary/schemas/memory_readiness_boundary_contract.schema.json`, `mechanics/readiness-boundary/examples/memory_readiness_boundary_contract.example.json` |
| Readiness boundary tests | `mechanics/readiness-boundary/tests/test_readiness_boundary_mechanic.py` |

## Interface

Inputs are high-pressure memory refs, reviewed memory objects, bounded recall
candidates, memory/canon delta refs, retention pressure, contradiction refs,
bridge candidates, and service traces.

Outputs are bounded memory-object landing guidance, owner-routed next claims,
and a contract that keeps memory gate, retention boundary, and writeback
boundary separate.
