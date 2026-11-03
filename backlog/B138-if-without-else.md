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
