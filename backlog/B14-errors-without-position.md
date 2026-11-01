# B14: A few errors have no position

kind: defect
state: done
priority: normal
found: self-host-cleanup, 2026-10-18
fixed: typed-core
where: `src/cdy/core.cdy`, `src/cdy/lower.cdy`, `src/cdy/emit.cdy`
refs: [[syntax.strings]], [[library.format]], [[programs.main]], [[B59]]

A brace inside a `format` hole, `main`'s type (its `Top` has no position), and the
internal errors of `lower` and `emit` say no `file:line:col`. Errors inside a `format`
hole point at the `(format ...)` form, since forms read from a hole have no positions of
their own (the hole's text is part of a string). From `doc/tech_debt.md`;
the audit's defect 13 (`doc/hl_rqmt/tracking.md`). Related: [[B59]].

## Notes

- 2026-10-31, Claude: fixed by typed-core step 4 ([[B129]]): `main`'s errors are at its definition; forms read from a `format` hole have positions (`read-hole`), and the brace errors are at the `(format ...)` form; `lower`'s and `emit`'s internal errors keep none, *lasting*, and say `internal error`. Also the operator-as-value error, at the operator. What is left is [[B131]].
