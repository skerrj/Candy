# B178: collections-2 step 3: the loops in check

kind: task
state: done
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/check.cdy`
refs: [[B123]], [[B69]]

Step 3 of `doc/hl_rqmt/collections_2.md`. `check.cdy`'s loops (about 20) onto the list operations, as step 2; the build's time measured.

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: built (the HLD's step 3 *Done* note): 14 of the 20 loops are one call;
  six stay. Found [[B184]] (an empty start fails mypy), worked around. The build unchanged,
  0.98 s. In review.
- 2026-11-11, the owner: ticked in review.
