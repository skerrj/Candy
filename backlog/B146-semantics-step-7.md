# B146: semantics step 7: `at` and `slice` bounds

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/emit.cdy`, `src/cdy_rt/primitives.py`, `src/cdy/*.cdy`, `spec/60-library.md`
refs: [[B35]], [[B71]]

Step 7 of `doc/hl_rqmt/semantics.md`. Out of range an error, negative indexes too (Question 9), in two boot steps (the translator's four negative indexes first); the check's cost measured on the translator's own build.

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
