# AGENTS.md

Local route card for `aoa-memo/evals/`.

## Purpose

This port captures repo-local memory eval pressure before it is accepted,
rejected, or normalized by `aoa-evals`.

`aoa-evals` owns central verdict, scoring, regression, and proof doctrine
authority. This port owns only memo-local intake, cases, fixtures, suites,
reports, and source refs.

## Operating Card

| Field | Route |
| --- | --- |
| role | memo-local eval pressure port |
| input | memory guardrail pressure, trace cue, suite need, fixture family, or local report |
| output | local intake packet, local suite/report, or route to `aoa-evals` |
| owner | `PORT.yaml` for port status; local files for memo evidence shape |
| next route | `intake/`, `suites/`, `reports/`, or `aoa-evals` local eval-port standard |
| validation | `python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .` |

## Rules

- Keep memory object truth in `aoa-memo`.
- Keep proof doctrine, verdicts, scoring, and regression authority in
  `aoa-evals`.
- Do not treat an intake packet as proof acceptance.
- Do not place private traces, secrets, or unreduced operator evidence here.
