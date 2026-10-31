# B93: Curried function types, and partial application

kind: idea
state: dropped
priority: low
found: self-host-cleanup, 2026-10-18
fixed:
where:
refs: [[expr.functions]]

Should `(Fn (Int Int) Int)` mean the same as `(Fn (Int) (Fn (Int) Int))`, as in ML and
Haskell, and should `(add 1)` be a function of one argument? Today a `Fn` type takes all
its arguments at once, and a call must pass them all. From `doc/brainstorm.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an idea to think about later.
- 2026-10-30, the owner: dropped, *lasting* (`doc/hl_rqmt/python_complete.md`, Question
  9): Candy takes typed rest parameters instead, and a curried type needs a fixed arity;
  a `fn` (or a later `partial` macro) covers partial application.
