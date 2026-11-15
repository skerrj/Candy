# B199: library-layers step 1: A library module, found by name

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `src/cdy/include.cdy`, `spec/10-programs.md`
refs: [[programs.import]], [[B66]], [[B68]], [[B62]]

Step 1 of `doc/hl_rqmt/library_layers.md`. The library directory (next to the translator) in `include.cdy`'s lookup, after the importing file's directory; the rule in `programs.import`; a test program importing a library module. And the prelude's costs measured (Question 7): the build, and a small program's translation, with and without it.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
