# B147: semantics step 8: `def` order

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/core.cdy`, `spec/10-programs.md`
refs: [[B31]]

Step 8 of `doc/hl_rqmt/semantics.md`. An initial value uses only values defined before it, through the functions it calls too, a `fn` in it counted as called (Question 10).

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
