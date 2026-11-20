# The standard library (HLD)

**Status: accepted (2026-11-18), with the answers to its questions, as proposed
(tasks [[B206]] to [[B213]]; Question 8 tabled); drafted 2026-11-17, for branch
`stdlib`. Epic: `python_complete.md` (its fifth branch, `library`, the second half: the
modules; the layering was `library_layers.md`).
After tag `library-layers`.** The built-ins grouped into modules a program imports by
name (`string`, `map`, `math`), their names without the prefixes that stand in for
modules today (`str-len` is `string.len`); a `list` module of what is built on the list
built-ins; the prelude trimmed, and its costs fixed; and a `test` module.

## Where things stand

- **The system** (`system.cdy`) is 75 built-ins, every file's, unqualified (and as
  `system.name`, since `library-layers`), each specified in `spec/60-library.md`. It is
  one flat set ([[B108]]): `cos` sits next to `map-get` and `slurp`. Its names carry
  their group, for want of modules and interfaces ([[B34]]): `str-len`, `char-at`,
  `substring`, `str-contains`; `map-get`, `map-has`, `map-set`, `map-keys`,
  `map-from`, `map-size`, `empty-map`.
- **The prelude** (`prelude.cdy`) is `rest`, `Maybe` with `find`, `index-of` and
  `with-default`, `Result`, and `map-update`; `prelude_macros.cdy` is `cond` and `put`.
- **The mechanism is there** (`library-layers`): a library module is found by name, next
  to the translator, after the importing file's directory; a declaration module declares
  built-ins with bodiless `sig`s, always the library's. But the declaration modules are a
  list in `include.cdy` (`DECLARATION_MODULES`), and a built-in is keyed by its bare
  name (`Prim "len"`, `spelling.py`'s `"len"`), so two modules can't declare one name.
- **`(import m ())`** imports a module with nothing unqualified, every use `m.name`
  ([[programs.import]]); an import's name shadows a built-in's ([[programs.shadowing]]).
- **The prelude's costs,** measured in `library-layers` step 1 (a four-module program):
  reading `special.cdy` and `system.cdy` is 62% of a translation, 11 times over, per
  module and per macro program ([[B66]]); compiling the prelude's macros per module 39%
  ([[B62]]); the whole prelude goes into every program's Python, 49 lines ([[B68]]).
- **No tests in Candy:** the test programs check their output against `.out` files,
  and the spec's examples are run by `test_spec.py`.
- **The uses, in the translator** (`src/cdy/`, not the library): the map built-ins about
  310 (`map-has` 93, `map-set` 83, `map-get` 67, `empty-map` 54, `map-keys` 11); the
  string ones about 115 (`str-len` 34, `substring` 26, `char-at` 12, `str-contains` 10);
  the files and paths 36; `math` none.

## Goals

- **Modules for the groups** ([[B108]]): `string`, `map` and `math` are library modules,
  declaration modules for their built-ins, with Candy for what is built on them; a
  program imports one by name and uses it qualified, `(string.split s ",")`.
- **Names without the prefix:** a module's operations are named for what they do,
  `string.len`, `string.at`, `string.slice`, `string.contains`, `map.get`, `map.set`,
  `map.keys`; the same verbs as the list's, until interfaces make them one ([[B34]]).
- **A `list` module** of what is built on the list built-ins, which stay in `system`
  (lists are everywhere: `len` 263 uses, `at` 296, `map` 86).
- **The prelude trimmed** to what nearly every program uses: `Maybe` and `Result` with
  their helpers, and `rest`; `map-update` goes to `map`.
- **The prelude's costs fixed:** the built-ins read once per translation ([[B66]]), the
  prelude's macros compiled once ([[B62]]), and, if cheap, a program's Python carrying
  only the prelude it uses ([[B68]]).
- **A `test` module:** `check`, `deftest` and a runner, which the modules test themselves
  with.
- **Each module specified,** as the system's built-ins are: a rule per module, its calls
  with their types and edges, and the index test extended to every declaration module.

## Not goals

- **The I/O refactor** ([[B95]]): the files and paths stay in `system`, and `put-err`
  with them, until a branch of its own designs `io` ("expect a big one", the owner).
- **A target extension, `py`** ([[B49]]): when a program needs one.
- **`parse`** (the epic's Question 6): not cheap here, as the epic allows; after the epic,
  as an `idea`.
- **Interfaces** ([[B34]]): `string.len` and `len` stay two names.
- **The spec's runner in Candy** (the epic's "Testing in Candy"): it needs the
  interpreter.
- **Macro code's prelude** ([[B52]]): `host-macros`'.
- **Moving the library out of `src/cdy/`:** Question 6.

## Proposal

### Declaration modules from the spellings, and built-ins keyed by module

A declaration module is a library module the target provides built-ins for, each a
bodiless `sig` there giving its type. A built-in is keyed by its module and name, as a
program's names are (`global-key`): `string.len` and `len` are two built-ins,
`spelling.py` spells `"string.len"`, and `system`'s keep their bare names. So the
spellings' keys name the declaration modules, and no list does (`DECLARATION_MODULES`
goes). `string.cdy` declares `len`; a file that imports `string` sees it as `string.len`
(and unqualified, as any import's names, Question 3).

The library's files, by what they are and how the translator finds each:

| File | What it is | Found | Seen by |
|---|---|---|---|
| `system.cdy` | a declaration module | by name; a bare spelling key is its | every file, implicitly |
| `translator.cdy`, later `string.cdy`, `map.cdy`, `math.cdy` | declaration modules | their spelling keys (`translator.fresh-name`) | a file that imports it |
| `prelude.cdy` | an ordinary Candy module | by name | every file but itself and the declaration modules, implicitly |
| `form.cdy`, later `list.cdy`, `test.cdy` | ordinary library modules | by file name, when imported | a file that imports it |
| `special.cdy`, `prelude_macros.cdy` | not modules (`NOT_MODULES`) | by name; the translator reads them | — |

The names the translator knows are the language's fixed points (`system`, `prelude`,
`special`, `prelude_macros`); every other library module is found by a rule.

