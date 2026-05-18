# Governance Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Governance boundary | [GOVERNANCE_MEMORY_BOUNDARIES](./docs/GOVERNANCE_MEMORY_BOUNDARIES.md), [GOVERNANCE_RUNTIME_MEMORY_BOUNDARIES](./docs/GOVERNANCE_RUNTIME_MEMORY_BOUNDARIES.md) | memo-side governance and runtime-governance memory stop-lines |
| Federation boundary | [FEDERATION_MEMORY_BOUNDARIES](./docs/FEDERATION_MEMORY_BOUNDARIES.md), [FEDERATION_FORGETTING_LAW](./docs/FEDERATION_FORGETTING_LAW.md) | cross-repo pattern memory, forgetting, and harvest gates without promotion authority |
| Install and certification boundary | [INSTALLATION_MEMORY_BOUNDARIES](./docs/INSTALLATION_MEMORY_BOUNDARIES.md), [CERTIFICATION_MEMORY_BOUNDARIES](./docs/CERTIFICATION_MEMORY_BOUNDARIES.md) | install/certification memory facts without release approval or proof |
| Precedent and stay order | [POLICY_PRECEDENT_MEMORY](./docs/POLICY_PRECEDENT_MEMORY.md), [PRECEDENT_MEMORY_INDEX](./docs/PRECEDENT_MEMORY_INDEX.md), [STAY_ORDER_MEMORY](./docs/STAY_ORDER_MEMORY.md) | recallable policy precedent and stay-order memory without forced adoption |

## Interface

Inputs are governance decisions, federation boundary signals, installation and
certification refs, policy precedent candidates, and stay-order memory refs.

Outputs are bounded authority-boundary memory surfaces and owner-routed next
claims. Stronger owners decide council authority, proof, release approval,
source-owner consent, Tree-of-Sophia writes, runtime governance, and live
policy execution.
