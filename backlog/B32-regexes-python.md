# B32: Regexes are Python's

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[library.strings]], [[B49]]

`re-search`, `re-findall` and `re-compile` use Python's syntax and return Python match
objects (typed `Any`: [[B49]]). From `doc/archive/leaks_imvp_py_translator.md`.
