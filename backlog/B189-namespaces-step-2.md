# B189: namespaces step 2: qualified names

kind: task
state: done
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-12
where: `src/cdy/core.cdy`, `spec/10-programs.md`, `spec/00-syntax.md`
refs: [[B47]]

Step 2 of `doc/hl_rqmt/namespaces.md`. `m.name` for a module `(import m)` imports, for
values, types and variants, and in patterns; the `.` rule in names, and `/` reserved (a
lone `/` the operator); two imports that define one name an error only where it is used
unqualified; `programs.qualified` (new), `programs.import`, `syntax.names`.

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-12, Claude: built (the HLD's step 2 *Done* note): `m/name`, the `/` rule, and a
  clash an error only where the name is used. In review.
- 2026-11-13, the owner: in review, the separator `.`, not `/` (the HLD's Question 3,
  changed), and a `/` in a name still an error, reserved. Claude: rebuilt with `.`
  (`has-dot`, and `name-error` for a definition's `.` or `/`); `.5` is now an error, a
  qualified name with no module. In review.
- 2026-11-13, the owner: ticked in review, the errors for a qualified name that doesn't
  resolve (`qualified-error`): a malformed name, a module the file doesn't import, a name
  the module doesn't define. The rest of the step is still in review.
- 2026-11-13, the owner: `.5` should say it is a number with no digit before its `.`.
  Claude: `number-hint`, for `.5` and `-.5` (`syntax.numbers`); field syntax with `.`
  filed as [[B195]].
- 2026-11-13, Claude: the text rewritten for `.` (the owner's change above) and the rule's
  id, `syntax.names`; it was:

  ```text
  Step 2 of `doc/hl_rqmt/namespaces.md`. `m/name` for a module `(import m)` imports, for values, types and variants, and in patterns; the `/` rule in names (a lone `/` the operator); two imports that define one name an error only where it is used unqualified; `programs.qualified` (new), `programs.import`, `syntax.symbols`.
  ```
- 2026-11-13, the owner: ticked in review.
