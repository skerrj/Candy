# B192: namespaces step 5: the rules written down

kind: task
state: done
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-13
where: `src/cdy/core.cdy`, `spec/10-programs.md`, `spec/50-macros.md`
refs: [[B40]], [[B11]], [[B50]]

Step 5 of `doc/hl_rqmt/namespaces.md`. One namespace, what every file sees, shadowing (`programs.top-level`); a variant, value or type with the same name as a macro an error (`macros.defmacro`).

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-13, Claude: built (the HLD's step 5 *Done* note): `programs.namespace`,
  `programs.sees` and `programs.shadowing` (new, under `programs.top-level`); a `deft`
  with the same name as a macro an error ([[B11]], done); [[B40]] kept; notes on [[B50]] and [[B46]].
  In review.
- 2026-11-14, the owner: "with the same name as a macro", not "named like a macro".
  Claude: the text reworded; it was:

  ```text
  Step 5 of `doc/hl_rqmt/namespaces.md`. One namespace, what every file sees, shadowing (`programs.top-level`); a variant, value or type named like a macro an error (`macros.defmacro`).
  ```
- 2026-11-14, the owner: a table of the naming rules, in this step, with a `Target` row
  for a target's own limits (Python's, for now). Claude: `spec/00-syntax.md`, "Naming
  rules, in one place", an index linking each rule; and "with the same name as a
  qualifier" in the HLD's Question 8 and [[B195]].
- 2026-11-14, the owner: ticked in review.
