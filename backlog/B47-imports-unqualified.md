# B47: Only `(import m)`, everything unqualified

kind: leak
state: done
priority: normal
found: modules, 2026-10-19
fixed: namespaces, 2026-11-14
where: `src/cdy/include.cdy`, `src/cdy/core.cdy`
refs: [[programs.import]]

The MVP of `doc/hl_rqmt/modules.md`: no qualified names, `import-as` or `import-from`,
and no private names, so two modules that both define a name can't be imported into the
same file. Fix: "After the MVP" in the HLD. From `doc/archive/leaks_modules.md`.

## Notes

- 2026-11-14, Claude: fixed by `namespaces` steps 2 to 4 ([[B189]], [[B190]], [[B191]]):
  qualified names (`m.name`, [[programs.qualified]]), `import`'s name list
  (`(import m (a b))`, [[programs.import]]), two imports that define one name an error
  only where it is used unqualified, and private names ([[programs.private]]). Not as
  "After the MVP" proposed: one form, not `import-as` and `import-from`, and no alias
  ([[B187]]). To review.
- 2026-11-14, the owner: ticked in review.
