# B70: `load-macros` finds `form.cdy`'s names from a Python name

kind: tech-debt
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy_rt/primitives.py` (`load_macros`)
refs:

`form__sym_name` gives the prefix `form__` (none for a translator built before modules,
which the bootstrap needed). From `doc/tech_debt.md`.
