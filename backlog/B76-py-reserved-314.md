# B76: `PY_RESERVED` is Python 3.14's

kind: tech-debt
state: open
priority: normal
found: library, 2026-10-22
fixed:
where: `src/cdy/emit.cdy`
refs:

Its keywords and built-ins, written out; `test_py_reserved_is_this_python` fails when
another Python adds one. From `doc/tech_debt.md`.
