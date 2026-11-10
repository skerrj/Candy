# B164: collections step 4: `++`, and `+` on numbers only

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections
where: `src/cdy/system.cdy`, `src/cdy/*.cdy`, `spec/`
refs: [[B162]]

Step 4 of `doc/hl_rqmt/collections.md`. `++` joins strings and lists, and `+` is for numbers only: two boot steps, with a script rewriting the translator's `+`s by type.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-09, Claude: built (step 4; `boot/60` with its commit); in review. One boot step,
  not two: the staged library is enough.
- 2026-11-09, the owner: ticked in review; noticed `to-list` ([[B174]], new).
