# B135: An operator's type error is at the call, not the argument

kind: defect
state: open
priority: low
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/check.cdy`
refs: [[checking.operators]], [[B124]], [[B48]]

A function call's type error is at the argument that is wrong (`(pick 1 "a" true)`:
`argument 2 of pick`, at the `"a"`), but an operator's is at the whole call: `(+ x "b")`
says `+: expected Int, got String` at the `(+`, not at `"b"`. Operators have no `sig`
(`special.cdy` declares `(op + variadic)`); their rules are code, `infer-op` in
`check.cdy`, which infers every argument, then joins their types (`join-all`) and checks
the kind (`needs-kind`), with the context still at the call. The kind check (`(- "a"
"b")`: expected a number) is about all the arguments and stays at the call.

The fix is expected with `collections`: constraint variables (`number`, `comparable`,
`appendable`; `doc/hl_rqmt/python_complete.md`, Question 4) give the operators types, so
they are checked as calls are, argument by argument ([[B124]]). Until then, `join-all`
could carry each argument's node and report at the first that disagrees.

## Repro

The translator should fail:

```candy error
(sig x Int)
(def x 1)
(put (+ x
  "b"))
```
```expect-error
line 4, column 3: +: expected Int, got String
```

## Notes

- 2026-10-31, the owner, in B129's review: asked why an error in a `format` hole,
  `"a {(+ x \"b\")} c"`, points at the `(+`. It isn't the hole: outside one the same
  `(+ x "b")` is reported at the call too. Not because `+` lost its polymorphism (it
  still takes numbers, `String`s and lists): because an operator has no `sig`.
