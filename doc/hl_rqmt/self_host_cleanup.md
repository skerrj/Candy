# Self-host cleanup: `import`, one translator, and paying down the bootstrap

**Status: accepted.** The open questions at the end are decided. Branch `self-host-cleanup`, after tag
`self-host-py` (Candy's translator is written in Candy, has its own reader, and rebuilds
itself on Python; see `doc/hl_rqmt/self_hosting_primo.md`).

## Where things stand

- **Two translators.** The Python one (`src/py_cdy/`, the iMVP) and the Candy one
  (`src/cdy/*.cdy`, checked in as `bin/py/cdy_translator.py`). Both accept the same
  language, and tests keep them in step: same output on every program, same forms from
  both readers.
- **The Candy translator is five files joined into one program** (`TRANSLATOR_FILES` in
  `self_host.py`), because Candy has no `import` (a leak).
- **Rebuilding `bin/py/` still goes through the Python translator** (`self_host.py`
  builds T1 with it, then T1 builds T2). The checked-in copy can rebuild itself, but no
  driver does that.
- **Shortcuts are listed** in `doc/archive/leaks_imvp_py_translator.md`,
  `doc/archive/leaks_pre_self_host.md` and `doc/tech_debt.md`.

## Goals

1. `import`, so that Candy programs, the translator first, can be split into files.
2. One translator to change: new language features go into the Candy translator only.
3. Close the gaps and shortcuts that the bootstrap left, where they get in the way.

## 1. `import`

The spec reserves `(import sym)`, `(import-as sym as-sym)` and `(import-from sym from-sym+)`
(`src/cdy/candy-special.md`, `[SKIP]` until after the bootstrap). Two steps are proposed.

### Step A: `import` as inclusion (proposed first)

As smz did (`get_imports_help` in `smz-core/src/smz/render_help.scm`): `(import name)` at
top level reads `name.cdy` from the importing file's directory and adds its forms to the
program, once (a file imported twice, or in a cycle, is included only the first time). The
result is still one program and one Python module.

- **What it fixes:** `TRANSLATOR_FILES` goes away. A `src/cdy/cdyc.cdy` (decided) imports
  `form`, `read`, `core`, `lower` and `emit`, and the driver passes one file.
- **What it doesn't:** there are no namespaces. Every top-level name is still global
  across all the files, and two files can't define the same name. That is a leak, but the
  same one as today's joined files.
- **Where it happens:** in the reader's caller, before `analyse`: forms are read, `import`
  forms are replaced by the imported file's forms, then everything is analysed together.
  The Candy translator needs to read files (`slurp`, already a built-in) and find them
  relative to the importing file (a path built-in, or a directory passed in).
- **`system.cdy` and `prelude.cdy`** (planned in the iMVP doc: bodiless `sig`s declare
  runtime built-ins, ordinary definitions go in the prelude) could arrive the same way:
  imported implicitly at the start of every program. That would let `table.py` shrink
  later; it is a separate step.

### Step B: modules (later)

One Python module per Candy file, qualified names (`(import-as emit e)` then `e/line`, or
another separator), `import-from` for unqualified names, and a rule for what a file
exports (everything with a `sig`, or an explicit list). This needs decisions on name
syntax, on how `deft` types and variants are exported, and on how generated modules find
each other (a package under `output/`, or relative imports). Not before the inclusion
step has been used for a while.

## 2. One translator

Today every language change goes into both translators, and both readers. Proposed:

- **The Candy translator becomes the only one that gets new features.** The Python
  translator is frozen at what it supports now (tag `self-host-py`). It stays as the
  bootstrap: it can still build T1 from a version of `src/cdy/` that it understands.
- **Rebuild `bin/py/` from itself:** `self_host.py` (or a new mode of `main.py`)
  translates `src/cdy/` with the checked-in `bin/py/cdy_translator.py`, checks the result
  (it passes `mypy --strict`, rebuilds itself, and the tests pass with it), and only then
  replaces the checked-in copy. A broken change can't then lock Candy out of its own
  translator: the previous copy is in git.
- **Tests move to the checked-in translator.** The golden programs run under `bin`; the
  Python translator's own tests stay as they are, but new programs that use new features
  run only under `bin`.
- **The two-reader check goes**, since `parse_cdy` stops changing.

The question is when: `import` (step A) is the natural first feature to add to the Candy
translator only.

## 3. Cleanup candidates

From the leak lists and `doc/tech_debt.md`; to be picked and ordered:

- **The spec:** add `sig`, `deft` (records and sums), `match`, `get` and `assoc` to
  `src/cdy/candy-special.md` (an open item since the iMVP).
- **The Candy translator's simpler output** (every operator parenthesised, `format` as a
  `str()` concatenation, more renaming, no conditional-expression merging, `and`/`or`
  arguments with statements not short-circuiting). The last one is a real semantic gap
  if such code ever appears; the rest only change what the generated Python looks like.
- **Types and values share one namespace** (a variant can't take its type's name).
- **The symbol table is an opaque `Any`** in the Candy translator. Typing it in Candy
  (`deft TableEntry ...`) would let `system.cdy` replace `table.py` later.
- **`get` before `match` is caught by mypy, not by Candy.** Candy has no type checker of
  its own yet; that is a much bigger project and probably its own HLD.
- **A driver in Candy:** `main.py`'s job (read a file, translate, write `output/`) as a
  Candy program using `SYS_ARGS`, `slurp` and `spit`, so `bin/py/` can be run directly.
- **Error positions:** only parse errors have a line and column. The reader knows
  positions; the forms don't carry them yet.
- **Recursion:** the Candy translator walks lists by recursion that isn't a self tail call
  in places, so `self_host.py` raises Python's recursion limit to 20,000.

## Open questions

1. **Is inclusion (step A) the right first `import`**, with real modules (step B) later?
   Decided: yes.
2. **Freeze the Python translator now** (new features only in the Candy translator), or
   keep both in step for a while longer? Decided: freeze it now; `import` goes into the
   Candy translator only.
3. **Which cleanup items, and in what order?** Decided: `import` step A, the
   self-rebuilding `bin/py/`, the spec update, then the rest as they get in the way.
4. **The top file's name** for the translator. Decided: `src/cdy/cdyc.cdy`.
