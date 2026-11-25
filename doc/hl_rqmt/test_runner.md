# The spec's runner in Candy (HLD)

**Status: accepted (2026-11-25), with the answers to its questions, as proposed (tasks
[[B233]] to [[B237]]); for branch `test-runner`. Epic:
`python_complete.md` (its eighth branch). After tag `host-macros`.** The spec's runner,
which reads a spec file's examples and checks each one, written in Candy, a module of the
translator: it runs each example on the interpreter, or translates it, and reports by
`file:line`. pytest calls it, and keeps what is about Python (the translated example run
as a Python program, `mypy --strict`, T1 and T2 agreeing). A new host then runs the
conformance suite with the translator alone (`cdy_translator.py --spec FILE ...`), without
Python's test code.

## Where things stand

- **The runner is Python** (`tst/py_cdy/test_spec.py`, 300 lines; `executable_spec.md`,
  "The runner", *lasting while the translator could break it*): it reads the fences of
  `spec/*.md` and of the backlog's items with `script/doc_links.py`'s `blocks`, pairs them
  into examples (`examples`, `error_table`), and makes one pytest case per example, named
  `file:line`. 549 tests, 30 s:
  - **`run`** (86): translated by T1 and run as a Python program (a process each), and run
    on T1's interpreter in pytest's process; the output must be the `expect` block;
  - **`panic`** (9): the same, the panic's message must hold the `expect-panic` text;
  - **`error`** (325, the `candy errors` tables' rows most of them): translating must
    fail, the message holding the `expect-error` text;
  - **`setup`** (4): an error table's setup must translate;
  - **per file** (9 each): the `run` examples pass `mypy --strict` together, and T2
    translates them as T1 does.

  A `status: draft` file's tests may fail; a backlog item's repro must (strict).
- **What it needs from Candy, and has:** the interpreter (`interpret-text`, in-process;
  `interpreter`), the translator in-process (`translate-text`), the `string` module
  (`stdlib`). What it lacks: a way to catch a panic. `fail` is a panic, which Candy can't
  catch, *lasting* ([[library.errors]], [[B39]]): an `error` example's whole point is the
  translator's panic, and pytest catches it as Python's `CandyFail`. [[B139]] (a
  `catch-panic` for tools) is the idea filed for this branch. And a way to see what an
  example wrote: the interpreter writes to the host's stdout, which pytest captures.
- **The test module** (`test.cdy`, `stdlib`): `deftest`, `check`, `test.run`, for a
  program's own tests. The spec's examples aren't that kind of test: each is a whole
  program, compared with text.
- **Fences elsewhere:** `test_doc_links.py` reads the spec's fences too, with the same
  `blocks`, to check that each example belongs to a rule and each stable rule has one.

## Goals

- **The spec's runner in Candy** (the epic's "Testing in Candy"; its Question 8): reading
  a spec file's examples (fences, pairs, error tables with their setup, the status line)
  and checking each one, the Candy implementation's checks: `run` and `panic` on the
  interpreter, `error` and `setup` through the translator, each in-process. Its errors
  (an `expect` with no example before it, a bad table row) as today's, by `file:line`.
