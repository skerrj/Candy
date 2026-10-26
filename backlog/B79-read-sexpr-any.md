# B79: `tst/cdy/read_sexpr.cdy` types forms as `Any`

kind: tech-debt
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `tst/cdy/read_sexpr.cdy`
refs:

Written before Candy had sum types, it tells a symbol from a number or a list only through
Python's runtime types. The translator's own `Form` is a sum (`src/cdy/form.cdy`); this
test program could be too. Partly fixed: the leak "Forms are `Any`" (`doc/archive/leaks_imvp_py_translator.md`) is left only
here.
