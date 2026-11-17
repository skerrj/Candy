# B32: Regexes are Python's

kind: leak
state: done
priority: low
found: py-py-translator, 2026-10-15
fixed: library-layers, 2026-11-16
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[library.strings]], [[B49]]

`re-search`, `re-findall` and `re-compile` use Python's syntax and return Python match
objects (typed `Any`: [[B49]]). From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): matters once there is a second target.
- 2026-11-16, Claude: fixed by dropping them (library-layers step 4, [[B202]]): none was
  used. Regexes come back as a portable module, or in `py`, when a program wants them.
