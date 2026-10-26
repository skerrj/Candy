# B27: `=` is Python's `==`

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy_rt/spelling.py`
refs: [[expr.comparisons]], [[B29]]

Equality is structural, and across types: `1 == 1.0` is true, and so are a `Tup`, a `List`
and a record with the same items ([[B29]]). From `doc/archive/leaks_imvp_py_translator.md`.
