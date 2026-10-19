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

### Step A as built

- **`src/cdy/include.cdy`** does it, between the reader and `analyse`. `read-program`
  reads a file and replaces each top-level `(import name)` with the forms of `name.cdy`,
  found in the importing file's directory (resolved to an absolute path), recursively.
  A file already included (imported twice, or in a cycle, or the main file itself) is
  skipped. The name may hold a relative path: `(import lib/util)`.
- **Errors:** `import: expected (import name)` for any other shape, `import: can't find
  name.cdy in dir` for a missing file, and `import is only allowed at top level` for an
  import inside an expression. `import-as` and `import-from` aren't supported.
- **Entry points** are in `src/cdy/cdyc.cdy`, which imports `form`, `read`, `include`,
  `core`, `lower` and `emit`: `translate-file` (a path; imports found next to it, which
  `main.py --translator t1|bin` uses) and `translate-text` (text; imports found in the
  current directory).
- **New runtime built-ins:** `file-exists`, `path-dir`, `path-join`, `path-resolve`.
- **Tests:** `tst/cdy/cdyc/imports.cdy` (a cycle and repeated imports, from a
  subdirectory), the error cases in `test_self_host.py`, and a `main.py` test that an
  import is found next to the importing file, not in the current directory.
- **Leak:** no namespaces (`doc/leaks.md`). **Tech debt:** errors don't name their file.

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

### As built

- **Frozen** with `import` (step A), the first feature in the Candy translator only.
- **`self_host.py`:** `build_t1` builds T1 with `bin`; `build_bin` has T1 build T2, checks
  that T2 translates the translator into itself and passes `mypy --strict`, and only then
  copies it over `bin` (see `bin/README.md`). The order mattered: `import` first went into
  `src/cdy/` unused and `bin` was rebuilt by the Python translator one last time; then
  `cdyc.cdy` started using it and `bin` rebuilt itself.
- **Tests:** T1 is built by `bin`. Programs in `tst/cdy/t1/` and `tst/cdy/` still run
  under both translators, new ones that need the Candy translator go in `tst/cdy/cdyc/`.
  The reader agreement tests stay until the first syntax change. The test that `bin` runs
  without `py_cdy` now has it rebuild itself.
- **Bootstrapping from nothing:** check out tag `self-host-py`.

## 3. Cleanup candidates

From the leak lists and `doc/tech_debt.md`; to be picked and ordered:

- ~~**The spec:** add `sig`, `deft` (records and sums), `match`, `get` and `assoc` to
  `src/cdy/candy-special.md` (an open item since the iMVP).~~ Done, with `import`
  (step A), the type names, and the rules decided in the iMVP doc.
- **The Candy translator's simpler output** (every operator parenthesised, `format` as a
  `str()` concatenation, more renaming, no conditional-expression merging). These only
  change what the generated Python looks like.
- ~~**`and`/`or` arguments with statements didn't short-circuit**~~ in the Candy
  translator: `(or (< n 0) (do (put "x") (> n 10)))` printed `x` even when `n` was
  negative. Fixed: `value-boolop` in `lower.cdy` does what the Python translator's
  `value_boolop` does, `(and a b)` becoming `t = a; if t: t = b` (`or` tests `not t`).
  The translator's own code had such cases, so `bin` changed. Test:
  `tst/cdy/short_circuit.cdy`, run under both translators.
- **Tuple patterns in `match`**, so a `tup` can be taken apart anywhere, not only in a
  `let` binding (the stopgap that rewrites it into `at` calls, in
  `doc/archive/leaks_imvp_py_translator.md`). Candy translator only; the `let` form could
  then become one more kind of pattern.
- **Types and values share one namespace** (a variant can't take its type's name).
- **The symbol table is an opaque `Any`** in the Candy translator. Typing it in Candy
  (`deft TableEntry ...`) would let `system.cdy` replace `table.py` later.
- **`get` before `match` is caught by mypy, not by Candy.** Candy has no type checker of
  its own yet; that is a much bigger project and probably its own HLD.
- ~~**A driver in Candy:** `main.py`'s job (read a file, translate, write `output/`) as a
  Candy program using `SYS_ARGS`, `slurp` and `spit`, so `bin/py/` can be run directly.~~
  Done; see "The driver as built" below.
- **Error positions:** only parse errors have a line and column. The reader knows
  positions; the forms don't carry them yet.
- **Recursion:** the Candy translator walks lists by recursion that isn't a self tail call
  in places, so `self_host.py` raises Python's recursion limit to 20,000.

### The driver as built

- **`main` is the entry point** (a convention, not a special form): a program that defines
  `main`, typed `(Fn ((List String)) Int)`, runs it after its top-level forms when the
  program is run, with the command-line arguments, and exits with its result. `analyse`
  checks the type (`has-main` in `core.cdy`); `emit-main` adds
  `if __name__ == "__main__": cdy_rt.table_defs.run_main(main)`, so loading the module
  (as `self_host.py` and the tests load `bin`) doesn't run it. `run_main` turns a `fail`
  or an unreadable file into `candy: <error>` on standard error and exit status 1.
- **The driver** is `main` in `cdyc.cdy`: `python bin/py/cdy_translator.py FILE.cdy
  [OUT.py]`, `OUT.py` by default `output/FILE.py`, as `main.py` does; usage errors exit
  with 2. It doesn't run the result (no `--run`: Candy can't start a process yet), so
  `main.py --translator bin --run` stays for that.
- **New runtime built-ins:** `put-err`, `make-dirs`, `path-stem`; `SYS_ARGS` is now a
  `(List String)` (a tuple, as `List` is everywhere; it was a Python list).
- **Tests:** `tst/cdy/cdyc/main.cdy`; `bin` run as a program, with `py_cdy` and `parsec`
  blocked, rebuilds itself and translates a program, and its errors and exit codes.

## Open questions

1. **Is inclusion (step A) the right first `import`**, with real modules (step B) later?
   Decided: yes.
2. **Freeze the Python translator now** (new features only in the Candy translator), or
   keep both in step for a while longer? Decided: freeze it now; `import` goes into the
   Candy translator only.
3. **Which cleanup items, and in what order?** Decided: `import` step A, the
   self-rebuilding `bin/py/`, the spec update, then the rest as they get in the way.
4. **The top file's name** for the translator. Decided: `src/cdy/cdyc.cdy`.
