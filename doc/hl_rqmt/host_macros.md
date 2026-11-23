# Macros on the interpreter (HLD)

**Status: accepted (2026-11-22), with the answers to its questions, as proposed (tasks
[[B225]] to [[B231]]); for branch `host-macros`. Epic:
`python_complete.md` (its seventh branch). After tag `interpreter`.** Macros run on the
interpreter instead of being translated to Python and run with `exec` ([[B41]]): macro
code is checked like a program ([[B42]]), gets the prelude ([[B52]]), and is modules,
not inclusion ([[B45]]); a template's built-in names mean the built-ins wherever it
expands ([[B46]], narrowed: Question 2). What runs macros is then Candy's, so a
translator on another host runs them the same way.

## Where things stand

- **How a macro runs today** (`macros.md`, "How `load-macros` runs macro code";
  `expand.cdy`, `load-defs`): a file's `defmacro`s, with `form.cdy`'s definitions and
  its macro files' helpers, become one flat macro program, `macro__NAME` a `defn` from
  `(List Form)` to `Form` for each. `cdyc.cdy`'s `compile-macros` translates it to
  Python (module `""`, quoting allowed, no type check), and `translator.cdy`'s
  `load-macros` runs it with `exec` in a copy of the translator's namespace, putting
  `form.cdy`'s names back to the translator's own so the macros build its `Form`s
  ([[B70]]); `call-macro` calls one, prefixing a panic or a host error with the call's
  position ([[macros.errors-at-call]]). A `Macro`'s function is typed `Any` ([[B49]]).
