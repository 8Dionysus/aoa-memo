# AGENTS.md

## Guidance for `mechanics/agon/docs/`

`mechanics/agon/docs/` owns active mechanic-owned doctrine and support notes
for the Agon memo mechanic.

This docs route keeps Agon candidate memory, bridge, retention, evidence, and
wave landing notes together while preserving the same boundary:
`aoa-memo` remembers candidate context and source refs; it does not run trials,
write durable scars, mutate rank, decide verdicts, or promote Tree-of-Sophia
canon.

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

## Validation

For Agon mechanic-doc edits, run the mechanics gate and the affected Agon
validators:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agon_memo_prebindings.py
python scripts/validate_agon_epistemic_memo_bridge.py
python scripts/validate_agon_kag_memo_evidence_package_registry.py
python scripts/validate_agon_mechanical_trial_memo_intakes.py
python scripts/validate_agon_retention_rank_memo_bridge.py
python scripts/validate_agon_slc_memo_bridge_registry.py
python scripts/validate_agon_sophian_memo_evidence_registry.py
python scripts/validate_agon_vds_memo_bridge.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report which Agon source family changed, whether any config, generated,
manifest, quest, schema, example, or test surfaces changed, and whether any
old Agon docs-root or docs-district reference remains outside allowed
provenance.
