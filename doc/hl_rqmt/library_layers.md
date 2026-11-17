# The library's layers (HLD)

**Status: accepted (2026-11-15), with the answers to its questions, as proposed (tasks
[[B199]] to [[B205]]); proposed 2026-11-14, for branch `library-layers` (Question 1).
Epic: `python_complete.md` (its fifth branch, `library`, the first half: the layering;
the modules are the second). After tag `namespaces`.** The system revisited: the
translator's built-ins out of every program's sight, what is Python's or unused dropped,
the built-ins a module of their own, each built-in specified; and what the standard
library and the target extensions need first: modules found by name in the library, and
declaration modules. The epic's "The library" (layers 2 and 3, and the mechanism for 4
and 5) is the starting point, with the earlier `library.md`'s "What a program sees".

## Where things stand

Counts from today's source (2026-11-14, after tag `namespaces`).

| Item | Today | Seen where |
|---|---|---|
| the system | 94 bodiless `sig`s and 12 bodiless `deft`s in one file, every file seeing all of them | `system.cdy` |
| [[B50]] the translator's five host built-ins | `py-spellings`, `load-macros`, `call-macro`, `module-dir`, `fresh-name`: every program's | `system.cdy`, `library.builtins` |
| unused built-ins | 14 that nothing uses: not the translator, the spec's examples, the test programs or the backlog's repros: `re-search`, `re-findall`, `re-compile`, `is-coll`, `is-str`, `is-alpha`, `is-neg-int`, `strip`, `is-empty-str`, `file-put-lines`, `sin`, `cos`, `tan`, `SYS_ARGS` | `system.cdy` |
| [[B32]], [[B49]] Python's in disguise | the three regex built-ins return Python's objects, typed `Any`; `is-coll` and `is-str` take `Any`, a Python `isinstance` | `system.cdy` |
| [[B54]] `slurp` searches | a missing path is looked for under `src/`, `tst/` and `lib/` | `primitives.py`, `get_path` |
| [[B197]] the built-ins' module | `""` in Core; no program can write `system.len`, so a file that defines `text` can't reach the built-in | `core.cdy`, `programs.sees` |
| built-ins specified | all 94 named in the spec, most only in `library.builtins`' table, with no rule or example of their own | `spec/60-library.md` |
| a library module by name | none: `(import m)` finds `m.cdy` only in the importing file's directory; the library files are found by the translator itself, next to it | `include.cdy`, `expand.cdy` |
| declaration files | only `system.cdy` may hold a bodiless `sig` or `deft` | `core.cdy` |
| [[B51]] `with-default` a built-in | stale: it is the prelude's, written in Candy, since `semantics` | `prelude.cdy` |

## Goals

- **The translator's built-ins kept to the translator** ([[B50]]): a declaration module
  only the translator imports.
