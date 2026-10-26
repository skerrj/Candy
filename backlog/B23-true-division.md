# B23: `/` on integers is true division

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy_rt/spelling.py`
refs: [[expr.arithmetic]], [[B24]]

`(/ 7 2)` is `3.5`. A strongly typed Candy will want `Int / Int` to stay an `Int`, or a
separate operator (`quot` exists: [[B24]]). From `doc/archive/leaks_imvp_py_translator.md`.
