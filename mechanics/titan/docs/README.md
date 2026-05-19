# Titan Memo Mechanic Docs

This directory contains source docs for the Titan memo mechanic.

The files here preserve candidate recall, source-ref, audit-memory,
remembrance, closeout, bridge, console, personality, and swarm memory posture.
They do not write memory automatically, grant role rights, prove findings,
persist private data, or replace owner-repo truth.

## Source Families

| Family | Surfaces |
|---|---|
| Recall and remembrance posture | [TITAN_MEMORY_POSTURE](TITAN_MEMORY_POSTURE.md), [TITAN_MEMORY_LOOM_POSTURE](TITAN_MEMORY_LOOM_POSTURE.md), [TITAN_RECALL_CANDIDATE_POLICY](TITAN_RECALL_CANDIDATE_POLICY.md), [TITAN_REMEMBRANCE_SOURCE_REF_POLICY](TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md) |
| Closeout and digest posture | [TITAN_BRIDGE_MEMORY_POSTURE](TITAN_BRIDGE_MEMORY_POSTURE.md), [TITAN_CLOSEOUT_MEMORY_POSTURE](TITAN_CLOSEOUT_MEMORY_POSTURE.md), [TITAN_CONSOLE_MEMORY_DIGEST](TITAN_CONSOLE_MEMORY_DIGEST.md) |
| Audit, personality, and swarm policy | [TITAN_AUDIT_MEMORY_POLICY](TITAN_AUDIT_MEMORY_POLICY.md), [TITAN_PERSONALITY_MEMORY_POLICY](TITAN_PERSONALITY_MEMORY_POLICY.md), [TITAN_SWARM_MEMORY_POLICY](TITAN_SWARM_MEMORY_POLICY.md) |

## Companion Surfaces

Titan docs currently pair with:

- `mechanics/titan/parts/recall-and-remembrance-posture/schemas/titan_remembrance_record.schema.json`
- `mechanics/titan/parts/recall-and-remembrance-posture/examples/titan_remembrance_record.example.json`
- `mechanics/titan/parts/closeout-and-digest-posture/examples/titan_bridge_memory_candidate.example.json`
- `mechanics/titan/parts/audit-personality-and-swarm-policy/examples/titan_audit_memory_candidate.example.json`
- `mechanics/titan/parts/recall-and-remembrance-posture/tests`
- `mechanics/titan/parts/closeout-and-digest-posture/tests`
- `mechanics/titan/parts/audit-personality-and-swarm-policy/tests`

When a Titan source family changes, keep source refs in part-local examples,
schemas, and tests aligned with this district.

## Stop-Lines

Titan memo surfaces may say:

- what a recall candidate must include
- what source refs are needed
- which uncertainty or owner confirmation remains
- what should be proposed during closeout

They may not say:

- that memory was durably written
- that a role right has been granted
- that a finding has proof status
- that private or sensitive data can be retained without explicit approval
- that `aoa-memo` owns Titan source doctrine

## Validation

The mechanic-doc route is pinned by:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
