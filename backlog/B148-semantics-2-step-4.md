# B148: semantics-2 step 4: errors: panics and `Result`

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/prelude.cdy`, `spec/60-library.md`
refs: [[B39]], [[B139]]

Step 4 of `doc/hl_rqmt/semantics_2.md` (step 9 of `semantics.md`). `fail` a panic; `(deft (Result a e) (Ok ((v a))) (Err ((err e))))` in the prelude (Question 11; `catch-panic` left to `test-runner`: [[B139]]).

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
- 2026-11-06, Claude: retitled for `semantics_2.md` (its Question 2, as the owner
  chose): was "semantics step 9: errors: panics and `Result`".
