# B50: The translator's five host built-ins are every program's

kind: leak
state: review
priority: low
found: system-prelude, 2026-10-19
fixed: library-layers, 2026-11-16
where: `src/cdy/system.cdy`, `src/cdy/translator.cdy`
refs: [[library.builtins]]

`py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name` are in
`system.cdy`, so every program can call them, and a second target would have to provide
them (a program's own definition of one wins). The rest were dropped or rewritten in Candy
(`doc/hl_rqmt/library.md`, "The translator's built-ins become Candy"). Fix: a declaration
file only the translator imports. From `doc/archive/leaks_system_prelude.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): matters once there is a second target.
- 2026-11-13, Claude: `namespaces` step 5 ([[B192]]) writes it into the shadowing rule,
  [[programs.shadowing]], as *for now*: the five stay in `system.cdy` until `library`
  gives a file of declarations only the translator imports.
- 2026-11-16, Claude: fixed by `library-layers` step 2 ([[B200]]): the five are
  declared in `translator.cdy`, a declaration module, and only a file that imports
  `translator` sees them ("fresh-name is declared by translator, which this file doesn't
  import: (import translator)"); macro code imports it implicitly. A second target still
  needs them while the translator runs on it ([[B49]]'s target extension, later). `where`
  was:

  ```text
  where: `src/cdy/system.cdy`
  ```
