# B70: `load-macros` finds `form.cdy`'s names from a Python name

kind: tech-debt
state: review
priority: low
found: modules, 2026-10-19
fixed: host-macros, 2026-11-24
where: `src/cdy_rt/primitives.py` (`load_macros`)
refs:

`form__sym_name` gives the prefix `form__` (none for a translator built before modules,
which the bootstrap needed). From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
- 2026-11-24, Claude: gone with `load-macros` (`host-macros` step 6b): macro code builds
  `form.cdy`'s own `Form`s on the interpreter, so no names are put back.
