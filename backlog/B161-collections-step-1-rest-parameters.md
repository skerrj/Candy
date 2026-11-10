# B161: collections step 1: rest parameters

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections
where: `src/cdy/check.cdy`, `src/cdy/core.cdy`, `src/cdy/emit.cdy`, `src/cdy/system.cdy`, `spec/`
refs: [[B99]], [[B171]], [[expr.rest]]

Step 1 of `doc/hl_rqmt/collections.md`. `(Rest t)` in a `Fn` type, last (Question 1, *lasting*); the checker (the arguments from the rest on, each against `t`; as a value, the arguments before it) and emit (Python's `*rest: T`); `List` a built-in over it, `(sig List (Fn ((Rest a)) (List a)))`.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-08, Claude: built (step 1; `boot/57` with its commit); in review. `List` stays
  the analyser's constructor ([[B171]], the owner's choice).
- 2026-11-09, the owner: ticked in review.
