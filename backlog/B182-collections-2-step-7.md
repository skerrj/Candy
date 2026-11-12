# B182: collections-2 step 7: equatable

kind: task
state: done
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/check.cdy`, `src/cdy/system.cdy`, `src/cdy/prelude.cdy`, `spec/`
refs: [[B173]]

Step 7 of `doc/hl_rqmt/collections_2.md`. `equatable`, a constraint variable for every type but one that is or holds a function; `=` and `!=` take it, and the generic functions that compare say so (`contains`, `elem-index`, `index-of`, the translator's) (Question 1).

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: built (the HLD's step 7 *Done* note): `equatable`, checked once a
  definition's types are known; `infer-compare` gone. Fixes [[B173]]. The build 0.94 s to
  0.95 s. In review.
- 2026-11-11, the owner: ticked in review.
