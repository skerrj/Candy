# `system.cdy` and `prelude.cdy` (HLD)

**Status: done (MVP scope); steps 1, 3, 4 and 5 built, step 2 dropped.** Branch
`system-prelude`, after tag `modules`. The owner chose the simplest option on every
question ("Questions", at the end); the proposal below is the first pass.

*Since (reviewed 2026-10-26):* "the 66 that aren't special forms or operators" means
all 14 operators (`+ - * / quot`, `= != < > <= >=`, `and or not`), which `special.cdy`
declares untyped ([[B48]]); `symbol-table` made the built-ins one map (`special.cdy`,
`system.cdy`), `library` made the list, string and map operations built-ins (75 `sig`s;
the prelude is `rest` and `map-update`), and `runtime-names` renamed `table.py` and
`table_defs.py` to `spelling.py` and `primitives.py`. The rest is kept as history.

## Where things stand

- **Built-ins live in Python.** `src/cdy_rt/table.py` lists 100 entries:
  - 57 calls to runtime functions (`len`, `slurp`, `map-get`, ...);
  - 14 operators (`+`, `=`, `and`, `not`, ...);
  - 7 constants (`PI`, `nil`, `empty-list`, ...);
  - `at` and `slice`;
  - the 20 special forms.

  Each entry has a Python name, a kind (how `emit` writes it) and an arity. None has a
  Candy type: mypy reads the runtime functions' types from `table_defs.py`'s annotations.
- **The translator asks the table** whether a name is a special form or an operator, and
  for its kind and arity (`core.cdy`), and for its Python name (`emit.cdy`).
