# Candy macros (HLD)

**Status: draft.** Branch `macros`, after tag `self-host-cleanup`. Nothing here is decided
except the order (below). The open questions are at the end.

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
2. **`quote` and quasiquote**, so a macro can build forms without spelling out
   `(Lst (+ (to-list (Sym "if" NOWHERE)) ...))`.
3. **`gensym`**, for names a macro introduces.
4. **A first real macro** that proves the design. Proposed: a `when`/`unless` pair in a
   test library; then `cond` moved out of `core.cdy` (open question 6).

Not goals: hygiene beyond `gensym`, reader macros other than the quote family, macros in
the frozen Python translator.

## Proposal

### Writing a macro

```clojure
(defmacro unless (test body)
  `(if ~test nil ~body))

(defmacro my-cond (& clauses)            ; & collects the rest as (List Form)
  (if (= (len clauses) 0)
    `nil
    (let ((c (list-items (at clauses 0))))
      `(if ~(at c 0) ~(at c 1) (my-cond ~@(rest-of clauses))))))
```

- **`(defmacro name (params) body)`**, top level only. Every parameter is a `Form`; a final
  `& rest` collects the remaining arguments as a `(List Form)`. The body returns a `Form`.
  No `sig` is needed (the types are fixed), and `defmacro` is a new special form.
- **A call** `(unless (ready) (go))` is a list whose head names a macro. The macro gets the
  argument forms unevaluated and its result replaces the call; expansion repeats until the
  head is no longer a macro, then goes on into the result's parts.
- **Errors:** too few or too many arguments for the parameters is an error at the call.

### Quote and quasiquote

| Reader | Form | Meaning |
|---|---|---|
| `'x` | `(quote x)` | `x` as a form, unevaluated |
| `` `x `` | `(quasiquote x)` | like quote, but with holes |
| `~x` | `(unquote x)` | inside a quasiquote: the value of `x` (a `Form`) |
| `~@xs` | `(unquote-splicing xs)` | inside a quasiquoted list: the items of `xs` (a `(List Form)`) |

- These are Clojure's characters. `'` is already reserved for this; `` ` `` and `~` are
  ordinary symbol characters today and become reserved (the reader rejects them in a
  symbol). Clojure's `~` is chosen over Scheme's `,` because Candy might want `,` later.
- `analyse` rewrites `quote`/`quasiquote` into calls that build `Form` values (`Sym`,
  `Lst`, literals), so nothing new reaches `lower` or `emit`.
- **Only in macro code** at first (open question 3): an ordinary program has no use for a
  `Form` value yet, and its runtime has no `Form` type.

### Running macros: compile them, load them into the translator (proposed)

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

### Staging: what macro code can use (open question 1)

Macro code runs before the program exists, so it can't call functions that the program
defines and expansion hasn't seen yet. Proposed:

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
- `quote` and quasiquote bodies aren't expanded (except quasiquote's unquoted parts);
- the parts of everything else are expanded.

It doesn't know about local names, so a local variable named like a macro is still
expanded as the macro when it heads a list (open question 5).

### Positions

The forms a macro returns are made at translate time, so their positions are `NOWHERE`
or wherever the macro's own source put them. **Expansion stamps the call's position** on
every form in the result that is `NOWHERE`, so an error in expanded code points at the
macro call. Forms passed through from the arguments keep their own positions.

### `gensym`

`(gensym "tmp")` returns a fresh symbol (`tmp__1`, `tmp__2`, ...) that no source program
can spell, for a name a macro introduces. The counter is state in the runtime (a leak: the
only impure built-in besides I/O). `__` is chosen because the reader accepts it but a
Candy program is unlikely to use it; the reader could reject it in source to make it
certain (open question 4).

## Through the translator

| Layer | Change |
|---|---|
| reader (`read.cdy`) | `'`, `` ` ``, `~`, `~@` read as `quote`, `quasiquote`, `unquote`, `unquote-splicing` lists |
| `include.cdy` | `import-macros`: a second form list, the macro program |
| `expand.cdy` (new) | compile and load the macro program; expand macro calls; stamp positions |
| `core.cdy` | `defmacro` (only in the macro program), `quote`/`quasiquote` to `Form` constructors |
| runtime | run a translated macro program in the translator's namespace; `gensym` |
| `lower`, `emit` | nothing new |

The Python translator stays frozen: programs with macros are tested under the Candy
translator only (`tst/cdy/cdyc/`). Adding `'` and friends to `read.cdy` ends the check
that `parse_cdy` and `read.cdy` agree on every input; it becomes "agree on inputs without
the new characters".

**Bootstrapping.** The translator can only use macros in its own source after `bin` has
learned them (two rebuilds, as with `import`). Moving `cond` out of `core.cdy` comes last.

## Steps

1. **Reader:** the quote characters, and their tests.
2. **`quote` and quasiquote** in `analyse`, usable in macro code; tests that they build
   the right forms.
3. **`defmacro` and expansion**, with `defmacro` bodies limited to built-ins and `Form`
   helpers; `gensym`; position stamping. Tests: `when`/`unless`, argument count errors, an
   error inside an expansion pointing at the call.
4. **`import-macros`** and helpers in macro files.
5. **A real macro in the translator:** `cond` (or whichever question 6 settles on), then
   remove it from `core.cdy`.

## Open questions

1. **Staging:** macro files via `import-macros`, plus same-file `defmacro`s limited to
   built-ins and macro-file helpers (proposed)? Or let a `defmacro` use any definition
   above it in the same file (more convenient, but the translator then compiles parts of
   the program twice and must order them)?
2. **Macro parameters:** `Form` parameters with `& rest` (proposed, as in Clojure), or a
   single `(List Form)` of all the arguments (simpler to implement, clumsier to write)?
3. **Quote outside macros:** keep `quote`/quasiquote to macro code for now (proposed), or
   give ordinary programs `Form` values too (the runtime would then need the `Form` type)?
4. **`gensym` names:** `tmp__1` (proposed), and should the reader reject `__` in source
   names to make gensyms unforgeable?
5. **Shadowing:** should a local name hide a macro of the same name (expansion would then
   need to track `let`, `fn` and pattern bindings), or is it an error to bind a macro's
   name (proposed: simpler, and it catches the confusing case)?
6. **First macro in the translator:** `cond` (proposed: it is variadic and the translator
   uses it everywhere, so it tests the design hard), `defn` (as the spec says; it expands
   to `def` plus `fn`, but `defn` is also what `sig` attaches to and what tail calls look
   for), or neither yet?
7. **Quasiquote characters:** Clojure's `` ` `` `~` `~@` (proposed) or Scheme's
   `` ` `` `,` `,@`?
