# B21: Missing values are `None`

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`
refs: [[expr.conditionals]], [[expr.unit]], [[macros.cond]]

An `if` with no else whose test is false, a `cond` with no match, and the value of a
`def` form are `None`. Candy will need a real unit (or a required `else`). From `doc/archive/leaks_imvp_py_translator.md`.
