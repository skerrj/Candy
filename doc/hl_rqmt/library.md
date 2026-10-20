# Candy's library: system, translator and prelude (HLD)

**Status: draft; three decisions in.** Drafted on branch `system-prelude`, as the follow-up to its MVP
(`doc/hl_rqmt/system_prelude.md`). Proposed as its own branch after that one is merged.
The questions at the end are open.

## Where things stand

After `system-prelude` there are three library files next to the translator, besides
`form.cdy`:

- **`system.cdy`:** 69 bodiless `sig`s, one flat set of built-ins that every file sees.
  It mixes what programs need (`len`, `put`, `slurp`, `map-get`) with what only the
  translator uses:
  - the symbol table: `initial-table` and the `table-*` functions;
  - writing Python: `py-mangle`, `py-repr`, `get-indent`, `PY_IMPORTS`;
  - macros: `load-macros`, `call-macro`, `module-dir`, `fresh-name`.

  That is a leak (`doc/leaks.md`, "The translator's built-ins are every program's").
- **`prelude.cdy`:** a module every file imports: only `rest`, since `map`, `filter` and
  `fold` became built-ins for speed (`system_prelude.md`, step 5). It is sparse, and it all
  goes into every program's output (`doc/tech_debt.md`).
- **`prelude_macros.cdy`:** the macros every file gets (`cond`).

Meanwhile the translator writes these functions by hand, over and over:

- 95 copies of `(slice xs 1 (len xs))`, and 50 calls of `form.cdy`'s `rest-of`, which is
  `rest` for `Form`s;
- 94 `defn`s that thread an accumulator (`acc`), most of them a `map`, `filter`, `any`
  or `fold` in disguise: `analyse-all`, `expand-all`, `stamp-all`, `quoted-all`,
  `stems-of`, `field-names`, `has-clause`, `unique-stems` and so on.

## Goals

1. **Two layers, each with a clear audience** (below): built-ins (`system.cdy`) and Candy
   definitions for everyone (`prelude.cdy`).
2. **A program doesn't see the translator's helpers.** Most of them become ordinary Candy
   in the translator's own modules; only the few that need the host stay built-ins.
3. **A fuller prelude**, enough that Candy code (the translator first) stops writing list
   loops by hand.
4. **A program's output holds only the prelude it uses.**

Not goals: other targets' `system` files (the layout questions in
`doc/hl_rqmt/multi_target.md` stay open, but this split should fit them); interfaces and
`Collection`; a type checker.

## Proposal

### Two layers

| File | What it holds | Who imports it | Runs on |
|---|---|---|---|
| `system.cdy` | built-ins: `len`, `put`, `slurp`, `map-get`, ... | every file, implicitly | the **target** (its runtime provides them) |
| `prelude.cdy` | Candy definitions built on `system.cdy` | every file, implicitly | anywhere: plain Candy |

An earlier draft had a third file, `translator.cdy`, declaring the translator's own
built-ins for its files alone. It was dropped (below): the rule "anything that can be
written in Candy is Candy" applies to the translator's helpers too.

### The translator's built-ins become Candy (decided)

`system.cdy` declares 17 built-ins that only the translator calls. Each goes where the rule
puts it:

| Built-in | Used in | Becomes |
|---|---|---|
| `table-add-fun`, `table-is-bin-op`, `table-get-arity`, `is-lit` | nothing | **dropped** |
| `table-is-special`, `table-is-op`, `table-get-py`, `table-get-kind` | `core`, `expand`, `emit` | **Candy**: lookups in a map |
| `initial-table` | `cdyc`, `expand` | **one built-in** (the data), or Candy (question 1) |
| `py-mangle` | `emit`, `expand` | **Candy** in `emit.cdy`, with its reserved names as a Candy list |
| `get-indent`, `PY_IMPORTS` | `emit`, `cdyc` | **Candy** in `emit.cdy` |
| `py-repr` | `emit` | **Candy** in `emit.cdy` (string escapes), or kept (question 2) |
| `load-macros`, `call-macro`, `module-dir` | `expand`, `include` | **built-ins**: they load and run generated Python |
| `fresh-name` | `form` | **built-in**: it keeps a counter, and Candy has no mutation |

