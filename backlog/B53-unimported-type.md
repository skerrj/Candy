# B53: A type from a module the file doesn't import isn't caught

kind: leak
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/core.cdy`
refs: [[programs.import]], [[types.names]]

A `sig` naming it keeps the bare name, and mypy (or Python) reports it in the output. In
`doc/tech_debt.md` until now, but a Candy user sees it (the audit, `doc/hl_rqmt/tracking.md`).
