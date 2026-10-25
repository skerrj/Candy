# The executable spec: spec by example (process HLD)

**Kind: process** (how work is done: the spec, its tests, the lifecycle), not a design of
the language or translator. **Status: accepted (2026-10-23), with the proposed answers to
its questions, question 3 changed (the small test programs move into the spec).** For a
branch `executable-spec`, after tag `runtime-names`. From a chat with the owner
(2026-10-23, "Twine, spec-by-example, and the HLD plan"), mapped onto what Candy already
has; where the chat and the process or the code disagree, the conflict is flagged here
(**Conflict**) rather than settled. It also takes in `doc/brainstorm.md`'s "An SRS for the
current design" (its open format question).

## The idea (from the chat)

Docs, spec and tests become one artifact: every claim in the spec is an example that the
test runner executes. A spec file is plain Markdown; its prose explains, and its fenced
blocks are normative:

````markdown
## Exhaustive match

A `match` over a sum must cover every variant, unless it has an `else`.

```candy run
(deft Shape (Circle ((r Int))) (Square ((s Int))))
(put (match (Square 2) ((Circle r) r) ((Square s) (* s s))))
```
```expect
4
```

```candy error
(deft Shape (Circle ((r Int))) (Square ((s Int))))
(put (match (Circle 1) ((Square s) s)))
```
```expect-error
match on Shape: no clause for Circle
```
````

The runner extracts each `candy run` and `candy error` block, translates it with the real
translator, runs it, and compares with the `expect` block. (Both examples are checked
against today's translator: the first prints `4`; the second fails with
`2:6: match on Shape: no clause for Circle (or add else)`.)

The chat's other points: test behaviour, not translated text; the spec suite as the
bootstrap gate (stage 0, 1, 2 and a fixpoint); a per-feature lifecycle (`draft`, `stable`,
`deprecated`, `since`) tied to the bootstrap; a runner not written in Candy at first; coded
errors (`E0012`) for `expect-error`; `grammar.ebnf` as the only syntax authority; a
`CHANGELOG.md` that only links to the spec; doc generation (mdBook) for free.

**Conflict (syntax):** the chat's examples were in an ML-like syntax
(`deft Shape = Circle(r) | Square(s)`); Candy is S-expressions. The examples above are
rewritten in Candy.

## Where things stand

| The chat's piece | What Candy has |
|---|---|
| A spec | `src/cdy/candy-special.md`: informal, one section per special form, with grammar lines (`> (match *expr* ...)`) and no runnable examples. The HLDs record decisions branch by branch, not the whole language (`doc/brainstorm.md`, "An SRS"). |
| Examples as tests | `tst/cdy/**/NAME.cdy` + `NAME.out`: 18 whole programs, run through T1 (output and `mypy --strict`), and T1 and T2 must agree on each (`tst/py_cdy/test_self_host.py`). Errors are tested in Python: tables of `(source, message)` pairs (`test_errors`, `test_macro_errors`, `test_match_errors`, ...), matched as substrings. |
| Test behaviour, not text | Already so: the programs are run and their output compared; the translator's own text is checked only by the fixpoint (T2 reproduces itself, and is `bin`). |
| Stage 0, 1, 2 and a fixpoint | Already so: `bin` (stage 0) builds T1, T1 builds T2, T2 must reproduce itself and pass `mypy --strict`, and `bin` becomes T2 (`src/py_cdy/self_host.py`). Beyond the chat: the bootstrap chain, `boot/00` to `boot/31`, checks every past promotion (`doc/hl_rqmt/bootstrap.md`). |
| A runner not in Candy | Already so: pytest, in Python. |
| Coded errors | None: errors are `file:line:col: msg` (`fail`, about 116 calls in `src/cdy/`). |
| A grammar | None written down: the reader is hand-written (`src/cdy/read.cdy`); the literal rules are in CLAUDE.md and the iMVP doc. |
| Feature lifecycle | HLD statuses (*draft*, *proposal*, *accepted*, *done*) per branch (`doc/process.md`); no per-feature status, and no versions. |
| A changelog | None: the history is CLAUDE.md ("History and branches"), the feature tags and the HLDs. |

## Goals

- **One spec, whose examples run:** a Markdown spec of the language, one file per feature,
  where each example is a test, so the spec can't drift from the translator.
- **The spec in the gate:** the examples run wherever the test programs run (T1, and T1
  and T2 agreeing), so a `bin` that breaks the spec never becomes `bin`.
