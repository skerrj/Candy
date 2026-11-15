# B200: library-layers step 2: declaration modules, and `host.cdy`

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `src/cdy/core.cdy`, `src/cdy/expand.cdy`, `src/cdy/system.cdy`, `src/cdy/host.cdy`
refs: [[B50]], [[library.builtins]]

Step 2 of `doc/hl_rqmt/library_layers.md`. A bodiless `sig` or `deft` allowed in a library module whose forms are all such; the spelling check across all the declaration modules; `py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name` moved to `host.cdy`; the translator's modules import `host`, and macro programs get it implicitly (`gensym` calls `fresh-name`). Staged.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
