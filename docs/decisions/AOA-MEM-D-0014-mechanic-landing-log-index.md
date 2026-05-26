# Mechanic Landing Log Index

- Decision ID: AOA-MEM-D-0014

## Index Metadata

- Original date: 2026-05-18
- Surface classes: generated/readout, mechanic package
- Mechanic parents: none
- Guard families: mechanic topology, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

The memo mechanics tree now has package cards, owner maps, route-card
generation, owner-route generation, readiness checks, and package-local
artifact inventory. Every package also has a `LANDING_LOG.md`, but those logs
had mixed shapes: some used dated sections, some used tables, and a few named
landed shape and stop-lines without an explicit validation route.

For OS Abyss, landing logs are the public receipt trail for what was actually
landed in a mechanic package. They need to be inspectable without pretending
to be proof, owner acceptance, or runtime authority.

## Decision

Add `generated/memo_mechanic_landing_logs.min.json` as a generated landing
receipt index built from package `LANDING_LOG.md` files.

The index checks that each package has a dated receipt, landing evidence, a
release validation route, and stop-lines naming proof, runtime, and an
authority boundary. It is a receipt and validation companion only. It is not
proof, owner acceptance, runtime authority, release authority, route dispatch,
role authority, KAG truth, playbook choreography, stats truth, or source
doctrine.

## Alternatives

- Force every landing log into a single Markdown template. That would make
  parsing simple, but it would discard useful existing receipt shapes.
- Keep landing logs only as human-readable Markdown. That preserves local
  prose, but OS Abyss agents would have to scan every package to know whether
  a landing was dated, validated, and bounded.
- Fold landing-log checks into the readiness matrix only. That would hide the
  receipt trail inside readiness and make future landing audits harder.

## Consequences

- OS Abyss can inspect every mechanic landing receipt from one compact
  generated surface.
- Release validation fails when a mechanic has no dated landing evidence,
  release validation route, or stop-line receipt.
- Package `LANDING_LOG.md` files remain the authored receipt source.
- The readiness matrix can reference the landing-log index without becoming
  the landing receipt authority.

## Affected Surfaces

- `generated/memo_mechanic_landing_logs.min.json`
- `scripts/build_memo_mechanic_landing_logs.py`
- `scripts/validate_memo_mechanic_landing_logs.py`
- `scripts/memo_mechanic_landing_logs_common.py`
- `tests/test_memo_mechanic_landing_logs.py`
- `mechanics/*/LANDING_LOG.md`
- `generated/memo_mechanic_readiness.min.json`
- `scripts/mechanic_readiness_common.py`
- `config/root_technical_districts.json`
- `scripts/release_check.py`
- `mechanics/README.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `mechanics/AGENTS.md`

## Verification

Use:

```bash
python scripts/build_memo_mechanic_landing_logs.py --check
python scripts/validate_memo_mechanic_landing_logs.py
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_memo_mechanic_landing_logs.py tests/test_memo_mechanic_readiness.py
python scripts/release_check.py
```