- **A home for a feature's lifecycle:** what is settled, what is a draft, what is going.
- **The process says when the spec is written** (a feature's examples with its HLD, or
  before its code).
- **A better way to review items and tasks:** its own HLD, `doc/hl_rqmt/review.md`
  (question 9).

**Not goals (for now):** generated docs (mdBook or the like: "After the MVP"); porting the
runner to Candy; a second target's runner (`doc/hl_rqmt/multi_target.md`).

## Proposal

### Layout

```
spec/
  README.md            how to read and write the spec; the block kinds
  00-syntax.md         literals, comments, the reader's rules (question 6)
  10-bindings.md       def, let, fn, defn, sig
  20-types.md          the type names, deft, get, assoc
  30-match.md          sum types and match
  ...                  one file per feature, in candy-special.md's order
tst/py_cdy/test_spec.py   extracts and runs every example in spec/*.md
```

`spec/` at the top level, beside `doc/`, since it is normative and tested (question 1).

### Blocks

- ` ```candy run ` then ` ```expect `: a whole program; its standard output must equal
  the `expect` block.
- ` ```candy error ` then ` ```expect-error `: translating it must fail, with a message
  that contains the `expect-error` text (as the Python error tables match today), without
  the `file:line:col: ` prefix unless the block gives it (question 4).
- ` ```candy errors `: a table of error cases, one per line, `source` ` => ` `message`
  (the substring), for a rule's edge cases, as the Python error tables hold them today
  ("Scale").
- ` ```candy ` alone: an illustration, not run (grammar lines, fragments).
- **Output is numbers and text** (*for now*, question 12): an example prints numbers and
  strings it builds with `format`, never a raw list, `Bool`, `nil` or record, whose
  printing is Python's. Rules that are *for now* say so, with their leak ("Pros and
  cons").
- Each example is its own program, in its own temporary file, with the prelude and the
  prelude macros as every program has them. A multi-module example is out of scope at
  first: those stay in `tst/cdy/cdyc/` (question 3).

### The runner

`tst/py_cdy/test_spec.py`, beside `test_self_host.py`, whose T1 and T2 fixtures it reuses:

- extracts the blocks from `spec/*.md` (a small Markdown fence scanner, not a Markdown
  library: fences are all it needs);
- one pytest case per example, named `file:line` (so a failure points at the spec), run
  through T1, and checked with `mypy --strict` like the test programs;
- the fixpoint's "T1 and T2 agree" covers the examples too.

Written in Python (the chat's point 4, *lasting* while the translator could break it).

### Scale

As the spec grows, three costs grow with it: the test time, the reading time, and what
Claude Code has to re-read.

**Test time,** measured on today's suite (2026-10-23), per program:

| Check | Per program |
|---|---|
| translate with T1 and run (`test_output`) | about 0.05 s |
| translate an error case (`test_errors`) | about 0.02 s |
| T1 and T2 agree (the fixpoint) | about 0.06 s |
| `mypy --strict` on the output | about 0.5 s |

T1 is loaded once and stays in the process, so translating and running scale well: 500
examples would be about 25 to 60 s. `mypy --strict`, one run per file, would be 4 minutes
or more, so:

- **one `mypy` run per spec file** (or for the whole spec), on all its generated files
  together, so mypy starts and loads its cache once (to be measured in step 1);
- **`mypy` only for `run` blocks:** an error example makes no Python;
- **parallel tests** (`pytest-xdist`) if that isn't enough (question 10).

The bootstrap chain is unaffected: `pytest -m bootstrap` rebuilds each step's `bin` and
runs no spec (the old steps have none).

**Reading:** "every claim is an example" turns into hundreds of fenced blocks that bury the
rules. So:

- every **normative** claim has at least one example, not every edge case;
- edge cases go in `candy errors` tables (one line each), or stay in `tst/`;
- one file per feature, and each test named `file:line`, so a failure points at its rule.

(The CommonMark spec has about 650 examples in one file and stays usable, with minimal
examples and a fast runner.)

**Claude Code's re-reading:** each file read costs context, and a summary of the
conversation loses detail, so a large spec is re-read often. So:

- **small files:** one feature each, a few hundred lines at most; split a file that grows
  past that;
- **an index:** `spec/README.md` lists the files with a line on each, so the right one is
  found without reading the others (CLAUDE.md points at it, not at the files);
- **rules before examples** in each section, so the prose can be read on its own and the
  examples only where needed.

This is better than today, where a rule is reconstructed from `candy-special.md`, the
HLDs' decisions and the tests.

### Feature lifecycle

Each spec file starts with a status line: `status: draft | stable | deprecated` and
`since: <tag>`, where the tag is the feature branch that brought it (`since: macros`),
since Candy has no versions (question 5).

- **draft:** its examples may fail (pytest `xfail`, so a passing one is reported); written
  with the HLD, before the code.
- **stable:** its examples must pass. A branch's docs step makes its features stable.
- **deprecated:** its examples still pass until the feature goes; the file says what
  replaces it.

**The bootstrap rule** (the chat's point 3: the translator may use a feature only once it
is stable and in stage 0): Candy already enforces the mechanical half, since `bin` has to
translate the translator's source, and the chain checks every step (a step that needs the
new feature before `bin` has it needs staging, `doc/hl_rqmt/bootstrap.md`). The policy
half, *stable* before the translator uses it, is new (question 5).

