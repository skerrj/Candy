# B147: semantics-2 step 3: `def` order

kind: task
state: done
priority: normal
found: semantics, 2026-11-02
fixed: semantics-2
where: `src/cdy/check.cdy`, `spec/10-programs.md`
refs: [[B31]]

Step 3 of `doc/hl_rqmt/semantics_2.md` (step 8 of `semantics.md`). An initial value uses only values defined before it, through the functions it calls too, a `fn` in it counted as called (Question 10).

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
- 2026-11-06, Claude: retitled for `semantics_2.md` (its Question 2, as the owner
  chose): was "semantics step 8: `def` order".
- 2026-11-06, Claude: built (step 3; `boot/55` with its commit); in review.
- 2026-11-06, Claude: added to `programs.def-order`, as the owner asked, the cases
  that may be in any order: mutual recursion, a reference inside another function's body,
  types (`sig`s and fields naming a later `deft`, two `deft`s naming each other) and
  macros, with a run example.
- 2026-11-06, the owner: ticked in review.
