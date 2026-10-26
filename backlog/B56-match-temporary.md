# B56: Every `match` subject gets a temporary

kind: tech-debt
state: open
priority: normal
found: pre-self-host, 2026-10-17
fixed:
where: `src/cdy/lower.cdy`
refs: [[match.form]], [[match.exhaustive]]

Only because the Python chain tests the subject more than once. It is typed `object` for a
non-generic sum, to keep mypy fast (`doc/hl_rqmt/sum_types.md`), so mypy no longer checks
that a chain is exhaustive or that its variants belong to the subject's sum (`analyse`
checks both). From `doc/tech_debt.md`.
