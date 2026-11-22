# B208: stdlib step 3: The `test` module

kind: task
state: done
priority: normal
found: stdlib, 2026-11-18
fixed: stdlib, 2026-11-19
where: `src/cdy/test.cdy`, `spec/60-library.md`
refs: 

Step 3 of `doc/hl_rqmt/stdlib.md`. `check`, `deftest`, `test.run`, with its own tests; the rule `library.test`.

## Notes

- 2026-11-18, Claude: filed on the HLD's acceptance (the owner, 2026-11-18).
- 2026-11-19, Claude: built (the HLD's step 3, "Done"), with a new rule the owner chose,
  a top-level `do` spliced ([[programs.top-do]]), so `deftest` can define a name with its
  `sig`; [[B214]] and [[B215]] filed.
- 2026-11-21, the owner: ticked in review.
