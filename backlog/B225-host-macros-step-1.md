# B225: host-macros step 1: Macros on the interpreter

kind: task
state: done
priority: normal
found: host-macros, 2026-11-22
fixed: host-macros, 2026-11-22
where: `src/cdy/interp_macros.cdy`, `src/cdy/interp.cdy`, `src/cdy/expand.cdy`, `src/cdy/cdyc.cdy`
refs: 

Step 1 of `doc/hl_rqmt/host_macros.md`. The macro program as today (flat, module `""`, no check) analysed and loaded on the interpreter (`interp.load`, `interp.call`); the bridge, forms to values and back (`interp_macros.cdy`, Questions 4 and 6); `Macro`'s function typed, `call-macro` retyped (Question 3); `fresh-name` in the interpreter's table for macro code (Question 5); the Expander handed a loader in place of `compile`. The spec's `IndexError` row; the suite's time compared.

## Notes

- 2026-11-22, Claude: filed on the HLD's acceptance (the owner, 2026-11-22).
- 2026-11-22, Claude: built (the HLD's step 1, "Done").
- 2026-11-24, the owner: ticked in review.
