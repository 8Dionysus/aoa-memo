# AGENTS.md

## Applies To

This card applies to `mechanics/operational-gate/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
operational-gate memo mechanic.

It is not a release authority lane, runtime incident system, proof bundle,
service health monitor, role policy lane, route dispatcher, stats source, ToS
write surface, or legacy route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

When a doc points into schemas, examples, generated surfaces, quests, scripts,
or tests, read that district's nearest `AGENTS.md` before changing the linked
artifact.

## Boundaries

- Keep operational-gate docs memory-only, evidence-linked, and
  operation-first.
- Do not claim release approval, current service health, incident root cause,
  runtime remediation, proof verdicts, role rights, route dispatch, stats
  truth, ToS runtime writes, or owner acceptance.
- Keep root technical artifacts in root districts unless
  `mechanics/ARTIFACT_TOPOLOGY.md` proves a package-local move.
- Keep retention outcomes with retention and writeback return lanes with
  writeback unless this package only gates memory admission.
- Do not preserve old flat docs-root aliases as active routes.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_memo.py
python -m pytest -q tests/test_operational_gate_mechanic.py tests/test_experience_wave5_seed_contracts.py
```

## Closeout

Report active operational-gate docs changed, whether root technical contract
refs changed, whether artifact placement changed, and whether stronger owners
remain outside `aoa-memo`.
