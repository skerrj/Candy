# Candy macros (HLD)

**Status: accepted.** Branch `macros`, after tag `self-host-cleanup`. All the questions
at the end are decided: the order (below), staging by macro files, `defmacro` with
Scheme-style parameters, the quote forms' names (`quo`, `quasi`, `unq`, `unq-sp`, with no
reader shorthand yet), quoting only in macro code, `tmp__1` gensyms with `__` rejected in
source, binding a macro's name an error, and `cond` as the first macro in the translator.

## Why now

- **The spec plans on them.** `defn` and `cond` are to become macros, `quote` is
  reserved for them (skipped since the iMVP), and `'` is reserved for a Clojure-style reader
  macro (`src/cdy/candy-special.md`).
- **They shrink the translator:** each form that becomes a macro is one fewer special case
  in `core.cdy`.
- **The ground is laid.** The translator is written in Candy, `src/cdy/form.cdy` defines
  `Form` (the data a macro works on), and forms carry positions, so an error in expanded
  code can point back at the source.
- **Static types don't get in the way.** Expansion comes before analysis, so the type
  checker, whenever it comes, sees only expanded code. That argues for macros before the
  checker; otherwise the checker's rules cover forms that later become macros.

## Order: macros before modules (decided)

An initial macro implementation comes before modules (`import` step B). The two interact:

- **Hygiene starts with `gensym` only** (Common Lisp style): symbols in a macro's template
  are plain, so a template that names a helper relies on it being visible where the
  macro is used. With inclusion every top-level name is global, so this works for now.
- **Rework point:** once modules exist, a macro's symbols should resolve in the module
  that defined it, the way Clojure's syntax-quote qualifies them. Expect to revisit
  quasiquote then.
- The symbol table work (`system.cdy`, `prelude.cdy`) comes after both.

## Goals

1. **`defmacro`:** a macro is Candy code that takes forms and returns a form, run by the
   translator while it translates.
2. **`quo` and `quasi`** (quote and quasiquote), so a macro can build forms without
   spelling out `(Lst (+ (to-list (Sym "if" NOWHERE)) ...))`.
3. **`gensym`**, for names a macro introduces.
4. **A first real macro** that proves the design: a `when`/`unless` pair in a test
   library; then `cond` moved out of `core.cdy` (decided, question 6).

