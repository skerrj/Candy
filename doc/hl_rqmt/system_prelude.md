# `system.cdy` and `prelude.cdy` (HLD)

**Status: accepted, MVP scope.** Branch `system-prelude`, after tag `modules`. The owner
chose the simplest option on every question ("Questions", at the end); the proposal
below is the first pass.

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
   arity comes from the `sig`.
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
   there. Copy it next to the translator (`self_host.LIBRARY`). Rebuild `bin`.
2. **`table.py` without arities:** rebuild `bin` first, then drop the field. Tests:
   `test_table.py`, and an error test for each half missing.
3. **`prelude.cdy`:** an implicit import into every file; the four functions; a test
   program; and a test that a program's own `map` wins.
4. **Docs:** the spec (`sig` in `system.cdy`, the prelude), CLAUDE.md, the iMVP doc's
   "Signature statement", `multi_target.md`, and new leaks and tech debt.

## Questions (decided: the simplest option for the MVP)

1. **Names and place:** `system.cdy` and `prelude.cdy` next to the translator in
   `src/cdy/`, with `form.cdy` and `prelude_macros.cdy`.
2. **Operators:** left out of `system.cdy`; the table describes them.
3. **Variadic built-ins:** typed `Any`, so no arity check.
4. **Overloaded built-ins:** type variables where they fit, `Any` elsewhere; leaks.
5. **Prelude priority:** an ordinary import (own definitions win; a clash with an explicit
   import is an error).
6. **Prelude contents:** `rest`, `map`, `filter`, `fold`; the translator doesn't use them
   yet.
7. **Prelude output:** all of it, in every program.
8. **Macro programs:** don't get the prelude.
9. **Special forms:** stay in `table.py` for now.
10. **One prelude or two:** two; `prelude_macros.cdy` stays apart.
