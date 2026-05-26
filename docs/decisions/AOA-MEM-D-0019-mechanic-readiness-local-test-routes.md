# Mechanic Readiness Local Test Routes

- Decision ID: AOA-MEM-D-0019

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package, validation guard
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

Package-local mechanic tests are now part of the OS Abyss readiness story for
memo mechanics. The readiness matrix can prove that tests exist, but existence
alone is not enough for operational use: the nearest route card should tell a
future agent how to run the local package check.

Agon had package-local tests and script validators, but its validation route did
not name the local pytest command. Other mechanic packages already exposed the
same command shape.

## Decision

`generated/memo_mechanic_readiness.min.json` now includes a `local-test-route`
check.

When a mechanic package has package-local tests, its validation text must name:

```bash
python -m pytest -q mechanics/<slug>/tests
```

Agon's route card and landing log now name the local pytest command.

## Alternatives Considered

- Keep relying on `python scripts/release_check.py`. Rejected because release
  validation is broad and does not help a future agent run a package-local
  regression while editing one mechanic.
- Infer local test commands from the artifact inventory only. Rejected because
  inference helps machines, but route cards should still carry the shortest
  human and agent validation path.
- Require every individual test file to be named. Rejected for now because the
  package-level pytest command is stable and already matches the other mechanic
  packages.

## Consequences

- A mechanic with local tests cannot be marked ready if its route/validation
  surface hides the local pytest command.
- Agon now has the same package-local validation affordance as the other
  mechanic packages.
- Future local test additions must update the nearest validation route instead
  of relying on broad release validation only.

## Affected Surfaces

- `scripts/mechanic_readiness_common.py`
- `generated/memo_mechanic_readiness.min.json`
- `mechanics/agon/AGENTS.md`
- `mechanics/agon/LANDING_LOG.md`
- `tests/test_memo_mechanic_readiness.py`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Verification Route

Run:

```bash
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests
python -m pytest -q tests/test_memo_mechanic_readiness.py
python scripts/release_check.py
```
