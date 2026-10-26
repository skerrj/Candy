# B26: `and` and `or` return an operand, not a `Bool`

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy_rt/spelling.py`
refs: [[expr.logic]], [[B100]]

`(or x 5)` can be `5`, as in Python. From `doc/archive/leaks_imvp_py_translator.md`. Related: [[B100]].
