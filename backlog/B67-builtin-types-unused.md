# B67: The built-ins' types are read but not used

kind: tech-debt
state: open
priority: low
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/core.cdy`, `src/cdy_rt/primitives.py`
refs:

Beyond arity: there is no type checker, and mypy gets the runtime's types from
`primitives.py`'s annotations. From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): covered by [[B15]].
