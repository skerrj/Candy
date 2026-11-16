# B199: library-layers step 1: A library module, found by name

kind: task
state: done
priority: normal
found: library-layers, 2026-11-15
fixed: library-layers, 2026-11-15
where: `src/cdy/include.cdy`, `spec/10-programs.md`
refs: [[programs.import]], [[B66]], [[B68]], [[B62]]

Step 1 of `doc/hl_rqmt/library_layers.md`. The library directory (next to the translator) in `include.cdy`'s lookup, after the importing file's directory; the rule in `programs.import`; a test program importing a library module. And the prelude's costs measured (Question 7): the build, and a small program's translation, with and without it.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
- 2026-11-15, Claude: built (the HLD's step 1 *Done* note): the library directory in
  `import-path`, `special` and `prelude_macros` not modules, `library_module.cdy`; the
  prelude's costs measured. To review.
- 2026-11-15, the owner: ticked in review.