- **Decided long ago** (iMVP doc, "Signature statement"): `system.cdy` declares the
  built-ins with **bodiless `sig`s** (Carp's `register`, without a separate form), and
  `prelude.cdy` holds ordinary Candy definitions that every program gets. Everywhere else
  a bodiless `sig` stays an error.
- **Already in place:** library files next to the translator (`form.cdy`,
  `prelude_macros.cdy`, copied into `bin/py/`), and an implicit import into every file
  (`prelude_macros.cdy`). Modules give a file's own definitions priority over imports.
- **`doc/hl_rqmt/multi_target.md`** plans to split `table.py` into a target-neutral table
  (name, kind, arity, Candy type) and one mapping per target (the Python name), with the
  neutral half in Candy. The layout across targets is open there ("Open: abstracting
  `system.cdy`").

## Goals

1. **Every built-in has a Candy type**, declared in Candy: `(sig len (Fn ((List a)) Int))`
   in `src/cdy/system.cdy`. Types are documentation, and arity checks, until Candy has a
   type checker; then they are its input.
2. **`table.py` shrinks to the Python mapping:** a built-in's Python name and kind. Its
   arity comes from the `sig`. (As built, `table.py` keeps `arity` for the frozen Python
   translator; see step 2.)
3. **`prelude.cdy`:** Candy definitions every program gets, starting with a few generic
   list functions that Candy code keeps writing by hand.
4. **The translator keeps rebuilding itself.**

Not goals: the multi-target layout of `system.cdy` (one file, for Python, for now);
interfaces or `Collection`; Candy's type checker; moving the special forms out of the
table (question 9); macro programs getting the prelude (question 8).

## Proposal

### `system.cdy`: built-ins, declared

A library file next to the translator, like `form.cdy`. It holds only bodiless `sig`s:

```
;; Strings
(sig strip (Fn (String String) String))
(sig to-int (Fn (String) Int))
;; Maps
(sig map-get (Fn ((Map k v) k) v))
(sig map-keys (Fn ((Map k v)) (List k)))
;; Values
(sig PI Double)
(sig empty-list (List a))
```

- **The translator reads it on every translation**, before analysing, into a map from
  name to `CType`. It isn't a module: built-in names stay unprefixed and visible
  everywhere, as the table's are now.
- **It is checked against the table**, both ways:
  - every `sig` must have a Python mapping in `table.py`;
  - every table entry other than a special form must have a `sig`.

  So a new built-in needs both halves: `built-in x has no sig in system.cdy`, or
  `system.cdy: x has no Python mapping`.
- **Arity comes from the `sig`:** the number of `Fn` parameters. A constant (not a `Fn`)
  is a value. `table.py` loses its `arity` field once the old `bin` no longer reads it
  (see "Bootstrap").
- **Bodiless `sig`s are allowed only in `system.cdy`**, as decided. Elsewhere the error
  stays `sig for x, but no def or defn of x in this file`.

### Types that don't fit yet (questions 2–4, decided)

- **Operators stay out of `system.cdy`** (`+`, `=`, `and`, `not`, ...: the table's
  `binop`, `compare`, `boolop` and `unary` kinds). They take two or more arguments, which
  a `Fn` type can't say, and the table already describes them. So `system.cdy` covers the
  66 calls, values, `at` and `slice`.
- **`print`, `display` and `put` take any number of arguments:** typed `Any`. A built-in
  whose type isn't a `Fn` has no arity to check, which is what they need. A leak.
- **Overloaded built-ins:** `len`, `at` and `in` work on lists, strings and maps. Without
  interfaces there is no honest type, so a type variable where one fits and `Any` where
  it doesn't, each a leak. That is what `Collection` (iMVP doc) will fix.
- **Runtime types with no Candy name** (the result of `re-compile`): `Any`, as today.

### `prelude.cdy`: definitions every program gets

A library file next to the translator, imported into every file except itself, as
`prelude_macros.cdy` is.
- **It is a module** (stem `prelude`, names `prelude__map` in Python), written against the
  built-ins.
- **It is an ordinary import** (question 5): a file's own definitions win over it, as
  over any import, so a program that defines its own `map` keeps working. A module the
  file imports that defines one of the prelude's names is a clash, as between any two
  imports.
- **Output** (question 7): all the prelude's definitions go into every program's Python
  file.
- **First contents** (question 6): `rest` (all but the first item; `form.cdy`'s
  `rest-of` is this for `Form`s), `map`, `filter` and `fold`. The translator doesn't start
  using them on this branch.

  Each is a `defn` with a generic `sig`, such as `(sig map (Fn ((Fn (a) b) (List a)) (List b)))`.
- **Prelude macros stay separate** (question 10): `prelude_macros.cdy` runs at translate
  time, `prelude.cdy` at run time, and a macro file's `defn`s are helpers, not program
  code.

### Bootstrap

The checked-in `bin` reads the live `table.py`, as in macros step 5. So:
1. **Add `system.cdy`** and the reading and checking, while `table.py` keeps its arities.
   The old `bin` builds this, and T1 builds T2.
2. **Take `arity` out of `table.py`** once `bin` gets arities from `system.cdy`.
3. **Add the prelude** last. It is ordinary Candy, so the bootstrap is a plain rebuild.

## Steps

1. **`system.cdy`:** a `sig` for each of the 66 entries that aren't special forms or
   operators; read and check it (both ways); arity from the `sig`; bodiless `sig`s only
   there.

   *Done.* As built:
   - **`src/cdy/system.cdy`** has 66 bodiless `sig`s, grouped as `table.py` is. `Any` marks
     the variadic, overloaded and Python-object built-ins (the leaks in `doc/leaks.md`).
   - **`core.cdy`:** `system-sigs` reads them into a map from name to type, and checks them
     against the table, both ways:
     - `built-in x has no sig in system.cdy`;
     - `system.cdy: x has no Python mapping in table.py` (which also catches a `sig` for an
       operator or a special form);
     - `system.cdy: more than one sig for x`;
     - `system.cdy: expected (sig name Type)` for anything else in the file.

     `Scope` holds the types (`builtins`). `check-call` takes a built-in's arity from its
     type (its number of parameters; none for `Any` or a constant), and an operator's from
     its kind (`not` takes one, the others two or more). It no longer reads the table's
     arities.
   - **`cdyc.cdy`:** `builtin-sigs` reads `system.cdy` from next to the translator, for each
     translation and each macro program.
   - **Bodiless `sig`s are only in `system.cdy`:** it is read on its own and never analysed
     as a program, so everywhere else the old error stands.
   - **The library:** `system.cdy` joins `self_host.LIBRARY`. A translator without its
     library now fails on any program (`the translator needs system.cdy next to it, in
     DIR`, which replaces `macros need ...`).
   - **Bootstrap:** one rebuild, as planned (the table still has its arities for the old
     `bin`).
   - **Tests:** `test_system_errors` (each check, on an edited copy of `system.cdy`),
     `test_builtin_arity_comes_from_system`, and `test_translator_needs_its_library`.
2. ~~**`table.py` without arities**~~ *Dropped:* the frozen Python translator still
   checks arity from `table.py` (`src/py_cdy/core_cdy.py`), and its tests still run. So
   `arity` stays, used only by it; the Candy translator takes arity from `system.cdy`
   (step 1). Retiring the Python translator was considered and not chosen. (Tech debt in
   `doc/tech_debt.md`.) *Later done* on branch `bootstrap`, once the Python translator
   left `master` (`doc/hl_rqmt/bootstrap.md`, step 3).
3. **`prelude.cdy`:** an implicit import into every file; the four functions; a test
   program; and a test that a program's own `map` wins.

   *Done.* As built:
   - **`src/cdy/prelude.cdy`:** `rest`, `map`, `filter` and `fold`, generic and tail
     recursive (so `lower` makes them loops), with `map-into` and `filter-into` as their
     accumulating helpers.
   - **`include.cdy`:** `add-module` puts the prelude (`prelude-module`) before a module's
     own imports, unless the module is the prelude; its import has no position, so a clash
     points at the other import (`import: prelude and a both define map`). `library-path`
     moved here from `expand.cdy`, which still uses it.
   - **The library:** `prelude.cdy` joins `self_host.LIBRARY`.
   - **The translator** gets the prelude too, so `bin` now holds `prelude__map` and the
     rest, unused. Its own `expand.cdy` already had a `prelude-import`, which the new clash
     rule caught.
   - **Bootstrap:** one rebuild; T2 reproduces itself.
   - **Tests:** `tst/cdy/cdyc/prelude.cdy`, a clash case in `test_module_errors`, and
     `test_own_definitions_win_over_the_prelude`.
4. **Docs:** the spec (`sig` in `system.cdy`, the prelude), CLAUDE.md, the iMVP doc's
   "Signature statement", `multi_target.md`, and new leaks and tech debt.

   *Done.* The spec, `bin/README.md`, CLAUDE.md, leaks and tech debt went in with steps 1
   and 3; then the iMVP doc ("Signature statement", "Symbol table" and the note on
   built-ins' types), `multi_target.md` ("The symbol table across targets") and the
   macros HLD's pointer.
5. **`map`, `filter` and `fold` built in** (added after step 4, from the library HLD's
   discussion, `doc/hl_rqmt/library.md`). Candy adds to a list by copying it (`(+ acc
   (to-list x))`), so the prelude's versions took quadratic time.

   *Done.* As built:
   - **`table_defs.py`:** `list_map`, `list_filter` and `list_fold` (Python's `map`,
     `filter` and `functools.reduce`, into tuples); **`table.py`** maps the three names to
     them, and **`system.cdy`** gives their `sig`s, as `prelude.cdy` had them (69 `sig`s
     now).
   - **`prelude.cdy`** keeps only `rest`; `map-into` and `filter-into` are gone.
   - **Timing** (`map` of `(fn (x) (+ x 1))`): 1000 items 2 ms, 4000 items 30 ms, 16000
     items 506 ms in the prelude; 0.05, 0.16 and 0.67 ms built in.
   - **Bootstrap:** the old `bin` reads its own `bin/py/system.cdy` and the live table, so
     the new `system.cdy` was copied into `bin/py/` before the rebuild.
   - **Tests:** `test_list_functions` (runtime); `test_list_functions_are_built_in` (the
     output calls `list_map`); `test_own_definitions_win_over_the_prelude` now defines its
     own `rest` and `map`. No timing test.

## Questions (decided: the simplest option for the MVP)

*For now* marks an answer meant to change, with where its follow-up is tracked; *lasting*
marks one meant to stay.

1. **Names and place:** `system.cdy` and `prelude.cdy` next to the translator in
   `src/cdy/`, with `form.cdy` and `prelude_macros.cdy`. *For now:*
   `doc/hl_rqmt/library.md`, question 4 (a `lib/` directory?).
2. **Operators:** left out of `system.cdy`; the table describes them. *For now:*
   `doc/leaks.md`, "Operators have no Candy type".
3. **Variadic built-ins:** typed `Any`, so no arity check. *For now:* `doc/leaks.md`,
   "Built-ins typed `Any`".
4. **Overloaded built-ins:** type variables where they fit, `Any` elsewhere. *For now:*
   `doc/leaks.md`, "Built-ins typed `Any`" (until `Collection`).
5. **Prelude priority:** an ordinary import (own definitions win; a clash with an explicit
   import is an error). *Lasting;* how a program sees the prelude changes later
   (`doc/hl_rqmt/library.md`, "What a program sees", B).
6. **Prelude contents:** `rest`, `map`, `filter`, `fold`; the translator doesn't use them
   yet. (Step 5 made the last three built-ins.) *For now:* `doc/hl_rqmt/library.md`,
   questions 5 and 6.
7. **Prelude output:** all of it, in every program. *For now:* `doc/tech_debt.md`, "The
   whole prelude goes into every program's Python file"; `doc/hl_rqmt/library.md`,
   question 7 (tree shaking).
8. **Macro programs:** don't get the prelude. *For now:* `doc/leaks.md`, "Macro code
   doesn't get the prelude" (in `doc/tech_debt.md` until `library`, step 5).
9. **Special forms:** stay in `table.py`. *For now:* `doc/leaks.md`, "Special forms are
   described by the Python table".
10. **One prelude or two:** two; `prelude_macros.cdy` stays apart. *Lasting.*
