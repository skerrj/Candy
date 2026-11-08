# B23: `/` on integers is true division

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: semantics-2
where: `src/cdy_rt/spelling.py`
refs: [[expr.arithmetic]], [[B24]]

`(/ 7 2)` is `3.5`. A strongly typed Candy will want `Int / Int` to stay an `Int`, or a
separate operator (`quot` exists: [[B24]]). From `doc/archive/leaks_imvp_py_translator.md`.

## Notes
- 2026-11-06, Claude: fixed in `semantics-2` step 1: `/` takes a `Float` or `Double` and
  gives the same type, `(/ 7 2)` an error, and `mod` is beside `quot` ([[expr.arithmetic]],
  [[checking.operators]]).
