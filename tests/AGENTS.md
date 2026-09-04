# AGENTS.md

## Guidance for `tests/`

`tests/` protects memory schemas, examples, generated catalogs, recall
contracts, lifecycle audit examples, retired docs district checks, memo
mechanics, validator topology, validation lanes, test topology, and writeback boundaries. The
phrase recall contracts is intentional route-law vocabulary here.

Tests should expose provenance loss, recall overreach, stale context, schema mismatch, AGENTS mesh drift, and generated/source drift.

Root tests are part of the root technical-district contract. Each non-route
test file or public fixture must be listed in exactly one
`config/root-topology/root_technical_districts.json` `test_families` entry that
names the owner surface and protected refs. The broader test-family map lives
in `docs/testing/test_inventory.json`.

`tests/root-topology/test_root_technical_districts_index.py` protects the compact district
atlas in `generated/root-topology/root_technical_districts.min.json` so root folder routing
can be inspected without opening the full allowlist first.

## Conditional route scope

- Above: source docs, schemas, examples, scripts, generated companions, and
  `config/root-topology/root_technical_districts.json` name what root tests protect.
- Here: root tests protect repo-wide and cross-mechanic invariants.
- Below: package-local mechanic tests live under the owning package or part
  when they protect a single mechanic operation.

Do not update expected outputs without checking the source-owned memory docs, schemas, or examples that own the meaning.

Keep fixtures public-safe. No private memories, secrets, hidden telemetry, or unreduced personal data.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this card
names only focused owner checks and lane ids.

Run the focused test for the changed surface first; for broad test health, use the nearest `VALIDATION.md` route.
For test-topology, lane, or validator-authority changes, use the root-topology validation route.
For release-facing changes, use the composed validation route; focused tests do not establish release admission.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
