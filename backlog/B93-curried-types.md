# B93: Curried function types, and partial application

kind: idea
state: open
priority: normal
found: self-host-cleanup, 2026-10-18
fixed:
where:
refs: [[expr.functions]]

Should `(Fn (Int Int) Int)` mean the same as `(Fn (Int) (Fn (Int) Int))`, as in ML and
Haskell, and should `(add 1)` be a function of one argument? Today a `Fn` type takes all
its arguments at once, and a call must pass them all. From `doc/brainstorm.md`.
