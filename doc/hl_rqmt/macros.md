# Candy macros (HLD)

**Status: done; merged into `master` and tagged `macros`.** Branch `macros`, after tag `self-host-cleanup`. All the questions
at the end are decided: the order (below), staging by macro files, `defmacro` with
Scheme-style parameters, the quote forms' names (`quo`, `quasi`, `unq`, `unq-sp`, with no
reader shorthand yet), quoting only in macro code, `tmp__1` gensyms with `__` rejected in
source, binding a macro's name an error, and `cond` as the first macro in the translator.

## Terms: host and target

| | What it is | Today |
|---|---|---|
| **Host** | where the translator itself runs | Python (`bin/py/cdy_translator.py`) |
| **Target** | what the translator writes the program into | Python (`output/foo.py`) |

These are a cross-compiler's terms: GCC running on an x86 laptop and producing ARM code has
an x86 host and an ARM target. Today both are Python, which makes them easy to mix up. There
are three kinds of code to keep apart:

1. **The translator** (`src/cdy/*.cdy`) is written in Candy. Once built, it runs on the **host**.
2. **The program** is written in Candy too. It is translated into the **target** and runs
   later, after translation is done.
3. **Macros** are also written in Candy and sit in the program's files, but they run
   *during* translation, inside the translator. So they run on the **host**, not the target.

The third point is the one that confuses: macro code is part of the program's source but
behaves like part of the translator. A Candy translator hosted on Python and targeting
JavaScript would still run its macros in Python.

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
- The symbol table work (`system.cdy`, `prelude.cdy`) comes after both (branch
  `system-prelude`, `doc/hl_rqmt/system_prelude.md`).

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

### How `load-macros` runs macro code (Python `exec`)

The one place the translator runs Candy code it has just translated. In steps:

1. **Translate.** `expand.cdy` builds the macro program as forms: `form.cdy` (read from
   next to the translator), then the helpers (macro files' other definitions, step 4),
   then one `sig` and one `defn` per `defmacro`, named `macro__NAME` and taking the
   arguments as one `(List Form)` called `args__`. `cdyc.cdy`'s `compile-macros`
   translates it like any program, except that it is macro code (quoting allowed), so the
   result is an ordinary Python module's source, with its own imports of `cdy_rt`.
2. **Pick a namespace.** `load-macros` gets one of the translator's functions
   (`sym-name`) and takes that function's `__globals__`: the dictionary that is the
   translator's module namespace, however the translator was loaded (run as a script,
   imported by `self_host.py`, or under another module name). It copies that dictionary.
3. **`exec`.** It runs `compile(python, "<macros>", "exec")` with the copy as the
   globals. Every `def`, `class` and assignment in the macro program lands in the copy,
   and every global name the macro code looks up is looked up there, when it runs. The
   translator's own namespace is not touched, so a macro can't redefine a translator
   function, and two programs' macros don't see each other.
4. **Put the `Form` names back.** The macro program defined its own `Sym`, `Lst`, `Pos`,
   `NOWHERE`, `sym_name` and so on, from its copy of `form.cdy`: new classes, which the
   translator's `match` (an `isinstance` chain on its own classes) would not recognise.
   So after the `exec`, `load-macros` sets each name that `form.cdy` defines back to the
   translator's value. Python functions look globals up at call time, so from then on the
   macro code builds and takes apart the translator's own `Form`s. (`form.cdy` was still
   needed in step 1: `analyse` must know `Form`'s variants and names to translate the
   macro code.) Only `form.cdy`'s names are put back, so a helper may have the same name
   as some translator function.
5. **Take the macros.** It returns the entries named `macro__...` from the copy; `expand`
   keeps them in `Macro` records. `call-macro` calls one on the argument forms and turns
   any error in it (a `fail`, or a Python exception from a bug) into a `CandyFail` that
   starts with the call's position and the macro's name.

The Python is never written to a file and never checked by mypy. The `exec` is the leak
(`doc/leaks.md`): the translator must run on Python, and macro code relies on Python's
late-bound globals. A translator on another host would need its own way to load
translated code (or an interpreter).

### Why a macro can't simply be a `defn` of the program (Q&A)

*Question (owner): why can't expanding a macro just be like calling any `defn` that gets
read in, producing a form?*

Mostly it is. A macro is compiled as an ordinary `defn` (`macro__when`), and the forms it
returns are treated exactly as if they had been read from the source: they go on to
`analyse`. The one real difference is **when the code runs**:

