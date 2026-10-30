# B122: A type error in a leaf is reported at its parent

kind: leak
state: open
priority: low
found: type-checker, 2026-10-29
fixed:
where: `src/cdy/check.cdy`, `src/cdy/core.cdy`, `src/cdy/read.cdy`
refs: [[checking.definitions]], [[B15]]

Core's leaves (`Lit`, `Local`, `Global`, `Prim`) have no position, and neither do the
literal forms (`Txt`, `IntLit`, ...; only `Sym` and `Lst` carry a `Pos`), so a type error
in one is reported at the innermost node above it that has one: in

```
(sig x Int)
(def x
  "a")
```

the error is `2:1: def x: expected Int, got String`, the `def`'s position, not `3:3`,
the `"a"`'s. The message names the definition, so it is usually close enough. Fix: a
position on the literal forms (the reader) and on Core's leaves, which changes their
patterns throughout `lower`, `emit` and `check`.