*Revised (2026-11-19, the owner and Claude),* as built in step 1: a declaration module
found by the spellings, not by reading every library file to see what it holds, which
`library-layers` had proposed too and also built otherwise (a list, its step 2a). It
was:

```text
A library module whose forms are all bodiless `sig`s and `deft`s is a declaration
module, found by what it holds, not by a list (`DECLARATION_MODULES` goes). A built-in
is keyed by its module and name, as a program's names are (`global-key`): `string.len`
and `len` are two built-ins, `spelling.py` spells `"string.len"`, and `system`'s keep
their bare names. `string.cdy` declares `len`; a file that imports `string` sees it as
`string.len` (and unqualified, as any import's names, Question 3).
```

### The modules

Each module is a declaration module for its built-ins and, for what is built on them,
Candy: a declaration module holds only bodiless forms, so a module with both is two
files, the declarations in one the module imports and its importers don't see
(`string_sys.cdy`, say) and the Candy in `string.cdy`, which defines each name over them;
or a declaration module may hold ordinary definitions too (Question 2).

- **`string`:** `len`, `at` (a `Char`), `slice`, `contains`, `starts-with`, `ends-with`,
  `split`, `join` (from `system`'s, which takes a list of strings), `repeat`, `replace`,
  `to-int`, `to-float`, `code` (`char-code`), `hex-char`, `is-decimal`, `is-space`
  (`isspace`); in Candy, `trim` and `lines`.
- **`map`:** `empty`, `get`, `has`, `set`, `keys`, `from`, `size`; in Candy, `update`
  (the prelude's `map-update`), `values` and `get-or` (a key's value, or a fallback). The
  name: Question 4.
- **`math`:** `PI`, `sin`, `cos`, `tan`; in Candy, `abs`, `min` and `max` (on a
  `comparable` or `number`).
- **`list`:** Candy over `system`'s list built-ins: `last`, `sort` (a merge sort, on a
  `comparable`), `sum` (a `number`), `flat-map`, `partition`. What else, Question 5.

Each moves out of `system` as a whole, its old names gone, and the translator onto the
new ones, a step per module. `system` keeps the types, the operators, `nil`, `fail`,
output (`put-line`, `text`, `show`), the lists, and the files until `io`.

### The prelude

