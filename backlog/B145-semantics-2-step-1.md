# B145: semantics-2 step 1: numbers

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/special.cdy`, `src/cdy/check.cdy`, `src/cdy/read.cdy`, `spec/`
refs: [[B23]], [[B22]], [[B24]]

Step 1 of `doc/hl_rqmt/semantics_2.md` (step 6 of `semantics.md`). `/` on `Float` and `Double` only, `mod` beside `quot` (Question 4); the sizes and literal ranges (Question 5; overflow and `Float`'s 32 bits on Python left in [[B22]] for `porting-surface`). With [[B153]] (orderings) and [[B151]] (a float shown as its literal), its Question 1.

## Notes

- 2026-11-04, Claude: moved to branch `semantics-2`, as the owner chose at Question 1's
  checkpoint; still `semantics.md`'s step, to be renumbered in `semantics-2`'s HLD.
- 2026-11-06, Claude: retitled for `semantics_2.md` (its Question 2, as the owner
  chose): was "semantics step 6: numbers".
