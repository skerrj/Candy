# B25: `if` tests use Python truthiness

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: type-checker
where: `src/cdy/emit.cdy`
refs: [[expr.conditionals]], [[B15]], [[checking.if]]

`0`, `""` and an empty list are false. A test should have to be a `Bool`; mypy accepts
any type in a test, so nothing enforces it until Candy has its own type checker
([[B15]]). From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-10-29, type-checker step 3: an `if`'s test must be a `Bool`, and so must `and`'s,
  `or`'s and `not`'s arguments (`check.cdy`): `(put (if 1 2 3)) => if: the test is Int,
  not Bool`, a row of `[[checking.if]]`. A test program relied on it (`(or false nil)` in
  `tst/cdy/t1/basics.cdy`, now `(or false true)`).
