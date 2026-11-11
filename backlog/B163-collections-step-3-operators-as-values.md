# B163: collections step 3: operators as values

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections
where: `src/cdy_rt/`, `src/cdy/emit.cdy`, `spec/`
refs: [[B38]]

Step 3 of `doc/hl_rqmt/collections.md`. An operator used as a value (`(fold + 0 xs)`) is the runtime's function of its arguments before the rest; emit's spelling.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-09, Claude: built (step 3; `boot/59` with its commit); in review. `=` and `!=`
  were not values, *for now* ([[B172]]), then are, the owner's choice; the hole that
  remains is [[B173]], new.
- 2026-11-09, the owner: ticked in review.
