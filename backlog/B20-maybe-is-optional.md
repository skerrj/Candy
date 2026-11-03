# B20: `(Maybe a)` is `a | None`

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: semantics
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[types.table]], [[library.lists]], [[B25]], [[B51]]

A `Maybe` is Python's `Optional`, not a sum to be unwrapped: mypy's narrowing
(`if x is not None`) is all there is, and `nil` tests use truthiness
([[B25]]). So `(Maybe (Maybe a))` collapses: `find` and `index-of` return `None` for
"not found", which is also what a list of `Maybe`s holds for "nothing", and `with-default`
takes either as missing. Fix: a real sum, `(deft (Maybe a) (Nothing) (Just ((val a))))`,
once Candy's types are its own. From `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_library.md`. Related:
[[B51]].

## Notes

- 2026-11-02, Claude: fixed in semantics step 4 ([[B143]]): `Maybe` is the prelude's sum, `(deft (Maybe a)
  (Some ((v a))) (None))` (the HLD's Question 6 named them `Some` and `None`, not `Just`
  and `Nothing`), and `find`, `index-of` and `with-default` are prelude Candy on it, over
  the new built-ins `find-index` and `elem-index` (`-1` for none). The checker's rules
  (a `t` accepted as a `(Maybe t)`, `nil` as any `Maybe`) are gone. The spec's rule
  [[checking.maybe]] was, before (now rewritten in place, with [[library.maybe]] new in
  `spec/60-library.md`):

  ````text
  A `t` is accepted where a `(Maybe t)` is expected, and `nil` where a `Unit` or any
  `(Maybe t)` is. A `(Maybe t)` isn't a `t`: `with-default` takes the `t` out (*for now*:
  no narrowing after `(= m nil)`, and `Maybe` isn't a sum, [[B20]]).

  ```candy run
  (sig some (Maybe Int))
  (def some 5)
  (sig none (Maybe Int))
  (def none nil)
  (put (with-default 0 some) (with-default 0 none))
  ```
  ```expect
  5 0
  ```

  ```candy errors
  (sig m (Maybe Int)) (def m 5) (put (+ m 1)) => +: expected a number, String or a list, got (Maybe Int)
  (sig n Int) (def n nil) => def n: expected Int, got Unit
  ```
  ````

  `spec/60-library.md`'s [[library.lists]] said (now: `None` when nothing is found,
  [[library.maybe]]):

  ```text
  speed, since Candy adds to a list by copying it. `find` and `index-of` give a `(Maybe a)`:
  `nil` when nothing is found, which `with-default` replaces.
  ```

  and `spec/20-types.md`'s table row (now: `(Some v)` or `None`, the prelude's sum):

  ```text
  | `(Maybe a)` | an `a`, or `nil` |
  ```
