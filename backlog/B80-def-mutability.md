# B80: Decide whether a `def` is a constant or a variable

kind: task
state: done
priority: normal
found: tracking, 2026-10-25
fixed: semantics
where: `doc/hl_rqmt/mutation_optimization.md`
refs: [[types.sig]]

No form changes a `def`'s value yet, so it is neither (`doc/hl_rqmt/mutation_optimization.md`,
open question 4). The owner (2026-10-25): "this will eventually be an issue... if it's
undefined as either we should track it".

## Notes

- 2026-11-02, Claude: semantics step 1: decided, a `def` is a constant (*lasting*), stated in [[programs.top-level]] with `defined more than once` as its example; a mutable cell, if one comes, is a form of its own (`doc/hl_rqmt/mutation_optimization.md`).
