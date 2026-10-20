# Candy modules (HLD)

**Status: done (MVP scope); merged into `master` and tagged `modules`.** Branch `modules`,
after tag `macros`. This is `import` step B of `doc/hl_rqmt/self_host_cleanup.md`. The owner chose the simplest option on
every question for the first pass ("Questions", at the end). Qualified names,
`import-as` and `import-from` come later ("After the MVP").

## Where things stand

- **`import` is inclusion** (step A, `src/cdy/include.cdy`): `(import util)` pastes in
  `util.cdy`'s forms, once per program. Every top-level name is global across all the files,
  two files can't define the same name, and a file sees names from files it doesn't import.
  This is the leak in `doc/archive/leaks_self_host_cleanup.md`.
- **The translator leans on that.** Only `cdyc.cdy` imports anything. `core.cdy` uses
  `form.cdy`'s names and `emit.cdy` uses `core`'s and `lower`'s, all without importing
  them, because `cdyc.cdy` includes everything.
- **One program is one Python file**, and so is the translator (`bin/py/cdy_translator.py`).
- **Macros were built expecting this to change** (`doc/hl_rqmt/macros.md`):
  - a template's symbols are plain, so they mean whatever the use site sees ("rework
    point", under "Order");
  - the macro program copies `form.cdy` and swaps in the translator's names after `exec`
    (`doc/archive/leaks_macros.md`);
  - a macro file is compiled once per importer (`doc/tech_debt.md`).

## Goals (MVP)

1. **A file sees only what it defines and what it imports.**
2. **Two files can define the same name**, as long as no file imports both.
3. **The translator keeps rebuilding itself**, with the fixpoint (T1 = T2) intact, after
   its own files are made to import what they use.

