# B46: Macro templates aren't hygienic across modules

kind: leak
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/expand.cdy`
refs: [[macros.quoting]]

A template's symbols mean whatever the use site sees (`doc/hl_rqmt/macros.md`, "Rework
point"): a macro whose expansion calls a helper of its own module works only where that
helper is imported. Fix: qualify a template's free symbols, as Clojure's syntax-quote
does, once qualified names exist. From `doc/archive/leaks_modules.md`.
