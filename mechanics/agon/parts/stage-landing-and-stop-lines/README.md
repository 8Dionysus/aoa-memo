# Stage landing and stop-lines

This active part belongs to `mechanics/agon/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [AGON_STAGE7_MEMO_LANDING](../../docs/AGON_STAGE7_MEMO_LANDING.md)
- [AGON_STAGE11_MEMO_LANDING](../../docs/AGON_STAGE11_MEMO_LANDING.md)
- [AGON_STAGE13_MEMO_LANDING](../../docs/AGON_STAGE13_MEMO_LANDING.md)
- [AGON_STAGE13_MEMO_STOP_LINES](../../docs/AGON_STAGE13_MEMO_STOP_LINES.md)
- [AGON_STAGE14_MEMO_LANDING](../../docs/AGON_STAGE14_MEMO_LANDING.md)
- [AGON_STAGE15_MEMO_LANDING](../../docs/AGON_STAGE15_MEMO_LANDING.md)
- [AGON_STAGE16_MEMO_LANDING](../../docs/AGON_STAGE16_MEMO_LANDING.md)
- [AGON_STAGE17_MEMO_LANDING](../../docs/AGON_STAGE17_MEMO_LANDING.md)
- [AGON_STAGE18_MEMO_LANDING](../../docs/AGON_STAGE18_MEMO_LANDING.md)

## Function

keeps landing history reviewable without promoting it to source Agon law

## Technical Homes

- `manifests/` owns stage recurrence components and hook bindings.
- `tests/` protects manifest references so stage landing surfaces cannot point
  back to old package-level artifact homes.

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
