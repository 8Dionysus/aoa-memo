# AGENTS.md

## Applies To

This card applies to `mechanics/operational-gate/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
operational-gate memo mechanic.

It is not a release authority lane, runtime incident system, proof bundle,
service health monitor, role policy lane, route dispatcher, stats source, ToS
write surface, or legacy route.

## Route Stack

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

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
- Keep operational-gate technical artifacts in the nearest operational-gate
  part unless `mechanics/ARTIFACT_TOPOLOGY.md` proves a shared root contract.
- Keep retention outcomes with retention and writeback return lanes with
  writeback unless this package only gates memory admission.
- Do not preserve old flat docs-root aliases as active routes.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_memo.py
python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/post-release-boundaries/tests
```

## Closeout

Report active operational-gate docs changed, whether part-local contract refs
changed, whether artifact placement changed, and whether stronger owners remain
outside `aoa-memo`.
