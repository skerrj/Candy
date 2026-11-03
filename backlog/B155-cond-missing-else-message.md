# B155: A `cond` with no `else` isn't reported as an `if` with no `else` is

kind: defect
state: open
priority: normal
found: semantics step 4, 2026-11-02
fixed:
where: `src/cdy/prelude_macros.cdy`, `src/cdy/check.cdy`
refs: [[checking.if]], [[macros.cond]], [[B138]], [[B143]]

An `if` with no `else` whose `then` isn't a `Unit` says `if: with no else, the then is
Int, not Unit`; a `cond` with no `else` clause, which the spec says is checked likewise,
says `if: the branches are Int and Unit`. One rule, two messages: the second names a
branch the program never wrote, and an `if` the program never wrote either. The cause:
`cond`'s expansion ends in a written `nil` (`(quo nil)`, with a position), so the
checker's `is-missing-else` (an `else` at `NOWHERE`) doesn't see a missing one. Fix: the
macro leaves the last `if` without an `else`, or marks its `nil` as missing; and the
message should name `cond` and its clause, not the `if` it expands into (a macro's
errors are reported in its expansion's words, more generally).

## Repro

The translator should fail:

```candy error
(put (cond (false 1)))
```
```expect-error
with no else, the then is Int, not Unit
```

## Notes

- 2026-11-02, the owner, at step 4's commit: not a minor inconsistency; noted.
