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

## Notes

- 2026-11-13, Claude: found writing `programs.shadowing` (`namespaces` step 5, [[B192]]):
  within one file too, a file that defines `text` (`(defn text (n) ...)`) changes `put`,
  the prelude's macro, which expands to `(text x)`: `(put (text 1))` is "argument 1 of
  text: expected Int, got String", in the expansion. The built-ins have no qualifier yet
  ([[B108]]), so the fix waits for `library`; the rule says so, *for now*.
- 2026-11-24, Claude: narrowed by `host-macros` step 5: a template's built-in and prelude
  names are qualified (`system.text`), so a file's own `text` no longer changes `put`
  ([[macros.hygiene]]). Open for the rest: a template's call of a macro file's own
  helper still needs the helper where the macro is used (Clojure's whole rule, (b) in
  `host_macros.md`'s Question 2).
