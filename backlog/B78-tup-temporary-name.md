# B78: The destructuring temporary is named `_tup`

kind: tech-debt
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[match.tup]]

A plain local, renamed like any other if the name is taken. In the iMVP's leaks
(`doc/archive/leaks_imvp_py_translator.md`), but a Candy user can't see it.
