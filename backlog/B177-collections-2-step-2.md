# B177: collections-2 step 2: the loops in core and lower

kind: task
state: done
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/core.cdy`, `src/cdy/lower.cdy`
refs: [[B123]], [[B69]]

Step 2 of `doc/hl_rqmt/collections_2.md`. `core.cdy`'s and `lower.cdy`'s loops (about 45) onto `map`, `filter`, `fold`, `any`, `all`, `find` and `map-acc`, where each is exactly one; the build's time measured.

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: built (the HLD's step 2 *Done* note): 31 of the 38 loops are one call;
  seven stay. The build 0.97 s to 1.00 s. In review.
- 2026-11-11, the owner: ticked in review.
