# B124: The operators are polymorphic, but a program can't write a polymorphic function

kind: leak
state: open
priority: normal
found: master, 2026-10-30
fixed:
where: `src/cdy/check.cdy` (`infer-op`), `src/cdy/special.cdy`
refs: [[checking.operators]], [[checking.generics]], [[B34]], [[B38]], [[B48]]

`+` takes any number type, `String` or a list; `-`, `*`, `/` and `quot` any number type;
the comparisons any one type ([[checking.operators]]). Each operator gets that power
from rules built into the checker (`infer-op`), not from a type a program could write:
a generic function can't add or compare its arguments (`(+ x 1)` on an `a` is an error,
[[checking.generics]]), and the operators have no `sig` in `system.cdy` ([[B48]]), so
they can't be values either ([[B38]]). A Python leak behind it: `emit` needs no types
for `+` because Python's `+` works on all three; a target whose `+` doesn't (Rust has
none on `Vec`) would need the checker's types in its backend.

Fix (`doc/hl_rqmt/python_complete.md`, Question 4, proposed): Elm's design, in
`collections`. `++` appends strings and lists (an `appendable` constraint variable);
`+`, `-`, `*` and the comparisons take a `number` or a `comparable` constraint
variable, which a program's own `sig`s can use; `=` is declared for every type
(Question 12). Interfaces ([[B34]]) after the epic, without undoing either.

## Notes

- 2026-10-30, Claude: a survey of the separate-operators option (OCaml, Gleam, SML,
  Elm, Haskell, Go, Rust) is in the HLD's Question 4. About 300 `+`s in the translator
  (roughly 140 on lists, 80 on strings, 80 on numbers) and 76 in `spec/` and
  `tst/cdy/`: a mechanical rename, from a list of each `+` and its type the checker can
  print, in two boot steps (the new operator into `bin`, then the translator's uses).
- 2026-10-31, the owner and Claude, in typed-core's review (B129, [[B135]]): the goal, for
  the `collections` HLD: **no operators in the language.** A built-in and a user's
  function are one kind of thing (the owner: "whether it's user defined or defined by the
  system, they'd both just be operators"). What makes an operator different today is
  shortcuts, each with its fix: no type (constraint variables, Question 4), checked by
  `infer-op` with its error at the call ([[B135]]), not a value ([[B38]], [[B48]]),
  variadic (typed rest parameters, Question 8: a user's function can be too), a closed set
  in `special.cdy`. Folding and chaining are what the function does with its rest list.
  The one real difference is `and`/`or`'s short-circuit, which a function can't do:
  macros ([[B100]], `semantics`). So `op` can leave `special.cdy`: `+` and the
  comparisons become bodiless `sig`s in `system.cdy`, `not` a one-argument function.
  Infix Python (`(a + b)`) is the backend's business, a spelling (`spelling.py`), not the
  language's; mypy's view of the variadic, constrained signatures is the cost, in `emit`.
