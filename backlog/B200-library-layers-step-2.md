# B200: library-layers step 2: declaration modules, and `translator.cdy`

kind: task
state: done
priority: normal
found: library-layers, 2026-11-15
fixed: library-layers, 2026-11-16
where: `src/cdy/core.cdy`, `src/cdy/expand.cdy`, `src/cdy/system.cdy`, `src/cdy/translator.cdy`
refs: [[B50]], [[library.builtins]]

Step 2 of `doc/hl_rqmt/library_layers.md`. A bodiless `sig` or `deft` allowed in a library module whose forms are all such; the spelling check across all the declaration modules; `py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name` moved to `translator.cdy`; the translator's modules import `translator`, and macro programs get it implicitly (`gensym` calls `fresh-name`). A declaration module is always the library's. Two commits, 2a and 2b (the HLD's Questions 9 and 10).

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
- 2026-11-15, the owner: the declaration module is `translator`, not `host` (the HLD's
  Question 5, revised). Title, `where` and text were:

  ```text
  # B200: library-layers step 2: declaration modules, and `host.cdy`
  where: `src/cdy/core.cdy`, `src/cdy/expand.cdy`, `src/cdy/system.cdy`, `src/cdy/host.cdy`
  ... `fresh-name` moved to `host.cdy`; the translator's modules import `host`, and ...
  ```
- 2026-11-15, the owner: a declaration module is always found in the library (the HLD's
  Question 9), and the step is two commits, not staged (Question 10). The text ended:

  ```text
  ... and macro programs get it implicitly (`gensym` calls `fresh-name`). Staged.
  ```
- 2026-11-15, Claude: 2a built (the HLD's step 2, "2a done"): `translator.cdy`, a
  declaration module with the five, always the library's; every program still sees them
  until 2b.
- 2026-11-16, Claude: 2b built (the HLD's step 2, "2b done"); [[B50]] to review.
- 2026-11-16, the owner: ticked in review.
