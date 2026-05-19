# AGENTS.md

## Applies To

This card applies to `mechanics/agon/`.

## Role

The Agon mechanic owns memo-side Agon candidate memory, source refs,
prebinding posture, evidence-package memory, bridge memory, retention/rank
memory boundaries, and stage landing notes.

It does not run Agon trials, decide verdicts, write durable scars, mutate rank,
execute retention, promote KAG substrate, publish Tree-of-Sophia canon, or own
the source Agon mechanic.

## Route Stack

- Above: root `AGENTS.md` owns repo identity and release route;
  `mechanics/AGENTS.md` owns shared mechanic package law and validators.
- Here: `README.md` is the mechanic card, `DIRECTION.md` names current
  pressure, `PARTS.md` lists active function nodes, `OWNER_MAP.md` names
  stronger owners, and `PROVENANCE.md` plus `legacy/` preserve placement
  history.
- Below: `docs/` holds active source docs, `parts/` holds functioning
  contracts and artifact homes, and `legacy/` is historical evidence only.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target
`docs/AGON_*.md` surface.

## Post-Change Review

After Agon changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- matching config, schema, generated, manifest, quest, script, example, and
  test companions
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/stage-landing-and-stop-lines/tests
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the Agon source family changed, whether legacy/provenance was
consulted, whether Agon quest follow-through stayed in `quests/agon/<state>/`,
which stronger owner route remains outside `aoa-memo`, and whether
any old Agon docs-root or docs-district reference remains outside allowed
provenance.