Not goals: hygiene beyond `gensym`, reader shorthands (`'`, `` ` ``, `~`; later, as reader
macros), macros in the frozen Python translator.

## Proposal

### Writing a macro

```clojure
(defmacro unless (test body)
  (quasi (if (unq test) nil (unq body))))

(defmacro my-cond clauses                ; a bare name: all the arguments, as a (List Form)
  (if (= (len clauses) 0)
    (quo nil)
    (let ((c (list-items (at clauses 0))))
      (quasi (if (unq (at c 0)) (unq (at c 1)) (my-cond (unq-sp (rest-of clauses))))))))
```

- **`(defmacro name (params) body)`**, top level only (decided). Every parameter is a
  `Form`. **Scheme style (decided):** a bare name instead of the parameter list,
  `(defmacro name args body)`, gets all the arguments as one `(List Form)`, as Scheme's
  `(lambda args ...)` does; fixed parameters and a rest don't mix (the macro takes the
  first items off the list itself). The body returns a `Form`. No `sig` is needed (the
  types are fixed), and `defmacro` is a new special form. The name may change later
  (`defsyn`, say, if macros become syntax objects); `defmacro` for now.
- **A call** `(unless (ready) (go))` is a list whose head names a macro. The macro gets the
  argument forms unevaluated and its result replaces the call; expansion repeats until the
  head is no longer a macro, then goes on into the result's parts.
- **Errors:** too few or too many arguments for the parameters is an error at the call.

### Quoting: `quo`, `quasi`, `unq`, `unq-sp` (decided)

| Form | Meaning | Usual name |
|---|---|---|
| `(quo x)` | `x` as a form, unevaluated | quote |
| `(quasi x)` | like `quo`, but with holes | quasiquote |
| `(unq x)` | inside `quasi`: the value of `x` (a `Form`) | unquote |
| `(unq-sp xs)` | inside a list in `quasi`: the items of `xs` (a `(List Form)`), spliced in | unquote-splicing |

- **Plain special forms, no reader shorthand yet** (decided). The reader doesn't change, so
  `parse_cdy` and `read.cdy` still agree on every input, and `'` stays reserved for a
  shorthand later (as a reader macro, as the spec says), with `` ` `` and `~` free.
- **`quo` replaces `quote`**, which has been reserved (`[SKIP]`) since the iMVP: the spec
  and `table.py`'s special forms change. The frozen Python translator rejects `quote` by
  name (`NOT_IN_IMVP` in `core_cdy.py`), so renaming it in the shared table must keep it
  rejecting `quo` too (step 1).
- `analyse` rewrites `quo`/`quasi` into calls that build `Form` values (`Sym`, `Lst`,
  literals), so nothing new reaches `lower` or `emit`.
- **Only in macro code** at first (decided, question 3): an ordinary program has no use for a
  `Form` value yet, and its runtime has no `Form` type.

### Running macros: compile them, load them into the translator (accepted)

The translator runs on Python (`bin/py/`), so a macro runs there too, whatever the
program's target: macros run where the translator runs, not where the program runs.

1. The translator collects the macro code (the `defmacro`s and the definitions they use;
   staging, below) into a small program, translates it with itself (`translate`), and
   hands the Python to a new runtime built-in that executes it.
2. The macro code runs in a copy of the translator's own module namespace, so its `Sym`,
   `Lst` and `Form` are the translator's classes, and the forms it returns are ones the
   translator can `match`. (If the macro program brought its own copy of `form.cdy`, its
   classes would be different ones, and `match` would see no variant.)
3. Expansion calls the loaded macro functions on `Form`s.

This reuses the whole translator, needs only a couple of runtime built-ins, and keeps
macro code ordinary Candy (typed by mypy like the rest, through the generated code). It is
a leak to record: Candy code is run with Python's `exec`.

**Rejected: an interpreter.** A Candy evaluator over Core, written in Candy, would make
macros independent of the translator's host, but it means a second implementation of
every form and every built-in (each needs a Python function to call by name), and macro
code would run slowly. The translator's host is Python for the foreseeable future
(`doc/hl_rqmt/multi_target.md` plans other targets for programs, not for the translator).

### Staging: what macro code can use (decided, question 1)

Macro code runs before the program exists, so it can't call functions that the program
defines and expansion hasn't seen yet. Decided:

- **Macro files:** `(import-macros lib/when)` reads `lib/when.cdy` like `import`, but its
  forms go into the macro program, not into the program: its `defmacro`s become available
  to the importing file, and its `defn`s are helpers that run at translate time only.
- A macro file can `import` ordinary files (their definitions become helpers too) and
  `import-macros` other macro files (whose macros expand inside it).
- **`defmacro` outside a macro file** is allowed, with a body that may use only built-ins,
  `Form` and its helpers (`form.cdy`), and what the file's `import-macros` brought. That
  covers short macros without a separate file, and keeps the rule simple: the macro
  program never needs the program's own definitions.

This is Racket's and Clojure's idea (macros and their helpers live in a separate stage)
in its simplest form. Inclusion makes it workable before modules.

### Where expansion happens

`read` → `include` (imports and macro imports) → **expand** → `analyse` → `lower` →
`emit`. A new step `src/cdy/expand.cdy` walks the forms:

- a list whose head is a macro is replaced by its expansion (repeatedly);
- `quo` and `quasi` bodies aren't expanded (except the parts under `unq` and `unq-sp`);
- the parts of everything else are expanded.

It doesn't know about local names, so a local variable named like a macro would still be
expanded as the macro when it heads a list. **Binding a macro's name is an error**
(decided, question 5): `analyse` rejects a `let`, `fn`, `defn` parameter or pattern name
that names a macro, and a `def`/`defn` of one.

### Positions

The forms a macro returns are made at translate time, so their positions are `NOWHERE`
or wherever the macro's own source put them. **Expansion stamps the call's position** on
every form in the result that is `NOWHERE`, so an error in expanded code points at the
macro call. Forms passed through from the arguments keep their own positions.

### `gensym`

`(gensym "tmp")` returns a fresh symbol (`tmp__1`, `tmp__2`, ...) that no source program
can spell, for a name a macro introduces. The counter is state in the runtime (a leak: the
only impure built-in besides I/O). **The reader rejects `__` in a symbol** (decided,
question 4), so a gensym can't be forged; only expansion makes such names. That is a
change to `read.cdy` the frozen `parse_cdy` won't get, so the check that the two readers
agree skips inputs with `__` (step 3).

## Through the translator

| Layer | Change |
|---|---|
| reader (`read.cdy`) | nothing (no shorthand yet) |
| `include.cdy` | `import-macros`: a second form list, the macro program |
| `expand.cdy` (new) | compile and load the macro program; expand macro calls; stamp positions |
| `core.cdy` | `defmacro` (only in the macro program), `quo`/`quasi` to `Form` constructors |
| runtime | run a translated macro program in the translator's namespace; `gensym` |
| `lower`, `emit` | nothing new |

The Python translator stays frozen: programs with macros are tested under the Candy
translator only (`tst/cdy/cdyc/`). With no reader change, the check that `parse_cdy` and
`read.cdy` agree stays as it is.

**Bootstrapping.** The translator can only use macros in its own source after `bin` has
learned them (two rebuilds, as with `import`). Moving `cond` out of `core.cdy` comes last.

## Steps

1. **Names:** `quo`, `quasi`, `unq`, `unq-sp` and `defmacro` as special forms in the table
   (replacing `quote`), the spec updated, and the frozen Python translator still rejecting
   them.
   *Done:* in `table.py` (`quote` removed), `src/cdy/candy-special.md`, the VS Code
   grammar, and `CLAUDE.md`. The Python translator needed no change: a special form it
   has no rule for is "a special form, not a value" (`test_macro_forms_rejected`); it
   still rejects `quote` from its own list. The Candy translator says "not supported by
   the Candy translator yet" until steps 2 and 3.
2. **`quo` and `quasi`** in `analyse`, usable in macro code; tests that they build the
   right forms.
   *Done:* `an-quo` and `an-quasi` in `core.cdy` build `Form`s with `Form`'s constructors
   (`Sym`, `Lst`, the literals), all at `NOWHERE`; `unq-sp` joins a list's parts with `+`.
   Until step 3 limits them to macro code, they need the program to have `Form` (from
   `form.cdy`): `quo: only in macro code (it needs Form, from form.cdy)` otherwise. A
   `quasi` inside a `quasi` is an error for now. Tests: `tst/cdy/cdyc/quoting.cdy`
   (imports `form.cdy`, writes the forms back as text) and `test_quoting_errors`.
3. **`defmacro` and expansion**, with `defmacro` bodies limited to built-ins and `Form`
   helpers; `gensym` and `__` rejected by the reader; binding a macro's name an error;
   position stamping. Tests: `when`/`unless`, argument count errors, an
   error inside an expansion pointing at the call.
4. **`import-macros`** and helpers in macro files.
5. **A real macro in the translator:** `cond` (or whichever question 6 settles on), then
   remove it from `core.cdy`.

## Questions (all decided)

1. **Staging:** macro files via `import-macros`, plus same-file `defmacro`s limited to
   built-ins and macro-file helpers. (Rejected: a `defmacro` using any definition above it
   in the same file, which would compile parts of the program twice.)
2. **Macro parameters:** Scheme style, fixed `Form` parameters or a bare name for all the
   arguments as a `(List Form)`.
3. **Quoting outside macros:** not yet; `quo`/`quasi` only in macro code. (Later: `Form`
   values in ordinary programs, with the `Form` type in the runtime.)
4. **`gensym` names:** `tmp__1`, and the reader rejects `__` in source names.
5. **Shadowing:** binding a macro's name is an error. (Rejected: a local hiding a macro,
   which would need expansion to track `let`, `fn` and pattern bindings.)
6. **First macro in the translator:** `cond`, after `when`/`unless` in tests. (`defn`
   later, if at all: `sig` attaches to it and tail-call loops look for it.)
7. **Quasiquote characters:** no shorthand yet; the forms are `quo`, `quasi`, `unq` and
   `unq-sp`. A shorthand (and its characters) comes later as a reader macro.
