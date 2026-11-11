# B162: collections step 2: constraint variables and the operators' sigs

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections
where: `src/cdy/check.cdy`, `src/cdy/special.cdy`, `src/cdy/system.cdy`, `spec/`
refs: [[B124]], [[B135]], [[B48]]

Step 2 of `doc/hl_rqmt/collections.md`. `number`, `integer`, `float`, `comparable` and `appendable` in the checker; the operators move from `(op ...)` to `system.cdy` `sig`s, and `infer-op` goes.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-09, Claude: built (step 2; `boot/58` with its commit); in review. `and` and `or`
  are typed built-ins too, not special forms as the HLD said: their short-circuit is
  `lower`'s, by name, as before. `+` takes `addable` until step 4.
- 2026-11-09, the owner: asked whether `?N:number` is Candy syntax: no, the checker's
  own naming of a fresh variable for a constraint variable; kept, with comments in
  `check.cdy`'s header and `core.cdy`'s `constraint-of` (the alternatives, a map in the
  checker's state or a field on `TVar`, cost more for the same).
- 2026-11-09, the owner: ticked in review.
