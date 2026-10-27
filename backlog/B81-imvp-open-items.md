# B81: Settle the iMVP doc's open items

kind: task
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: triage
where: `doc/hl_rqmt/iMVP_py_translator.md` ("Open items (summary)")
refs:

`deft` (proposed), the literal parser rules, and confirming that `defn` and `sig` are top
level only and that a top-level `do` isn't spliced. Carried over in `TODOS.md` since the
iMVP.

## Notes

- 2026-10-26, the owner: done in triage ([[B103]]): the spec settles each item, and its files are
  `stable` (`deft`, `get` and `assoc` in `spec/20-types.md`, the literals in
  `spec/00-syntax.md`, top level only, `do` too, in [[programs.top-level]]); the iMVP
  doc's *proposed* marks are history.
