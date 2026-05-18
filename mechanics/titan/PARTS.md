# Titan Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Core memory posture | [TITAN_MEMORY_POSTURE](./docs/TITAN_MEMORY_POSTURE.md), [TITAN_MEMORY_LOOM_POSTURE](./docs/TITAN_MEMORY_LOOM_POSTURE.md), [TITAN_RECALL_CANDIDATE_POLICY](./docs/TITAN_RECALL_CANDIDATE_POLICY.md), [TITAN_REMEMBRANCE_SOURCE_REF_POLICY](./docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md) | keeps Titan recall and source refs explicit without granting write authority |
| Closeout and digest posture | [TITAN_BRIDGE_MEMORY_POSTURE](./docs/TITAN_BRIDGE_MEMORY_POSTURE.md), [TITAN_CLOSEOUT_MEMORY_POSTURE](./docs/TITAN_CLOSEOUT_MEMORY_POSTURE.md), [TITAN_CONSOLE_MEMORY_DIGEST](./docs/TITAN_CONSOLE_MEMORY_DIGEST.md) | keeps bridge, closeout, and console memory proposals bounded |
| Specialized policy | [TITAN_AUDIT_MEMORY_POLICY](./docs/TITAN_AUDIT_MEMORY_POLICY.md), [TITAN_PERSONALITY_MEMORY_POLICY](./docs/TITAN_PERSONALITY_MEMORY_POLICY.md), [TITAN_SWARM_MEMORY_POLICY](./docs/TITAN_SWARM_MEMORY_POLICY.md) | keeps audit, personality, and swarm memory posture reviewable |

## Interface

Inputs are reviewed source refs, public-safe candidates, digest notes, and owner
confirmations. Outputs are bounded memo docs, schema/example refs, tests, and
clear stronger-owner routes.
