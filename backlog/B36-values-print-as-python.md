# B36: Values print as Python shows them

kind: leak
state: open
priority: high
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy_rt/spelling.py`, `src/cdy/system.cdy`
refs: [[library.format]], [[library.builtins]], [[B95]], [[B15]]

`put`, `print` and `display` are Python's `print`, and `format` shows a value with
Python's `str()`: a `Bool` is `True`, a record `Vector2(x=1, y=2)`, `nil` `None`, a list
`(1, 2)`. So the spec's examples print only numbers and text (`spec/README.md`). Fix: a
show for each type in Candy (`doc/hl_rqmt/executable_spec.md`, question 12), part of
[[B95]]. From `doc/archive/leaks_imvp_py_translator.md` ("`format`", "`print` for `put` and `display`").

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): the spec can't show a `Bool`, a list or `nil` until it is fixed.
- 2026-10-28, the owner: where does this stand for multiple targets and hosts? Neither
  doc covered it, so `doc/hl_rqmt/multi_target.md` has "Open: showing values" and
  `doc/hl_rqmt/macros.md` a note under "Terms: host and target". The catch: a `show` in
  Candy's syntax needs each value's type. At run time, Python can't tell a `Char` from a
  `String` (both `str`) or an `Int` from a `Byte`; from the static type, it needs
  [[B15]]'s checker. So a full fix likely comes after [[B15]]; an interim one could show
  `true`, `nil` and lists, but not `Char`.
