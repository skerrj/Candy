# B182: collections-2 step 7: equatable

kind: task
state: open
priority: normal
found: collections-2, 2026-11-10
fixed:
where: `src/cdy/check.cdy`, `src/cdy/system.cdy`, `src/cdy/prelude.cdy`, `spec/`
refs: [[B173]]

Step 7 of `doc/hl_rqmt/collections_2.md`. `equatable`, a constraint variable for every type but one that is or holds a function; `=` and `!=` take it, and the generic functions that compare say so (`contains`, `elem-index`, `index-of`, the translator's) (Question 1).

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
