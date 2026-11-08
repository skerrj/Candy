# B162: collections step 2: constraint variables and the operators' sigs

kind: task
state: open
priority: normal
found: collections, 2026-11-07
fixed:
where: `src/cdy/check.cdy`, `src/cdy/special.cdy`, `src/cdy/system.cdy`, `spec/`
refs: [[B124]], [[B135]], [[B48]]

Step 2 of `doc/hl_rqmt/collections.md`. `number`, `integer`, `float`, `comparable` and `appendable` in the checker; the operators move from `(op ...)` to `system.cdy` `sig`s, and `infer-op` goes.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
