# B128: typed-core step 3: nested functions typed

kind: task
state: review
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/lower.cdy`, `src/cdy/emit.cdy`
refs: [[B19]]

Step 3 of `doc/hl_rqmt/typed_core.md`. `SLocalFunc` carries its `Lambda`'s type, and `emit` annotates the nested `def` (a `?N` as `Any`); what mypy then finds, fixed or recorded.

## Notes

- 2026-10-31, Claude: built; see the HLD's step 3 *Done* note. [[B19]] fixed.