### Migration

1. The runner, and `spec/README.md`.
2. One feature, `deft` and `match` (the chat's choice: well specified, exhaustiveness
   errors already tested), moved from `candy-special.md` into `spec/30-match.md` with
   examples, and `test_match_errors`' table turned into `candy error` blocks.
3. The rest of `candy-special.md`, a file at a time, with the small `tst/cdy/` programs
   of each feature turned into its examples (question 3); it then goes, leaving a pointer
   (question 2). The Python error tables move into the spec where they are language
   rules (not the driver's or the bootstrap's).
4. **What points at it** moves with it. `src/cdy/special.cdy` says a special form is
   "analysed by its own rule (src/cdy/candy-special.md)": it holds only the names (34
   declarations), and `candy-special.md` the rules, so its pointer goes to the matching
   `spec/` file. That comment is in `bin/py/special.cdy` too, so this changes `bin`: a
   rebuild and a `boot/NN` step (no staging, a comment only). The others are docs:
   CLAUDE.md, `README.md`, `doc/process.md` (the docs step), `doc/brainstorm.md` and the
   iMVP doc; the older HLDs keep it, as history.

## Pros and cons

**Pros:**

- **The spec stops drifting:** `candy-special.md` is 142 untested lines; every rule gets an
  example that runs.
- **Cheapest now:** migrating means converting what exists (about 20 sections of
  `candy-special.md`, six small test programs, the language-rule cases of the Python error
  tables: `test_errors` alone has 32). A feature added before the spec is written twice,
  once the old way and once when migrated; after it, a feature is written once, straight
  into its spec file. So waiting is the con: variadic types, interfaces and generics would
  each be written twice.
- **Low bootstrap risk:** the translator's code is untouched; one comment in `special.cdy`
  is the only `bin` change.
