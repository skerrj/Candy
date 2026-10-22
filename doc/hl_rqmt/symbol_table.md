# The symbol table (HLD)

**Status: accepted (2026-10-21), with the proposed answers to its questions; steps 1 to 5
below.** Branch `symbol-table`, after tag `bootstrap` and before the library branch.
Written on `master`, broken out of the library HLD (`doc/hl_rqmt/library.md`, question 1)
and `doc/hl_rqmt/multi_target.md`: how the translator finds out what a name means today,
what has been decided, and the way forward.

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

**One symbol table: the analysis scope, seeded with the built-ins from Candy.** What a
built-in *is* (a special form, an operator, a function or value with a type) is a fact
about the language, stated in Candy and read by the front end; how it is *written* in
Python (its spelling and rendering) is the target's, and stays in `table.py`.

### What the front end needs, and what the backend needs

Today's `kind` mixes the two. Read by use:

| Today's kind | Front end (`core.cdy`, `expand.cdy`) | Backend (`emit.cdy`) |
|---|---|---|
| `special` | its own rule; an error as a value or a macro name | unused |
| `binop`, `compare`, `boolop` | an operator: 2 or more arguments, no type | `(a op b op c)` |
| `unary` | an operator: exactly 1 argument | `(op a)` |
| `call`, `value`, `index`, `slice` | a built-in with a `sig` (`BUILTIN_KINDS`) | `py(...)`, `py`, `a[i]`, `a[i:j]` |

So the front end needs three classes, and the backend the rendering kinds without
`special`.

### The built-ins in Candy

- **`special.cdy`** (new, next to `system.cdy`, copied into `bin` with the library): the
  special forms and the operators, one form each:

  ```
  (special def) (special defn) (special if) ...
  (op + variadic) (op = variadic) (op and variadic) ... (op not unary)
  ```

  `variadic` is 2 or more arguments, `unary` exactly one. It replaces the `special`
  entries of `table.py` and, in time, the informal list in `src/cdy/candy-special.md`.
  `system.cdy` is unchanged: the functions and values, each with its `sig`.
- **A `Builtin` sum** in `core.cdy`, the scope's one map of built-ins (replacing
  `builtins` and the table in `Scope`):

  ```
  (deft Builtin (Special) (Op ((unary Bool))) (Typed ((type CType))))
  ```

  `cdyc.cdy` reads `special.cdy` and `system.cdy` into it once (as `builtin-sigs` reads
  `system.cdy` today) and passes it to `expand.cdy` and `core.cdy`.
- **`resolve`, `check-call`, `is-special-head`, `let-bindings` and `defmacro-items`**
  match on it instead of calling `table-is-special`, `table-is-op` and `table-get-kind`.
- **The check both ways** moves to it: every name in `table.py` is an `op` or has a
  `sig`; every `op` and `sig` has an entry in `table.py`; a `special` has none.

### The Python spellings

- **`table.py` drops its `special` entries** and the `table-*` functions; it keeps each
  built-in's `py` and rendering kind, *for now* (question 2).
- **`initial-table`** is typed `(Map String (Tup String String))` (spelling, kind). No
  runtime change: `TableEntry` is a `NamedTuple`, so a `Mapping[str, TableEntry]` already
  is a `Mapping[str, tuple[str, str]]` to mypy, and Candy reads it with `map-get` and
  `at`. `emit.cdy`'s `Env` holds it typed, and its two lookups become Candy.
- **Tests that read `table.py`:** `test_editor_grammar.py` checks the grammar against
  `special.cdy` instead of `SPECIAL_FORMS`; `tst/cdy_rt/test_table.py` loses the `is_special`
  case.

## Steps