- **One reader:** pytest takes the examples from the Candy reader for what it still
  checks (the Python target's run, mypy, T2), so `test_spec.py`'s `examples` and
  `error_table` go.
- **Run without pytest:** `cdy_translator.py --spec FILE ...` checks spec files and
  backlog items, writes each failure as `file:line: ...` and a count, and exits non-zero
  on a failure: the conformance suite, for a new host.
- **Panics caught, for tools only:** a translator built-in, `catch-panic` ([[B139]]), so
  the runner can check an `error` or `panic` example in-process; a program can't import
  it (it is `translator.cdy`'s), so a panic stays uncatchable for programs, *lasting*.
  *Corrected in step 1:* a program can `(import translator)`, so it can reach
  `catch-panic` by importing the translator's module on purpose; the module's comments
  and [[library.builtins]] say it is for tools, not a program's logic.

## Not goals

- **The test programs** (`tst/cdy/`, `NAME.cdy` against `NAME.out`) and the fixpoint stay
  in `test_self_host.py`; the links' and the backlog's checks in Python (the epic's
  Question 8: the rest when a second host needs it).
- **The Python target's checks** stay pytest's: running the translated example as a
  process, `mypy --strict`, T1 and T2 agreeing. They are about Python.
- **The runner on the interpreter:** it runs translated, as part of the translator. On
  the interpreter it would interpret the translator's front end for every example
  (`interpreter.md`'s Question 1 declined the translator on the interpreter).
- **Multi-module examples:** still `tst/cdy/cdyc/`'s (`executable_spec.md`, question 3).
- **Fences for `test_doc_links.py`:** its Python reader stays (Question 6).

## Proposal

### The module

`src/cdy/spec_runner.cdy`, a module of the translator. It can't import `cdyc.cdy`, which
imports it for the flag, so `cdyc.cdy` hands it what it runs, as it hands the expander
its loaders: a function that translates a text and one that interprets it. Its parts:

- **The reader:** `examples text name` gives the file's examples, each an `Example`
  record (kind, source, expected text, line), or fails with `name:line: ...` for blocks
  that don't pair up, the messages `test_spec.py` has today. Fences as `doc_links.py`
  reads them: three or more backticks, closed by as many or more, an indented fence's
  lines losing its indent; and the `status:` line. Lines and their starts are `string`'s
  work (`split`, `trim`, `slice`); no regular expressions, which Candy dropped.
- **The checks:** `check-example run-text interpret-text ex` gives `None`, or `(Some
  msg)`, what went wrong:
  - `run`: interpreted, its output captured, no panic, the output the expected text;
  - `panic`: interpreted, a panic whose message holds the expected text;
  - `error`: translated, a panic whose message holds the expected text;
  - `setup`: translated, no panic.
- **The report:** `check-file path` gives the failures, each `file:line: kind: what`
  (for `run`, the expected and the actual output). The flag writes them and the count:
  `spec: 424 examples, 0 failed`.

### Catching a panic and capturing output

Two translator built-ins, declared in `translator.cdy`, each a few lines of the runtime
(`primitives.py`), and the porting surface's for a host (Question 2):

```candy
;; f applied to nil: (Ok v), or (Err msg) if it panicked, with the panic's message
;; (B139). For tools that check the translator or run examples; not for programs.
(sig catch-panic (Fn ((Fn (Unit) a)) (Result a String)))
;; f applied to nil, and what it wrote to the standard output meanwhile.
(sig capture-output (Fn ((Fn (Unit) a)) (Tup a String)))
```

In Python, `catch-panic` is `try`/`except` on `CandyFail` and `IndexError` (what
`stop_on_panic` treats as a panic; anything else is a bug and still raises), and
`capture-output` is `contextlib.redirect_stdout`. Both work on the interpreter's
examples as on the translator's own panics, since the interpreter runs in the host's
process and its `put-line` is the host's.

### pytest

`test_spec.py` keeps its file and its marks, with fewer tests (Question 4):

- **`test_candy`**, one per spec file and per backlog item with a repro: the Candy
  runner's `check-file`, which must give no failures (a draft file's may; a backlog
  item's must, strictly). The failures are its message, each `file:line`, so a failure
  still points at its example.
- **`test_python_run`** and **`test_python_panic`**, one per file: each example from the
  Candy reader translated by T1 and run as a process, as `test_run` and `test_panic` do.
- **`test_mypy_strict`** and **`test_t1_and_t2_agree`**, per file, as now, over the
  Candy reader's examples.
- **The reader's own tests** (`test_examples_pair_up` and the others): calls of the
  Candy reader, as `test_interp.py` calls the interpreter.

Nine files and 14 items with repros, a few tests each in place of 549; the work is the
same, so the time should be about today's 30 s (step 4 measures it).

## Pros and cons

- **For:** the conformance suite is Candy, run by the translator, so a new host gets it
  with the translator; one reader of examples, not one per language; [[B139]] closes,
  narrow and for tools; the runner is a second large program in Candy that isn't the
  translator, written against the `string` module.
- **Against:** pytest's per-example tests become per-file ones, so `pytest -k
  10-programs.md:123` no longer selects one example (the flag can check one file, and a
  failure's message names each example); two host built-ins more; a panic can be
  caught, by tools, a door the semantics HLD closed for programs.
- **Why now:** the interpreter, the `string` module and `Result` are built, the three
  things the epic said the runner waits for.

## Bootstrap

Step 1 adds two built-ins, as `host-macros` step 6a added one: the `bin` before reads
the step's `translator.cdy` and checks it against the live `spelling.py`, which both
declare them, so no staging. The other steps are translator code in the language `bin`
reads.

## Steps

1. **`catch-panic` and `capture-output`** ([[B139]]): `translator.cdy`, `spelling.py`,
   `primitives.py`, with the runtime's tests; [[library.builtins]] (the translator's
   seven).
   *Done (2026-11-25). As built:* the runtime can't build the prelude's `Result` (its
   `Ok` is a class of the translated program, and the runtime depends on itself only),
   so the host part is `run-caught`, `(Fn ((Fn (Unit) a)) (Tup (List a) String))`,
   `f`'s value in a list of one and `""`, or no value and the panic's message (Python's
   `run_caught`: `CandyFail` and `IndexError`, as `stop_on_panic` takes them; any other
   error raises); `catch-panic` is Candy over it in `translator.cdy`, which imports
   `prelude`'s `Result`, `Ok` and `Err` (a declaration module gets no prelude
   implicitly). `capture-output` is `contextlib.redirect_stdout`. So the translator's
   built-ins are seven, with `catch-panic` Candy ([[library.builtins]],
   [[programs.shadowing]], CLAUDE.md); and only `module-dir` is typed `Any` now
   ([[library.builtins]] still said three). A program can import `translator`, so
   "a program can't import it" (Goals) was wrong: corrected there. Tests:
   `test_run_caught` and `test_capture_output` (the runtime's), `test_catch_panic`
   (through T1). No staging, as planned. `bin` gains `catch-panic`'s Python (9 lines);
   checked against `boot/103`'s `bin`: the same output for all 109 programs.
2. **The reader:** `spec_runner.cdy`'s `examples` and the status line; the reader's tests
   ported to call it.
3. **The checks and the flag:** `check-example`, `check-file`, `--spec FILE ...` in
   `cdyc.cdy`'s `main` (its usage too); every spec file and repro checked by it, with
   the same results as `test_spec.py`'s.
4. **pytest on the Candy runner:** `test_spec.py` as above, `examples` and `error_table`
   gone; the time compared.
5. **Docs:** `executable_spec.md`'s "The runner" (its *lasting* answered),
   `spec/README.md` (how to run the spec), CLAUDE.md (the layout, the runner), the
   epic's eighth branch *done*; "Looking back".

## Questions

1. **Scope:** the spec's runner and the backlog's repros in Candy, the Python target's
   checks left to pytest (proposed); or the test programs too (`tst/cdy/`, their `.out`
   files), which the epic's Question 8 left for a second host; or the Python target's
   run too, the runner starting a process per example (a host built-in to run a
   process). **Proposed: the spec and the repros only:** the test programs are about
   whole programs and the fixpoint, mostly Python's business, and a process built-in is
   more porting surface for a check that is Python's anyway.
   *Answer (2026-11-25, the owner): the spec and the repros only.*
2. **Catching a panic:** `catch-panic` in `translator.cdy`, for tools (proposed); or in
   `system.cdy`, every program's (a panic then catchable everywhere, against the
   semantics HLD's Question 11); or no catch, a process per `error` example (325
   processes of about 0.14 s each, about 45 s more, and a process built-in).
   **Proposed: `translator.cdy`:** a program can't see it, so the rule for programs
   stays, and it is the shape Rust's `catch_unwind` has, for a later host.
   *Answer (2026-11-25, the owner): `catch-panic` in `translator.cdy`, for tools.*
3. **Capturing output:** `capture-output`, the host's stdout redirected (proposed); or
   the interpreter writing to a buffer it hands back, every output built-in's
   interpreter function changed to thread it, pure but a rewrite of its table's I/O.
   **Proposed: `capture-output`:** one host line, and the interpreter unchanged.
   *Answer (2026-11-25, the owner): `capture-output`.*
4. **pytest's tests:** per file, the Candy runner's failures as the message (proposed);
   or per example, as now, which needs the examples at collection time, before T1 is
   built (the checked-in `bin`'s reader, then, one build behind). **Proposed: per
   file:** the message names each failing example by `file:line`, and the flag checks
   one file on its own.
   *Answer (2026-11-25, the owner): per file.*
5. **Where it lives:** a module of the translator, `spec_runner.cdy`, run by a flag
   (proposed); or a program of its own that imports the translator's modules, with its
   own `bin`. **Proposed: a module and a flag,** as `--interpret` is: one program, one
   `bin`.
   *Answer (2026-11-25, the owner): a module, `src/cdy/spec_runner.cdy`, and a flag.*
6. **Fences in two readers:** `test_doc_links.py` keeps `doc_links.py`'s `blocks` for
   its checks of rules and links (proposed); or it calls the Candy reader too, needing
   T1 where today it needs nothing built. **Proposed: keep it:** those checks are about
   the docs, which the epic's Question 8 left in Python, and `blocks` is 20 lines.
   *Answer (2026-11-25, the owner): keep `doc_links.py`'s reader.*
