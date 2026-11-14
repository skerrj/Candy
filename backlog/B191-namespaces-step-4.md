# B191: namespaces step 4: private names

kind: task
state: review
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-13
where: `src/cdy/core.cdy`, `spec/10-programs.md`
refs: 

Step 4 of `doc/hl_rqmt/namespaces.md`. `(private a b)`: the names kept in their module, not visible unqualified, `m.a` an error; `programs.private` (new).

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-13, Claude: the text's `m/a` is `m.a`, the separator changed in step 2's review
  ([[B189]]); it was:

  ```text
  Step 4 of `doc/hl_rqmt/namespaces.md`. `(private a b)`: the names kept in their module, not visible unqualified, `m/a` an error; `programs.private` (new).
  ```
- 2026-11-13, Claude: built (the HLD's step 4 *Done* note): `(private a b)`, a private
  type's variants with it, and its errors where the name is used or listed. In review.
