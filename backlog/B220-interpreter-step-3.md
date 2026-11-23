# B220: interpreter step 3: Tail calls and panics

kind: task
state: review
priority: normal
found: interpreter, 2026-11-21
fixed: interpreter, 2026-11-22
where: `src/cdy/interp.cdy`
refs: [[expr.tail-calls]], [[library.errors]]

Step 3 of `doc/hl_rqmt/interpreter.md`. Self tail calls as a loop; the panics' messages and exit status as a translated program's; the depth an implementation's (Question 4).

## Notes

- 2026-11-21, Claude: filed on the HLD's acceptance (the owner, 2026-11-21).
- 2026-11-22, Claude: built (the HLD's step 3, "Done").
