# Brainstorm

Random thoughts about Candy's design: not decided, not planned, not tech debt. Add one
whenever it comes up; when one turns into real work, move it to a design doc
(`doc/hl_rqmt/`) and leave a pointer here.

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
- **dump** (i.e. needs expansion): IO, rust host, interpreter, reader improvements, repl, jit
- **Map, reduce, fold, etc**: optimized target implementations
- **Joy like recursive macros**: optimized target implementations