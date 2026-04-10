# Releasing `aoa-memo`

`aoa-memo` is released as the provenance-aware memory and recall layer of AoA.

See also:

- [README](../README.md)
- [CHANGELOG](../CHANGELOG.md)

## Recommended release flow

1. Keep the release bounded to memory, recall, and writeback posture.
2. Update `CHANGELOG.md` in the `Summary / Validation / Notes` shape.
3. Run the repo-level verifier:
   - `python scripts/release_check.py`
4. Run federation preflight:
   - `aoa release audit /srv --phase preflight --repo aoa-memo --strict --json`
5. Publish only through `aoa release publish`.
