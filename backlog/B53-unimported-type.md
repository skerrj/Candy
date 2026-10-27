# B53: A type from a module the file doesn't import isn't caught

kind: leak
state: done
priority: normal
found: modules, 2026-10-19
fixed: name-checks
where: `src/cdy/core.cdy`
refs: [[programs.import]], [[types.table]]

A `sig` naming it keeps the bare name, and mypy (or Python) reports it in the output. In
`doc/tech_debt.md` until now, but a Candy user sees it (the audit, `doc/hl_rqmt/tracking.md`).

## Notes

- 2026-10-26, Claude Code: fixed on `name-checks` (step 2), by the same check: a type
  from a module the file doesn't import says which module defines it, as a value does.
