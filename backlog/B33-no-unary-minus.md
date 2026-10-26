# B33: No unary minus

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/special.cdy`
refs: [[expr.arithmetic]], [[expr.operator-arity]]

`-` takes two or more arguments, so `(- x)` is an error: write `(- 0 x)`. A negative
literal (`-5`) is fine. From `doc/archive/leaks_imvp_py_translator.md`.