- **The system small and portable:** what nothing uses, or what is Python's, out
  ([[B32]]; [[B49]]'s regex half).
- **The built-ins a module:** `system`, imported by every file as the prelude is, so
  `system.text` reaches a built-in that a file shadows (`namespaces.md`, Question 5's
  *for now*), and a built-in type has a module ([[B197]]'s first half).
- **Each built-in specified:** a rule with an example that runs, for every `sig` in
  `system.cdy`, and a test that keeps it so.
- **The mechanism for the layers above:** a module found by name in the library, and a
  library module that declares built-ins, which the second branch's standard library and
  the target extensions both need.
- **`slurp` without a search** ([[B54]]).

## Not goals

- **The standard library's modules** (`list`, `string`, `map`, `math`, `io`, `test`,
  `parse`; [[B108]]): the second branch's, with its own HLD. So the built-ins keep their
  names here (`str-len`, `map-get`), and are renamed, if at all, when a module takes
  them (`string.len`).
- **The I/O refactor** ([[B95]]): the `io` module's design, the second branch's.
- **A target extension** (`py`; [[B49]]'s other half, opaque host types): the second
  branch's, or later, when a program needs one; this branch only lets one exist.
- **Re-export**, a program seeing only the prelude, which re-exports the system
  (`library.md`, "What a program sees", B): Question 6.
- **The prelude's costs** ([[B66]], [[B68]], [[B62]]): measured here (Question 7), fixed
  in the second branch, whose modules make them larger.
- **Macro code's module** ([[B197]]'s other half): `host-macros`', with [[B42]] and
  [[B45]].

## Proposal

### A library module, found by name

`(import m)` finds `m.cdy` in the importing file's directory, as now, and otherwise in the
**library directory**, the one the translator reads `system.cdy` and `prelude.cdy` from
(next to it: `bin/py/`, `output/t1/`). So `(import translator)` in the translator, and later
`(import string)` in any program, find a file the translator brings. A local file with a
library module's stem wins (Question 3), and two modules with one stem stay an error
(`programs.import`). A library module is an ordinary module otherwise: its names are
`m.name` too, and it can have private names.

### Declaration modules

A **declaration module** is a library module whose every top-level form is a bodiless
`sig` or `deft` (a `deft` only in `system.cdy`, *for now*): it declares built-ins, which the target supplies, as `system.cdy` does
now. Only a library module may be one (Question 4), and each name it declares needs the
target's spelling (`spelling.py`), checked both ways, as now, across all of them: a
spelling no declaration has is an error, as a declaration with no spelling is. A program
can't declare a built-in, so it can't reach the translator's five by declaring them.

A declaration module is always the library's (Question 9): `(import translator)` finds
the library's `translator.cdy` even next to a file with that stem, as the translator
already reads what it supplies itself (`system.cdy`, `special.cdy`, the prelude) from its
library only (`library-path`), never from a program's directory. So the translator's own
`src/cdy/translator.cdy` is only the source of the library's copy, as `src/cdy/system.cdy`
is, and a program can't put its own declarations in their place. Which library files are
declaration modules is a list, `system` and `translator`, *for now*: the runtime can't
list a directory.

### The translator's built-ins: `translator.cdy`

`translator.cdy` declares the built-ins only the translator needs: each a bodiless `sig`,
typed in Candy and defined by the runtime it runs on. `system.cdy` is the built-ins every
program gets, `translator.cdy` those only the translator does; both are declaration
modules.

The five move from `system.cdy` to `translator.cdy`, a declaration module next to it in
`src/cdy/` (copied to `bin/py/` with the others). The translator's modules that call them
import it (`cdyc.cdy`, `include.cdy`, `expand.cdy`, by the survey); a program that doesn't
import it doesn't see them, and `library.builtins`' sentence on them becomes a rule:
"only for the translator, in `translator`". Its name is Question 5's.

Macro code needs one of them: `gensym` (`form.cdy`, which every macro program includes)
calls `fresh-name`. A macro program runs inside the translator, so it gets `translator`
as it gets the
system, implicitly (`form.cdy` is included, not imported, until `host-macros`, [[B45]]);
an ordinary program doesn't.

### The system, a module

`system.cdy` becomes module `system`: every file imports it implicitly, as it imports
the prelude, so every built-in is also `system.name`. The shadowing rule stays (a file's
own `text` wins in that file, [[programs.shadowing]]), and `system.text` is the built-in
there, as a qualified name is never shadowed. In Core a built-in type's module is
`"system"`, not `""` ([[B197]]'s first half): every check for a built-in type
(`is-any`, `is-rest`, the constraints) reads `"system"`, and [[B196]]'s
`show` can tell a program's `Map` from the built-in's by its module. Macro code keeps
`""` until `host-macros`. `system.cdy` stays one file, a declaration module; the special
forms stay unqualified and unmoduled (`special.cdy`), as the language.

### The system, revisited

- **Dropped, Python's** (Question 2): `re-search`, `re-findall`, `re-compile` (Python's
  syntax and objects, [[B32]]), and `is-coll` and `is-str` (a host `isinstance` on an
  `Any`); none is used. Regexes come back as a portable module, or in `py`, when a
  program wants them.
- **Dropped, unused:** `is-alpha`, `is-neg-int`, `strip`, `is-empty-str` (`(= s "")`),
  `file-put-lines` and `SYS_ARGS` (`main` takes the arguments, [[programs.main]]).
- **Kept, unused:** `PI`, `sin`, `cos` and `tan`: portable, and `math`'s first, in the
  second branch.
- **Spelling and runtime:** each dropped built-in's spelling and primitive go too, and
  any runtime helper only they used.

That leaves 83 built-ins in `system` and 5 in `translator`.

### Each built-in specified

Every built-in in `system` gets a rule in `spec/60-library.md` (or the operators',
`40-expressions.md`), with an example that runs: by group, as now (lists, strings, maps,
files, output, math, the program), each rule naming its built-ins with their types and
what they do on the edges (an empty list, an index out of range, a missing key, a missing
file), *lasting*. `library.builtins`' table becomes the index, one row per group, linking
the rules. A test (`test_doc_links.py`) checks that every `sig` in a declaration module is
named in some `candy run` example, so a new built-in comes with one. The translator's five
are specified in `translator.cdy`'s comments, not the spec: they aren't the language's.

### `slurp` without a search

`slurp` reads the path it is given; a missing file is a panic, "can't read path"
([[library.errors]]). `get_path`'s search goes ([[B54]]). The translator reads its
library files by their full path already (`module-dir`), so nothing there relies on it.

### The spec

No draft file: the rules change in `spec/10-programs.md` (`programs.import`: the library
directory; `programs.sees`: `system` a module; `programs.shadowing`: `system.name`) and
`spec/60-library.md` (`library.builtins` and a rule per group). Their examples come with
their steps.

## Pros and cons

- **For:** the porting surface gets its shape: what a target supplies is the declaration
  modules and their spellings, each specified, and a program can't see the translator's.
  The second branch starts with its mechanism in place: `(import string)` finds the
  library's `string`, and `string` can declare built-ins.
- **Against:** a branch with little a program sees, beyond `system.name` and fewer
  built-ins; dropping built-ins no program uses can break a program outside this repo
  that does (none is known).
- **Timing:** after `namespaces`, which gave the qualified names `system.name` needs;
  before the standard library, which needs library modules by name.

## Bootstrap

Two steps can't be read by the last `bin`: declaration modules other than `system.cdy`
(step 2's `translator.cdy`, a bodiless `sig` there an error to it), and the dropped built-ins'
spellings (the last `bin` checks its own `system.cdy` against the runtime's
`spelling.py` both ways, so dropping a spelling it declares breaks it). Step 2 is two
commits instead (Question 10): 2a brings declaration modules and `translator.cdy`, so
its `bin` has one, and 2b, which imports it, is read by that `bin`.
Step 4 is a staged boot step (`script/bootstrap.py`, `STAGING`), as `namespaces` step 3
was. The rest is ordinary: one `boot/NN` per step that changes `bin`.

## Steps

1. **A library module, found by name:** the library directory in `include.cdy`'s lookup;
   the rule in `programs.import`; a test program importing a library module. And the
   prelude's costs measured (Question 7): the build, and a small program's translation,
   with and without it.
   *Done (2026-11-15). As built:* `import-path` (`include.cdy`) looks in the importing
   file's directory, then in `library-dir`, the translator's; `import-macros` too, which
   finds its file "as `import` does" (`macros.import-macros`). The error says both: "can't
   find nope.cdy in . or the library". Two of the library's files aren't modules
   (`NOT_MODULES`): `(import special)` and `(import prelude_macros)` are "special is the
   translator's, not a module"; `(import prelude)` works, and `(import system)` fails on
   its bodiless `deft`s until steps 2 and 3. The rule: `programs.import`;
   `tst/cdy/cdyc/library_module.cdy` (new) imports the library's `form`, the only library
   file that is an ordinary module today. Checked against `boot/76`'s `bin`: the same
   Python for every program but the new one, which it can't find. No staging.
   The costs, for `modules.cdy` (a top file importing two modules, four modules with the
   prelude), with `bin`: 0.22 s to translate, 0.22 s with an empty prelude; `(put 1)`
   0.15 s against 0.15 s, 80 lines of Python against 31. Profiled, reading `special.cdy`
   and `system.cdy` is 62% of the translation (`library-builtins`, 11 times: per module,
   and per macro program), and compiling the prelude's macros per module 39% (the two
   overlap, since a macro program reads the built-ins too). So [[B66]] is the cost that
   matters, [[B62]] the next, and [[B68]] small in time (2%) but 49 lines in every
   program's Python.
2. **Declaration modules, and `translator.cdy`** ([[B50]]), two commits (Question 10):
   - 2a: a bodiless `sig` or `deft` allowed in a library module whose forms are all
     such; a declaration module always the library's; the spelling check across all of
     them; the five moved to `translator.cdy`, every program still seeing them.
   - 2b: only a module importing `translator` sees them; the translator's modules import
     it, and macro programs get it.

   *2a done (2026-11-15). As built:* the five could move in 2a already, since every file
   still sees them: `bin` reads its own `system.cdy`, which has them, and 2a's own
   translator its `translator.cdy`; so 2a is testable, and 2b is what [[B50]] asks.
   `translator.cdy` (`src/cdy/`, in `LIBRARY`) declares the five, bodiless `sig`s only:
   only `system.cdy` declares types, *for now* ("translator.cdy: only system.cdy
   declares types"). `DECLARATION_MODULES` (`include.cdy`) lists the declaration
   modules, `translator` (`system` joins in step 3); `import-path` finds one in the
   library before looking anywhere else, and `is-declaration` tells one by its key, the
   library file's path, so a top file named `translator.cdy` stays ordinary. A
   declaration module imports no prelude, and `expand-modules` (`cdyc.cdy`) gives it no
   definitions, only `declared-exports` (`core.cdy`): each name a new `Entry`,
   `Declared`, which `resolve` makes a `Prim`, so an import's name list, `m.name` and
   the namespace errors work for it as for any module. `library-builtins` reads
   `system.cdy` and each declaration module (`read-builtins` takes them as a list of
   files, its errors naming the file), and checks the spellings across them all
   ("spelling.py: fresh-name is declared in none of special.cdy, system.cdy,
   translator.cdy"). The rule: `programs.import`. Staged `old-library`: `boot/77`'s
   `bin` builds 2a next to its own library (`self_host.py` does so), not next to 2a's,
   whose `system.cdy` no longer has the five its source calls
   (`test_newest_step_reads_the_library`, which now skips a library file the old step
   doesn't have). 2b needs none: 2a's `bin` reads `translator.cdy`.

   *2b done (2026-11-16). As built:* `Typed` (`core.cdy`) carries the declaration module
   that declares it, and `resolve` makes a `Prim` of a name no entry has only if
   `system` declares it (`is-everyones`); one another declaration module declares is
   "fresh-name is declared by translator, which this file doesn't import: (import
   translator)" (`declaring-module`). `cdyc.cdy`, `include.cdy`, `expand.cdy` and
   `form.cdy` import `translator` (`form.cdy` only `fresh-name`, for `gensym`). Macro
   code imports it implicitly: `analyse-program` takes its imports, `macro-imports`
   (`cdyc.cdy`); `form-defs` (`expand.cdy`) drops `form.cdy`'s import, and in a macro
   file an import of a declaration module adds nothing (`include-forms`). The rules:
   `programs.import`, `programs.shadowing`, `macros.macro-code`, `library`. Staged
   `old-library` too, unlike what 2a's note says: `boot/78` reads macro code's
   `form.cdy` from the library as it is, and 2b's has an import, an error in macro code
   to 78. [[B50]] fixed.
3. **The system, a module** ([[B197]]'s first half): `system.name`; a built-in type's
   module `"system"`; `programs.sees` and `programs.shadowing`. [[B196]] looked at again.
   *Done (2026-11-16). As built:* `system` isn't imported as a module: every file's table
   gets each built-in function, value and type as `system.name`, a `Declared` entry
   (`with-system`, `core.cdy`), and `system` as a qualifier; unqualified, a built-in stays
   the last a name can mean (`resolve`'s fallback), so an import's `len` still shadows
   it rather than clashing with it, as `programs.shadowing` says. `system.Int` in a type
   is the built-in type (`check-type`), and a type as a value, or a value as a type, says
   so. `(import system)`, of the library's file or a program's, is "import: every file
   imports system, implicitly". `system.cdy` stays out of `DECLARATION_MODULES`, read
   by `library-builtins` as before. In Core a built-in type's module is `SYSTEM`
   (`core.cdy`): `analyse-type` writes it, and `rename-type` keeps it for a name no
   usable entry has (`global-ref`; before, `""` there); `is-any`, `is-rest`,
   `returns-unit`, the constraints, `tcon` and `emit` read it. [[B196]] fixed:
   `show-name` (`emit.cdy`) writes a program's type with its module (`main.Map`,
   `.Map`), so `show` can't take it for the built-in's; its repro is `library.show`'s
   example now. The rules: `programs.sees`, `programs.qualified`, `programs.import`.
4. **The system, revisited** ([[B32]]; [[B49]] narrowed): the 11 built-ins dropped, with
   their spellings and primitives. Staged.
   *Done (2026-11-16). As built:* `system.cdy` and `spelling.py` lose the 11, and
   `primitives.py` their seven functions (`get_args` stays, for `run_main`); generated
   code no longer imports `re` (`PY_IMPORTS`, `emit.cdy`), so `re` is a name a program
   may take. No `system` built-in is typed `Any` now: only three of `translator`'s
   (`checking.any`, `library.builtins`). Not staged, unlike the Bootstrap section says:
   the chain puts the step's own library next to the translator before, and the step's
   `system.cdy` and runtime agree, so `boot/80` reads them
   (`test_newest_step_reads_the_library`). Only a local rebuild needs `bin/py`'s copies
   replaced first. `system` has 78 built-ins left, not 83 (the count above was taken
   with `translator`'s five still in it). [[B32]] fixed; [[B49]] narrowed to the macros.
5. **`slurp` without a search** ([[B54]]).
6. **Each built-in specified:** a rule per group in `spec/60-library.md`, the index, and
   the test.
7. **Docs:** CLAUDE.md, the epic's fifth branch *done in part*, `library.md`'s "What a
   program sees", `multi_target.md`; "Looking back".

## Questions

1. **The branches, and this one's name:** the epic's `library` as two branches, the
   layering first (this HLD), then the modules (`list`, `string`, `map`, `math`, `io`
   with the I/O refactor, `test`, perhaps `parse`; and the prelude's costs), or one
   branch with both? A tag `library` already exists (the branch that made the list,
   string and map operations built-ins), so neither can be called `library`.
   **Proposed: two, `library-layers` then `stdlib`,** each with its HLD, as
   `collections` and `collections-2` were.
   *Answer (2026-11-15, the owner): two, `library-layers` then `stdlib`.*
2. **What goes from the system:** the 11 above (the five that are Python's and the six
   that are unused), keeping the unused math; or only the five that are Python's,
   leaving the rest for the second branch's modules to take or drop; or all 14 unused,
   the math too? **Proposed: the 11,** so the surface the spec covers is what something
   uses or a module will; the math stays as `math`'s start.
   *Answer (2026-11-15, the owner): the 11.*
3. **A local file or the library's, for one stem:** the importing file's directory first
   (proposed: a program's own file wins, as Python's script directory does, and a new
   library module can't break a program); or the library first (a program can't hide the
   library's, but a new library module breaks a program with that stem); or an error,
   two files for one stem? **Proposed: the local one first,** *lasting*.
   *Answer (2026-11-15, the owner): the local one first,* *lasting*.
4. **Who may declare built-ins:** only a library module (proposed: a target brings its
   declarations, and a program can't declare one); or any module, each declaration
   checked against the spellings (a program could then name a host built-in itself,
   which [[B50]] means to stop)? **Proposed: only a library module.**
   *Answer (2026-11-15, the owner): only a library module.*
5. **The translator's declaration module's name:** `host` (proposed: they are the host's,
   macros and the spellings, and `host-macros` will move them on), `translator`, or
   `cdyc`? **Proposed: `host`.**
   *Answer (2026-11-15, the owner): `host`.*
   *Revised (2026-11-15, the owner): `translator`.* Every built-in is defined by the
   host, `system`'s too, so `host` named what the two share; what sets these five apart
   is that only the translator needs them. A tag on `system.cdy`'s declarations
   (metadata, as Clojure's) was weighed and left to `doc/brainstorm.md`: what a file
   sees is its imports' to say.
6. **What a program sees:** the system and the prelude, both imported implicitly, as now,
   `system` now a module (proposed, *for now*); or `library.md`'s B, a program seeing
   only the prelude, which imports the system and re-exports what programs need (one
   interface for every target, but it needs re-export, a feature of its own)? **Proposed:
   both implicit,** *for now*, re-export when the standard library shows it is needed
   (a new idea item).
   *Answer (2026-11-15, the owner): both implicit,* *for now* ([[B198]], new: re-export).
7. **The prelude's costs** ([[B66]], [[B68]], [[B62]]): measured in step 1 and fixed in
   the second branch (proposed: its modules make them grow, and its HLD can weigh them
   against them); or fixed here? **Proposed: measured here, fixed there.**
   *Answer (2026-11-15, the owner): measured here, fixed there.*
8. **[[B51]]:** closed as done, `fixed: semantics` (proposed: `with-default` has been the
   prelude's, in Candy, since `Maybe` became a sum), in the start commit.
   *Answer (2026-11-15, the owner): closed,* in this commit.
9. **Where a declaration module is found** (raised in step 2): the translator's own
   `(import translator)` would find `src/cdy/translator.cdy` first, a program's file,
   which can't declare (Question 4). Always in the library, even next to a file with its
   stem (proposed: the rule that already holds for what the translator reads itself,
   `library-path`, extended to an import by name, and a program can't replace a
   target's declarations); or the library's sources in a directory of their own,
   `src/lib/`, so the translator's modules have no local copy (one lookup rule for
   every import, but a layout change, and a program's file could still hide
   `system`)? **Proposed: always in the library.**
   *Answer (2026-11-15, the owner): always in the library.*
10. **Step 2's bootstrap** (raised in step 2): two commits, 2a with declaration modules
    and an empty `translator.cdy`, 2b with the five moved and the imports (proposed: 2a's
    `bin` reads 2b, so no new staging kind); or one commit, a staging kind that strips
    `(import translator)` from the source for the last `bin`? **Proposed: two commits.**
    *Answer (2026-11-15, the owner): two commits.*