- **The symbol table's data** is the hard part. `table.py` holds it, and the frozen
  Python translator and the generated code's imports still need `table.py`. The simplest
  step: `initial-table` stays the one built-in, typed as a Candy map of records (a
  `deft TableEntry`), and every lookup is Candy. Later the data itself can move into
  Candy (`doc/hl_rqmt/multi_target.md`'s target-neutral table plus a mapping per target),
  and `table.py` checks against it, or is generated from it.
- **What stays built-in** is four functions for macros (plus `initial-table`). They are
  host built-ins: they exist because the translator runs on Python, not because a program
  targets it (`doc/hl_rqmt/macros.md`, "Terms"). They stay in `system.cdy`, marked as the
  translator's, so the leak ("The translator's built-ins are every program's") shrinks
  from 17 names to 5. A separate declaration file that only the translator imports can
  come later, if it is still wanted (question 3).
- **Cost:** none in speed (lookups in a map, string work), and the translator's own
  `emit.cdy` gets the Python-specific code, which is where it belongs: Python is the
  target there, not the host.

### Built-in or prelude (decided)

**Anything that can be written in Candy goes in the prelude**, not in `system.cdy`. A
built-in is only what Candy can't express: arithmetic and comparison, getting at data
(`len`, `at`, `slice`, `map-get`, `map-set`), I/O (`put`, `slurp`, files and paths) and a
few conversions (`to-int`, `hex-char`). So `system.cdy` shrinks to primitives, the prelude
grows, and each target's runtime has fewer built-ins to provide. Today's built-ins that
move, for example:
- `is-empty-str`: `(= s "")`;
- `isspace-at`: `isspace` of a one-character `slice`;
- `is-neg-int` and `join`: `slice` and a loop.

Exception, for speed: while lists are tuples that Candy copies to add to, list operations
that build a list stay built-in. `map`, `filter` and `fold` already are
(`system_prelude.md`, step 5); the long-term fix is in `mutation_optimization.md`.

### What a program sees (decided: A now, B later)

- **Now (A):** a program sees `system.cdy`'s primitives and the prelude, both implicitly.
  That needs nothing new.
- **Later (B):** a program sees only the prelude. `system.cdy` is imported by the prelude,
  which re-exports the primitives programs need, as they are or wrapped (an `at` that
  returns a `Maybe`, say), as OCaml's `Stdlib` and Elm's core do. That makes the
  prelude's names the one interface for every target, while each target's `system.cdy`
  can differ underneath: the answer to `doc/hl_rqmt/multi_target.md`'s "abstracting
  `system.cdy` while allowing specifics". It needs re-export, which modules don't have.
- **Meanwhile,** the prelude's names are designed as if they were that interface, so that
  moving to B is mostly adding re-exports.

The few built-ins left for the translator (above) are visible to programs either way,
until a declaration file can be imported (question 3).

### A fuller prelude (question 5)

Candidates, from what the translator and the test programs write by hand:
- **lists:** `rest`, `any`, `all`, `find` (the first match, as a
  `Maybe`), `reverse`, `range`, `take`, `drop`, `concat` (a list of lists), `zip`,
  `index-of`, `contains`;
- **strings:** `starts-with`, `ends-with`, `split`, `repeat`; some of `table_defs.py`'s
  helpers could become Candy here (`is-empty-str` is `(= s "")`);
- **maps:** `map-update`, `map-from` (a list of pairs);
- **`Maybe`:** `with-default`.

Whether the translator moves onto them is a separate step (question 6): it would rewrite
dozens of functions, but not change what the translator does, which the fixpoint checks.

### Only the prelude a program uses (question 7)

With dozens of functions, putting the whole prelude into every output is no longer small.
Proposed: emit a prelude definition only if the program uses it, directly or through other
prelude definitions (tree shaking over the `Top`s, before `lower`). The same could apply to
every imported module, later.

### Private names (question 8)

A prelude helper is exported, like every top-level name (the old `map-into` and
`filter-into` were). A fuller prelude has more of them. Either names get a way to be private (a convention, such
as a leading `-`, or a form), or the helpers get written so they aren't needed.

## Steps (sketch)

1. **The translator's helpers into Candy:** drop the four unused built-ins; the table
   lookups, `py-mangle`, `get-indent` and `PY_IMPORTS` (and maybe `py-repr`) become Candy
   in the translator's modules, with `initial-table` typed as a map of records. Tests that
   a program can't see `py-mangle`, and that the fixpoint holds (the output shouldn't
   change).
2. **Private names** (if decided).
3. **Tree shaking** of the prelude (and maybe of every module).
4. **The fuller prelude**, with a test program per group.
5. **The translator on the prelude** (optional; its own step).
6. **Docs.**

## Questions (open)

Decided so far: anything that can be written in Candy goes in the prelude ("Built-in or
prelude"); a program sees the primitives and the prelude now, and only the prelude later
("What a program sees"); the translator's helpers become Candy, with no `translator.cdy`
("The translator's built-ins become Candy").
Leaning (not decided): a small implicit prelude plus opt-in library modules for the rest
(`(import list)`), so "the prelude" in the rule above means Candy's library; open: how
imports find library modules, their names (`std/list`?), and what the prelude keeps.

1. **The symbol table's data:** `initial-table` stays one built-in, typed as a Candy map
   (proposed), or the table moves into Candy now (the multi-target split)?
2. **`py-repr`:** rewrite in Candy (string escapes, a few lines), or keep the built-in?
3. **The five host built-ins:** stay in `system.cdy`, marked as the translator's
   (proposed), or a declaration file only the translator imports?
4. **Names and place:** `system.cdy` and `prelude.cdy` next to the translator, or a `lib/`
   directory?
5. **Prelude contents:** which of the candidates, and in what order?
6. **The translator on the prelude:** rewrite its loops with `map`, `filter` and the rest,
   or leave it alone?
7. **Tree shaking:** only what a program uses (proposed), or the whole prelude?
8. **Private names:** how, and whether this branch needs them?
9. **Where `form.cdy` and `prelude_macros.cdy` fit:** `form.cdy` is the macro layer's
   library, used on the host only (with `fresh-name`). Is it part of the translator, or
   its own layer (macro code's library)?
