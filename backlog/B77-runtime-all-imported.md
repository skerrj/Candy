# B77: Every runtime module is imported

kind: tech-debt
state: dropped
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/emit.cdy` (`PY_IMPORTS`)
refs:

Whether the program uses it or not. A Candy user can't see it, so it is tech debt, though
it was in the iMVP's leaks (`doc/archive/leaks_imvp_py_translator.md`).

## Notes

- 2026-10-26, the owner: dropped in triage ([[B103]]): two small modules; importing both costs nothing worth fixing.
