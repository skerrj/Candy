# B120: `get` or `assoc` on a value whose type isn't known yet is an error

kind: leak
state: open
priority: low
found: type-checker, 2026-10-29
fixed:
where: `src/cdy/check.cdy`
refs: [[checking.order]], [[B15]]

The checker reads a call's non-`fn` arguments before its `fn`s, so a `fn`'s parameters
usually have types when its body is read; when one doesn't, `(get p name)` fails with
`get: the type of p isn't known here (name)`, rather than becoming a constraint solved
once `p`'s type is known (Question 4 of `doc/hl_rqmt/type_checker.md`). The survey (step
1) found it never fires on the translator or the test programs. Fix: a field constraint
on the type variable, solved when it is bound.
