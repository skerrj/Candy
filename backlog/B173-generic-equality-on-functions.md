# B173: A generic function's `=` compares functions

kind: defect
state: open
priority: normal
found: collections step 3, 2026-11-09
fixed:
where: `src/cdy/check.cdy` (`infer-compare`), `src/cdy/system.cdy`
refs: [[expr.equality]], [[expr.operator-values]], [[checking.constraints]], [[B172]]

Functions can't be compared, an error when translated ([[expr.equality]]): the checker
looks into `=`'s and `!=`'s argument type at a call (`infer-compare`, `has-fn`). Inside a
generic function the type is the `sig`'s fixed `a`, which isn't a function type, so the
check passes; a call then makes `a` a function type, and Python compares the functions by
identity. `=` as a value, an `(Fn (a a) Bool)` ([[expr.operator-values]]), is the same.

Fix: a constraint that excludes, as Haskell's `Eq a`: `equatable`, every type but one that
is or holds a function ([[checking.constraints]]), with `has-fn`'s check when one is bound;
`(sig = (Fn (equatable equatable (Rest equatable)) Bool))`, and `infer-compare` gone. A
generic function that compares says so in its `sig` (`(Fn (equatable equatable) Bool)`),
the prelude's among them. Elm has none (comparing functions fails when run).

## Repro

The translator should fail:

```candy error
(sig same (Fn (a a) Bool))
(defn same (x y) (= x y))
(sig inc (Fn (Int) Int))
(defn inc (n) (+ n 1))
(put (same inc inc))
```
```expect-error
argument 1 of =: expected equatable, got a
```

## Notes

- 2026-11-09, the owner: asked why `primitives.py` has no `=`; Claude found the hole
  checking why (`(same inc inc)` prints `true`), and the owner chose to make `=` and `!=`
  values ([[B172]] dropped) and file this, for later (a step of its own, or
  `collections-2`).