- **What macro code sees** ([[macros.macro-code]]): the built-ins, `form.cdy`,
  `translator` (for `gensym`'s `fresh-name`) and `string`'s built-ins qualified; its
  macro files' helpers; not the prelude ([[B52]]; so `form.cdy` has `rest-of`). Its
  module is `""` ([[B197]]'s second half). It isn't type-checked by Candy, and its
  Python isn't by mypy ([[B42]]).
- **Macro files** ([[macros.import-macros]]): `(import-macros m)` reads `m.cdy`; its
  `import`s are inclusion, pasting files in as helpers ([[B45]]); a file's macro files
  are compiled for it, again for each file that imports them ([[B63]]).
- **Templates** mean what the use site sees ([[B46]]): `put` expands to `(text x)`, so a
  file that defines `text` breaks every `put` in it, with an error in the expansion.
- **The interpreter** (`interpreter.md`) runs checked Core: `interpret` folds the
  top-level forms into a `Ctx` (globals by `global-key`) and calls `main`. Its table
  has every built-in a program can use, not `translator`'s.
- **The macros in use:** the prelude's `cond` and `put` (`prelude_macros.cdy`), the test
  module's `deftest` and `check` (`test_macros.cdy`), and the test programs' own
  (`tst/cdy/cdyc/macros.cdy`, `macro_files.cdy`, `lib/`). The translator's own source
  calls `cond` 127 times and `put` 18.

## Goals

- **No `exec`:** a macro program is analysed, checked and run on the interpreter; its
  forms cross to the interpreter as `Value`s and its result comes back a `Form`.
  `load-macros` goes, and so does putting `form.cdy`'s names back ([[B41]], [[B70]]).
- **Macro code checked** ([[B42]]): the macro program is type-checked before it runs, so
  a macro that returns an `Int` is an error at its `defmacro`, not a confusing one later;
  a `Macro`'s function is typed, `(Fn ((List Form)) Form)` ([[B49]], narrowed).
- **Macro code gets the prelude** ([[B52]]): `rest`, `Maybe`, `find`; `rest-of` goes.
- **Macro files are modules** ([[B45]]): a macro file is a module, its `import`s real
  imports, its helpers its own definitions; macro code's module is its file's
  ([[B197]]); each macro module is loaded once per translation ([[B63]]).
- **Translated programs unchanged:** macros run while translating, inside the
  translator, so a translated program holds only their expansions and never needs the
  interpreter; it still depends on `cdy_rt` alone. Its Python is byte for byte today's,
  checked at each step by comparing every test program's translation with the `bin`
  before (`cmp3`) and by the fixpoint (the translator, its `cond`s expanded on the
  interpreter, translating itself to the same text). The only differences are at
  translation time: a macro's error messages, macro code's new type errors, and, from
  step 5, a program that defines its own `text` translating where it failed before.
- **Templates' built-ins are hygienic** (Question 2): a symbol in a template that names
  a built-in or a prelude name is written qualified, `system.text`, so a file's own
  `text` doesn't change `put`.

## Not goals

- **`gensym`'s purity** ([[B43]], low): `fresh-name` stays the host's counter, in the
  interpreter's table for macro code only (Question 5).
- **A macro that expands into `import` or `defmacro`** ([[B44]], low): needs top-level
  forms expanded one at a time, before `include`, include and expand one loop
  ([[B224]]); later, though the epic gave [[B44]] to this branch (Question 1).
- **`expand.cdy`'s knowledge of special forms' shapes** ([[B61]]): `syntax.cdy` could
  take it over, but it isn't how macros run; later.
- **`form.cdy` next to every translator** ([[B64]], low): it stays, now as the source
  of macro code's `form` module, which the interpreter needs as Core.
- **A template's helpers across modules** ([[B46]]'s first case): a template that calls
  its macro file's own helper still needs the helper where it expands, since a macro
  file runs only while translating (Question 2).
- **Speed:** macro code was compiled; on the interpreter it is slower per call, but the
  expansions are small (Pros and cons).

## Proposal

### The macro program

A file's macros come, as today, from its own `defmacro`s and its `import-macros`. Each
`defmacro` is still a `defn`, `macro__NAME` of type `(Fn ((List Form)) Form)`
(`macro-program`). What changes is what is done with the program:

1. **Analysed and checked** (`analyse-program`, then `type-check`), as a program is, with
   the imports macro code gets implicitly (`macro-imports`): `form`, the prelude (step 3),
   `translator`'s `fresh-name`, `string` qualified.
2. **Loaded on the interpreter:** its top-level forms folded into a `Ctx`, as
   `interpret` does before it calls `main` (a new `interp.load`, split out of
   `interpret`); a macro is the global `macro__NAME` there (`interp.call`, a global by
   its key with `Value`s in and out, which [[B217]] wants too).
3. **Called through the bridge:** a `Macro`'s function is a Candy closure, `(fn (args)
   ...)`, that turns the argument forms into `Value`s, calls the macro's global, and
   turns the result back into a `Form`; `call-macro` calls it, as now (Question 3).

`expand.cdy` doesn't import the interpreter or the checker: `cdyc.cdy` hands the
Expander a function that does steps 1 and 2 (today it hands it `compile`), so the
expander stays the forms' business.

### Forms as values: the bridge

A new module, `interp_macros.cdy` (Question 6): `form-value`, a translator's `Form` (and
its `Pos`) as the interpreter's value of macro code's `form` module (a `VRec` of module
`form`, its variant and its fields), and `value-form`, back; ten variants, by `match`.
A form is copied each way at each call (Question 4): a `cond` with four clauses is a few
dozen records. The result's check is the type checker's now, so `value-form` meets only
a `Form`'s value; anything else is an internal error.

### Errors

A macro's `fail`, an out-of-range `at` in it and the host's errors (a recursion too
deep) are still reported at the call, with the macro's name
([[macros.errors-at-call]]): `call-macro` does it, retyped generically,
`(Fn ((Fn ((List a)) b) (List a) String) b)` in place of `Any`s, its Python unchanged
(Question 3). What the host's error was changes: `at` out of range is the interpreter's
panic, `f: at: index out of range: 5, for length 0` in place of `f: IndexError`, the
spec's message, so that row of the rule changes. A type error in macro code is a new
error, at the `defmacro`'s code, with its position.

### The prelude for macro code

Macro code imports the prelude implicitly, as a program does. `prelude.cdy` uses no
macros, so it can be loaded before the prelude's macros are, with no cycle; it stays
written without them (a comment says why). `form.cdy`'s `rest-of` goes, for the
prelude's `rest` (the translator's two calls and `test_macros.cdy`'s one).

### Macro files as modules

`(import-macros m)` reads `m.cdy` as a module of the macro world: its `import`s are real
imports (`include.cdy`'s module reading, with the library's search), its other
definitions its own, private as `(private ...)` says; its `defmacro`s are what it gives
the importing file. Macro code's module is its file's stem, a file's own `defmacro`s
included (in a `Ctx` of their own, so the stem is the program's too without a clash),
and `form` is a module it imports, so quoting builds `form.Sym`, closing [[B197]]. The
loaded macro modules are kept in the Expander, which threads through the translation's
files, so each loads once ([[B63]]); a cycle is still an error.

### Hygiene for built-ins (Question 2)

In a `quasi` template, a symbol that names a built-in value (an operator too) or a
prelude name, where the macro is defined, is written qualified: `(text x)` in `put`
becomes `(system.text x)`. A program's own `text` then doesn't change `put` ([[B46]]'s
note, [[programs.shadowing]]). Special forms and macro names stay as they are. A
template that binds a built-in's name (`(let ((text ...)) ...)` in a template) is
unusual; it would be qualified too, and so an error: `gensym` is the way
([[macros.gensym]]).

## Pros and cons

- **For:** macros stop depending on the host running translated Python ([[B41]]); macro
  code is checked like any code ([[B42]]); it sees the library a program sees
  ([[B52]]); four tech-debt or leak items close with it ([[B45]], [[B63]], [[B70]],
  [[B197]]); `translator.cdy` loses its two `Any`-typed macro built-ins; the interpreter
  gets a second user, and the way in [[B217]] wants (`interp.call`).
- **Against:** macro calls are slower, and every form crosses the bridge twice; the
  interpreter's depth (about 130 calls, [[expr.tail-calls]]) bounds a macro's non-tail
  recursion, where Python allowed about 1000 (the translator's macros are loops: `cond`
  is a self tail call, `put` a `map`).
- **The cost, measured:** a `cond`-like expansion of four clauses, written as macro code
  over records of its own and run on the interpreter, takes about 0.2 ms (2000 in 0.45
  s with the front end); the translator's 145 `cond`s and `put`s are a few
  hundredths of a second. Loading the prelude's macros once per translation replaces
  compiling them and running `exec`; step 1 measures the suite's time against today's.
- **Why now:** the interpreter is built and checked against the spec; every item here is
  the epic's for this branch.

## Bootstrap

Steps 1 to 5 are translator code in the language `bin` reads, with no new built-in:
`call-macro`'s new type is a declaration (`translator.cdy`), its Python the same, and
`bin` still uses its own `load-macros` to build T1. Step 6 drops `load-macros` from
`translator.cdy`, `spelling.py` and `primitives.py`; the `bin` before still declares it
and calls it, checking its declarations against the live `spelling.py`, so step 6 is
staged `old-runtime` (`script/bootstrap.py`). If step 3's `prelude_macros.cdy` uses the
prelude, the `bin` before reads its own copy, so no staging there.

## Steps

1. **Macros on the interpreter:** the macro program as today (flat, module `""`, no
   check) analysed and loaded on the interpreter (`interp.load`, `interp.call`); the
   bridge (`interp_macros.cdy`); `Macro`'s function typed, `call-macro` retyped;
   `fresh-name` in the interpreter's table for macro code; the Expander handed a loader
   in place of `compile`. The spec's `IndexError` row; the suite's time compared.
2. **Macro code checked** ([[B42]]): the macro program type-checked before it loads;
   every macro in use passes; [[macros.macro-code]] says it is checked, with an error
   example.
3. **The prelude for macro code** ([[B52]]): imported implicitly; `rest-of` goes;
   [[macros.macro-code]].
4. **Macro files as modules** ([[B45]], [[B63]], [[B197]]): `import-macros` reads a
   module; macro code's module is its file's; each loaded once per translation;
   [[macros.import-macros]].
5. **Hygiene for built-ins** ([[B46]], narrowed; Question 2): a template's built-in and
   prelude names qualified; [[programs.shadowing]]'s *for now* about `put` and `text`
   goes, with an example.
6. **`load-macros` dropped** ([[B41]], [[B70]]; staged): from `translator.cdy`,
   `spelling.py`, `primitives.py`; `macros.md`'s account of `exec` marked history;
   [[B49]] narrowed to `module-dir`.
7. **Docs:** CLAUDE.md ("Macros", "The interpreter"), `macros.md`, `modules.md`'s
   "Macro modules on the host", the epic's seventh branch *done*; "Looking back".

## Questions

1. **Scope:** in, [[B41]], [[B42]], [[B52]], [[B45]], [[B63]], [[B70]], [[B197]]'s second
   half, and [[B46]] for built-ins (Question 2); out, [[B43]] (Question 5), [[B44]],
   [[B61]], [[B64]], each low or not how macros run. **Proposed: as listed.** Or take
   [[B44]] too, expanding top-level forms one at a time before `include`: a change to
   the pipeline's order, its own branch's size.
   *Answer (2026-11-22, the owner): as listed; [[B44]] left out, though the epic gave it
   this branch, and its fix filed as [[B224]] (include and expand as one loop).*
2. **Hygiene:** (a) a template's symbols that name built-ins or prelude names written
   qualified (`system.text`), which fixes `put` and `text`, leaving a template's call of
   its macro file's own helper as it is; (b) Clojure's whole rule, every free symbol
   qualified, a macro file's helpers then needed where it expands, so macro files would
   be imported for the program too, not only while translating; (c) none, [[B46]] left
   open. **Proposed: (a):** the case that bites, every program's `put`, for a small
   change to `quasi`; (b) changes what a macro file is.
   *Answer (2026-11-22, the owner): (a).*
3. **Errors at the call:** keep `call-macro`, retyped generically, catching what the
   interpreter raises (proposed); or have the interpreter return a panic as a value
   (every `eval` a `Result`: a rewrite, and slower); or drop the prefix (worse errors).
   **Proposed: keep `call-macro`, retyped:** one host built-in, its Python unchanged, so
   no staging.
   *Answer (2026-11-22, the owner): as proposed.*
4. **Forms across the bridge:** copied each way at each call (proposed); or a `Value`
   variant holding the translator's `Form` itself, no copy, but the interpreter's
   `match`, `get`, `=` and `show` then each know a second kind of record. **Proposed:
   copied:** the interpreter stays one kind of record, and the copies are small.
   *Answer (2026-11-22, the owner): copied.*
5. **`gensym`** ([[B43]]): `fresh-name` in the interpreter's table, the host's counter,
   for macro code only (proposed); or pure now, a counter passed through expansion,
   every macro taking and returning it. **Proposed: the table entry:** [[B43]] is low,
   and the pure version changes every macro's type.
   *Answer (2026-11-22, the owner): the table entry.*
6. **The bridge's module:** `interp_macros.cdy` (proposed), beside `interp.cdy` and
   `interp_builtins.cdy`; or in `expand.cdy`, which then imports the interpreter.
   **Proposed: `interp_macros.cdy`**, so `expand.cdy` stays the forms'.
   *Answer (2026-11-22, the owner): `interp_macros.cdy`.*
