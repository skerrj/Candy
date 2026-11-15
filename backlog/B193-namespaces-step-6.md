# B193: namespaces step 6: the module in Core

kind: task
state: done
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-14
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`, `src/cdy/lower.cdy`, `src/cdy/emit.cdy`, `tst/py_cdy/`
refs: [[B65]]

Step 6 of `doc/hl_rqmt/namespaces.md`. `Global` with its module and its name, definitions and the table's `global` too; `emit`'s spelling unchanged; the tests' `candy(t1, "form/Sym")` helper.

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-14, Claude: built (the HLD's step 6 *Done* note): the module and the name in
  `Global`, `TCon`, `Clause` and the definitions; `global-key` inside the checker and
  `emit`; `candy(t1, "form.Pos")` in the tests ([[B65]]). In review.
- 2026-11-14, the owner: in review, `""` for a built-in type and for macro code stays,
  *for now* ([[B197]], new). Claude: a comment on `TCon` and `Global`, and the HLD's note.
- 2026-11-14, the owner: ticked in review.
