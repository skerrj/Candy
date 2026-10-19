# Candy macros (placeholder)

**Status: placeholder.** Nothing here is decided. Proposed as the next major branch after
`self-host-cleanup` (see `doc/hl_rqmt/self_host_cleanup.md`), once errors carry positions,
and ahead of modules (`import` step B) and a Candy type checker.

## Why

- **The spec already plans on them.** `defn` and `cond` are to become macros, `quote` is
  reserved for them (skipped since the iMVP), and `'` is reserved for a Clojure-style reader
  macro (`src/cdy/candy-special.md`).
- **They shrink the translator:** each form that becomes a macro is one fewer special case
  in `core.cdy`.
- **The ground is laid.** The translator is in Candy, and `src/cdy/form.cdy` already defines
  `Form`, the data a macro works on. A macro could be a function `(Fn ((List Form)) Form)`,
  expanded between the reader (and `include`) and `analyse`.
- **Static types don't get in the way.** Expansion comes before analysis, so the type
  checker, whenever it comes, sees only expanded code. That argues for macros before the
  checker; otherwise the checker's rules cover forms that later become macros.

## Why not yet

- **Error positions first.** An error in expanded code needs to point back at the source;
  today only parse errors have a line and column.
- **Running Candy at translate time** is the hard part: a macro runs while the translator
  runs. On Python, the translator could translate the macro definitions, load them as a
  Python module and call them on `Form`s (a leak, but workable).
- **Modules aren't needed**: inclusion is enough to share macros between files at first.

## Decisions it needs

1. **Staging:** must a macro be defined before it's used, or in a separate file
   (compiled first)?
2. **Hygiene:** a `gensym` helper (Common Lisp, Clojure) or full hygiene (Scheme)?
3. **Quasiquote syntax:** probably Clojure's `` ` `` `~` `~@`, plus `'` for `quote`. That
   changes the reader, which ends the check that `parse_cdy` and `read.cdy` agree.
4. **Which forms become macros**, and when: `defn`, `cond`, maybe `let` (it is already an
   applied `fn` in Core).
5. **How a macro is declared and typed:** `(defmacro name (args) body)` with a `sig`, or
   an ordinary `defn` typed `(Fn ((List Form)) Form)` and marked as a macro.