- **Features start spec-first:** a draft spec file with the HLD, stable at its docs step.
- **Temporary rules become visible** (the owner's reading, 2026-10-23): much of today's
  behaviour is *for now* (`if` with no else gives `nil`, `tup` destructuring, `Maybe`
  collapsing). The spec marks each such rule *for now*, with its leak, so the hacks are
  written down where the rules are, and changing one later is expected, not a break.
- **Less re-reading for Claude Code:** one indexed home for the rules ("Scale").

**Cons:**

- **The expected output is Python's** (significant; question 12): `put` shows values with
  Python's `str()`, so `tst/cdy/lists.out` reads `(1, 2, 3)`, `True`, `None` and
  `('ann', 'bo')` (the leak: `doc/archive/leaks_imvp_py_translator.md`, "How each value is
  shown is Python's `str()`"). A spec whose `expect` blocks hold those makes the leak
  normative, and a second target would fail them.
- **Upkeep grows with the language:** every change to a feature edits its examples
  (`defn` may become a macro; variadic types, a real `Maybe` and a type checker are
  coming). Not migration but lasting work; the alternative is the same edits to an
  untested `candy-special.md`, or none.
- **Opportunity cost:** a branch with no language progress.
- **More process:** each feature branch writes its spec; reviews and test levels are
  still open (`doc/hl_rqmt/review.md`, question 11), so the process changes again.

**Timing:** now, before the next language branches, with a checkpoint: after step 2 (the
runner, and `deft` and `match`) the owner reviews how the spec reads before the rest of
`candy-special.md` moves. If it reads badly, one file is lost, not the migration.

## Process changes (`doc/process.md`)

- **The lifecycle:** an HLD for a language feature includes (or points at) its draft spec
  file; the steps make its examples pass; the docs step marks it stable. Today's docs step
  updates `candy-special.md`; it would update `spec/` instead.
- **"Where notes go":** a row for the spec: *a language rule, with its examples* →
  `spec/`.
- **Design docs:** the HLDs stay the record of decisions and what was built; the spec is
  the current whole (the SRS idea: the HLDs aren't its functional specs, the spec files
  are).

## Test levels (open)

The spec is one level of testing. The others exist but aren't named, and how each is
written, run and reviewed isn't defined anywhere (the owner, 2026-10-23; question 11).
Today, by level:

| Level | What it checks | Where |
|---|---|---|
| **spec** (the language) | a rule, by example | `spec/` (this HLD) |
| **unit** (a component's parts) | the runtime's primitives and spellings; the translator's internals, called directly (`py-mangle`, the reader) | `tst/cdy_rt/`; parts of `tst/py_cdy/test_self_host.py` |
| **component** (the translator) | whole programs and multi-file ones translated and run; the driver's and the bootstrap's own errors; `mypy --strict` on the output | `tst/cdy/` (the twelve kept), the rest of `test_self_host.py`, `test_main.py` |
| **system** (the translator building itself) | the fixpoint (T1 builds T2, T2 reproduces itself, is `bin`); the bootstrap chain from `self-host-py` | `test_self_host.py` (fixpoint), `pytest -m bootstrap` |

Open: whether these levels are the right ones; where each lives (one directory each, or
markers); and each one's process: who writes its tests and when (in an HLD's steps, like
the spec's draft examples?), when it runs (every step, or before a merge, as the chain
does), and how its results are reviewed (`doc/hl_rqmt/review.md`). Possibly a process HLD
of its own.

## Reviewing items and tasks

Its own HLD: `doc/hl_rqmt/review.md` (draft; question 9). A spec example could be what a
step's review points at, as that step's tests.

## Conflicts with the process and the code (flagged)

- **Stage 0 promotion:** the chat promotes stage 2 to stage 0 at a release; Candy
  promotes at every commit that changes `bin` (each a `boot/NN` step). No change
  proposed: the spec just joins the existing gate.
- **`since: 0.x`:** Candy has no versions; a feature tag stands in (question 5).
- **Coded errors:** every `fail` would need a code, about 116 calls; the substring match
  does the job without them (question 4).
- **`grammar.ebnf` as the only syntax authority:** checking examples against an EBNF needs
  a parser generator (a new test dependency), and the reader is the real authority today
  (question 6).
- **`CHANGELOG.md`:** the history already lives in CLAUDE.md, the tags and the HLDs; a
  fourth place would drift (question 7).
- **`candy-special.md` is "the spec"** for CLAUDE.md, the docs step and the editor
  grammar test (`test_editor_grammar.py` lists the special forms from `special.cdy`, not
  from it, so that test is unaffected).

## Steps (sketch)

1. **The runner** (`tst/py_cdy/test_spec.py`) and `spec/README.md` (the index), with one
   example to prove it; `mypy` batched per file, and its time measured ("Scale").

   *Done. As built:* `tst/py_cdy/test_spec.py` scans `spec/*.md` for fences (three or
   more backticks, closed by as many or more, possibly indented in a list item, whose
   lines then lose the indent), pairs `candy run` with `expect` and `candy error` with
   `expect-error`, reads `candy errors` rows, and fails at collection, naming `file:line`,
   on a block that doesn't pair up. Tests: `test_run` and `test_error`, one per example
   (`README.md:51`); per file, `test_mypy_strict` (all its `run` examples in one mypy run)
   and `test_t1_and_t2_agree`; `test_spec_files_have_a_status` (every file but the
   index); and the runner's own tests. A `status: draft` file's tests are `xfail`. The
   T1 and T2 fixtures moved from `test_self_host.py` into `tst/py_cdy/conftest.py`, so
   both share one T1 per session. `spec/README.md` is the index (no files yet), the guide
   to writing a spec file (the status line, rules before examples, *for now* rules with
   their leak, numbers and text for output) and an example of each block kind, which are
   the step's proof (4 examples). Measured (2026-10-23), 40 small examples: `mypy --strict`
   one file at a time 22.5 s (0.56 s each), in one batched run 0.4 s, so the spec's mypy
   time is negligible and question 10's `pytest-xdist` stays unneeded. Tests: 279 (15
   new). No `bin` change.
2. **`deft` and `match`** as the first spec file; `test_match_errors` moves into it.
   **Checkpoint:** the owner reviews how the spec reads before step 3 ("Pros and cons",
   timing).

   *Done. As built:* `spec/30-match.md` (`status: stable, since: self-host-py`): the
   grammar lines, then "Declaring a sum type", "Taking it apart: match" and "Taking a
   tuple apart" (since `self-host-cleanup`), each rule in prose before its examples: 10
   `candy run` examples, one `candy error`, and four `candy errors` tables (30 tests).
   The examples use `Int` fields, so their output is numbers and text. Two rules say
   *for now*: types and values share a namespace, and patterns are flat. Moved in:
   `test_match_errors` (20 cases, and its `SHAPES`), `test_errors`' `Box` row, and
   `tst/cdy/cdyc/tup_match` (its `True` now a string). Records, `get` and `assoc` stay in
   `candy-special.md` for `20-types.md`; its `deft` section keeps the record and points
   at the spec for sums, its `match` section is a pointer. The runner gained **setup
   lines** for a `candy errors` table (before a `---` line, put before each row), since
   the match table repeated its `deft` on every row; `spec/README.md` shows them. The
   setup is a test of its own (`test_setup`: it must translate alone, so a broken setup
   can't make a row pass on a matching message); one `---` per table (a second is a
   `SpecError`), surrounding spaces allowed. The
   first setup example in the README was wrong (calling an `Int` isn't an error the
   translator catches, only mypy would: no type checker yet). Tests: 291 (312 less the
   24 moved, all now in the spec, plus the two setups and a runner test).
3. **The other features**, from `candy-special.md`, one commit per file or two;
   `candy-special.md` goes.

   *Accepted at the checkpoint (2026-10-24):* the files, from
   `candy-special.md`'s sections and the small programs (question 3):

   | File | From `candy-special.md` | Programs folded in |
   |---|---|---|
   | `00-syntax.md` | literals, comments, `'` reserved; the reader is the authority (question 6) | — |
   | `10-programs.md` | programs, `main`, `import`, `import-macros` | — (`imports`, `modules` stay in `tst/`: multi-module) |
   | `20-types.md` | types, `sig`, `def`, records, `get`, `assoc`, `tup` | — |
   | `30-match.md` | done (step 2) | `tup_match` (done) |
   | `40-expressions.md` | `do`, `if`, `cond`, `let`, `defn`, `fn`; `Unit` and `nil` | `short_circuit` |
   | `50-macros.md` | `defmacro`, `quo`, `quasi`, `unq`, `unq-sp` | — |
   | `60-library.md` | `system.cdy`'s built-ins, the prelude, `format` | `lists`, `maps`, `strings`, `prelude` |

   In four commits: `00` and `10`; `20` and `40` (the Python error tables' language rows
   move with them); `50` and `60`; then the pointers (`candy-special.md` goes,
   `special.cdy`'s comment points at `spec/`, the `boot/32` step). **Tuples:** `tup` goes
   in `20-types.md`, pointing at `30-match.md` for taking one apart, so `30-match.md`
   holds every pattern and is retitled "Patterns and match" (rather than moving its tuple
   section out).

   *As built, commit 1 (`00` and `10`):* `spec/00-syntax.md` (forms, comments, literals,
   names: 6 `candy run` examples, 6 `candy errors` tables, with every error the reader
   gives) and `spec/10-programs.md` (top level, `main`, the prelude, `import`: 4 run
   examples, 3 tables). **One change to the table:** `import-macros` goes in
   `50-macros.md`, not `10`, since a macro file is about macros, and its examples need a
   second file. Moved in: nine `test_errors` rows (`()`, the top-level-only and `import`
   rows, `main`'s two) and `test_own_definitions_win_over_the_prelude`. The reader's own
   tests stay (`test_reader_accepts`, `test_reader_errors`, `test_reader_positions`):
   they check fragments and line and column, a unit level the spec leaves out (question
   11). Learned: a char can't be written in a `format` hole, since the string's escapes
   are read first (`"{\(}"` is a bad escape).

   *As built, commit 2 (`20` and `40`):* `spec/20-types.md` (the types, `sig` and `def`,
   records, tuples) and `spec/40-expressions.md` (names and calls, the operators, `do`,
   `if`, `cond`, `let`, `fn` and `defn`, `Unit`). **One addition to the table:** the
   operators (`special.cdy`'s `op`s) go in `40`, with `short_circuit`, which moved in
   (its `Bool`s now printed as `yes`/`no`; `tst/cdy/short_circuit.*` removed).
   `30-match.md` is retitled "Patterns and match". Moved in: 19 more `test_errors` rows,
   which leaves it the quoting and `format` rows (for `50` and `60`). Found by asking the
   translator what each rule does: three leaks (`doc/leaks.md`, "Found writing the
   spec": checks that only mypy or the run make, forms accepted that shouldn't be, and
   `quot`'s rounding) and two bugs (`doc/tech_debt.md`: `(sig x (List))` crashes the
   translator, and `(def (x) 1)` gets a message with no name). mypy rejects comparing
   two different literals (`(!= 1 2)`), so the examples compare names.

   *As built, commit 3 (`50` and `60`):* `spec/50-macros.md` (`defmacro`, macro code,
   errors at the call, quoting, `gensym`, `import-macros`, `cond`) and
   `spec/60-library.md` (the built-ins by group, lists, strings, maps, the prelude's
   `rest` and `map-update`, `format`). Folded in: `lists`, `maps`, `strings` and
   `cdyc/prelude` (their tuples, `True`s and `None`s now printed through `show` and `yes`
   helpers; the programs removed). Moved in: the rest of `test_errors` (the test is gone),
   `test_macro_errors`, `test_quoting_errors`, `test_quoting_only_in_macro_code`, and the
   single-file rows of `test_macro_file_errors`. The rows about where a macro's error
   points give the position (`line 2, column 1: `), which the README now allows.
   `candy-special.md` is all pointers now. Learned: a `format` hole can't hold a brace,
   so no `format` in a hole. Tests: 364.

   *Done. As built, commit 4 (the pointers):* `src/cdy/candy-special.md` is removed.
   `special.cdy`'s comment points at `spec/` ("the file for its feature"), and `bin` was
   rebuilt: only `bin/py/special.cdy` changed (`cdy_translator.py` is the same), the
   `boot/32` step. The live pointers moved too, minimally (the docs step does the rest):
   CLAUDE.md, `README.md`, `doc/process.md`, `doc/brainstorm.md`, `TODOS.md`'s `main`
   item, `mutation_optimization.md` (whose "`def` is mutable" pointed at a line the spec
   now states as "no form changes a `def` yet", `spec/20-types.md`), and two spec files.
   The older HLDs keep the name, as history.
4. **The process** (`doc/process.md`): the lifecycle, "Where notes go", design docs.

   *Done. As built:* a section "The spec" (the spec is the current whole, the HLDs the
   record; the statuses; the spec says what the translator does, and a gap it finds is a
   leak or tech debt, *for now*, not a fix in passing, as step 3 did; what stays in
   `tst/`). The lifecycle: a language feature's HLD comes with its draft spec file, each
   step changes the spec with the language, and the docs step marks the files `stable`.
   A row in "Where notes go", and the log.
5. **Docs:** CLAUDE.md (the spec, the tests), the iMVP doc, `doc/brainstorm.md` (the SRS
   entry moves here, leaving a pointer).

One `bin` change: `special.cdy`'s pointer (Migration, 4), copied into `bin/py/`, a
chain step with no staging. The translator's code is untouched.

## After the MVP

- A built-in that shows a value in Candy's syntax (`true`, `nil`, `(1 2 3)`), for the
  examples' output, with the I/O refactor (question 12).
- Generated docs from `spec/` (mdBook or similar), with the examples' outputs.
- Coded errors, if messages start changing under the tests.
- A grammar file checked against the reader (or generating it).
- Multi-module examples (a block that names its file), so `tst/cdy/cdyc/` can shrink.
- The runner in Candy, as dogfooding, once it can't hide a translator bug.
- Tutorials outside `spec/` whose code blocks run through the same extractor.

## Questions

1. **Where the spec lives:** `spec/` at the top (proposed), `doc/spec/`, or
   `src/cdy/spec/` beside `candy-special.md`?
   *Proposed:* `spec/`: it is neither design history (`doc/`) nor the translator's input.
   *Answered (2026-10-23):* `spec/`. *Lasting.*
2. **`candy-special.md`:** migrate it into `spec/` and remove it (proposed), or keep it as
   a one-page summary that links into `spec/`? Either way `special.cdy`'s pointer to it
   moves to `spec/` (Migration, 4), which is a `bin` change (its copy in `bin/py/`).
   *Answered (2026-10-23):* migrate and remove it. Each spec file starts with its forms'
   grammar lines, so the one-page overview survives, spread over the files, with
   `spec/README.md` as the index. *Lasting.*
3. **`tst/cdy/` programs:** keep them as they are (proposed: whole, multi-module and
   translator-scale programs), or move the small ones into the spec?
   *Answered (2026-10-23):* move the six small one-feature programs (`lists`, `maps`,
   `strings`, `short_circuit`, `prelude`, `tup_match`) into the spec, each with its
   feature's migration, where they become its examples; keep the other twelve (the
   multi-file ones in `cdyc/`, and the whole programs: `read_sexpr`, `sums`, `loops`,
   `t1/`) as translator tests ("Test levels").
4. **`expect-error`:** a substring of the message (proposed, as the Python tables do
   today), or error codes (`E0012`) now?
   *Proposed:* substrings *for now*; codes after the MVP.
   *Answered (2026-10-23):* substrings, *for now* ("After the MVP", coded errors: if
   rewording messages starts breaking examples).
5. **Lifecycle:** per-file `status`/`since` with a feature tag for `since` (proposed);
   and is "the translator uses only stable features" a rule, or is the bootstrap chain's
   mechanical check enough?
   *Proposed:* the status line yes; the translator rule no (the chain enforces what
   matters), revisited if a draft feature gets into the translator.
   *Answered (2026-10-23):* the status line, per file, with `since:` a feature tag
   (*lasting*); no translator rule, the chain's check is enough (*for now*: revisit if a
   draft feature gets into the translator).
6. **The grammar:** an `00-syntax.md` in prose and examples, with the reader as the
   authority (proposed), or a `grammar.ebnf` checked by a parser generator?
   *Answered (2026-10-23):* `00-syntax.md`, with `candy run` examples and `candy errors`
   tables for what the reader rejects; the reader is the authority (*for now*: "After the
   MVP", a grammar file, when a second reader or a formal grammar is needed).
7. **A changelog:** none (proposed: CLAUDE.md's history and the tags are it), or
   `CHANGELOG.md` linking to spec sections?
   *Answered (2026-10-23):* none (*lasting*): CLAUDE.md's history, the feature tags and the
   HLDs are it, and the spec files' `since:` lines say which branch brought each feature
   (a "what changed" view could be generated from them).
8. **The branch:** its own branch after `runtime-names` (proposed)?
   *Answered (2026-10-23):* its own branch, `executable-spec`, after `runtime-names`, for
   this HLD only (this file renamed to match); reviews (`doc/hl_rqmt/review.md`) and test
   levels (question 11) stay separate, to build on the spec.
9. **Reviewing items and tasks:** part of this HLD, or an HLD of its own?
   *Answered (2026-10-23):* its own, `doc/hl_rqmt/review.md`, linked from here.
10. **Parallel tests:** add `pytest-xdist` (a test dependency) if the spec makes the suite
    slow?
    *Proposed:* not at first; batch `mypy` first and measure (step 1), and add it only if
    the suite passes about a minute.
    *Answered (2026-10-23):* as proposed (*for now*).
11. **Test levels:** how unit, component (the translator) and system (the self-build and
    the chain) tests live beside the spec, and how each one's process is defined ("Test
    levels")? Open, no proposal yet: in this HLD, or a process HLD of its own?
    *Answered (2026-10-23):* a process HLD of its own, drafted later; "Test levels
    (open)" stays here until then, and points at it once it exists.
12. **The Python output in `expect` blocks** ("Pros and cons"): how does the spec avoid
    making Python's printing normative?
    - **A.** Examples print only numbers and text (built with `format`), never a raw
      list, `Bool`, `nil` or record.
    - **B.** A built-in that shows a value in Candy's syntax (`true`, `nil`, `(1 2 3)`),
      used by the examples; a small language change, and what a second target needs.
    - **C.** Both: A now, B later (in "After the MVP").
    *Proposed:* C.
    *Answered (2026-10-23):* C. A *for now*; B waits for the I/O refactor the owner
    expects (I/O as a whole is weak today: `doc/brainstorm.md`, "An I/O refactor"), and
    the examples switch to it then.