Not goals: qualified names, `import-as` and `import-from` ("After the MVP"); separate
compilation; one target module per Candy file; macro hygiene beyond `gensym`; export
lists and private names; search paths beyond "relative to the importing file" (plus the
translator's directory for macros); `system.cdy` and `prelude.cdy`.

## Design (MVP, decided)

### A module is a file

A module is one `.cdy` file. It is named as `import` names it today, as a path relative to
the importing file without `.cdy` (`util`, `lib/util`), and identified by its resolved
absolute path, as inclusion already does. The file being translated is the **top module**.

### `(import m)` is the only import form

`(import m)` makes every top-level name `m` defines visible, unqualified, in the
importing file. That covers every `def` and `defn` (each has a `sig`), and every `deft`
type with its variants. It stays top-level only, and importing the same module twice is
fine.

- **No re-export:** a file doesn't see what its imports import. A file that uses `Form`
  has to import `form` itself.
- **Clashes:**
  - two imports that both define a name are an error at the second import, naming both
    modules (`import: util and other both define greet`);
  - a file's own definition wins over an imported one, so a new name in an import can't
    break the file.
- **A name that isn't visible** is the usual undefined-name error. Where the translator
  knows which module defines the name, the error says so
  (`greet is not defined here; util defines it, but this file doesn't import util`).
- **Built-ins** (the table) are visible everywhere, as today.

### Cycles are an error

Inclusion allows cycles. Modules with top-level values (`(def x (f 1))`) need an order to
initialise in, and an error is simplest (as in OCaml and Go): `import: cycle a -> b -> a`.
Today's cycle test (`tst/cdy/cdyc/imports.cdy`) changes.

The translator has one cycle of its own: `core.cdy` uses `expand.cdy`'s `Macro` type, and
`expand.cdy` uses `core.cdy`'s `top-names`. Moving `Macro` into `form.cdy` breaks it.

### Output: one Python file, names prefixed by module

Namespaces are resolved in Candy's front end, and the output stays one Python file.
`include.cdy` returns the modules in dependency order, each with its forms and its
imports, instead of one flat list of forms. `analyse` resolves each module's names in
that module's scope, which maps each visible Candy name to a Python name. The table
already maps names this way (`table-add-fun name py arity`), so a scope is mostly a
per-module table. Then the modules are lowered and emitted, one after another, into the
same file.

**Python names:**
- the top module's names keep their mangled names, as today, so `translate_file` and
  `main` keep their names;
- every other module's top-level names get its file stem as a prefix: `util__greet`, and
  `Form` from `form.cdy` becomes `form__Form`. No Candy name contains `__`, so a
  prefixed name can't clash with an unprefixed one;
- **two modules with the same stem** in one program (`util` and `lib/util`) are an error.
  That's the simplest rule for now; a path-based prefix can replace it.

`load-macros`' "put back the translator's `form.cdy` names" step uses Python names, so it
has to use the prefixed ones (`form__Sym`). Step 2 checks that the macro program and the
translator prefix them the same way.

### `main`

Only the top module's `main` is the entry point. An imported module can define `main` too:
it is an ordinary, prefixed function there.

### Macros

- **`import-macros` is unchanged.** A macro file's helpers see what the macro file imports.
- **Templates stay plain.** A template that names a function needs the use site to see
  that name. That is the leak the macros HLD planned on; this branch records it.
- **The prelude's macros** (`prelude_macros.cdy`) are still imported into every file.
- A macro still can't expand into an `import` (`doc/leaks.md`).

### The bootstrap

The checked-in translator understands `import` as inclusion. The translator's names are
already unique across its files, so for the translator, inclusion and modules mean the
same thing. Two steps:
1. **Add the imports:** each `src/cdy/*.cdy` file imports what it uses, and the cycle is
   broken, while `import` still means inclusion. The old `bin` builds this unchanged.
2. **Switch to modules:** the old `bin` builds a T1 that has modules, and T1 builds T2.
   The table doesn't change, so no A/B rebuild (as in macros step 5) is needed.

## Steps

1. **The translator imports what it uses**, under inclusion: an import list per file, and
   `Macro` moved into `form.cdy` to break the cycle. Rebuild `bin`.

   *Done:* as planned:
   - `read` imports `form`; `include` imports `form` and `read`; `core` imports `form`;
     `expand` imports `form`, `read`, `include` and `core`; `lower` imports `core`; and
     `emit` imports `form`, `core` and `lower`.
   - `cdyc.cdy` imports `core` before `expand`, so `bin`'s functions moved but didn't
     change.
   - `prelude_macros.cdy` doesn't import `form`: every macro program already gets
     `form.cdy`.
   - Nothing checks these lists yet; step 2 does, since a missing import becomes an
     error then.
2. **Modules:**
   - per-module scopes and prefixed Python names;
   - errors for a clash between imports, a cycle, a repeated stem, and a name that isn't
     imported;
   - tests: `tst/cdy/cdyc/modules.cdy`, with `lib/` files that define the same name and
     are imported by different files; rework `imports.cdy`, which has a cycle;
   - rebuild `bin`, and strike the inclusion leak through.

   *Done.* As built:
   - **`include.cdy`:** `read-modules` (a file) and `text-modules` (text, imports from
     the current directory) return `Module`s (path, key, stem, forms without their
     imports, and `Imp`s), each after those it imports, the top module last. A cycle is
     an error at the import that closes it (`b.cdy:1:1: import: cycle a -> b -> a`), and
     so are two imported modules with one stem. Macro files still use inclusion
     (`read-program`).
   - **`cdyc.cdy`:** `translate-modules` expands each module on its own (with its own
     macro imports and the prelude's macros), works out each module's `Exports`, analyses
     each module, and lowers and emits all their definitions together (`python-of`).
     `translate-expanded` (a macro program) is unchanged: one program, no prefixes.
   - **`core.cdy`:** `Exports` (a module's names, variants, sums and global names) and
     `analyse-module`. `Scope` has `names` (each visible name's global name) and
     `elsewhere` (for the "not imported" error). Names are analysed as Candy names, and
     the global names go in where they reach the output: `Global`s, match clauses
     (`global-clauses`), and the definitions and types of each `Top` (`rename-tops`).
     `lower` and `emit` didn't change.
   - **Runtime:** `map-keys` (new), and `load-macros` finds the translator's `form.cdy`
     names under the prefix of `home`'s Python name (`form__sym_name`). That covered the
     bootstrap too: T1, built with inclusion, has no prefixes; T2 has.
   - **Bootstrap:** one rebuild, as planned; T2 reproduces itself.
   - **Tests:** `tst/cdy/cdyc/modules.cdy` (with `lib/shapes`, `lib/tags` and
     `lib/report`), `imports.cdy` without its cycle, `test_module_errors`, and the tests'
     uses of the translator's internals now use prefixed names (`t1.form__Pos`).
3. **Docs:** the spec (`candy-special.md`, `import`), CLAUDE.md, and any new leaks and
   tech debt.

   *Done* with step 2: the spec's `import`, CLAUDE.md, three leaks (`doc/leaks.md`) and
   four entries in `doc/tech_debt.md`. The editor grammar needed nothing: no new forms.

## After the MVP

- **Qualified names and the other import forms.** One base import, with each spelling
  filling in a record in `include.cdy`:
  ```
  (deft Names (All) (Only ((names (List String)))))
  (deft Import ((path String) (alias String) (names Names)))
  ```
  - `(import m)` would be the stem as alias, with `All`;
  - `(import-as m u)` would be `u`, with `(Only ())`;
  - `(import-from m a b)` would be the stem, with `(Only (a b))`.
  - Each import could always bind a qualifier, defaulting to the stem (`util/greet`), with
    `/` as the separator, as in Clojure. The reader already reads `u/greet` as one symbol.
  - The spellings could become prelude macros only once a macro can expand into an
    `import` (`doc/leaks.md`).
- **"Ambiguous only where used"** in place of the clash-at-import error.
- **Modules all the way to the backend, so each target picks its output unit.** A Candy
  module is a namespace, which the front end settles the same way for every target; how
  many files a backend writes is that target's choice (`doc/hl_rqmt/multi_target.md`,
  "Modules and output units"). Today the module is lost early: a `Global` holds
  `"util__greet"`, so a backend can't tell it is `greet` from `util`. Proposed:
  - `Global`, definitions and type names carry the module and the name
    (`(Global "util" "greet")`);
  - each module's Tops stay grouped, with its imports;
  - each backend spells a reference its own way: flat and prefixed (`util__greet`, as
    now, which suits C), qualified (`util.greet` in Python), or imported (an ES module's
    `import {greet} from "./util.js"`);
  - writing one unit per module (one `.py` per module, as a package) is then an option
    per target, the way to separate compilation.
- **Macro modules on the host:** caching compiled macro files, and letting the macro
  program import the translator's `form` module instead of copying it. Macro code runs in
  the translator, so this concerns the host's modules, whatever the target.
- **Qualified template symbols** in `quasi` (macro hygiene); export lists or private names;
  a plain `import` bringing a file's `defmacro`s; `system.cdy` and `prelude.cdy`.

## Questions (decided: the simplest option for the MVP)

1. **Exports:** everything defined at top level.
2. **Import forms:** only `(import m)`, everything unqualified; the rest after the MVP.
3. **Qualified-name separator:** deferred with qualified names (`/` is the likely choice).
4. **Clashes:** an error at the import; a file's own definitions win.
5. **Output:** one Python file per program.
6. **Cycles:** an error.
7. **Python names:** `stem__name` for every module but the top one; a repeated stem is an
   error.
8. **Macro hygiene:** templates stay plain.
9. **Macros and exports:** `import` doesn't bring `defmacro`s; `import-macros` stays.
