# B12: Module prefixes can collide with mangled names

kind: defect
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/emit.cdy`, `src/cdy/include.cdy`
refs: [[programs.import]], [[B3]]

`util__greet` (module `util`'s `greet`) is also what `py-mangle` makes of a top module's
`util--greet`. Nothing checks. The reader rejects `__` in a name, but not `--`. The repro
needs two files, so it is text. From `doc/tech_debt.md`; the audit's defect 11 (`doc/hl_rqmt/tracking.md`). Related:
[[B3]].
