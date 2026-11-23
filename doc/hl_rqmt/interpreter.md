# The interpreter (HLD)

**Status: accepted (2026-11-21), with the answers to its questions, as proposed (tasks
[[B218]] to [[B223]]); for branch `interpreter`. Epic: `python_complete.md` (its sixth
branch). After tag `stdlib`.** A tree-walking
interpreter over typed Core, written in Candy, with values of its own: the second
implementation, so the spec's examples run on two and their output is compared
(the epic's exit test, its first part; [[B101]]). It is also what `host-macros` will
run macros on ([[B41]]), and a REPL's start; neither is this branch's.

## Where things stand

- **One implementation.** A program is read, expanded, analysed into Core, checked,
  then lowered and written as Python (`cdyc.cdy`: `analyse-program`, `type-check`,
  `check-order`, `lower-program`, `python-of`). Everything a program means at run time
  is what the Python it becomes does, with `cdy_rt`'s primitives under it.
- **Typed Core** (`typed_core.md`): after the check every `Expr` has its type and a
  position. Core is small: 15 kinds of expression (`Lit`, `Local`, `Global`, `Prim`,
  `Call`, `If`, `Do`, `Lambda`, `Tuple`, `ListOf`, `Fmt`, `Field`, `Assoc`, `MatchE`,
  `Temp`, the last `lower`'s only) and 5 of top-level form (`TDeft`, `TDeftSum`, `TDef`,
  `TDefn`, `TExpr`). `let` is already an applied `Lambda`, `cond` a macro, so nothing
  else reaches it.
- **The spec** (`spec/`) has 84 `candy run` examples and 8 `candy panic` ones, each run
  by `test_spec.py` through T1 and a Python process; the `candy error` ones fail in the
  front end, before anything runs. `tst/cdy/` has the test programs, whole programs
  (modules, `main` with arguments, macro files, the translator's own internals).
- **The built-ins** are declared in `system.cdy`, `math.cdy`, `string.cdy`, `map.cdy`
  (and `translator.cdy`, the translator's only): 75 for programs, each specified in
  `spec/60-library.md`, each spelled for Python in `spelling.py`. That list is the
  porting surface a second implementation must cover.
- **Recursion:** a `defn` calling itself in tail position runs as a loop
  ([[expr.tail-calls]]); other recursion uses the host's stack, about 1000 calls deep
  ([[B37]]).

## Goals

- **The spec runs on two implementations:** every `candy run` example prints its
  `expect` on the interpreter too, and every `candy panic` one panics with its text.
  A difference is a gap in the spec or a bug in one of them, fixed in the branch or
  filed.
- **Written from the spec:** what a program means (equality, `show` and `text`,
  `format`, `match`, a call, a closure, the bounds of `at` and `slice`, `main`'s exit)
  is the interpreter's own Candy, not the Python target's; only leaf work on host data
  (a string's characters, a number's arithmetic, a file) is handed to the host's
  built-ins, as the epic said ("The interpreter").
- **Every built-in, checked:** a table of the interpreter's built-ins, checked against
  the declarations both ways, as `spelling.py` is: the porting surface, counted.
- **Runnable by hand:** the driver interprets a file (Question 2).

## Not goals

- **Macros on the interpreter,** the prelude for macro code, macro results checked:
  `host-macros` ([[B41]], [[B52]], [[B42]]).
- **The spec's runner in Candy:** `test-runner`. pytest drives both implementations.
- **A REPL,** an expression at a time: it comes nearly free after this, but needs a
  reader loop and a scope that grows; later ([[B101]]'s REPL-style examples too).
- **Speed:** the examples are small, and the translator stays compiled. It isn't meant
  to run the translator, and would be of little use if it were fast: it runs only where
  the compiled translator already does. Its parts are another matter ([[B217]]).
- **Changing the language.** Where the two disagree, the spec says which is right; the
  fix may be either implementation's, or a sentence of the spec.

## Proposal

### Where it lives

A module of the translator, `src/cdy/interp.cdy` (the evaluator and the values) and
`src/cdy/interp_builtins.cdy` (the built-ins), imported by `cdyc.cdy`: the same front
end (read, expand, analyse, check, `check-order`), then `interpret` in place of `lower`
and `emit` (Question 5). It is Candy, so `bin` builds it and it runs wherever the
translator does; on Python it is the translator's Python.

### Values

Its own sum, as the epic proposed ("The interpreter"), so nothing of Python's
representation leaks in by accident:

```
(deft Value
  (VInt ((n Int))) (VLong ((n Long))) (VByte ((n Byte)))
  (VFloat ((x Float))) (VDouble ((x Double)))
  (VBool ((b Bool))) (VChar ((c Char))) (VStr ((s String))) (VUnit)
  (VList ((items (List Value)))) (VTup ((items (List Value))))
  (VMap ((m (Map Value Value))))
  (VRec ((module String) (name String) (fields (List Value))))  ; a record or variant
  (VFn ((params (List Expr)) (body Expr) (env Env) (name String)))  ; a closure
  (VPrim ((key String))))                                       ; a built-in as a value
```

Each size of number is its own variant, so `show` can write `1500l` from the value
(Question 3). A record and a variant are one kind, named by their module and name, so
`=` by structure and class ([[expr.equality]]) is the host's equality on `Value`s.

### Evaluation

- **An environment:** locals by their Core `id` (every `Local` has one, unique in its
  definition), a `(Map Int Value)`; globals by `global-key` (`util.greet`), filled from
  the top-level forms in order before any runs, a `defn` as a `VFn` with no
  environment, which looks its globals up when it is called. A `def`'s value is
  computed in order ([[programs.def-order]] has checked it can be).
- **`eval`** over each `Expr`: a literal to its value; a `Call` evaluates the callee and
  the arguments, then applies: a `VFn` binds its parameters (a rest parameter takes the
  rest, as a `VList`) and evaluates its body, a `VPrim` calls the built-in; `If`, `Do`,
  `Lambda` (a `VFn` closing over the environment), `Tuple`, `ListOf`, `Fmt` (each hole
  as `text` writes it), `Field` and `Assoc` (by the field's index, from the `TDeft`'s
  fields), `MatchE` (the first clause whose variant is the value's, binding its fields,
  else the default; exhaustiveness was checked).
- **Operators** are built-ins like any other, with their rest parameters: `(+ 1 2 3)`
  folds left, a comparison chains, `and` and `or` short-circuit (so they are evaluated,
  not applied).
- **Tail calls:** a `defn` calling itself in tail position must run as a loop
  ([[expr.tail-calls]]). `apply` runs a body that ends in a self call by rebinding and
  going round (a tail-recursive Candy `defn`, which `lower` makes a loop on Python), so
  `(count 100000 0)` runs. Other recursion is deeper in the host's stack than on the
  Python target, a few Python frames per Candy call (Question 4).
- **Panics:** `fail`, an index out of range, a file that can't be read: the
  interpreter's built-in fails with the spec's message, the same `candy: msg` and exit
  status 1 as a translated program ([[library.errors]]).
- **`main`:** if the program defines it, it is called with the arguments after the
  others run, and the driver exits with its result ([[programs.main]]).

### The built-ins

A table, built-in key (`len`, `string.split`, `math.sin`) to a Candy function from the
argument `Value`s to a `Value`, checked both ways against the declared built-ins (all
but `translator`'s). Most unwrap, call the host's built-in of the same name and wrap:
`(VInt (string.len (str-of a)))`. Written from the spec rather than handed over
(Question 7):

- **`=` and `!=`** on `Value`s, and `<` and its kin on the comparable ones;
- **`show` and `text`,** by the value ([[library.show]]): a literal as its literal, a
  list, tuple or map by its constructor, a record or variant by its name, with the
  host's `show` only for a float's digits;
- **`at` and `slice`,** with their bounds, and `string.at` and `string.slice`
  ([[library.bounds]]), so the panics' messages are the interpreter's;
- **the ones that take a function** (`map`, `filter`, `fold`, `map-acc`, `any`, `all`,
  `find-index`): their loops over a `VList`, applying the `VFn`.

### How the tests run it

`test_spec.py` gets `test_interpret` beside `test_run`, and `test_interpret_panic`
beside `test_panic`: each example's source through T1's front end and its interpreter,
in the test's own process (`candy(t1, "interp.run-source")`, its output captured), no
Python file and no process each (Question 6). An example the interpreter can't run yet
is a strict expected failure, with a backlog item, until it can: none at the branch's
end. The 16 test programs (`tst/cdy/`) run on it too, each to its `.out` (Question 1):
a program's macros are expanded in the front end, before the interpreter sees it, so
`import-macros` is no obstacle, and none of them reaches the translator's internals
(those are `test_self_host.py`'s Python tests).

### The spec

No rule changes by design; `spec/README.md` says every example runs on both. Each
difference found is fixed where it is wrong, and where the spec was silent it gets the
sentence, in the step that finds it.

## Pros and cons

- **For:** the spec gets a second reader, which is the only test that it says enough;
  the porting surface is counted, not estimated; `host-macros` gets what it runs on;
  it is written once, against a language the five branches before it settled.
- **Against:** a second implementation is a second place to change for every language
  change after it; it duplicates what the built-ins mean, on purpose; it is slow, which
  doesn't matter at the examples' size but rules out running the translator on it.
- **Why now:** the language changes are done (`semantics` to `stdlib`), Core is typed,
  and `host-macros` waits on it.

## Bootstrap

New translator code in the language `bin` already reads, no new built-in: no staging.
`bin` grows by the interpreter's Python.

## Steps

1. **Values and the evaluator:** `Value`, the environment, `eval` and `apply` for every
   Core expression and top-level form, `main`; the built-ins only `put` and the
   operators need; the driver's way in (Question 2); a first test.
   *Done (2026-11-21). As built:* `interp.cdy`, imported by `cdyc.cdy`: `Value` as
   proposed, but a `Long` and a `Byte` hold an `Int`, and a `Float` a `Double`, as a
   literal form does (`form.cdy`), since Candy has no conversion between the number
   types ([[B22]]); a `VCtor` for every record and variant, a fieldless one too, since
   Core writes `Dot` as a call with no arguments; and a `Ctx` of the globals and the
   built-ins. `interpret` runs the top-level forms in order, then `main`; `eval` covers
   every `Expr` (a `Temp` an internal error), an applied `fn` bound where it is, `and`
   and `or` short-circuit. The built-ins so far are those `put` and the operators need,
   with `at` (a `Tup` pattern's, so it takes a tuple too), `len` and `fold`; each takes
   the function that applies a value, for the ones that call one. The flag:
   `cdy_translator.py --interpret FILE [ARGS]` (`interpret-file`), and `main.py FILE
   --interpret`. Tests: `test_interp.py` (a program of every kind of expression and
   form, in-process, by the flag and against the Python target), `test_main.py`'s
   `test_main_interpret`. A `Do` folded from `VUnit` failed T2's `mypy --strict`, the
   start typed as that variant alone: [[B184]]'s mechanism, noted there, and avoided.
   Checked against `boot/92`'s `bin`: the same output for all 108 programs. `bin` grows
   from 7707 lines to 8398, and the translator translates itself in 1.0 s, from 0.86 s,
   for the interpreter's own lines. No staging.
2. **The built-ins:** every one, its table checked against the declarations both ways;
   `=`, ordering, `show`, `text`, bounds written from the spec.
   *Done (2026-11-21). As built:* `interp_builtins.cdy`, its table `BUILTINS`: 71
   functions, every one a declaration module declares but `translator`'s; with the four
   values interp.cdy's `prim-value` gives (`nil`, `empty-list`, `map.empty`, `math.PI`),
   the 75. `check-interp-builtins` checks it against the declared ones both ways, on
   every run, as the spellings are. Written from the spec: `=` and `!=` (the host's
   equality on `Value`s, so by structure and class), the comparisons (`compare`),
   `show` and `text` by the value (the host's `show` only for a float's digits; a
   string's escapes, a control character's `\u`, in Candy), the bounds of `at`, `slice`,
   `string.at` and `string.slice`, with the spec's messages, and the loops of `map`,
   `filter`, `fold`, `map-acc`, `any`, `all` and `find-index`. The rest unwrap and call
   the host's built-in of the same name. The driver hands the table to `interpret`, so
   neither module imports the other; a format hole is the table's `text`. `interpret-text`
   runs Candy text, as `translate-text` translates it, for the tests. Tests:
   `test_every_declared_builtin_is_interpreted` (both ways),
   `test_show_and_text_agree_with_the_python_target`. Run in-process, the spec's 94 `run`
   and `panic` examples agree but two, `expr.tail-calls`' and `list.sort`'s 500 items,
   which recurse past the host's stack: step 3's. Checked against `boot/93`'s `bin`: the
   same output for all 108 programs. No staging.
3. **Tail calls and panics:** self tail calls as a loop; the panics' messages and exit
   status as a translated program's.
   *Done (2026-11-22). As built:* a trampoline: `eval-tail` evaluates a function's body
   in tail position (an `if`'s branches, a `do`'s last form, a `let`'s body, a clause's
   body; `choose-clause` shared with `eval-match`), giving its value (`Done`) or the
   call it ends in, still to make (`Again`), and `apply` goes round again on that, a
   self tail call that `lower` makes a Python loop. So every tail call runs as a loop,
   mutual ones too, more than [[expr.tail-calls]] promises. Other recursion goes 138
   calls deep (about seven Python frames a call), against about 1000 on the Python
   target; the rule now says the depth is an implementation's (Question 4), and
   [[B37]] has a note. Past it, both stop with Python's traceback ([[B160]]). The panics
   needed nothing new: `fail` and the interpreter's own bounds raise the host's panic,
   which the translator's `main` writes as `candy: msg`, exiting with 1. Tests:
   `test_interpret_tail_calls` (a self, a mutual and a `match` clause's tail call),
   `test_interpret_panics` (`fail`, an index out of range, by the flag). In-process,
   all 94 of the spec's `run` and `panic` examples agree. Checked against `boot/94`'s
   `bin`: the same output for all 108 programs. No staging.
4. **The spec on both:** `test_interpret` and `test_interpret_panic`; each difference
   fixed, or filed and marked.
   *Done (2026-11-22). As built:* `test_spec.py`'s `test_interpret` and
   `test_interpret_panic`, one test per `candy run` and `candy panic` example, through
   T1's `interpret-text` in pytest's process (its output captured, a panic caught and
   written `candy: msg`), with the same marks as the translated runs: all 94 pass, in
   about 4 s, with no difference to fix or file; steps 2 and 3 had found the two there
   were. The backlog's repros are all `candy error`, the front end's, so none runs on
   the interpreter; one for a Python-target defect would pass there and fail as a strict
   expected failure, a difference to decide (`test_spec.py`'s docstring).
   `spec/README.md` says every `run` and `panic` example runs on both. No translator
   change, so no `boot/NN`.
5. **The test programs on both:** all 16 (Question 1).
6. **Docs:** CLAUDE.md ("How the translator works"), `spec/README.md`, the epic's sixth
   branch *done*, `multi_target.md` (the porting surface counted); "Looking back".

## After the MVP

- **Parts of the translator on the interpreter** ([[B217]]; the owner, 2026-11-21): not
  the whole translator, which takes minutes on a tree-walker and, even fast, runs only
  where the compiled one already does, but one module or function at a time, run when a
  change needs it, its result compared with the compiled one's. The reader (`read.cdy`'s
  `read-forms`) on every spec file's examples, `syntax.cdy`'s shape check, `check.cdy`'s
  unification on the test programs' types: each a large, real program the examples are
  not, at the cost of one part's run. It needs a way to call one interpreted function from
  a test (`interp.call`, a global by its key, with `Value`s in and out), and the
  translator's modules kept small enough to load on their own, which `namespaces` began.
  `host-macros` gets some of it anyway: macro code runs on the interpreter, with
  `form.cdy`'s functions.

## Questions

1. **Scope:** the spec's `run` and `panic` examples on both, and the 16 test programs
   (proposed); or the spec only, as the exit test says; or the translator too,
   interpreting itself? **Proposed: the spec and the test programs**: the programs are
   whole things (modules, `main`), which the examples don't cover; the translator would
   take minutes, for little the programs don't test.
   *Answer (2026-11-21, the owner): the spec and the test programs; not the translator*,
   though parts of it, run when needed, are a note for later ("After the MVP").
2. **How a person runs it:** a flag on the translator, `cdy_translator.py --interpret
   FILE [ARGS]`, and `main.py FILE --interpret` (proposed); or a second program,
   `cdy_interp.py`, built from its own top file? **Proposed: a flag,** one program, one
   `bin`, the front end shared.
   *Answer (2026-11-21, the owner): a flag.*
3. **`show` by the value or by the static type:** the Python target shows by the type,
   which typed Core has for the interpreter too; but the interpreter's values know
   their type, the sizes of number included. **Proposed: by the value,** which is
   simpler and agrees with the type wherever the type is known; they differ only for a
   value typed `Any`, where the Python target can't tell `1` from `1l` ([[B18]]): an
   example of that runs on the Python target only, marked so, *for now*.
   *Answer (2026-11-21, the owner): as proposed.*
4. **Recursion beyond tail calls:** the interpreter uses a few host frames per Candy
   call, so it runs out sooner than 1000 calls; accept it (proposed: the spec says
   "about 1000", *for now* [[B37]], and no example goes near), or raise Python's limit
   (a host setting, through a new built-in)? **Proposed: accept it,** and say in
   [[expr.tail-calls]] that the depth is an implementation's.
   *Answer (2026-11-21, the owner): as proposed.*
5. **Where it lives:** a module of the translator (proposed), or its own program, which
   imports the front end's modules? **Proposed: a module,** run by the driver: `bin`
   stays one file, and the front end is the translator's anyway.
   *Answer (2026-11-21, the owner): as proposed.*
6. **How the tests run it:** in pytest's process, through T1's module (proposed: fast,
   92 examples with no Python process each, as `test_self_host.py` reaches internals);
   or a process each, as `test_run` does (closer to a person's run, but slower)?
   **Proposed: in-process,** with one test that runs the driver's flag in a process.
   *Answer (2026-11-21, the owner): as proposed.*
7. **What is written from the spec, what handed to the host:** the list above
   (equality, ordering, `show`, `text`, bounds, the higher-order built-ins), the rest
   unwrapped and handed to the built-in of the same name (proposed); or more of it in
   Candy (`string.split` over characters, `math.sin` as a series); or less (equality
   and `show` handed over too)? **Proposed: as listed:** what the spec specifies beyond
   the host's word is written, the leaf work isn't, so the interpreter tests the spec
   where it says something, and inherits the host where it defers to it ([[B160]]).
   *Answer (2026-11-21, the owner): as proposed.*
8. **Its name:** `interp` (proposed), `eval`, or `run`? **Proposed: `interp`**: `eval`
   names its central function, and `run` is too common a word for a module.
   *Answer (2026-11-21, the owner): as proposed.*
