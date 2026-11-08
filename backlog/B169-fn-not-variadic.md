# B169: A `fn` can't be variadic

kind: leak
state: open
priority: low
found: collections, 2026-11-07
fixed:
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`
refs: [[B161]]

A rest parameter is marked only in a `sig`'s `Fn` type, `(Rest t)`, with no marker in
the parameters (`doc/hl_rqmt/collections.md`, Question 1, *lasting*). A `fn` has no `sig`, so it can't take a
rest parameter, *for now*.

Fix: a way to write a `fn`'s type (an annotation on a `fn`, or a `the` form), which
then can say `(Rest t)`.

## Notes

- 2026-11-07, the owner: the cost accepted with Question 1's answer.
