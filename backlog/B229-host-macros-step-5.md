# B229: host-macros step 5: Hygiene for built-ins

kind: task
state: review
priority: normal
found: host-macros, 2026-11-22
fixed: host-macros, 2026-11-24
where: `src/cdy/core.cdy`, `spec/50-macros.md`, `spec/10-programs.md`
refs: 

Step 5 of `doc/hl_rqmt/host_macros.md`. A `quasi` template's symbols that name built-ins or prelude names written qualified (`system.text`; [[B46]], narrowed, Question 2); [[programs.shadowing]]'s *for now* about `put` and `text` goes, with an example.

## Notes

- 2026-11-22, Claude: filed on the HLD's acceptance (the owner, 2026-11-22).
- 2026-11-24, Claude: built (the HLD's step 5, "Done"; [[macros.hygiene]]).