- **The translator doesn't run the program; it translates it.** A `defn` in the program
  becomes Python text in `output/foo.py`, and nothing executes it until someone runs that
  file, after translation is over. A macro has to run *during* translation: before the
  translator can analyse `(unless (ready) (go))` it needs the form `unless` returns. So
  the macro's code must execute inside the translator's own process, mid-translation.
- **There are two ways to run code inside the translator:** interpret it (an evaluator for
  Candy in the translator; rejected above, as a second implementation of every form and
  built-in), or compile it and load it into the running process. `exec` is that load: an
  `import` of a module that exists only as a string. Writing the Python to a file and
  importing it with `importlib` would be the same thing with an extra file.
- **Lisps hide this** because their compiler always runs inside a live image with
  `eval`/`load`. Clojure compiles and loads each top-level form as it reads it, so a
  `defmacro` is just a function the compiler also calls. A batch translator has no live
  image until we make one; `load_macros` is that step.

**Same-file `defn`s as macro helpers are possible too**: the Clojure model, translating
and loading a file one top-level form at a time, so a macro can call any function defined
above it. It was not chosen (question 1, "rejected: ... would compile parts of the program
twice") because:

- **Top-level code would run at translate time:** a top-level `(put ...)`, or any other
  effect, would run while translating, unless something separates the forms to load.
- **The translator works on whole files:** `analyse` collects all top-level names and
  `deft`s first, so definitions can refer to each other in any order. Loading form by form
  needs everything a form uses defined, and loaded, before it.
- **The program would be compiled twice:** once to load the parts macros use, once for
  the output.

So "helpers live in a separate stage" (macro files) is a choice for simplicity, not a
technical wall. If same-file helpers are wanted later, incremental Clojure-style loading is
the route; its cost is mostly translate-time effects and ordering, not the `exec`.

*Follow-up (owner): eventually, pull this out of the Python "style" so it isn't reinvented
for each target?*

Yes, but the boundary is the translator's **host**, not the program's **target**. Macros
run where the translator runs. A translator on Python that emits, say, JavaScript would
still run its macros with Python's `exec`: a new target needs no new macro machinery. Only
a translator that itself runs elsewhere (built for JavaScript or native code) needs a new
way to run macro code. Most of the machinery is already host-independent Candy:
`expand.cdy` builds the macro program, the translator translates it, and expansion,
stamping and errors are all Candy. The host-specific part is two built-ins, `load-macros`
(load translated code, keep the translator's `Form`s) and `call-macro`. So "pulling it
out" means making those two a declared host interface (a `sig` in `system.cdy`, with each
host implementing them: `exec` here, `new Function`/`eval` in JavaScript, loading a shared
library natively), or else replacing them with an interpreter over Core written in Candy,
which would run on any host but is the second implementation rejected above. With modules,
the macro program can also import the translator's `form` module instead of copying
`form.cdy`, which removes the "put the names back" step, the most Python-specific detail.

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
expanded as the macro when it heads a list. (As built, it does skip binding positions, so
that the error below is the one reported; see step 3.) **Binding a macro's name is an error**
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
   *Done:* `src/cdy/expand.cdy`, between include and analyse (`translate` in `cdyc.cdy`).
   As built:
   - **Compiling.** Each `(defmacro name params body)` becomes
     `(sig macro__name (Fn ((List Form)) Form))` and
     `(defn macro__name (args__) (let ((p1 (at args__ 0)) ...) body))` (a bare name is
     bound to all of `args__`). Neither name can clash with the program's, since source
     can't contain `__`. The macro program is `form.cdy` followed by these, translated as
     macro code (`compile-macros`: `analyse` allows quoting there and nowhere else).
   - **Loading.** `load-macros` (runtime) runs the Python in a copy of the translator's
     module namespace, found from one of its functions (`sym-name`), then puts back every
     name the translator defines, so the macros build the translator's own `Form`s rather
     than those of their copy of `form.cdy`. `call-macro` calls one, and turns an error
     in it (a `fail` or a Python exception) into one at the call: `file:L:C: name: ...`.
   - **`form.cdy` sits next to the translator** (`bin/py/form.cdy`; `self_host.py` copies
     it next to every translator it builds), which reads it to compile macros, as a
     compiler reads its own library files.
   - **Expansion** follows the plan, plus one thing: it leaves alone what isn't an
     expression. That is `sig`, `deft`, `import`, `quo` and `quasi` forms, the name and
     parameters of `defn` and `fn`, `let` names, `match` patterns, and `cond` clauses
     (only their parts are expanded). So `(defn f (m) ...)` with a macro `m` reaches
     `analyse`, which says "m is a macro, so it can't be bound", instead of expanding
     `(m)`. The forms in `format` holes are expanded too.
   - **`gensym`** is in `form.cdy`, over a runtime counter (`fresh-name`) that restarts
     whenever a program's macros are loaded, so a translation doesn't depend on what was
     translated before (T1 and T2 make the same names).
   - **The reader** rejects `__` in a symbol. No reader-agreement input contains `__`, so
     that test needed no skip; the new error is in `test_reader_errors`.
   - **Quoting is only in macro code** now: `tst/cdy/cdyc/quoting.cdy` moved to
     `tst/cdy/cdyc/macro_code/`, and the tests translate it as macro code.
   Tests: `tst/cdy/cdyc/macros.cdy` (`when`, `unless`, a bare-name `my-cond`, a macro with
   no parameters, `gensym`, splicing, a macro in a `format` hole), `test_macro_errors`,
   `test_bin_driver_expands_macros` (away from the repository, so `form.cdy` can only come
   from `bin/py/`), and runtime tests for the new built-ins.
4. **`import-macros`** and helpers in macro files.
   *Done:* as planned, in `include.cdy` and `expand.cdy`. As built:
   - **`include`** resolves `(import-macros name)` like `import` (`name.cdy` next to the
     importing file) but leaves the form, as `(import-macros "path")`, for `expand`.
   - **Loading a macro file** (`import-file`): its forms (with its ordinary `import`s
     included) are expanded like a file of their own (`expand-file`), with the macros of
     its own `import-macros`. Its `defmacro`s are compiled with its helpers (its other
     forms) and with its imports' helpers. Each file is loaded once per file that imports
     it; an `import-macros` cycle is an error.
   - **What an importer gets:** the file's own macros (not the ones it imported, so a file
     imports every macro file whose macros it calls), and its helpers, with those of the
     files it imports (each file's once), for the importer's own `defmacro`s to call.
     Helpers never reach the program: calling one there is "unknown name".
   - **A helper can't use its own file's macros**, only imported ones: the file's macros
     are compiled together with its helpers.
   - **Two macros with one name** (two files, or a file and its import) are an error at
     the second `defmacro`.
   - **`load-macros` restores only `form.cdy`'s names** after the `exec` (it is given
     them, from `top-names`), so a helper can share a name with a translator function
     (tested with a helper named `guard`, like `lower.cdy`'s).
   Tests: `tst/cdy/cdyc/macro_files.cdy` (with `lib/control.cdy`, which imports
   `lib/base_macros.cdy`) and `test_macro_file_errors`.
5. **A real macro in the translator:** `cond` (or whichever question 6 settles on), then
   remove it from `core.cdy`.
   *Done:* `cond` is a macro in `src/cdy/prelude_macros.cdy`, and `core.cdy` and the
   shared table no longer know it. As built:
   - **The prelude's macros** (proposed name and place): a macro file that every file
     imports without saying so, except the prelude itself (`prelude-import` in
     `expand.cdy`). Like `form.cdy`, it sits next to the translator
     (`bin/py/prelude_macros.cdy`, in `self_host.py`'s `LIBRARY`). Its code can't use its
     own macros, so `cond` is written with `if`; and `form.cdy`, which goes into every
     macro program unexpanded, no longer uses `cond` either.
   - **Same output:** the macro builds the nested `if`s `an-cond` made (`(if t e)` for a
     last clause without `else`, which is `If t e nil`), so every program, the translator
     included, translates to the same Python as before; the errors are the same, at the
     `cond` form. It builds the chain from the last clause back, in a loop, so a long
     `cond` (`test_long_cond`, 150 clauses) doesn't recurse in the macro.
   - **Bootstrapping took two rebuilds, A and B.** The translator reads the runtime's table
     live, so removing `cond` from it breaks the old `bin`, which has no prelude. A: the
     prelude mechanism with an empty prelude, `cond` still in the table and `core.cdy`.
     B: `cond` out of both, the macro in the prelude, and the prelude copied into
     `bin/py/` before rebuilding, since a translator expands with its own copy.
   - **The frozen Python translator** dispatches special forms on its own map, so it still
     handles `cond`; with `cond` gone from the table, `cond` used as a value there says
     "unknown name" instead of "a special form, not a value".

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
