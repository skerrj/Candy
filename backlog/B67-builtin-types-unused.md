# B67: The built-ins' types are read but not used

kind: tech-debt
state: done
priority: low
found: system-prelude, 2026-10-19
fixed: type-checker
where: `src/cdy/core.cdy`, `src/cdy_rt/primitives.py`
refs:

Beyond arity: there is no type checker, and mypy gets the runtime's types from
`primitives.py`'s annotations. From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): covered by [[B15]].
- 2026-10-29, the epic HLD's pass (`python_complete.md`): done by `type-checker`, whose `check.cdy` instantiates every built-in's `system.cdy` type (`infer`, `Typed`); mypy still reads `primitives.py`'s annotations, as the second check.
