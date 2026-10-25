# Brainstorm

Random thoughts about Candy's design: not decided, not planned, not tech debt. Add one
whenever it comes up; when one turns into real work, move it to a design doc
(`doc/hl_rqmt/`) and leave a pointer here.

- **variadic args, interfaces, and generics**: *break this up*
- **vscode syntax extension**: `(defn line (level text) (+ (get-indent level) text "\n"))`: get-indent is the same color as args... should be similar to `+`
- **rewrite parsec-v4 in Candy**: ref *publish parsec*
- **type checker**: *lean4*?
  - fork and start rewriting with lean4? 
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
  types, the spec in `spec/`), and in time at a test suite or test library that
  checks each requirement (`tst/cdy/` is the start). Open: its format, whether the HLDs
  become its functional specs, and how a requirement names its tests. *Moved to*
  `doc/hl_rqmt/executable_spec.md` (draft): a Markdown spec whose examples run.
- **An I/O refactor** (the owner, 2026-10-23: "I/O is total crap at the moment"; expect a
  big one): `print`, `display` and `put` are all Python's `print`, typed `Any`, showing
  values with Python's `str()` (`True`, `None`, `(1, 2)`: the leaks in
  `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_system_prelude.md`),
  and the file and path built-ins are thin wrappers. A built-in that shows a value in
  Candy's syntax belongs to it (`doc/hl_rqmt/executable_spec.md`, question 12).
- **"No code changes" commits** (tabled, 2026-10-23; revisit when needed): a docs-only
  commit says so and skips the rebuild, `boot/NN`, linters and tests. Pitfalls found: a
  file in `bin/<target>/` (even a `.md`) changes `bin`; `spec/` is tests, not docs; and the
  label must come from the commit's files (`git diff --cached --name-only`), since it skips
  checks.
- **A better way to review items and tasks:** no ideas yet (the owner, 2026-10-23). *Moved
  to* `doc/hl_rqmt/review.md` (draft), linked from `doc/hl_rqmt/executable_spec.md`.
- **Build a host and target(s) from their own library files:** a host's and each
  target's `system.cdy` and `prelude.cdy`, and probably another set of files, or a
  completely separate set of spec files that give a system and prelude for each spec
  (`doc/hl_rqmt/multi_target.md`, `doc/hl_rqmt/library.md`)
- **Recursion limits and trampolines:** should Candy get a trampoline, or a Clojure-style
  `loop`/`recur` form, for mutual and deep recursion? Today only a self tail call in a
  top-level `defn` that makes no `fn` is a loop (`lower.cdy`, `loop-tail-calls`); the rest
  uses the Python stack (about 1000 levels). And could `self_host.py`'s raise of the
  recursion limit (to 20,000) go once T1 no longer recurses so deeply? See
  `doc/hl_rqmt/mutation_optimization.md` ("Tail calls"), the leak "Only self tail calls
  are loops" (`doc/archive/leaks_imvp_py_translator.md`) and `doc/tech_debt.md`.
- **Variadic types (to revisit):** a `Fn` type for two or more arguments (or any number),
  so the arithmetic and comparison operators, `tup`, and `put`/`print` (typed `Any` now)
  get Candy types and move to `system.cdy` (`doc/leaks.md`, "Some of `special.cdy`'s
  entries are there for want of a type")
  - Macros are variadic already (`(defmacro name args body)` binds `args` to all the
    argument forms; `cond` is one), and untyped (host functions from forms to a form), so
    they never hit the gap. So the operators could be variadic macros over two-argument
    functions: `(+ a b c)` → `(add (add a b) c)`, with only `add` typed. That runs into
    another gap: `+` works on `Int`, `Double` and `String`, and Candy has no overloading or
    type classes, so `add` is `Any` or one function per type. It doesn't help `tup`, whose
    type depends on how many arguments it gets, or `put`.
- **`and` and `or` as macros?** Short-circuiting needn't make them operators: macros over
  `if` (as in Scheme, and like `cond`), or functions with lazy arguments (`doc/leaks.md`,
  "Some of `special.cdy`'s entries are there for want of a type")
- **An interpreter, and what it does to the spec** (from *dump*: interpreter, repl, jit;
  2026-10-24): the spec's examples vs the programs in `tst/cdy/` isn't a cost line, so an
  interpreter wouldn't erase it: an example states one rule, and the programs left in
  `tst/` test whole things (modules importing each other, `main` with arguments, macro
  files, the self-host), integration tests for the test-levels HLD
  (`doc/hl_rqmt/executable_spec.md`, question 11). What it would change:
  - REPL-style examples (`> (+ 1 2)` then `3`), an expression at a time, like doctests;
  - a printer in Candy syntax, which is question 12's deferred show built-in, retiring the
    numbers-and-text rule;
  - a second implementation: every example runs on both, and the spec becomes a
    conformance suite (as for more targets, `doc/hl_rqmt/multi_target.md`).
  It wouldn't type-check: until Candy has a checker, mypy on the translation is the check,
  so the examples still go through the translator. A JIT is speed only, and speed isn't
  the problem (the whole suite is about 20 s).
