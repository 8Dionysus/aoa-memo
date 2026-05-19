# Spark Lane

`.agents/spark/` is the Codex Spark fast-session lane for `aoa-memo`.

Use it when a small model can finish one bounded memory-layer scenario or
leave a portable handoff for a slower session. Spark is calibrated here as a
real-time, interruptible, lightweight coding loop for targeted audits, small
patches, narrow checks, and handoff packets. It does not author memory
doctrine, mechanic law, generated truth, proof authority, route policy, role
rights, KAG meaning, playbook composition, or runtime state.

## Core Contract

| Rule | Meaning |
|---|---|
| one scenario | choose exactly one registered scenario from `registry.json` |
| one scope | keep the memory surface and validation path small |
| done-or-handoff | finish the lane or write a handoff; do not wait for an in-session model switch |
| memory boundedness | preserve provenance, temporal posture, salience limits, and memory-is-not-proof boundaries |
| evidence | name files read, files changed, validation run, skipped checks, and remaining risk |

## Operating Route

1. Read root `AGENTS.md`.
2. Read `.agents/AGENTS.md`.
3. Read [`AGENTS.md`](AGENTS.md).
4. Choose a scenario from [`registry.json`](registry.json).
5. Read that scenario `README.md` and `PROMPT.md`.
6. Finish with a result packet or a handoff packet.

Use [`SWARM.md`](SWARM.md) only when a Spark swarm is explicitly requested.

## Scenarios

| Scenario | Use |
|---|---|
| [`memory-audit`](scenarios/memory-audit/README.md) | read-only audit of boundedness, duplicate meaning, stale paths, provenance visibility, public hygiene, and owner route |
| [`memory-refinement`](scenarios/memory-refinement/README.md) | one small source-backed patch to an existing memory surface |
| [`recall-contract-check`](scenarios/recall-contract-check/README.md) | inspect recall, retention, checkpoint, or adoption contracts for temporal and provenance clarity |
| [`generated-parity-check`](scenarios/generated-parity-check/README.md) | compare source, builder, generated companion, and validator without treating generated output as truth |
| [`mechanic-seam-scout`](scenarios/mechanic-seam-scout/README.md) | map one mechanic seam, legacy bridge, or part-local artifact route before deeper mechanic work |
| [`diff-review`](scenarios/diff-review/README.md) | review a concrete diff or PR for memory-layer risk and missed checks |
| [`registry-sync`](scenarios/registry-sync/README.md) | align Spark docs, registry, validator, tests, release gate, and generated companions |
| [`test-factory`](scenarios/test-factory/README.md) | add bounded tests for an already clear memory contract |
| [`release-prep`](scenarios/release-prep/README.md) | run a fast release-readiness pass without publishing |

## Output Homes

| Home | Role |
|---|---|
| [`handoffs/open`](handoffs/open/) | portable packets for later Spark or non-Spark sessions |
| [`handoffs/closed`](handoffs/closed/) | resolved or superseded handoff packets kept as traceable examples |
| [`results`](results/) | reusable completed Spark results worth preserving beyond chat closeout |

Ordinary closeout belongs in the conversation or pull request. Commit result or
handoff packets only when the packet helps future sessions reproduce a bounded
lane.

The registry's per-scenario `default_validation` values are validation routes,
not an instruction to run every broad repository check by default. Ordinary
Spark work should keep the loop narrow and report skipped checks honestly.
