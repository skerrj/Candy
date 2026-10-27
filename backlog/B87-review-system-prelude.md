# B87: Review system-prelude steps 1, 3 and 5 as built

kind: task
state: done
priority: normal
found: bootstrap, 2026-10-20
fixed: carried-reviews
where: `doc/hl_rqmt/system_prelude.md`, `src/cdy/system.cdy`, `src/cdy/prelude.cdy`
refs: [[programs.prelude]], [[library.builtins]]

Each step's "Done" note: step 1 (`system.cdy`'s types, and its leaks and tech debt, now
items), step 3 (`prelude.cdy`) and step 5. Carried over in `TODOS.md` for the owner's review.

## Notes

- 2026-10-26, the owner: ticked in review; the HLD has a *Since:* note, naming the 14
  operators that "aren't special forms or operators" leaves out.
