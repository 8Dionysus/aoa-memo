# Memo Mechanic Artifact Topology

## Purpose

Memo mechanics are not documentation archives only.

This surface explains where mechanic-adjacent schemas, examples, config,
generated companions, scripts, tests, manifests, and quest rules should live as
the mechanics tree matures.

It owns placement law only. It does not replace package cards, source docs,
schema contracts, generated indexes, or release validation.

## Root Technical Districts

Root technical districts remain valid when an artifact is repo-wide, public
contract-shaped, or shared across multiple memory families:

| District | Root-owned when |
|---|---|
| `schemas/` | the contract is part of the public memory-object or support-object canon |
| `examples/` | the example teaches public-safe object shape across more than one mechanic |
| `config/` | the input config drives repo-wide builders or validators |
| `generated/` | the output is a compact public companion consumed outside one package |
| `scripts/` | the builder or validator is part of the release gate or shared contract lane |
| `tests/` | the regression protects repo-wide behavior or cross-district references |
| `manifests/` | the recurrence manifest is a public component contract rather than package-local lore |
| `quests/` | the obligation belongs in the public quest store and should survive the current diff |

Root technical districts must not keep convenience aliases for mechanic-owned
source docs. Route to `mechanics/<slug>/docs/` directly.

## Mechanic Artifact Lane

Use a mechanic-local artifact home when the artifact only makes sense inside
one mechanic's owner boundary:

```text
mechanics/<slug>/
  config/
  generated/
  schemas/
  examples/
  scripts/
  tests/
```

If a mechanic later grows functioning parts, use the nearest part-local home
instead:

```text
mechanics/<slug>/parts/<part>/
  config/
  generated/
  schemas/
  examples/
  scripts/
  tests/
```

Package-local artifact homes must still follow the same stop-lines as the
mechanic card. A package-local artifact does not become proof, routing logic,
runtime storage, role authority, KAG substrate truth, or owner acceptance.

## Current Retention Rule

The first mechanics migration intentionally kept many schemas, examples,
generated companions, scripts, and tests in root technical districts because
they still participate in repo-wide validation and public contract surfaces.

Examples:

- Antifragility schemas, examples, generated object surfaces, and tests remain
  in root technical districts while they define public failure-lesson and
  recovery-pattern object contracts.
- Agon config, schemas, generated registries, manifests, quests, validators,
  and tests remain in root technical districts while they are public component
  contracts and release-gate companions.
- Titan schemas, examples, and tests remain in root technical districts while
  they define public remembrance and recall candidate contracts.
- adoption schemas and examples remain in `schemas/` and `examples/` while
  they teach public memory-object support contracts beyond one package.
- governance tests remain in `tests/` while they protect the public mechanics
  index and owner-boundary expectations.
- writeback generated companions such as `runtime_writeback_targets`,
  `runtime_writeback_intake`, and `growth_refinery_writeback_lanes` remain in
  `generated/` while they are release-gate companions for external consumers.
- retention examples remain in `examples/` while they validate public-safe
  audit, office, and post-release memory shapes.

This is a retention rule, not a permanent claim. When an artifact becomes
single-mechanic-owned and no longer needs a root technical lane, move it into
the package with callers, validators, generated outputs, and tests updated in
the same change.

## Move Rule

Before moving a root technical artifact into a mechanic:

1. identify the mechanic and stronger owner split
2. confirm the artifact is not a repo-wide public contract
3. add or update the nearest package or part `AGENTS.md`
4. update callers, docs, tests, builders, and generated companions
5. remove root aliases rather than preserving duplicate active paths
6. update `config/memo_mechanics.json` or another source map only when it owns
   the changed index
7. run the narrow mechanic validators before the broad release gate

## Legacy Rule

Legacy preserves placement history and provenance. It is not an artifact
parking lot.

Do not put active schemas, examples, generated outputs, scripts, or tests under
`legacy/` unless they are intentionally preserved as old evidence and are
indexed as legacy.

## Validation

Executable validation commands live in [mechanics/AGENTS](AGENTS.md#validation).

For release-bound artifact placement changes, run:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