1. **Drop the unused table functions:** `add_fun`, `is_bin_op` and their built-ins
   `table-add-fun`, `table-is-bin-op`, and the unused `is-lit`, from `table.py`,
   `table_defs.py` and `system.cdy`. (Also the library's step 1, first part.)

   *Done. As built:* as planned. `table.py` loses `add_fun`, `is_bin_op` and their entries
   (its docstring no longer says the table is extended), `table_defs.py` loses `is_lit`,
   `system.cdy` the three sigs; `test_table.py` and `test_table_defs.py` lose their cases
   (225 tests). Bootstrap: `src/cdy/system.cdy` copied into `bin/py/` before the rebuild;
   the translator comes out byte for byte the same (nothing called them), so the step's
   `bin` change is `bin/py/system.cdy` alone, a chain step all the same.
2. **`special.cdy` and the `Builtin` map:** the front end reads its built-ins from
   `special.cdy` and `system.cdy`; `core.cdy` and `expand.cdy` stop calling the table; the
   check both ways moves. `table.py` still has its `special` entries (the bootstrap,
   below).

   *Done. As built:* `src/cdy/special.cdy` (first `forms.cdy`, renamed after step 4: too
   close to `form.cdy`; the rename's `bin` keeps `bin/py/forms.cdy` for the `bin` before
   it, until step 5) declares the 20 special forms and the 14
   operators (`(special def)`, `(op + variadic)`, `(op not unary)`), and `self_host.py`'s
   `LIBRARY` copies it into `bin`. In `core.cdy`, `Builtin` (its third variant is `Typed`,
   not the plan's `Prim-fn`: it covers values like `PI` too) replaces `Scope`'s `table`
   and its map of types; `read-builtins` (replacing `system-sigs`) reads `special.cdy` and
   then `system.cdy`, and checks them against the table both ways, now by class: a
   `special` needs a `special` entry, a `variadic` op a `binop`, `compare` or `boolop`
   one, a `unary` op a `unary` one, a `sig` a `call`, `value`, `index` or `slice` one; and
   every entry needs a declaration (`table.py: x is declared in neither special.cdy nor
   system.cdy`, which replaces `built-in x has no sig in system.cdy`; a second
   declaration is `x is already declared`). `resolve`, `is-special-head`, `check-call`
   and `let-bindings` match on the map; `expand.cdy` reads it (`library-builtins`, which
   replaces `cdyc.cdy`'s `builtin-sigs`, since expand needs it too) for `defmacro-items`.
   The table is now read by `core.cdy` only to check the declarations, and by `emit.cdy`.
   Tests: `test_system_errors` became `test_library_errors` (11 cases, 6 for `special.cdy`),
   and `test_special_forms_are_declared` (232 tests). Bootstrap: no staging (the old `bin`
   doesn't read `special.cdy`).
3. **`emit.cdy` reads the spellings as Candy data:** `initial-table` typed as a map of
   pairs; `table-get-kind` and `table-get-py` replaced by lookups.

   *Done. As built:* `system.cdy` types `initial-table` as `(Map String (Tup String
   String))`, with no runtime change (mypy takes the `Mapping[str, TableEntry]` as one of
   pairs). `emit.cdy`'s `Env` holds it typed; `emit-prim` and `emit-prim-call` read an
   entry's text and kind with `map-get` and `at`. `core.cdy`'s declaration checks do too,
   through `spelling-kind` (an entry's kind, or `""`), which `emit-prim` shares, with
   `TYPED_KINDS`. So `bin` calls no `table-*` function any more, which step 4 needs. Tests:
   unchanged (232). Bootstrap: no staging.
4. **The `table-*` functions go:** from `table.py`, with their built-ins; the special forms
   may now have no entry (split from the plan's step 4, below).

   *Done. As built:* `table.py` loses `is_op`, `is_special`, `get_kind`, `get_py`,
   `table_fn` and the four `table-*` entries (`META_TABLE` keeps `initial-table`);
   `system.cdy` loses their sigs (copied into `bin/py/` before the rebuild).
   `SPECIAL_KINDS` takes `""` (no entry) as well as `special`, *for now*, until step 5.
   `test_table.py` tests the entries as data (`test_spellings`, replacing `test_lookups`
   and `test_get_py`; 231 tests). Why the split: the `bin` of step 3 checks that every
   special form has a `special` entry, so removing them in the same step would break it,
   and the `old-runtime` staging can't bridge it either (the parent's runtime still has
   the `table-*` entries, which the step's `system.cdy` no longer declares). With this
   step's `bin` accepting either, step 5 can remove them with no staging.
5. **`table.py` as the Python spellings only:** the `special` entries (`SPECIAL_FORMS`, the
   `special` kind) go; a special form must have no entry; the grammar test reads
   `special.cdy`.
6. **Docs:** `candy-special.md` points at `special.cdy`; CLAUDE.md, the leak (struck
   through), `library.md` (its step 1 shrinks to `py-mangle`, `get-indent`, `PY_IMPORTS`
   and `py-repr`), `multi_target.md`.

## Bootstrap

Each of steps 1 to 5 changes `bin`, so each is a chain step (`boot/NN`). The hazard
(`doc/process.md`, "Rebuilding `bin`") is that the checked-in `bin` reads the live
`table.py` and its own copy of the library. The order above avoids staging:

- **Removing a built-in** (steps 1, 4 and 5) waits until `bin` no longer uses it: in step
  1 nothing does; in step 4 the `bin` of step 3 calls no `table-*` function; in step 5 the
  `bin` of step 4 no longer needs special forms in the table. (The plan had steps 4 and 5
  as one, which missed that step 2's check needs the `special` entries; see step 4.) `src/cdy/system.cdy` is copied into `bin/py/` before
  the rebuild, so the old `bin` doesn't find sigs without table entries.
- **A new library file** (step 2): the old `bin` doesn't read `special.cdy`, and the new one
  finds it next to itself once `self_host.py`'s `LIBRARY` lists it.
- If a step still needs staging, its tag says how (`script/bootstrap.py`, `STAGING`).

## Questions (answered: the proposals, accepted)

1. **Where the operators and special forms are declared:** in `system.cdy` (a new form,
   since a `sig` can't say "two or more arguments"), or a file of their own
   (`special.cdy`)? The owner's brainstorm note favours a spec file of their own ("add
   special forms to the symbol table: via special spec file"), which could also replace
   `src/cdy/candy-special.md`'s informal list.
   *Proposed:* a file of their own, `special.cdy` next to `system.cdy`, with a form that
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
