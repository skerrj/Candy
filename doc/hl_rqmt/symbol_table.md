# The symbol table (HLD)

**Status: draft (notes).** Written on `master` after tag `bootstrap`, broken out of the
library HLD (`doc/hl_rqmt/library.md`, question 1) and `doc/hl_rqmt/multi_target.md`: how
the translator finds out what a name means today, what has been decided, and the way
forward. No branch yet; it is meant to come with, or before, the library branch.

## Where things stand

A name is looked up in three places, and the built-ins are described in two files.

### 1. The runtime table (`src/cdy_rt/table.py`): built-ins only

- **What it holds:** each built-in's Python spelling (`py`) and its `kind`: `special`,
  `binop`, `compare`, `boolop`, `unary`, `call`, `value`, `index` or `slice`.
  `INITIAL_TABLE` is an immutable Python `Mapping`; nothing ever adds to it.
- **How the translator reads it:** through built-ins of its own, since to Candy the table
  is an opaque `Any` (`initial-table`, read by `cdyc.cdy` and `expand.cdy`):
  - `table-is-special` (`core.cdy`, `expand.cdy`): is the name a special form;
  - `table-is-op` (`core.cdy`): is it a built-in at all;
  - `table-get-kind` (`core.cdy`, `emit.cdy`): how to analyse a call and write it;
  - `table-get-py` (`emit.cdy`): its Python spelling.
- **Unused:** `table-add-fun` (`add_fun`: smz registered each user function in a global
  table, `m_table_add_fun`; no Candy or Python translator ever called it) and
  `table-is-bin-op`. `table-get-arity` went with the table's `arity` field
  (`doc/hl_rqmt/bootstrap.md`, step 3).

### 2. The analysis scope (`Scope` in `src/cdy/core.cdy`): everything a program defines

- **What it holds,** built fresh for each module (`analyse-module`):
  - `env`: locals (function parameters, `let` bindings), name → Core expression;
  - `top` and `names`: the top-level names visible here, and each one's Python name
    (`util__greet` outside the top module). They are collected before analysis
    (`top-names`, `module-exports`), from the module's own `def`, `defn` and `deft` and
    its imports' `Exports`, so forward references and mutual recursion work;
  - `variants` and `sums`: the sum types and their variants;
  - `elsewhere`: names other modules define, for the error when one isn't imported;
  - `macros`: the program's macros (whose names can't be bound);
  - `builtins`: each built-in's Candy type, from `system.cdy` (`system-sigs`).
- **`Prog`** (`core.cdy`) tracks, alongside, which names have a `sig` and which are
  already defined, for the `sig` checks.
- **Lookup** (`resolve`): locals, then a variant with no fields, then a top-level name
  (`Global`), then the table: a special form is an error as a value, a built-in becomes
  `Prim`; then a name defined elsewhere but not imported; else "unknown name". User names
  come before the table, so a program's own definition shadows a built-in ("own
  definitions win").

### 3. The backend's names (`Env` in `src/cdy/emit.cdy`): Python spellings

- **What it holds:** `globals` (each top-level name's Python name), `locals` (each
  binding, by its unique id, → a Python name that avoids collisions), `taken`, and
  `generic` (generic sums); and the table again, for `table-get-kind` and `table-get-py`.

### Built-ins described twice

- `system.cdy`: each built-in's **Candy type** (a bodiless `sig`), which gives its arity;
- `table.py`: its **Python spelling and kind**;
- **kept in step** only by the check both ways (`system-sigs`: `built-in x has no sig in
  system.cdy`, `system.cdy: x has no Python mapping in table.py`).
