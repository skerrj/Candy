# B201: library-layers step 3: the system, a module

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`, `src/cdy/emit.cdy`
refs: [[B197]], [[B196]], [[programs.sees]], [[programs.shadowing]]

Step 3 of `doc/hl_rqmt/library_layers.md`. `system` imported implicitly by every file, so every built-in is also `system.name`; a built-in type's module `"system"`, not `""` ([[B197]]'s first half); `programs.sees` and `programs.shadowing`. [[B196]] looked at again.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
