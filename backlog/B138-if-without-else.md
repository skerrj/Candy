# B138: An `if` without `else` is allowed for `Unit`

kind: idea
state: open
priority: low
found: semantics HLD, 2026-11-01
fixed:
where: `src/cdy/check.cdy`, `spec/40-expressions.md`, `src/cdy/prelude_macros.cdy`
refs: [[B21]], [[expr.conditionals]]

The semantics HLD (Question 7) allows an `if` without `else` only when its `then` is
`Unit`, and makes it `Unit`, as Rust and OCaml do: `(if verbose (put x))`; `(if c 3)` is
an error. `cond` without `else` likewise. That is the answer *for now*. The others
weighed: always an error (Elm, Haskell); always allowed, the `then`'s value discarded
(about Scala's); or `if` always with both branches and a `when` macro for effects
(Lisps): `(when verbose (put x))`, which keeps `if` a two-branch expression and names the
effect form. A `when` can come as a prelude macro without changing `if`; then `if`
without `else` could become an error.

## Notes

- 2026-11-01, the owner: Option 1 (only for `Unit`) taken *for now* in the semantics HLD.
- 2026-11-02, Claude: built in semantics step 4 ([[B143]]): `if: with no else, the then is Int, not
  Unit`. `cond` with no `else` gives `if: the branches are Int and Unit` instead, since
  its expansion writes the `nil`; the `when` test in `tst/cdy/cdyc/macros.cdy`
  (`(quasi (if (unq test) (unq body) nil))`) lost its value case, which was:

  ```text
  (put (format "{(when true 7)}"))
  ```

  with `(Some 7)` in `macros.out`.