`Maybe` (`find`, `index-of`, `with-default`), `Result` and `rest` stay; `map-update` is
`map.update`. Its costs:

- **[[B66]], the built-ins read once:** `library-builtins` runs once per translation, its
  map passed to each module's analysis and each macro program's, not read again.
- **[[B62]], the prelude's macros compiled once:** expanded and loaded once per
  translation, not per module.
- **[[B68]], the prelude a program uses:** `emit` writes an imported module's
  definitions only when the program reaches them (from the top module's, through the
  bodies that call them); if that is more than a step, it waits, an `idea`.

### The `test` module

```
(import test ())
(import-macros test_macros)

(deftest splits (test.check (= (string.split "a,b" ",") (List "a" "b"))))
(deftest trims (test.check (= (string.trim "  x ") "x")))

(sig main (Fn ((List String)) Int))
(defn main (_) (test.run (List splits trims)))
```

- `(deftest name check ...)`, a macro, defines `name` as a `Test`: its name and a
  function giving its checks, each a `Check`, `Pass` or `(Fail text pos)`.
- `check`, a macro, is a `Check` of a `Bool`: `Fail` carries the expression's text and
  position, so a failure says `string_test.cdy:4:16: (= (string.trim "  x ") "x")`.
- `test.run` runs each test, writes each failure and a count, and gives `main`'s exit
  status: 0, or 1 if one failed.
- A test is a list of checks, not a panic: one failed check doesn't stop the others. A
  panic in a test stops the run, as any panic does (*lasting*: a panic is a bug).
- A program names its tests to `test.run`: no registry, since a module can't collect
  its definitions (*for now*; a macro over the module, later).

The modules' tests are `tst/cdy/stdlib/<module>_test.cdy`, run by pytest, which expects
exit status 0.

### The spec

`spec/60-library.md` keeps the system's groups; each module gets a rule of its own
(`library.string`, `library.map`, `library.math`, `library.list`, `library.test`), with
its calls' table and examples, and `library.builtins`' index a row per module. The
index test (`test_every_builtin_is_specified`) reads every declaration module, not
only `system.cdy`. `programs.import` changes for declaration modules found by the
spellings.

## Pros and cons

- **For:** the flat set is split as the epic planned; the names lose their prefixes;
  a program states what it uses (`(import string ())`); the porting surface is grouped;
  the costs that matter (62%, 39%) go; tests can be written in Candy.
- **Against:** about 425 of the translator's calls change (mechanically, a step per
  module); two built-ins may now have one name (`len`, `string.len`), which is the
  point but needs care in errors; each module's move is a bootstrap step that the last
  `bin` must read (see "Bootstrap").
- **Why now:** the mechanism is fresh (`library-layers`), and the epic's later branches
  (the interpreter, `host-macros`) write against the library's final shape: the
  interpreter implements every built-in, so fewer, grouped ones help it.

## Bootstrap

The last `bin` reads the step's own library, so a declaration module it doesn't know
breaks it: step 1 (found by the spellings) comes first, in its own commit, before any
new one. A module's move renames built-ins the translator's source calls: the step's
library declares the new names and the step's runtime spells them, which the last `bin`
reads, as in `library-layers` step 4; what the last `bin`'s own Python calls must stay
in the runtime (a renamed built-in keeps its Python function: `map_get` stays
`map_get`). Each step is checked with `test_newest_step_reads_the_library` and
`bootstrap.py --step`, as before.

## Steps

1. **Declaration modules from the spellings, built-ins keyed by module:**
   `DECLARATION_MODULES` gone; `Builtin` and the spellings keyed by `global-key`; the
   index test over every declaration module.
   *Done (2026-11-18). As built:* a built-in is keyed by `builtin-key` (`core.cdy`), its
   module's `global-key` but a `system` built-in's own name: `translator.fresh-name`,
   `len`; `read-sigs` keys each, `declared-name` gives a `Declared` entry's key, and
   `declaring-module` finds `m.name` for the "doesn't import" error. `spelling.py` keys
   the translator's five `translator.`; `system`'s keep their names, so nothing else
   changes. The declaration modules are found by what the target holds, not by what
   each file does: `declaration-modules` (`include.cdy`) is the modules the spellings'
   keys name, which needs no directory listing and no read of every library file (B66);
   `read-sigs` still checks each holds only bodiless forms, and a library module that
   holds both (Question 2) comes with step 4, the first. The rule: `programs.import`. The
   index test reads every declaration module the runtime's spellings name but
   `translator` (`declared_builtins`). Bootstrap: `boot/83` can't read the new keys
   (`spelling.py: translator.fresh-name is declared in none ...`), so this step is
   staged `old-runtime`; `test_newest_step_reads_the_library` now tries the step's own
   runtime too, and says which staging is needed. Checked against `boot/83`'s `bin` (run
   with its runtime): the same output for all 102 programs, the translator's too.
