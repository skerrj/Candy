# B25: `if` tests use Python truthiness

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`
refs: [[expr.conditionals]], [[B15]]

`0`, `""` and an empty list are false. A test should have to be a `Bool`; mypy accepts
any type in a test, so nothing enforces it until Candy has its own type checker
([[B15]]). From `doc/archive/leaks_imvp_py_translator.md`.
