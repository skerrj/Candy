# B180: collections-2 step 5: the other loops

kind: task
state: done
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/expand.cdy`, `src/cdy/include.cdy`, `src/cdy/cdyc.cdy`, `src/cdy/read.cdy`
refs: [[B123]], [[B69]]

Step 5 of `doc/hl_rqmt/collections_2.md`. The loops in `expand.cdy`, `include.cdy`, `cdyc.cdy` and `read.cdy` (about 31) onto the list operations, as step 2; the build's time measured.

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: built (the HLD's step 5 *Done* note): 29 of the 33 loops (with
  `prelude_macros.cdy`'s `put-parts`) are one call; `read.cdy`'s four stay. The build
  0.95 s to 0.94 s. In review.
- 2026-11-11, the owner: ticked in review.
