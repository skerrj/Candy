# B99: Variadic types

kind: idea
state: done
priority: normal
found: symbol-table, 2026-10-22
fixed: collections
where: `src/cdy/special.cdy`, `src/cdy/system.cdy`
refs: [[expr.operator-arity]], [[B48]]

A `Fn` type for two or more arguments (or any number), so the operators, `tup`, and
`put`/`print` get Candy types and move to `system.cdy` ([[B48]]). Macros are
variadic already, and untyped, so the operators could be variadic macros over
two-argument functions (`(+ a b c)` → `(add (add a b) c)`, with only `add` typed); but `+`
works on `Int`, `Double` and `String`, and Candy has no overloading or type classes, so
`add` is `Any` or one function per type. It doesn't help `tup`, whose type depends on how
many arguments it gets, or `put`. From `doc/brainstorm.md`.

## Notes

- 2026-11-08, Claude: done by `collections` step 1 ([[B161]], [[expr.rest]]): `(Rest t)`
  in a `sig`'s function type. The operators' types are step 2 ([[B162]]); `tup` goes
  (step 5) and `put` becomes a macro (step 6), neither a rest parameter.
