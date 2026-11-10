# B17: Taking a `tup` apart is a stopgap

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[match.tup]], [[types.tuples]], [[expr.let]], [[B48]]

A `tup` pattern (in `match` or a `let` binding) binds a temporary and reads each name with
`at`, so Core needs no pattern node. A record (also a Python tuple) can be taken apart as
one, a value typed `Any` is taken apart unchecked ([[B18]]), and parameters can't be
patterns. `tup` is a special form because
it takes any number of items ([[B48]]). Fix: real tuple types in Candy's type
checker, and patterns everywhere. From `doc/archive/leaks_imvp_py_translator.md` ("`tup` destructuring").

## Notes

- 2026-10-29, type-checker step 3: narrowed. The type checker checks a pattern's arity
  against a `(Tup ...)` (`(put (match (tup 1 2) ((tup a b c) a))) => a (Tup Int Int) has
  2 items, not 3`, a row of `[[checking.match]]`); it said "The translator doesn't check
  its arity (mypy does, with a `sig`; otherwise an `IndexError` at run time)".
- 2026-11-09, Claude: narrowed by [[B165]] (`collections` step 5): `tup` is gone for
  `Tup` (so it is no special form, [[B48]]'s part), `at` on a tuple is an error, the
  pattern's own read excepted, and a `Tup` pattern on a typed value that isn't a tuple
  (a record, a function) is an error, "a Tup pattern takes a tuple, not a P" (a row of
  [[checking.match]]). What stays: the pattern is still a temporary read with `at` in
  Core, a value typed `Any` is taken apart unchecked, and parameters can't be patterns.
