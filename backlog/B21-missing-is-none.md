# B21: Missing values are `None`

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: semantics
where: `src/cdy/emit.cdy`
refs: [[expr.conditionals]], [[expr.unit]], [[macros.cond]]

An `if` with no else whose test is false, a `cond` with no match, and the value of a
`def` form are `None`. Candy will need a real unit (or a required `else`). From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-11-02, Claude: fixed in semantics step 4 ([[B143]]), with Question 7's answer: an `if` with no
  `else` is allowed only when its `then` is a `Unit` (*for now*: [[B138]]), so the missing
  value is `nil`, `Unit`'s, never a value standing for a missing one; a `cond` with no
  `else` likewise, though its error reads `if: the branches are Int and Unit` (its
  expansion's last `else` is a written `nil`). A missing value is a `(Maybe a)`'s `None`
  ([[B20]]). The spec's rules were, before (rewritten in place): [[checking.if]]

  ````text
  An `if`'s test is a `Bool` (no other value counts as true or false), and its two
  branches have one type, the `if`'s. With no `else`, an `if` whose `then` is a `t` is a
  `(Maybe t)` (*for now*: [[B21]]), or `Unit` if the `then` is.

  ```candy run
  (sig half (Fn (Int) (Maybe Int)))
  (defn half (n) (if (= (* 2 (quot n 2)) n) (quot n 2)))
  (put (with-default -1 (half 8)) (with-default -1 (half 7)))
  ```
  ```expect
  4 -1
  ```

  ```candy errors
  (put (if 1 2 3)) => if: the test is Int, not Bool
  (put (if "" 2 3)) => if: the test is String, not Bool
  (put (if true 1 "a")) => if: the branches are Int and String
  ```
  ````

  [[expr.conditionals]]

  ```text
  `(do expr ...)` evaluates its forms in order; its value is the last one's. `(if test then
  else)` evaluates `then` or `else`; with no `else`, a false test gives `nil`. The test is a
  `Bool`, and the branches have one type ([[checking.if]]).

  `cond` is a macro (in `src/cdy/prelude_macros.cdy`, which every file gets), expanding into
  nested `if`s: the first clause whose test is true gives the value. The last clause may be
  `(else expr)`; with no `else` and no match, the value is `nil`.
  ```

  and [[expr.unit]]

  ````text
  `Unit` is the type with one value, `nil`. It is the value of an `if` with no `else` whose
  test is false, of a `cond` with no match, of `(do)`, and of a `def` form itself. `nil`
  also stands for a missing value in a `(Maybe a)` (*for now*: one `None` for both,
  [[B20]], [[B21]]; how the checker treats them is [[checking.maybe]]).

  ```candy run
  (sig m (Maybe Int))
  (def m nil)
  (put (if (= m nil) "missing" "there"))
  (put (if (= (if false 1) nil) "nil" "not nil"))
  ```
  ```expect
  missing
  nil
  ```
  ````
