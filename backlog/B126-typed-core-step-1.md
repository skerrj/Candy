# B126: typed-core step 1: positions on literal forms and Core's leaves

kind: task
state: open
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/form.cdy`, `src/cdy/read.cdy`, `src/cdy/core.cdy`, `src/cdy/check.cdy`
refs: [[B59]], [[B122]]

Step 1 of `doc/hl_rqmt/typed_core.md`. A `pos` on each literal form (the reader gives it) and on Core's leaves and `Do`; the checker reports at the node; macro code that builds or takes apart literal forms updated, and the spec's `macros.macro-code` example; an example of an error at a leaf.
