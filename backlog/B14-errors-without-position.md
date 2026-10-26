# B14: A few errors have no position

kind: defect
state: open
priority: normal
found: self-host-cleanup, 2026-10-18
fixed:
where: `src/cdy/core.cdy`, `src/cdy/lower.cdy`, `src/cdy/emit.cdy`
refs: [[syntax.strings]], [[library.format]], [[programs.main]], [[B59]]

A brace inside a `format` hole, `main`'s type (its `Top` has no position), and the
internal errors of `lower` and `emit` say no `file:line:col`. Errors inside a `format`
hole point at the `(format ...)` form, since forms read from a hole have no positions of
their own (the hole's text is part of a string). From `doc/tech_debt.md`;
the audit's defect 13 (`doc/hl_rqmt/tracking.md`). Related: [[B59]].
