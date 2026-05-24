# Releasing `aoa-memo`

`aoa-memo` is released as the provenance-aware memory and recall layer of AoA.

See also:

- [README](../README.md)
- [CHANGELOG](../CHANGELOG.md)

## Recommended release flow

1. Keep the release bounded to memory, recall, and writeback posture.
2. Update `CHANGELOG.md` in the `Summary / Validation / Notes` shape.
3. Run the repo-level verifier:
   - `python scripts/release/release_check.py`
4. Run the workspace release-tool compatibility verifier:
   - `python scripts/release_check.py`
5. Run federation preflight:
   - `aoa release audit /srv/AbyssOS --phase preflight --repo aoa-memo --strict --json`
6. Publish only through `aoa release publish`.

Workspace release tooling also probes `docs/RELEASING.md` and
`scripts/release_check.py`. Those files are compatibility entrypoints; this
file and `scripts/release/release_check.py` remain the active procedure and
gate.
