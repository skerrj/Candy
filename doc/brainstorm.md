# Brainstorm

Random thoughts about Candy's design: not decided, not planned, not tech debt. Add one
whenever it comes up; when one turns into real work, move it to a design doc
(`doc/hl_rqmt/`) and leave a pointer here.

- **Curried function types.** Should `(Fn (Int Int) Int)` mean the same as
  `(Fn (Int) (Fn (Int) Int))`, as in ML and Haskell? And should Candy support partial
  application (`(add 1)` as a function of one argument)? Today a `Fn` type takes all its
  arguments at once, and a call must pass them all.