2. **The prelude's costs:** [[B66]] and [[B62]], measured before and after; [[B68]] if it
   is cheap.

   *Done (2026-11-19). As built:* an `Expander` (`expand.cdy`), made once per
   translation (`expander`, `cdyc.cdy`), carries the built-ins, the macro compiler and
   the prelude's macros, compiled and loaded once (`new-expander`), which every file's
   expansion starts from, in place of `prelude-import`; `compile-macros` closes over the
   built-ins and macro code's imports, each read once, and `load-defs` takes the
   built-ins from it. `library-builtins` runs once per translation, against 11 times
   for `modules.cdy` and 23 for the translator. With `bin`, wall time (median of 5),
   before and after: `modules.cdy` 0.219 s and 0.119 s, `(put 1)` 0.153 s and 0.114 s,
   `macro_files.cdy` 0.240 s and 0.134 s, the translator 1.041 s and 0.861 s.
   [[B68]] waits: it is more than a step (a reachability pass over Core, through the
   functions' bodies as `check-order`'s `uses`, every node's and definition's types, for
   the annotations, and each clause's variant, for its sum; and whatever `lower` and
   `emit` name without a `Global`), for 49 lines of a program's Python and 2% of its
   time. No staging.
3. **`test`:** `check`, `deftest`, `test.run`, with its own tests.

   *Done (2026-11-19). As built:* `test.cdy` (`Check`, `Test`, `run`, `failures`) is an
   ordinary library module, and `test_macros.cdy` (`deftest`, `check`, and `form-text`,
   which writes a form back, its strings' escapes not, *for now*: [[B214]]) a library
   macro file; both are in `LIBRARY` (`self_host.py`). The macros write `test.`-qualified
   names, so a file imports `(import test ())`. `deftest` must define a name with its
   `sig`, two top-level forms, and a macro gives one, so the owner chose a language rule
   (2026-11-19): **a top-level `do` is its forms, spliced** (`splice-dos`, `expand.cdy`;
   [[programs.top-do]]), Scheme's `begin`; a `defmacro`, `import` or `import-macros` in
   one is an error, since those are read before expansion. `test.run` writes each failed
   check as `{pos}{test}: {text}`, then `tests: N, checks: N, failed: N`, and gives 0 or
   1. No registry ([[B215]], an idea). The rule: `library.test`;
   `tst/cdy/stdlib/test_test.cdy` (new, in `test_output`'s programs) tests the module
   with itself, without printing a failure, whose line holds its file's path. Checked
   against `boot/85`'s `bin`: the same output but for the three programs with a
   top-level `do` (`test_test.cdy` and the two spec examples), which it rejects ("sig is
   only allowed at top level"). No staging.
4. **`math`:** the four moved, and `abs`, `min`, `max`; nothing in the translator uses
   them.

   Two commits: `boot/86` finds `math` by its new spelling keys and can't read its Candy
   ("expected (sig name Type)"), and no staging helps, since the old runtime and the old
   library each fail too. So 4a teaches the translator a declaration module with
   Candy, and 4b moves `math`, which 4a's `bin` reads.

   *4a done (2026-11-19). As built:* a declaration module's declarations
   (`declarations`, `core.cdy`) are each `sig` of a name it doesn't define and each
   bodiless `deft`; the rest (`definitions`) is ordinary Candy. `read-sigs` reads only a
   module's declarations (all of `system.cdy`'s, which stays declarations only), and
   `declared-exports` too; `expand-modules` (`cdyc.cdy`) expands and analyses a
   declaration module's definitions as any module's, its exports both
   (`with-declared`), so its Candy uses its built-ins unqualified. A declaration module
   still imports no prelude, and macro code sees only `translator`'s built-ins. The rule:
   `programs.import`; `test_a_declaration_module_holds_candy`. Checked against
   `boot/86`'s `bin`: the same output for all 105 programs. No staging.
5. **`string`:** moved and renamed, `trim` and `lines`; the translator onto it.
6. **`map`:** moved and renamed, `update`, `values`, `get-or`; the translator onto it;
   the prelude's `map-update` gone.
7. **`list`:** the Candy operations.
8. **Docs:** CLAUDE.md, the epic's fifth branch *done*, `library.md`,
   `multi_target.md`; "Looking back".

## Questions

1. **Scope:** the modules `string`, `map`, `math` and `list`, the prelude's costs and
   `test` (proposed), with `io`, `py` and `parse` later; or smaller, the modules only,
   the costs and `test` a branch each? **Proposed: as listed**: the costs are a step,
   and `test` is what the modules test themselves with.
   *Answer (2026-11-18, the owner): as proposed.*
2. **A module with built-ins and Candy:** two files, the declarations apart
   (`string_sys.cdy`), which only the module imports; or a declaration module may hold
   ordinary definitions as well, its bodiless `sig`s the built-ins (one file each)?
   **Proposed: one file:** a declaration module is one with any bodiless `sig`, always
   the library's; the rest of it is ordinary Candy.
   *Answer (2026-11-18, the owner): as proposed.*
3. **How a program imports a module:** as any module (`(import string)` makes
   `string.len` unqualified `len`, which shadows the list's `len`, *lasting* rule, so the
   file's `(len xs)` is then a type error); with `()`, qualified only, by convention
   (the spec's and the tests' examples write `(import string ())`); or a new rule, an
   import doesn't shadow a built-in, and a name both define is an error where it is used
   unqualified ("len is defined by string and system: write string.len or system.len"),
   as for two imports? **Proposed: by convention, `()`,** *for now*, since the rule
   would change `programs.shadowing` for every module; revisited with interfaces.
   *Answer (2026-11-18, the owner): as proposed.*
4. **`map`'s name:** `map`, as the type is `Map` (`map.get`, next to the function
   `map`), or `dict` (Elm's `Dict`, Python's `dict`)? **Proposed: `map`**: the qualifier
   and the function can't be confused in a form (`(map.get m k)`, `(map f xs)`).
   *Answer (2026-11-18, the owner): as proposed.*
5. **What the Candy parts hold:** the lists above, drawn from what programs write by
   hand (the translator has few: `char-text`, `indent`, `name-set`, `put-all`), kept
   small and grown as programs need them? **Proposed: as listed,** each with a rule and
   tests.
   *Answer (2026-11-18, the owner): as proposed.*
6. **Where the library lives:** in `src/cdy/` with the translator's own files (as now),
   or a directory of its own (`src/cdy/lib/`, copied to `bin/py/lib/`), which the last
   `bin` couldn't find without staging? **Proposed: as now,** *for now*, an `idea` for
   the directory; the files' header comments say which they are.
   *Answer (2026-11-18, the owner): as proposed.*
7. **`test`'s tests in the run:** a program lists its tests (proposed, no registry), or
   `deftest` registers them (a macro writing a module-level list, which Candy can't
   append to)? **Proposed: listed.**
   *Answer (2026-11-18, the owner): as proposed.*
8. **Is `system` only the language?** Candy's code isn't its lists, as a Lisp's is: code
   is `Form`s (`form.cdy`), and `List` is an immutable vector (the host's tuple). The
   `List` type stays in `system`, since the language uses it (rest parameters, `++`, the
   built-ins' types), but the list operations are there because the host provides them,
   not because they define the language. `system` could be only the language (the
   types, the operators, `nil`, `fail`, `show`, `text`), the list primitives in a `list`
   declaration module every file imports implicitly (call sites unchanged, `list.len`
   beside `string.len`). It costs a second implicit declaration import and a file read
   per module, against [[B66]] and [[B62]], for symmetry mostly.
   *Tabled (2026-11-18, the owner),* to decide at `io` ([[B95]]), when the files leave
   `system`, or at a second target; `doc/brainstorm.md`, "is `system` only the
   language?".
