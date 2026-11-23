# B228: host-macros step 4: Macro files as modules

kind: task
state: open
priority: normal
found: host-macros, 2026-11-22
fixed:
where: `src/cdy/include.cdy`, `src/cdy/expand.cdy`, `spec/50-macros.md`
refs: 

Step 4 of `doc/hl_rqmt/host_macros.md`. `import-macros` reads a module, its imports real ([[B45]]); macro code's module is its file's ([[B197]]); each macro module loaded once per translation ([[B63]]); [[macros.import-macros]].

## Notes

- 2026-11-22, Claude: filed on the HLD's acceptance (the owner, 2026-11-22).
