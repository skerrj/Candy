# B127: typed-core step 2: types in Core

kind: task
state: review
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`, `src/cdy/lower.cdy`, `src/cdy/emit.cdy`
refs: [[B15]]

Step 2 of `doc/hl_rqmt/typed_core.md`. A `t` on every `Expr`; the checker elaborates, returning each node with its type, and puts in the final substitution; `type-check` returns the typed `tops`; a test that every node of the translator's own Core has a type.
