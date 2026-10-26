# B35: `at` and `slice` behave as Python's subscripts

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/emit.cdy`
refs: [[library.lists]], [[B71]]

`at` and `slice` are emitted as `coll[i]` and `coll[i:j]`, so mypy keeps the element type,
and their behaviour (negative indexes, out-of-range slices) is Python's. From `doc/archive/leaks_imvp_py_translator.md`.
Related: [[B71]].
