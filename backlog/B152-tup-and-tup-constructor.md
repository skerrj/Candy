# B152: `tup` and `Tup` are one form

kind: tech-debt
state: open
priority: low
found: semantics step 2, 2026-11-02
fixed:
where: `src/cdy/core.cdy`, `src/cdy/*.cdy`
refs: [[types.constructors]], [[types.tuples]]

A type's name is its constructor ([[types.constructors]]), so a tuple is `(Tup 1 "a")`,
but `tup`, the older name, still works the same (in an expression and as a pattern),
*for now*: the translator's own code writes `tup` throughout, and the checker reads a
`(Tup t ...)` of `t`s as a `(List t)` ([[checking.tup-lists]], [[B29]]). Fix: the
translator's `tup`s become `Tup` or `List` (a `List` where it means a list), then `tup`
goes.
