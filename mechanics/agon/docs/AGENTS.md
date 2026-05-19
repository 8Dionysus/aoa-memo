# AGENTS.md

## Guidance for `mechanics/agon/docs/`

`mechanics/agon/docs/` owns active mechanic-owned doctrine and support notes
for the Agon memo mechanic.

This docs route keeps Agon candidate memory, bridge, retention, evidence, and
stage landing notes together while preserving the same boundary:
`aoa-memo` remembers candidate context and source refs; it does not run trials,
write durable scars, mutate rank, decide verdicts, or promote Tree-of-Sophia
canon.

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

Start with:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/ARTIFACT_TOPOLOGY.md`
4. `mechanics/agon/AGENTS.md`
5. `mechanics/agon/README.md`
6. `mechanics/agon/PARTS.md`
7. `mechanics/agon/OWNER_MAP.md`
8. `mechanics/agon/PROVENANCE.md`
9. this file
10. `mechanics/agon/docs/README.md`
11. the target Agon doc plus matching config, schema, generated registry,
   manifest, quest, and test surfaces when they exist

## Boundaries

- Keep Agon memory surfaces candidate-only unless a stronger owner has already
  provided reviewed source evidence.
- Do not move verdict law, arena execution, rank mutation, durable scar writes,
  stats authority, KAG promotion, or authored canon here.
- Route proof to `aoa-evals`, role or rights policy to `aoa-agents`, graph lift
  to `aoa-kag`, source doctrine to `Agents-of-Abyss` or `Tree-of-Sophia`, and
  runtime storage to `abyss-stack`.
- Keep links and manifests pointed at `mechanics/agon/docs/`, not the old flat
  docs-root or transitional docs-district paths.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, tests,
  manifests, or quests.
- When an Agon source family changes, keep matching config, schema, generated
  registry, manifest, quest, example, script, and test companions aligned
  rather than editing the doc as an isolated note.

## Validation

For Agon mechanic-doc edits, run the mechanics gate and the affected Agon
validators:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
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
python scripts/release/release_check.py
```

## Closeout

Report which Agon source family changed, whether any config, generated,
manifest, quest, schema, example, or test surfaces changed, and whether any
old Agon docs-root or docs-district reference remains outside allowed
provenance.
