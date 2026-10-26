# B50: The translator's five host built-ins are every program's

kind: leak
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/system.cdy`
refs: [[library.builtins]]

`py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name` are in
`system.cdy`, so every program can call them, and a second target would have to provide
them (a program's own definition of one wins). The rest were dropped or rewritten in Candy
(`doc/hl_rqmt/library.md`, "The translator's built-ins become Candy"). Fix: a declaration
file only the translator imports. From `doc/archive/leaks_system_prelude.md`.
