# B189: namespaces step 2: qualified names

kind: task
state: open
priority: normal
found: namespaces, 2026-11-12
fixed:
where: `src/cdy/core.cdy`, `spec/10-programs.md`, `spec/00-syntax.md`
refs: [[B47]]

Step 2 of `doc/hl_rqmt/namespaces.md`. `m/name` for a module `(import m)` imports, for values, types and variants, and in patterns; the `/` rule in names (a lone `/` the operator); two imports that define one name an error only where it is used unqualified; `programs.qualified` (new), `programs.import`, `syntax.symbols`.

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
