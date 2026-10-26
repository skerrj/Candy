# B17: Taking a `tup` apart is a stopgap

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[match.tup]], [[types.tuples]], [[expr.let]], [[B48]]

A `tup` pattern (in `match` or a `let` binding) binds a temporary and reads each name with
`at`, so Core needs no pattern node. The translator doesn't check its arity (mypy does,
with a `sig`; otherwise an `IndexError` at run time), a record (also a Python tuple) can
be taken apart as one, and parameters can't be patterns. `tup` is a special form because
it takes any number of items ([[B48]]). Fix: real tuple types in Candy's type
checker, and patterns everywhere. From `doc/archive/leaks_imvp_py_translator.md` ("`tup` destructuring").
