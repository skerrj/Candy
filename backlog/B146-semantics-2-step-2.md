# B146: semantics-2 step 2: `at` and `slice` bounds

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/emit.cdy`, `src/cdy_rt/primitives.py`, `src/cdy/*.cdy`, `spec/60-library.md`
refs: [[B35]], [[B71]]

Step 2 of `doc/hl_rqmt/semantics_2.md` (step 7 of `semantics.md`). Out of range an error, negative indexes too (Question 9), in one boot step (the translator has no negative index left); the check's cost measured on the translator's own build. With [[B150]] (a function inside a record), its Question 1; whether to keep the check everywhere is decided with the measured cost (its Question 3).

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
- 2026-11-06, Claude: retitled for `semantics_2.md` (its Question 2, as the owner
  chose): was "semantics step 7: `at` and `slice` bounds".
