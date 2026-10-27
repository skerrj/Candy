# B64: `form.cdy` is copied next to every translator

kind: tech-debt
state: open
priority: low
found: macros, 2026-10-18
fixed:
where: `bin/py/form.cdy`, `src/py_cdy/self_host.py` (`copy_library`)
refs:

For macros to compile with; a translator copied elsewhere on its own can't expand macros
(it says so). From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
