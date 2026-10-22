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
| `table-add-fun`, `table-is-bin-op`, `table-get-arity`, `is-lit` | nothing | **dropped** (`table-get-arity` with the table's `arity`: `bootstrap.md`, step 3; the rest in `symbol_table.md`, step 1) |
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
  and `table.py` checks against it, or is generated from it. The whole design is now
  its own HLD: `doc/hl_rqmt/symbol_table.md`.
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

**Revised: a host type's operations are built-in.** A type whose representation is the
host's (lists, which are Python tuples; strings; maps) gets its operations from the host,
as built-ins, *all* of them, not only the ones Candy can't write. For lists this is about
speed: Candy can only add to a tuple by copying it, so a list built an item at a time takes
quadratic time. The first rule was "only what Candy can't express, plus the list operations
that build a list", but that line falls inside the list operations, by how each happens to
be written (`reverse` is linear on `map` and `range`, quadratic on `fold`), and moves when
one is rewritten. One line per type is simpler:

- **built-in:** every list operation (`map`, `filter` and `fold` already are:
  `system_prelude.md`, step 5; and `any`, `all`, `find`, `reverse`, `range`, `take`,
  `drop`, `concat`, `zip`, `index-of`, `contains`), and the string and map operations
  (`split`, `starts-with`, `join`, `map-from`, ...); each is a line in `table.py` and a
  `sig`, since Python has them;
- **prelude:** what is built on top of them, such as `with-default` and `map-update`, and
  later the library's own helpers;
- **cost:** every target's runtime provides these operations, about 15 for lists rather
  than 5; every likely target has them natively;
- ***for now*:** when Candy has its own list representation (`mutation_optimization.md`),
  list operations can move into Candy, and the line with them;
- **unchanged:** under B (below) programs see only the prelude, which re-exports these
  built-ins, so where an operation lives doesn't change its name.

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

### A fuller library (question 5)

Candidates, from what the translator and the test programs write by hand. By the revised
rule above, the list, string and map operations among them are built-ins; only what is
built on them (`with-default`, `map-update`) is prelude:
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

Each has a proposed answer, for review.

Decided so far: anything that can be written in Candy goes in the prelude, except a host
type's operations, which are all built-in ("Built-in or prelude", revised); a program sees the primitives and the prelude now, and only the prelude later
("What a program sees"); the translator's helpers become Candy, with no `translator.cdy`
("The translator's built-ins become Candy").
Leaning (not decided): a small implicit prelude plus opt-in library modules for the rest
(`(import list)`), so "the prelude" in the rule above means Candy's library; open: how
imports find library modules, their names (`std/list`?), and what the prelude keeps.

1. **The symbol table's data:** `initial-table` stays one built-in, typed as a Candy map
   (proposed), or the table moves into Candy now (the multi-target split)? See
   `doc/hl_rqmt/symbol_table.md`.
   *Proposed:* decided there, on its own branch before this one (its question 3).
2. **`py-repr`:** rewrite in Candy (string escapes, a few lines), or keep the built-in?
   *Proposed:* rewrite it in Candy in `emit.cdy`: it writes Python, so it belongs to the
   backend, not the runtime.
3. **The five host built-ins:** stay in `system.cdy`, marked as the translator's
   (proposed), or a declaration file only the translator imports?
   *Proposed:* stay in `system.cdy`, marked as the translator's, *for now* (the leak
   "The translator's built-ins are every program's", down to 5 names); a declaration
   file can come with B, when programs see only the prelude.
4. **Names and place:** `system.cdy` and `prelude.cdy` next to the translator, or a `lib/`
   directory?
   *Proposed:* next to the translator, *for now*: `bin` copies them and the translator
   finds them there; a `lib/` layout waits for how imports find library modules (the
   "Leaning" note above).
5. **Library contents:** which of the candidates, and in what order? Most are built-ins
   now ("Built-in or prelude", revised), so the prelude stays small, and questions 7
   and 8 matter less.
   *Proposed:* the list operations first (what the translator writes by hand), then the
   string and map ones, then `with-default` and `map-update` in the prelude.
6. **The translator on the prelude:** rewrite its loops with `map`, `filter` and the rest,
   or leave it alone?
   *Proposed:* only the mechanical cleanup: `(slice xs 1 (len xs))` and `rest-of`
   become `rest` (94 and 50 places). The `acc` loops stay *for now*: a `fn` becomes a
   nested Python `def` with `Any` annotations, so `map`/`fold` would cost the fixpoint's
   `mypy --strict` checking, and many loops also thread a counter or scope. Revisit when
   `fn`s get typed annotations.
7. **Tree shaking:** only what a program uses (proposed), or the whole prelude?
   *Proposed:* later; with the revised rule the prelude stays small, so the whole
   prelude in every output is cheap *for now* (`doc/tech_debt.md`).
8. **Private names:** how, and whether this branch needs them?
   *Proposed:* not in this branch: a small prelude needs no helpers.
9. **Where `form.cdy` and `prelude_macros.cdy` fit:** `form.cdy` is the macro layer's
   library, used on the host only (with `fresh-name`). Is it part of the translator, or
   its own layer (macro code's library)?
   *Proposed:* leave as they are for this branch; decide with the macro work.
