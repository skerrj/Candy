# B179: collections-2 step 4: the loops in emit

kind: task
state: done
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/emit.cdy`
refs: [[B123]], [[B69]]

Step 4 of `doc/hl_rqmt/collections_2.md`. `emit.cdy`'s loops (about 27) onto the list operations, as step 2; the build's time measured.

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: built (the HLD's step 4 *Done* note): 25 of the 29 loops are one call;
  four stay. The build unchanged, 0.93 s. In review.
- 2026-11-11, the owner: ticked in review.
