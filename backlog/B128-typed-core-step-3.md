# B128: typed-core step 3: nested functions typed

kind: task
state: open
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/lower.cdy`, `src/cdy/emit.cdy`
refs: [[B19]]

Step 3 of `doc/hl_rqmt/typed_core.md`. `SLocalFunc` carries its `Lambda`'s type, and `emit` annotates the nested `def` (a `?N` as `Any`); what mypy then finds, fixed or recorded.
