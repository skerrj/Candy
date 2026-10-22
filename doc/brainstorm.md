# Brainstorm

Random thoughts about Candy's design: not decided, not planned, not tech debt. Add one
whenever it comes up; when one turns into real work, move it to a design doc
(`doc/hl_rqmt/`) and leave a pointer here.

- **rewrite parsec-v4 in Candy**: ref *publish parsec*
- **type checker**: *lean4*?
- **rust host**: *pulled from dump*
- **Curried function types.** Should `(Fn (Int Int) Int)` mean the same as
  `(Fn (Int) (Fn (Int) Int))`, as in ML and Haskell? And should Candy support partial
  application (`(add 1)` as a function of one argument)? Today a `Fn` type takes all its
  arguments at once, and a call must pass them all.
- **Doc strings and other metadata.** How should a definition carry its documentation, and
  other data about it? Today docs are `;;` comments above a form, which the reader drops.
  Some questions:
  - **Where a doc string goes.** In the definition, as in Lisp and Clojure
    (`(defn f (x) "doc" body)`, though `defn` takes exactly one body form), or on the
    `sig`, which already holds the facts about a name apart from its definition
    (`(sig f "doc" (Fn (Int) Int))`)? Or should a comment directly above a definition
    count as its doc?
  - **General metadata,** as Clojure's `^{...}` maps: a doc string as one key among
    others (deprecated, inline, test, since). It would want a reader shorthand, so it
    joins the reader macros planned for `'`.
  - **Who reads it:** a doc generator, the editor (hover), the translator (an inline or
    deprecated flag), macros (a macro could read its argument's metadata), and, with
    modules, what a module exports. Forms already carry one piece of metadata, `Pos`.
- **up, down, down-splice, meta-template**: (`up`, `dwn`, `dwn*`, `mt`); replacements for quote, unquote, quasiquote, and quasi-splice (low pri)
- **dump** (i.e. needs expansion): IO, interpreter, reader improvements, repl, jit
- **Map, reduce, fold, etc**: optimized target implementations
- **Joy like recursive macros**: optimized target implementations
- **Curry**: could this be a macro?
- **Generics**: not sure where we are at... so just a note/question
- **cndy specifice macros**: any boiler plate patterns worth a macro
- **add special forms to the symbol table**: via special spec file
  (`doc/hl_rqmt/symbol_table.md`, question 1)
- **An SRS for the current design:** a requirements spec of the language and translator
  as they are (the HLDs record decisions, branch by branch, not the whole), pointing at
  functional specs where a part needs one (the symbol table, modules, macros, sum
  types, `src/cdy/candy-special.md`), and in time at a test suite or test library that
  checks each requirement (`tst/cdy/` is the start). Open: its format, whether the HLDs
  become its functional specs, and how a requirement names its tests.
- **Build a host and target(s) from their own library files:** a host's and each
  target's `system.cdy` and `prelude.cdy`, and probably another set of files, or a
  completely separate set of spec files that give a system and prelude for each spec
  (`doc/hl_rqmt/multi_target.md`, `doc/hl_rqmt/library.md`)