- **Special forms and operators** are only in `table.py`: `system.cdy` leaves them out
  (operators take two or more arguments, which a `Fn` type can't say). A leak:
  `doc/archive/leaks_system_prelude.md`, "Special forms are described by the Python
  table".

## Assessment

- **The split is normal:** most compilers have a fixed table of primitives and an
  environment for user bindings, and lookup falls through from one to the other. The
  scope and the backend's `Env` are separate on purpose (front end and target), and stay.
- **The awkward part is the built-ins:**
  - their facts are in two files, in two languages, checked against each other;
  - the table is `Any` to Candy, so every question about a built-in is a runtime call
    (`table-*`), and the translator can't see a built-in's kind as data;
  - what is a special form or an operator, a fact about the language, is stated only in
    the Python runtime, so every target would have to restate it.

## Decided elsewhere

- **The translator's helpers become Candy** (`doc/hl_rqmt/library.md`, "The translator's
  built-ins become Candy"): the four table lookups become map lookups in Candy, and the
  unused built-ins (`table-add-fun`, `table-is-bin-op`, `is-lit`) are dropped.
- **The multi-target split** (`doc/hl_rqmt/multi_target.md`, "The symbol table across
  targets"): a target-neutral table of built-ins (name, kind, Candy type), written in
  Candy, and one mapping per target (that target's spelling).

## The way forward (proposed)

**One symbol table: the analysis scope, seeded with the built-ins from Candy.**

1. **Built-ins as Candy data.** A `deft` for a built-in (its kind and type), filled from
   Candy files: `system.cdy` for the calls and values, and a new declaration of the
   operators and special forms, so the language's own forms are stated in Candy.
2. **The scope holds them,** in place of `builtins` and the `table-*` calls: `resolve`
   falls through to a Candy map, and `core.cdy` reads a built-in's kind as a field.
3. **`table.py` shrinks to the Python spelling,** a per-target mapping the backend
   (`emit.cdy`) reads; the check both ways stays, between the spellings and the Candy
   declarations.
4. **`initial-table`** stays the one built-in for the spellings, typed as a Candy map of
   records, until the mapping can be Candy too (question 2).

## Steps (sketch)

1. **Drop the unused table functions** (`add_fun`, `is_bin_op`) and their built-ins.
2. **A built-in record in Candy** and the scope seeded with it; `resolve` and `core.cdy`
   use it in place of `table-is-special`, `table-is-op` and `table-get-kind`.
3. **Operators and special forms declared in Candy;** the leak goes.
4. **`table.py` as the Python spelling only;** `emit.cdy` reads it through one built-in.
5. **Docs.**

Each step changes `bin`, so each is a chain step (`boot/NN`), and the ones that move facts
out of `table.py` need the bootstrap staging of `doc/process.md` ("Rebuilding `bin`").

## Questions (open)

Each has a proposed answer, for review.

1. **Where the operators and special forms are declared:** in `system.cdy` (a new form,
   since a `sig` can't say "two or more arguments"), or a file of their own
   (`forms.cdy`)? The owner's brainstorm note favours a spec file of their own ("add
   special forms to the symbol table: via special spec file"), which could also replace
   `src/cdy/candy-special.md`'s informal list.
   *Proposed:* a file of their own, `forms.cdy` next to `system.cdy`, with a form that
   can say a special form's or operator's shape; *lasting* (the language's forms are a
   front-end fact, apart from any target's built-ins).
2. **The Python spellings:** stay in `table.py` (read through `initial-table`), or become
   a Candy file too (`py/spelling.cdy`), with `table.py` generated from it or dropped?
   *Proposed:* stay in `table.py` *for now*, read through `initial-table` (way forward,
   point 4); a Candy spelling file comes with a second target
   (`doc/hl_rqmt/multi_target.md`).
3. **Order:** before the library branch (it changes what the library's first step
   rewrites), as part of it, or after?
   *Proposed:* before, as its own branch: the library's first step would otherwise
   rewrite the table lookups twice (as map lookups over `initial-table`, then over the
   seeded scope). Its first step, dropping the unused built-ins, is the library's too.
4. **Name:** "symbol table" for the seeded scope, or keep that for the built-ins and call
   the whole thing the environment?
   *Proposed:* "symbol table" for the seeded scope, the one place a name's meaning is
   found; the runtime's `table.py` becomes "the Python spellings".
