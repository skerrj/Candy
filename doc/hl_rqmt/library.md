# Candy's library: system, translator and prelude (HLD)

**Status: draft.** Drafted on branch `system-prelude`, as the follow-up to its MVP
(`doc/hl_rqmt/system_prelude.md`). Proposed as its own branch after that one is merged.
The questions at the end are open.

## Where things stand

After `system-prelude` there are three library files next to the translator, besides
`form.cdy`:

- **`system.cdy`:** 66 bodiless `sig`s, one flat set of built-ins that every file sees.
  It mixes what programs need (`len`, `put`, `slurp`, `map-get`) with what only the
  translator uses:
  - the symbol table: `initial-table` and the `table-*` functions;
  - writing Python: `py-mangle`, `py-repr`, `get-indent`, `PY_IMPORTS`;
  - macros: `load-macros`, `call-macro`, `module-dir`, `fresh-name`.

  That is a leak (`doc/leaks.md`, "The translator's built-ins are every program's").
- **`prelude.cdy`:** a module every file imports: `rest`, `map`, `filter` and `fold`.
  It is sparse, and it all goes into every program's output (`doc/tech_debt.md`).
- **`prelude_macros.cdy`:** the macros every file gets (`cond`).

Meanwhile the translator writes these functions by hand, over and over:

- 95 copies of `(slice xs 1 (len xs))`, and 50 calls of `form.cdy`'s `rest-of`, which is
  `rest` for `Form`s;
- 94 `defn`s that thread an accumulator (`acc`), most of them a `map`, `filter`, `any`
  or `fold` in disguise: `analyse-all`, `expand-all`, `stamp-all`, `quoted-all`,
  `stems-of`, `field-names`, `has-clause`, `unique-stems` and so on.

## Goals

1. **Three layers, each with a clear audience** (below): built-ins for programs, built-ins
   for the translator, and Candy definitions for everyone.
2. **A program sees only the first and third.** The translator's built-ins are imported by
   the translator's files alone.
3. **A fuller prelude**, enough that Candy code (the translator first) stops writing list
   loops by hand.
4. **A program's output holds only the prelude it uses.**

Not goals: other targets' `system` files (the layout questions in
`doc/hl_rqmt/multi_target.md` stay open, but this split should fit them); interfaces and
`Collection`; a type checker.

## Proposal

### Three layers

| File | What it holds | Who imports it | Runs on |
|---|---|---|---|
| `system.cdy` | built-ins for programs: `len`, `put`, `slurp`, `map-get`, ... | every file, implicitly | the **target** (its runtime provides them) |
| `translator.cdy` | built-ins for the translator: the symbol table, writing Python, macros | only the translator's own files, explicitly | the **host** (where the translator runs) |
| `prelude.cdy` | Candy definitions built on `system.cdy` | every file, implicitly | anywhere: plain Candy |

The second row ties into host vs target (`doc/hl_rqmt/macros.md`, "Terms"): the
translator's built-ins are the host's, and `py-mangle` is one only because the translator
runs on Python. A translator hosted elsewhere would provide its own `translator.cdy`,
whatever the target; a new target would provide its own `system.cdy`.

### Built-ins that belong to a module

Today built-ins are global: `system.cdy` isn't a module. For `translator.cdy` to be visible
only where it is imported, a file of bodiless `sig`s has to become something a file can
import (question 1). Proposed:
- a **declaration file** is a module whose `sig`s have no definitions;
- importing it makes its built-ins visible, as importing a module makes its definitions
  visible;
- `system.cdy` stays implicitly imported, and `translator.cdy` is imported with
  `(import translator)` like any module (found next to the translator, as a library file).

The table (`table.py`) is unchanged: it still maps every built-in to Python, and the check
against the declarations covers both files together.

### A fuller prelude (question 3)

Candidates, from what the translator and the test programs write by hand:
- **lists:** `rest`, `map`, `filter`, `fold`, `any`, `all`, `find` (the first match, as a
  `Maybe`), `reverse`, `range`, `take`, `drop`, `concat` (a list of lists), `zip`,
  `index-of`, `contains`;
- **strings:** `starts-with`, `ends-with`, `split`, `repeat`; some of `table_defs.py`'s
  helpers could become Candy here (`is-empty-str` is `(= s "")`);
- **maps:** `map-update`, `map-from` (a list of pairs);
- **`Maybe`:** `with-default`.

Whether the translator moves onto them is a separate step (question 4): it would rewrite
dozens of functions, but not change what the translator does, which the fixpoint checks.

### Only the prelude a program uses (question 5)

With dozens of functions, putting the whole prelude into every output is no longer small.
Proposed: emit a prelude definition only if the program uses it, directly or through other
prelude definitions (tree shaking over the `Top`s, before `lower`). The same could apply to
every imported module, later.

### Private names (question 6)

The prelude's helpers (`map-into`, `filter-into`) are exported, like every top-level name.
A fuller prelude has more of them. Either names get a way to be private (a convention, such
as a leading `-`, or a form), or the helpers get written so they aren't needed.

## Steps (sketch)

1. **Declaration files as modules,** and `translator.cdy` split off from `system.cdy`;
   the translator's files import it. Tests that a program can't see `py-mangle`.
2. **Private names** (if decided).
3. **Tree shaking** of the prelude (and maybe of every module).
4. **The fuller prelude**, with a test program per group.
5. **The translator on the prelude** (optional; its own step).
6. **Docs.**

## Questions (open)

1. **Built-ins in modules:** a declaration file as a module (proposed), or a separate
   mechanism (a list of "translator-only" names, checked by the translator)?
2. **Names:** `system.cdy`, `translator.cdy`, `prelude.cdy`? Or `host.cdy` for the
   second, after host vs target? A `lib/` directory for all of them?
3. **Prelude contents:** which of the candidates, and in what order?
4. **The translator on the prelude:** rewrite its loops with `map`, `filter` and the rest,
   or leave it alone?
5. **Tree shaking:** only what a program uses (proposed), or the whole prelude?
6. **Private names:** how, and whether this branch needs them?
7. **Where `form.cdy` and `prelude_macros.cdy` fit:** `form.cdy` is the macro layer's
   library, used on the host only. Is it part of `translator.cdy`'s world, or a fourth
   layer (macro code's library)?
