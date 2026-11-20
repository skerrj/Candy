# B209: stdlib step 4: The `math` module

kind: task
state: in-progress
priority: normal
found: stdlib, 2026-11-18
fixed:
where: `src/cdy/system.cdy`, `src/cdy/math.cdy`, `spec/60-library.md`
refs: [[library.math]]

Step 4 of `doc/hl_rqmt/stdlib.md`. The four moved (`PI`, `sin`, `cos`, `tan`), and `abs`, `min`, `max`; nothing in the translator uses them. The rule `library.math`.

## Notes

- 2026-11-18, Claude: filed on the HLD's acceptance (the owner, 2026-11-18).
- 2026-11-19, Claude: two commits (the HLD's step 4): 4a, a declaration module with
  Candy, built; 4b, `math` moved.
