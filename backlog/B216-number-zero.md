# B216: A number type variable has no zero

kind: leak
state: open
priority: low
found: stdlib, 2026-11-20
fixed:
where: `src/cdy/list.cdy`, `src/cdy/math.cdy`
refs: [[checking.constraints]], [[library.list]], [[library.math]]

A literal `0` is an `Int`, so Candy code on a `number` type variable can't write its
zero: `list.sum` of an empty list is a panic, since it starts from the first item, and
`math.abs` writes `(- x x)`. Elm's `number` literals take the constraint's type; a later answer could
be that, or a `zero` per number type (an interface, [[B34]]). Python's `sum([])` is `0`,
an `Int` whatever the list holds.

## Notes

- 2026-11-20, Claude: filed by step 7 of `doc/hl_rqmt/stdlib.md`.
- 2026-11-20, the owner: `list.sum`'s panic stays; the zero noted on the `number`
  constraint (`checking.constraints`).
