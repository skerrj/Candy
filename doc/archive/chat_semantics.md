*Archived 2026-11-04, from the Claude Code session that built branch `semantics`
(2026-11-02 to 2026-11-04; HLD `doc/hl_rqmt/semantics.md`, tag `semantics`), by
`script/chat_archive.py`, before the merge.* The owner's messages and Claude's replies on
the branch, verbatim; each tool call is a one-line marker, and thinking and tool output
are left out. The HLD's proposal and questions were on `master`, earlier in the same
session (2026-11-01 to 2026-11-02), and aren't in this file. What came of it: steps 1 to
5, `show` and the constructors ([[B36]]), equality ([[B27]], [[B137]]), `Maybe` a sum
and missing values gone ([[B20]], [[B21]]), narrowing and field constraints ([[B121]],
[[B120]]); found on the way, [[B150]] to [[B156]]; from the review, the type-level leaks
(`multi_target.md`) and [[B133]]'s note; at the checkpoint, steps 6 to 9 moved to
`semantics-2`.

# semantics

## Claude Code

*ran: Read unify and the checker state*

*ran: Read unify and node-type*

*ran: Read the existing typed-node test*

*ran: Find test helpers for translating snippets*

I've started on `semantics` step 1. Now I'm reading the checker's `unify` and the test helpers, so I can add the `Any` defaulting and B132's tests.

*ran: Read the test imports and translate_with*

*ran: Read show, core_nodes and is-flexible*

*ran: Probe today's types for unsolved-variable cases*

*ran: Check how the substitution is used and how vars are named*

*ran: Check fold's signature and use*

Now the change in `check.cdy`: `unify` marks the variables `Any` meets, and `node-type` defaults a marked variable that is still unsolved to `Any`.

*ran: Add Any marking in unify and defaulting in node-type*

*ran: Build T1 and probe the defaulted types*

*ran: Count unsolved types in the translator's Core before and after*

All 8 unsolved types in the translator's own Core are gone (8 before, 0 after). Now B132's tests:

*ran: Add B132's tests and run them*

*ran: Show the failing assertion*

The prelude's `rest` also has a local `xs`, so I'll give the test's locals names no other code uses.

*ran: Rename the test's locals and rerun*

The tests pass. Now the spec: `checking.any`, plus the three items closed with no code change.

*ran: Read the four spec rules step 1 changes*

*ran: Read B26, B28 and B80*

*ran: Check today's errors for and/or, Char and redefining a def*

*ran: Write step 1's spec rules*

*ran: Check the inserted errors table*

*ran: See how a step recorded an item's fix*

I've written step 1's spec rules. Next is the backlog: typed-core had one task item per step, so I'll check how those were made before adding semantics' tasks.

*ran: Read a step task item and how they were created*

*ran: Look at typed-core's start commit*

*ran: Read the process's branch-start and step rules*

The process's branch start adds a task item per step and puts the branch in the HLD's status, and it may include step 1. So I'll add tasks B140–B149 now.

*ran: Add a task item for each of semantics' ten steps*

Step 1's task goes to `review`. The four items it fixes close as `done`, which is what the process says for a step's own fixes.

*ran: Move step 1's task to review and close its items*

*ran: Read the def-constant open question*

*ran: Find where 20-types says def constancy is open*

*ran: Read the types.sig paragraph on def*

`spec/20-types.md:83` still says a `def`'s constancy is undefined. I'll update it to match, and answer the open question in `mutation_optimization.md`.

*ran: Update types.sig and the mutation doc for B80*

*ran: Fix the mutation doc's bullet heading and read the HLD's step 1*

*ran: Check the mutation doc bullet*

Now the HLD: the status line, and step 1's *Done* note.

*ran: See the format of a Done note*

*ran: Find typed-core's Done notes*

First, rebuild `bin` and run everything:

*ran: Rebuild bin with the new checker*

*ran: Look at what changed in the rebuilt bin*

The rest of the diff is temporary names renumbered. Now the full suite and the linters:

*ran: Run the full test suite*

*ran: Run the full test suite without xdist*

*ran: Run all the linters and type checkers*

Everything is clean: 502 passed, 6 expected failures, and all the linters pass. Now the HLD's status and step 1's *Done* note:

*ran: Write the status and step 1 Done note, rerun doc and spec tests*

I've created the `semantics` branch and built step 1. It's ready for review; nothing is committed. Everything passes: pytest (502 passed, 6 expected failures), ruff, mypy, pyright and pylint, and `bin` is rebuilt and reproduces itself.

**Branch start:**
- **The HLD's status** (`semantics.md:3`) now names the branch and its tasks.
- **Ten task items**, B140–B149, one per step. Each names its questions and the items it closes. B140, step 1's task, is in `review`.

**Step 1:**
- **`Any` defaulting** (`src/cdy/check.cdy`):
  - `unify` still binds nothing that `Any` meets, but `mark-any` now marks every unsolved variable it meets;
  - `node-type` uses a new `final-type`, which makes a marked variable that's still unsolved at the end `Any`;
  - a variable that's solved later keeps that later type, which is the precision Q13 asked for;
  - the marks sit in the substitution, under the key `any?4` for a variable named `?4`. Nothing iterates the substitution, so they can't be confused with bindings.
- **Effect on the translator:** its own Core had 8 unsolved types and now has 0. Its Python output is unchanged, apart from renumbered temporary names, because an unsolved variable was already written as `Any`.
- **B132's tests** (`tst/py_cdy/test_self_host.py`): `test_unsolved_types` has four cases:

  | case | type in Core |
  |---|---|
  | met `Any` | `(List Any)` |
  | met `Any`, then `Int` | `(Fn (Int) Int)` |
  | a `fn` never called | stays a variable (Python `Any`) |
  | an `empty-list` never added to | stays a variable (Python `Any`) |

  Each case checks both the type in Core and the Python. `test_every_node_is_typed` now also checks that the translator's own Core has no unsolved variable.
- **Spec rules:**
  - `checking.any` (`spec/25-checking.md:273`): the defaulting. Its tests are the two above, since these types show up in Core and the Python, not in printed output.
  - `expr.logic` (`spec/40-expressions.md:81`): a `Bool` result, *lasting*, with an errors table. This closes B26.
  - `syntax.chars` (`spec/00-syntax.md:99`): a `Char` is its own type, with the error `=: expected Char, got String`. This closes B28.
  - `programs.top-level` (`spec/10-programs.md:16`): a `def` is a constant, with the error `defined more than once`. This closes B80.
- **Follow-on edits:** `types.sig` (`spec/20-types.md:83`) and open question 4 in `mutation_optimization.md:40` now say a `def` is a constant. The replaced text is kept verbatim in step 1's *Done* note (`semantics.md:271`).
- **Items:** B132, B26, B28 and B80 are `done`, `fixed: semantics`, each with a dated note.

On gawc I'll commit this as "Start branch semantics, step 1: …", then tag it `boot/48`.

## Owner

> gawc

## Claude Code

*ran: Check for owner edits and commit step 1*

*ran: Check the bootstrap step and tag boot/48*

I committed step 1 on `semantics` as `7c45a67`, "Start branch semantics, step 1: unsolved types, Any defaulted". All the files were mine; you hadn't edited any. The bootstrap step checks out (`ok 48`), and `boot/48` is an annotated tag on `7c45a67`. Nothing is pushed: `semantics` and `boot/48` exist only locally, and master is still two commits ahead of origin.

B140, step 1's task, is in `review`, ready for a tick. When you say go, I'll start step 2: the `List` and `Tup` constructors, and `show`. Step 2 begins by counting how many `format` holes and `put` arguments have a type that's still a variable. Q3 made showing those an error, and the `Any` defaulting should leave only a few.

## Owner

> go

## Claude Code

Step 2 is the biggest so far. First I'll look at how `tup`, the operators and their spellings fit together, to choose how `List` and `Tup` are built.

*ran: Read the special forms and spelling kinds*

*ran: Find every use of the Tuple node and the tup form*

*ran: Read the spelling kinds*

*ran: Read the number and string literal rules*

*ran: Read the special-form dispatch and an-tup*

*ran: Read the Tuple cases in check and lower*

*ran: Find every traversal over Core expressions*

*ran: Check how built-ins and built-in types share a map*

*ran: Read analyse-list and is-builtin-type*

*ran: Read is-special-head*

*ran: Add the List node and Tup alias through core, check and lower*

*ran: Build T1 and try the List and Tup constructors*

Exhaustive `match` caught `emit-expr`. `lower` turns every `ListOf` into a `Tuple`, but `emit` still has to name it:

*ran: Handle ListOf in emit and retry*

*ran: Read Pos, and how emit renders put and format*

*ran: Find put's spelling and emit's call rendering*

*ran: Read emit-call and Env*

*ran: Test class attributes in a NamedTuple under Python and mypy*

*ran: Show mypy's complaints about the metadata*

*ran: Read how emit writes record and variant classes*

*ran: Read candy-name, own-name and emit-record-fields*

*ran: Read emit-prim and how lower types its temporaries*

*ran: Read the two places lower types a temporary as Any*

*ran: Check how emit writes an assignment to a temporary*

*ran: Read lambda-annotation*

*ran: Keep the value's type on lower's temporaries, then survey primitives.py*

*ran: Read primitives.py's header and remaining definitions*

Now the runtime side, a new "showing values" section in `src/cdy_rt/primitives.py`:

*ran: Add show and its helpers to the runtime*

*ran: Try the runtime show on each built-in type*

The runtime `show` gives the expected output for every built-in type. Now `emit`. First I'll check how it refers to the runtime module:

*ran: See how emit names the runtime and what it imports*

Now the emit changes:

*ran: Make emit show values in put, format and show*

*ran: Fix emit-prim's shape and register each class*

The `register` binding landed outside the `let`'s bindings. Fixing the parentheses:

*ran: Fix the let in emit-variants and find where to declare show*

*ran: Declare show, build T1 and try printing every kind of value*

`bin` reads its own copy of `system.cdy`, which has no `show` yet, but it checks against the live `spelling.py`, which does. I'll look at how earlier branches added a built-in across this boundary:

*ran: Search the docs for how a new built-in is bootstrapped*

*ran: Read how a rebuild stages the library*

*ran: Read build_t1 and copy_library*

*ran: Put the new library next to bin, build T1 and run the show test*

T1 built. The test program's own `{"s"}` hole isn't allowed in a `format` string, so I'll fix the test:

*ran: Run the show test program and mypy on its Python*

The printing works, including recursive and generic types. mypy finds one error at `output/c.py:51`:

*ran: Look at the line mypy rejects*

*ran: Check whether the old print form had the same mypy error*

The old `print` form passes mypy, so `show`'s `value: object` parameter is what pushes mypy to solve the lambda's type as `object`. I'll make `show` generic in its value instead:

*ran: Make show generic and recheck with mypy*

Now the real test: the translator built with itself, since its own `format` holes now go through `emit-text`.

*ran: Rebuild bin through T1 and T2*

T1 and T2 write different code, so some `format` hole that feeds generated Python has a type other than `String` or `Int`. A diff will show which:

*ran: Diff T2 against T2's own translation*

The diff is Bool literals: `emit-lit` writes `{b}`, which used to give Python's `True` and now gives Candy's `true`. I'll check whether anything else differs:

*ran: Find differences other than Bool literals, and read emit-lit*

*ran: Spell Bool literals directly and rebuild bin*

The fixpoint holds, and the translator has no hole whose type is a type variable, so Q3's error never fires on it. I'll count what its holes and `put`s became:

*ran: Count show and text_any calls in the new bin*

*ran: Look at the translator's show and text_any calls*

*ran: Run the full suite and list failures*

*ran: Show the assertion details of four failures*

Two kinds of failure: expected outputs changing as decided (`1500l`, `3.14f`, `true`), and `put` wrapping an `Int` in `str()`, which `print` doesn't need. I'll fix the second:

*ran: Let put pass an Int as it is, rebuild and rerun*

Now the expected outputs. I'll diff each failing program's new output against its `.out` file:

*ran: Diff each failing program's new output against its expected output*

*ran: Read how test_output runs a program*

*ran: Rerun the programs from the repo root and diff again*

All as decided. `read_sexpr` prints values typed `Any`, so they go through the run-time show (B18's leak) and appear as `(List …)`. Updating the five `.out` files:

*ran: Update the expected outputs and look at the remaining failures*

*ran: Find the old expectations in the two tests and the spec example*

*ran: Read the two macro tests' expected text*

*ran: Update the macro-code output and the literals example, then rerun*

What's left is the `test_unsolved_types` program, which does `(put never-added)`. It will take `len` of it instead; the error itself goes in the spec as a `candy errors` row.

*ran: Change the test program to measure the empty list, and rerun*

That's the defaulting at work again: `len` is typed `Any`, so the list meets `Any` and becomes `(List Any)`. The test needs a use that doesn't meet `Any`, so `never-added` will just be evaluated:

*ran: Use the empty list without meeting Any, and rerun*

B132's tests pass. Next, step 2's spec rules. I'll check how `candy errors` rows are matched, since an unsolved type's number isn't predictable:

*ran: Check error matching, the README output rule and the library's list examples*

*ran: Read the rest of the lists example, the format rule and the file head*

Writing step 2's spec rules: `library.show`, `types.constructors`, the lists example on the built-in `show`, and the README's output rule removed.

*ran: Write library.show, update the lists example and the README*

Now `types.constructors` in `spec/20-types.md`, after Tuples, which now mentions `Tup`:

*ran: Write types.constructors and run the spec and doc-link tests*

That's my own example tripping Q3's rule: `(put … (List) …)` is an empty list whose type nothing fixes. I'll use `(rest (List 1))`, a `(List Int)`:

*ran: Fix the empty list in the show example and rerun*

The spec passes. A few more things for step 2: `checking.tup-lists`, which should say that `List` checks its items directly, and backlog items for the gaps I found along the way.

*ran: Read checking.tup-lists and B29*

*ran: Update checking.tup-lists for the List constructor*

*ran: Confirm the two show gaps*

*ran: Read B137 as a defect template*

*ran: File B150, B151 and B152 and run the backlog tests*

*ran: Rename B152's file to lowercase and rerun*

*ran: Show the collection error*

*ran: Use the expect-error fence in B150's repro and rerun*

I've filed B150–B152; B150's repro runs as an expected failure. Now the linters, then the HLD note and the items:

*ran: Run all the linters and type checkers*

*ran: List pyright's findings and any existing suppressions*

*ran: Restructure the runtime show as dispatch tables*

`show_any` still has too many returns for pylint, so it gets a table too:

*ran: Rerun the formatter, linters, mypy on generated code and the show test*

*ran: Drop the unneeded noqa comments and recheck*

Everything is clean. The runtime's `show` should also have unit tests, next to the other primitives' tests. I'll check that file's style:

*ran: Read the runtime test file's style*

*ran: Add unit tests for the runtime show*

*ran: Check the string case reads right and lint the test*

*ran: Sort the imports and run pylint over everything*

Clean. Now a final rebuild and the full suite:

*ran: Rebuild bin and run the full suite*

All green: 526 passed and 7 expected failures, with B150's repro the new one. Now the items and the HLD:

*ran: Read B36 and the HLD's step 2*

B36 also names `print` and `display`, which `system.cdy` declares beside `put`. I'll check what they're spelled as:

*ran: Check print and display's spellings and uses*

All three are Python's `print`, and nothing uses `print` or `display`. They should still print the same way, so `emit` will treat all three like `put`:

*ran: Make print and display write values as put does, then rebuild*

Now the items and step 2's *Done* note:

*ran: Write the items' notes and step 2's Done note, then rerun everything*

*ran: Run the linters once more and show the working tree*

Step 2 is built and ready for review; nothing is committed. Everything passes: pytest (526 passed, 7 expected failures), ruff, mypy, pyright and pylint, and `bin` is rebuilt and reproduces itself.

**What it does:**
- **Constructors.** `(List 1 2 3)` builds a list whose items must all have one type: `(List 1 "a")` gives `List: an item: expected Int, got String`. `(Tup 1 "a")` builds a tuple, and works as a pattern too. `tup` still works the same, *for now* (B152).
  - `List` and `Tup` couldn't go in `special.cdy`: both names are already built-in *types*, and types and special forms share one map. So `analyse-list` recognises them by name (`core.cdy`, `BUILTIN_CONSTRUCTORS`).
  - `(List …)` is a new Core node, `ListOf`. The checker types it, and `lower` turns it into a plain tuple, so `emit` never sees one.
- **`show`.** It's declared in `system.cdy`. `emit` writes the value's static type for the runtime, as in `show(x, ("List", "Int"))`, and the runtime's `show` (`src/cdy_rt/primitives.py`) does the printing. Each record and variant class is registered with the runtime after its definition, so generic and recursive types show correctly: `(Node Leaf 2 (Node Leaf 3 Leaf))`.
  - mypy doesn't allow attributes in a `NamedTuple`'s body, so a registry is the only place for this information.
  - Showing a function or a type variable is an error at translation, as Q3 decided. `Any` gets the run-time show.
- **`put`, `print`, `display` and `format` holes** write a `String` or `Char` as plain text, and show everything else. So `true` prints as `true`, `1500l` as `1500l`, and a `Maybe` as `(Some 7)` or `None` already.

**What the translator itself needed:**
- **No hole in the translator has a type-variable type,** so Q3's error never fires on it.
- **A real catch: Bool literals.** `emit-lit` wrote them through `(format "{v}")`, so the new `show` would have generated `return true`, which isn't Python. It now writes `True` and `False` directly. The old `bin` reads that the same way, so there's no two-step bootstrap.
- **`lower`'s temporaries** now keep their value's type. They used to be typed `Any`, which would have sent typed values to the run-time show.

**Outputs that changed, all as decided:** six test programs' `.out` files: `basics`, `forms_1b`, `read_sexpr`, `macro_files`, `macros` and `macro_code/quoting`. The spec's literals example (`spec/00-syntax.md:76`) now prints `1500l 1b` and `3.14f`.

**The spec:**
- **New rules:** `library.show` (`spec/60-library.md`, at the end), with error rows, and `types.constructors` (`spec/20-types.md`).
- **The lists example** (`spec/60-library.md:22`) now prints lists and Bools directly, so its own `show` and `yes` helpers are gone.
- **Smaller updates:** `types.tuples`, `checking.tup-lists` and `library.format`.
- **`spec/README.md`** drops "output is numbers and text".

All the replaced text is kept verbatim in step 2's *Done* note (`semantics.md:316`).

**New items:**
- **B150** (defect, low): a record with a function field fails when run, rather than being refused at translation. Its repro runs as an expected failure.
- **B151** (leak, low): a float with no Candy literal, such as `1e+20`, shows as Python writes it.
- **B152** (tech-debt, low): `tup` and `Tup` are two names for one form.

**Items:** B36 is `done`, and B141, step 2's task, is in `review`.

On gawc I'll commit "semantics step 2: show, and the List and Tup constructors", then tag it `boot/49`.

## Owner

> <command-name>/restart</command-name>
>             <command-message>restart</command-message>
>             <command-args></command-args>

## Owner

> Gawc

## Claude Code

*ran: Check the working tree for owner edits*

*ran: Commit step 2, check its bootstrap step and tag boot/49*

I committed step 2 on `semantics` as `8cd6893`, "semantics step 2: show, and the List and Tup constructors". It has the 29 files I described; you hadn't edited any. The bootstrap step checks out (`ok 49`, no staging), and `boot/49` is an annotated tag on `8cd6893`. Nothing is pushed: `semantics`, `boot/48` and `boot/49` are local only.

The commit message ends with the new session link (`session_01QJbqusdHWruz1tUURLuJKA`), since this session restarted under a new ID.

B140 and B141, the tasks for steps 1 and 2, are in `review`. When you say go, I'll start step 3, equality:
- every record and variant class compares its class too, which fixes B137;
- `=` on a function becomes an error;
- the new rule `expr.equality` goes in the spec.

B29 also overlaps with step 3. It covers records behaving as tuples, including equality, so I'll note it there.

## Owner

> Go

## Claude Code

Step 3, equality. I'll look at how the checker handles `=` first:

*ran: Read the checker's operator rule*

*ran: Add the class methods and the function check, then test them*

*ran: Show the mypy error on the equality test*

*ran: Check what the ordering operators accept today*

`<` takes records, lists and `Bool`s in Python's order, and `nil` only fails when run. I'll file that as a leak for later. Now the items and the spec:

*ran: Read B27, the rest of B29, and expr.comparisons*

*ran: Write expr.equality, file B153, and close or note the items*

The nested fences break the note: the repro's own ``` lines would close the `text` fence. I'll use a four-backtick fence, and add the missing blank line after `## Notes`:

*ran: Fix B137's note fences, rebuild bin and run the suite*

*ran: Find and fix Notes headings with no blank line after them*

That fixed eight files. Seven are mine from this branch. The eighth, B19, is from `typed-core`, and its fix is the same one-line formatting change.

Now step 3's *Done* note and the linters:

*ran: Write step 3's Done note and run the doc tests and linters*

Step 3 is built and ready for review; nothing is committed. Everything passes: pytest (529 passed, 6 expected failures), ruff, mypy, pyright and pylint, and `bin` is rebuilt and reproduces itself.

**What it does:**
- **Classes compare their class** (`src/cdy/emit.cdy`, `eq-methods`). Every record and variant class now has its own `__eq__`, `__ne__` and `__hash__`, which include the class. So `(= (A 1) (B 1))` is false, and the same holds wherever Python compares values: `contains`, `index-of`, and map keys. This fixes **B137**. A variant with no fields no longer needs `pass`.
- **Comparing a function is an error at the call** (`src/cdy/check.cdy`, `has-fn`), and so is comparing a type that holds one, such as a list of functions: `=: a function can't be compared, got (Fn (Int) Int)`. A function *inside a record* still isn't caught. That's the same gap as B150, so I added a note there.
- **New rule `expr.equality`** (`spec/40-expressions.md`, after `expr.comparisons`). It shows variants, records, lists, tuples, `0.0` against `-0.0`, a variant as a map key, and two error rows.

**Found along the way:**
- **B153** (leak, low): `<` and the other orderings accept any one type. Records and lists order like Python tuples, `false` comes before `true`, and `(< nil nil)` only fails when run.
- **A mypy false positive.** `(= (List (A 1)) (List (B 1)))`, written with literals, is rejected by mypy, which narrows each literal to its own class. Candy types both as `(List S)`. A typed value avoids it, so I left it as mypy's problem, since mypy is the second checker (B125).

**Items:**
- **Closed:** B27 and B137 are `done`. B137's repro is now the spec's `(= a (B 1))` example, and its old text is kept verbatim in B137's note, in a four-backtick fence so its own fences don't break it.
- **Notes:** B29 gets a note: the equality part is fixed, but the rest stays open. B150 gets the note about `=`.
- **B142**, step 3's task, is in `review`. The *Done* note is at `semantics.md:368`.

I also fixed a formatting slip from my note-writing helper. It had left no blank line after a new `## Notes` heading in eight items: seven from this branch, plus B19 from `typed-core`.

On gawc I'll commit "semantics step 3: equality", then tag it `boot/50`.

## Owner

> Gawc

## Claude Code

*ran: Commit step 3, check its bootstrap step and tag boot/50*

I committed step 3 on `semantics` as `967973b`, "semantics step 3: equality". It has the 18 files I described; you hadn't edited any. The bootstrap step checks out (`ok 50`), and `boot/50` is an annotated tag on `967973b`. Nothing is pushed: `semantics` and `boot/48` to `boot/50` are local only.

B140, B141 and B142, the tasks for steps 1 to 3, are in `review`. Step 4 is next: `Maybe` becomes a real sum, `Some` or `None`, in the prelude. The checker's special `Maybe` rules go, and an `if` without `else` is allowed only for `Unit`. It's the first step that changes programs the translator itself compiles, so it may need a two-step bootstrap. Say go when you want it.

## Owner

> Go

## Claude Code

Step 4 changes the most so far, so I'll survey first: where `Maybe`, `find`, `index-of`, `with-default` and `nil`-as-missing appear in the translator, and where the checker and `emit` special-case `Maybe`.

*ran: Survey Maybe and its built-ins across the translator*

The translator never uses `find`, `index-of`, `with-default` or `Maybe` itself; they appear only in `system.cdy`. So the bootstrap risk is small. Next, how a missing `else` reaches the checker:

*ran: Read NIL, the cond macro and the prelude*

*ran: Read the Maybe built-ins' declarations, spellings and runtime*

*ran: Move Maybe, find, index-of and with-default into the prelude*

Now the checker:

*ran: Read the checker's header and where its Maybe helpers are used*

*ran: Remove the checker's Maybe rules and add the missing-else rule*

`is-unit` is unused now, so it goes too. Then the build, with the new library staged next to `bin`:

*ran: Drop is-unit, stage the library and try Maybe as a sum*

A clause's pattern is always a list, so a variant with no fields is written `((None) fallback)`:

*ran: Fix the None pattern and retry*

*ran: Show the mypy error on the Maybe program*

*ran: Read the prelude's generated Maybe functions*

`find`'s parameter `keep` came out as `v` in the Python, which looks like a naming bug. I'll reproduce it outside the prelude:

*ran: Reproduce the renamed parameter in a small program*

Not reproduced in a top-level module. I'll check the prelude copy `bin` actually read:

*ran: Compare the prelude copies and look for a hard-coded v*

The copies match, so the rename happens only in an imported module. I'll reproduce it with a module of my own:

*ran: Reproduce the rename in an imported module, with and without a field named v*

Still not reproduced, so it depends on something else in the prelude. I'll copy the whole prelude into the module:

*ran: Reproduce with a renamed copy of the whole prelude*

Not with `bin` either. `m.py` was translated by T1, the new translator, so I'll try the module with T1:

*ran: Translate the module with T1 and look at the two find functions*

T1 writes `keep` here. I'll retranslate `m.cdy` and check again:

*ran: Compare main.py's output with a direct T1 translation*

It depends on the program: `m.cdy`'s own `match` binds a `v`. A minimal case:

*ran: Reproduce with a one-line program and read how emit names locals*

*ran: Check the rename with the translator at boot/47, before this branch*

The old translator needs its own runtime too. I'll pull boot/47's `cdy_rt` alongside it:

*ran: Run boot/47's translator with its own runtime*

*ran: Find where emit's locals map is set and carried*

*ran: Read how emit writes a top-level function and builds Env*

*ran: Read where module-level locals are bound*

*ran: Find the module-level bind-locals call*

*ran: Find where Env is constructed*

*ran: Read the module-level emission*

I'm tracing a naming bug that predates this branch: `emit` keeps local names between modules. Then I'll go back to building step 4.

*ran: Find where Env is built and how taken names are tracked*

*ran: Read how the driver emits the program's statements*

*ran: Start each top-level function's locals afresh, then retest*

The names are right now. One mypy error is left:

*ran: Show the remaining mypy error*

*ran: Check a generic sum's field under mypy with the committed translator*

*ran: Read emit-binds*

*ran: Read emit-match*

`env` already knows which variants are generic (`generic`). `emit-binds` will annotate a binding from the name's checked type, for generic variants only:

*ran: Annotate generic variants' field bindings, then recheck with mypy*

mypy passes now. Rebuilding `bin`, then the full suite:

*ran: Rebuild bin and run the full suite*

*ran: Show the errors of the Maybe-related failures and the checking.maybe rule*

*ran: Read the failing part of the macros test program*

*ran: Read the test's when and unless macros*

*ran: Read checking.maybe and the conditionals rule*

I'm rewriting the spec's three `Maybe` rules: `checking.if`, `checking.maybe` and `expr.unit`. First I'll check what `(cond (false 1))` gives now:

*ran: Check the missing-else errors, and read programs.prelude*

*ran: Rewrite the spec's Maybe rules and add library.maybe*

*(The context was summarised here; the turns before it are above.)*

## Claude Code

*ran: Look for remaining nil-as-missing text in the spec*

*ran: Read the macros spec around unless and cond*

*ran: Fix the types table and conditionals text; find the tests to fix*

*ran: Read the tests to change*

*ran: Fix the three failing tests*

Spec and tests updated for step 4. Next I'll run the spec and the full test suite.

*ran: Rebuild bin and run all tests*

*ran: Run all tests*

*ran: Find how + checks its operand type*

The operands are joined before the kind check, and `Int` no longer joins with `(Maybe Int)`. So I'll change the example to `(+ m m)`, which reaches the kind check.

*ran: Fix the Maybe arithmetic example and rerun the checking spec*

Now the backlog items.

*ran: Read the backlog items to update*

*ran: Read the items' notes and the HLD's step 4*

*ran: Read the item notes and HLD step headings*

*ran: Find the step list in the HLD*

*ran: Read step 3's Done note as a model*

Now I'll write the notes, with the removed spec text verbatim from HEAD.

*ran: Get the removed expressions spec text*

*ran: Update B20, B21, B138, B143 and file B154*

*ran: Write the HLD Done note, regenerate the index, rebuild and test*

*ran: See the note format error*

The fences in a note must be indented under its bullet. I'll indent them.

*ran: Indent the note fences and regenerate the index*

*ran: Rebuild bin, run all tests and linters*

*ran: See which doc link is broken*

*ran: Check that B154's file exists*

The new file is untracked, so the link check can't see it. Running `git add -N`:

*ran: Mark B154 as intended-to-add and rerun the tests*

Step 4 is done but not committed yet. All 533 tests pass (6 expected failures), ruff, mypy, pyright and pylint are clean, and `bin` is rebuilt with the fixpoint holding.

**What changed:**
- **`Maybe` is a real sum.** It's now `(deft (Maybe a) (Some ((v a))) (None))` in `src/cdy/prelude.cdy`. `find`, `index-of` and `with-default` are prelude Candy on it, built on two new built-ins, `find-index` and `elem-index`, which give `-1` when nothing is found. The old `Maybe` declaration and its runtime support are gone from `system.cdy`, `spelling.py` and `primitives.py`.
- **The checker's `Maybe` rules are gone** from `src/cdy/check.cdy`. A plain `t` or `nil` is no longer accepted as a `(Maybe t)`. An `if` with no `else` now needs a `Unit` then: `if: with no else, the then is Int, not Unit`.
- **`emit.cdy`:** variables bound by a `match` on a generic variant now get a type annotation (`v: a = …`). Without it, mypy reads them as `Any`.
- **New defect, B154, already fixed (it predates this branch):** one module's local variables could get another module's Python names inside a top-level function. For example, the prelude's `rest` wrote `v` for its `xs`. The fix is that `emit-func` now starts from an empty map of locals.
- **Spec:** I rewrote `checking.if`, `checking.maybe`, `expr.conditionals` and `expr.unit`, and added `library.maybe`. I also updated the `Maybe` row in `spec/20-types.md`, plus `library.lists` and `programs.prelude`. The old text is kept word for word in the notes of B20, B21 and the HLD.
- **Tests:**
  - I dropped the two `Maybe` rows of `test_show`.
  - `test_unsolved_types` now writes any unsolved type variable as `tN`, because the numbers shift with what the prelude holds.
  - I dropped the line using `when` as a value from `tst/cdy/cdyc/macros.cdy`; it's kept in B138's note.
- **Backlog:** B20 and B21 are `done`, B143 is in `review`, and B138 has a note.

**Decision for you:** a `cond` with no `else` gives `if: the branches are Int and Unit`, not the new "with no else" message. That's because `cond` expands to an explicit `nil` as its last branch. I've accepted that for now and noted it in B138 and the spec. If you'd rather it give the same message as `if`, the `cond` macro would need to leave its last branch out instead of writing the `nil`.

The step's write-up is in `doc/hl_rqmt/semantics.md:420`. Say gawc and I'll commit it as "semantics step 4: Maybe a sum, missing values gone" and tag boot/51.

## Owner

> Just note the if/cond inconsistency...  Which to me is not a minor one .. gawc

## Claude Code

*ran: Find a defect item with an error repro as a model*

*ran: File B155 for the cond/if message inconsistency and rerun the tests*

B155's repro runs as a strict expected failure (7 xfailed now). Committing:

*ran: Commit step 4, check the bootstrap step and tag boot/51*

*ran: Tag boot/51 and verify it is annotated*

Step 4 is committed as `144f19b`, "semantics step 4: Maybe a sum, missing values gone". The bootstrap step passes, and `boot/51` is an annotated tag. Nothing is pushed.

I filed the if/cond inconsistency as **B155**, a defect at normal priority. Your remark that it isn't minor is the item's note. Its repro is `(put (cond (false 1)))`, which should fail with the "with no else" message. Until it's fixed, the test suite runs it as a strict expected failure, so the count went from 6 to 7.

B155 covers two problems:
- **The check:** `cond`'s expansion ends in a written `nil`, so the checker doesn't see a missing `else`. The fix is either to leave the last `if` without an `else`, or to mark that `nil` as missing.
- **The message:** it should name `cond` and its clause, not the `if` it expands into. More generally, errors inside a macro are reported in the expansion's words.

`checking.if` in the spec, B138 and the HLD's step 4 note all link to it now.

Next is step 5, narrowing and field constraints (B121, B120), then the checkpoint where the branch merges. B140–B143 are waiting for your tick.

## Owner

> Should we go over 140-143, or continue?

## Claude Code

I'd go over them now, before step 5. Step 5's narrowing works on `match` clauses, so it builds directly on step 4's sums. If the review changes anything about `Maybe` or the missing-else rule, it's cheaper to change it before more is built on top. Each step is also still fresh, and four items is a short review.

Here's what each one is, with where to look:

- **B140, step 1:** a type variable that met only `Any` becomes `Any` once its definition is checked. B132 got its tests (`test_unsolved_types`), and the spec got rules for B26, B28 and B80. Write-up: `doc/hl_rqmt/semantics.md:268`.
- **B141, step 2:** `show` works from the static type, `(Some 4)` and `(List 1 2)` style, with the `List` and `Tup` constructors. It also found B150–B152. Write-up: `semantics.md:313`.
- **B142, step 3:** equality is structural and compares the class too, so two different variants are never equal. Comparing a function is an error at translation. It also found B153: orderings are still Python's. Write-up: `semantics.md:395`.
- **B143, step 4:** the step just committed, including B154 (fixed) and B155 (open).

The two points most worth your eye are step 2's `show` format, which becomes visible in every spec example from now on, and B155 itself, since it's open and you rated it as not minor.

Shall we take them in order, starting with B140?

## Owner

> b140

## Claude Code

Login expired · Please run /login

*ran: Read B140 and step 1's write-up*

B140 is step 1, which was all small fixes. The write-up is at `doc/hl_rqmt/semantics.md:268`, and here is what to check:

**1. A type variable that met only `Any` now becomes `Any` once its definition is checked.** This is the one code change. Matching against `Any` still doesn't fix a type variable to `Any`, but it now flags the variable. At the end of the definition's check, a variable that is flagged and never got a type becomes `Any`. A variable that met `Any` and later got a real type keeps that type.

For example, with `a` typed `Any`:
- `(reverse a)` becomes a `(List Any)`;
- a `fn` that is called with `a` and later with `1` is a `(Fn (Int) Int)`.

A variable that met nothing at all stays a type variable, which Python writes `Any`. That covers a `fn` never called and an `empty-list` never added to. The spec says this is *lasting*.

The translator's own code had eight such unsolved nodes, all of this kind. All eight are now `Any`, and its Python didn't change apart from renumbered temporaries.

**2. Tests:** `test_unsolved_types` has one case per kind and checks both the type the checker gives and the Python. `test_every_node_is_typed` now also checks that the translator's own code has no unsolved variable left.

**3. Three items closed with no code change, only spec rules:**
- B26: `and`, `or` and `not` take and give `Bool` only (`expr.logic`);
- B28: `Char` is its own type, so `(= \a "a")` is an error (`syntax.chars`);
- B80: a `def` is a constant (`programs.top-level`). This settles open question 4 in `mutation_optimization.md`. The old text is kept verbatim in the write-up.

The one thing I'd look at is the "met nothing stays a variable, *lasting*" rule in `checking.any` (`spec/25-checking.md:289`). It means a `fn` never called gets no type in Candy at all, only Python's `Any`. The alternative would be to report it as an error, or to drop it as unused.

Tick, or comments?

## Owner

> why are type variables getting any as a type?

## Claude Code

There are two separate cases, and only one of them really becomes `Any` in Candy.

**1. The variable met `Any`, and nothing else: it becomes `Any` in Candy.**

Take `(reverse a)` with `a` typed `Any`. `reverse` is `(Fn ((List t)) (List t))`, so the checker has to find `t`. The only thing it learns is that `(List t)` matched `Any`. That match tells it nothing, since `Any` matches every type both ways.

There were three choices:
- **Fix `t` to `Any` as soon as it meets `Any`.** This is too eager: a later `(+ (at r 0) 1)` could no longer make it `Int`.
- **Leave `t` unsolved.** That is what happened before step 1, and Python wrote `Any` anyway.
- **Mark `t` and decide at the end (Question 13).** If something later solves it, it keeps that type. If nothing does, `Any` was the only thing it ever met, so `(List Any)` is the honest answer.

This is ordinary gradual typing: `Any` turns checking off, and whatever only came from it stays unchecked. It's also the only way `Any` gets into a type the checker infers.

**2. The variable met nothing: it stays a variable in Candy, and only Python writes `Any`.**

Take `(let ((never-called (fn (y) y))) ...)` where the function is never called. Its real type is `(Fn (t) t)` for any `t`: it is generic. Candy has no let-polymorphism yet (B133), so a local can't be generic. The checker leaves `t` as an unsolved variable, which is still visible in Core.

Python can't express it either. A local variable's annotation can't have its own type parameter, so emit writes `_cdy_Callable[[_cdy_Any], _cdy_Any]`. That `Any` belongs to Python's spelling, not to Candy's type.

**Where I'd push back on what I built:** I marked case 2 *lasting* in `checking.any`, and that's too strong. There are better answers:
- **Generalise:** with B133, `never-called` becomes properly generic, and an unused `empty-list` is a `(List t)` for any `t`.
- **Make it an error:** report "can't infer the type of y", as Elm and Rust do. OCaml makes it an error only when such a type escapes into a module's interface.
- **Default it:** to `Unit` or a fixed type, the way Haskell defaults numbers.

None of these is needed for the MVP, since the value is never used where its type matters. So I'd reword case 2 from *lasting* to *for now*, linking B132/B133 with these options noted. Case 1 can stay *lasting*.

Should I make that change before you tick B140?

## Owner

> Yes, reword it, then tick... just as an aside: would it ever be helpful to consider type variables and generics as meta leaks?

## Claude Code

*ran: Reword checking.any to for now, note B133, tick B140*

*ran: Add checking.any to B133's refs and recheck*

I reworded it and ticked B140; neither change is committed yet.
- **The reword:** `checking.any` (`spec/25-checking.md:299`) now says a variable that met nothing is *for now*, linking B133. The old *lasting* text is kept verbatim in B133's note, with the three possible answers (make it generic, report an error, pick a default), and B133 now refers back to `checking.any`. The other case, a variable that met only `Any` becoming `Any`, stays *lasting*.
- **The tick:** B140 is `done` with the "ticked in review" note.

**Your aside: generics as leaks one level up.** Yes, I think that's a useful way to look at it. The backlog's leaks so far are about values: Python's division, `None`, tuple ordering. Type variables leak too, but into what Candy's type system can say rather than into what a program does. Mypy is the second check, and the annotations Python can write limit what Candy can generate and still have mypy check. We've already hit this three times:
- **A local `fn` can't be generic in Python** (that is, can't have its own type parameter). So even once B133 gives Candy let-polymorphism, emit would have to write `Any`.
- **Mypy narrows an `isinstance` on `Maybe[a]` to `Some[Any]`.** That's why step 4 annotates the variables a `match` binds: Candy knew the type, Python's narrowing lost it.
- **Types are erased at run time,** so `show` and `=` can't look at what a type variable stands for. Step 2 made showing a type variable a translation error for that reason (Question 3). That's a semantic rule shaped by how the host represents types.

They differ from value leaks in that a user doesn't see them in output. They show up either as "mypy rejects what Candy accepts" (B125) or as a Candy rule written to fit the host. They also matter most for a second target. A C target would have a different set: no generics without templates or `void*`, and nothing like Python's `Any`. JavaScript would have no static check at all.

I wouldn't add a new kind for them. I'd keep them as `leak` items, marked "type-level" in their text, and gather them under a heading in `doc/hl_rqmt/multi_target.md`, since that's where they'll be needed. If you agree, I'll add that as an idea, under that heading or in `doc/brainstorm.md`, whichever you prefer.

Next is B141, `show`.

## Owner

> Add it to multi_target.md, then b141

## Claude Code

*ran: Read multi_target.md's structure, B141 and step 2's write-up*

*ran: Read the parts of multi_target.md where the section goes*

*edited: `doc/hl_rqmt/multi_target.md`*

*ran: Check the new section's links*

I added the section to `doc/hl_rqmt/multi_target.md` as "Open: type-level leaks", after "Open: showing values". It lists the three leaks found so far and the C and JavaScript contrast. They stay `leak` items, marked type-level in their text, and get a kind of their own only if there come to be many. Its links check out. That section is now partly answered by step 2, so I'll update it at step 10, as the HLD plans.

**B141, step 2: `show`, and the `List` and `Tup` constructors.** The write-up is at `doc/hl_rqmt/semantics.md:313`.

**1. Every type's name is its constructor.**
- `(List 1 2 3)` and `(Tup 1 "a")` build values.
- `tup` stays as an alias for `Tup` for now (B152).
- `(List ...)` checks that its items are one type: `List: an item: expected Int, got String`.

**2. `show` writes a value the way Candy would read it back (Question 2):** `true`, `1500l`, `\a`, `"a \"b\""`, `(List 1 2)`, `(Some 4)`, `(Box (List 1))`.
- **It works from the static type.** emit passes the value's type to the runtime, for example `show(x, ("List", "Int"))`. That's how a `Char` and a `String` print differently, even though both are a Python `str`.
- **Records and variants:** each class registers its Candy name and field types, so the runtime can show generic and recursive ones.
- **Two cases are translation errors:** showing a type variable (Question 3), and showing a function.
- **A value typed `Any`** is shown by looking at the Python value when the program runs (`show_any`), so a `Char` there would print as a `String`.

**3. `put` and `format` write text as it is.** A `String` or `Char` prints without quotes, and anything else is shown. A value typed `Any` is printed as text if it's a Python string, and shown otherwise (`text_any`). That's how the translator's own 26 untyped holes print.

**4. Spec examples can print anything now.** The "output is numbers and text" rule is gone. Seven test programs' outputs changed as decided, for example `true` where Python printed `True`.

**Found, and still open:**
- B150: a function inside a record is only caught when the program runs, not at translation.
- B151: a `Double` with no literal form (`1e+20`) prints as Python's `repr`.
- B152: `tup` and `Tup` are two names for one thing.

**What I'd look at:**
- **The `Any` path:** both `show_any` and `text_any` decide by looking at the Python value. That's a leak, but only for code that already opted out of checking with `Any`. Each value-level leak there doesn't have its own item.
- **Whether `put` should show a `String` with quotes, as `show` does.** It doesn't: `(put "a")` prints `a`, and `(put (show "a"))` prints `"a"`. That matches most languages' print vs repr.

Tick, or comments?

## Owner

> tick, then b142

## Claude Code

*ran: Tick B141 and read B142*

B141 is ticked.

**B142, step 3: equality.** The write-up is at `doc/hl_rqmt/semantics.md:395`.

**1. `=` compares structure, and the class too.**
- **The bug this fixed:** a record or variant is a Python `NamedTuple`, which compares as a plain tuple. So `(A 1)` equalled `(B 1)`, and even another record with the same fields. That was B137, a defect.
- **The fix:** every class now gets an `__eq__` that also checks the class (`type(self) is type(other) and tuple.__eq__(...)`), plus `__ne__` and a `__hash__` that includes the class. Every class gets them, because a class without them would still compare as a tuple from its own side.
- **Everywhere:** since Python's own `==` is now Candy's `=`, the fix also applies in `contains`, in `index-of`, and to map keys.
- **The other types:** lists, tuples and maps compare item by item, and floats as IEEE 754 does (`0.0` equals `-0.0`). The spec calls all of this *lasting* (`expr.equality`, `spec/40-expressions.md:81`).

**2. Comparing a function is an error at translation**, including a value holding one, such as a list of functions: `=: a function can't be compared, got (Fn (Int) Int)`. A function inside a record isn't caught (B150, from step 2).

**3. Closed or noted:** B27 and B137 are done, and B29 (a tuple is a list in Python) got a note: equality was one of its consequences, and the rest stays.

**Found:**
- **B153 (leak, open):** `<` and the other orderings accept any one type. So records, lists and `Bool`s order like Python tuples, and comparing `nil`s fails when the program runs.
- **A mypy gap, left to mypy as the second check:** mypy refuses `(= (List (A 1)) (List (B 1)))` written with literals, though Candy types both as `(List S)`. A value with a declared type doesn't hit it. It belongs with the new type-level leaks section, and I'll add it there unless you say otherwise.

**What I'd look at:**
- **B153's priority:** it's low now. But `(< nil nil)` crashing at run time is the kind of thing this branch is meant to remove. One option is to restrict the orderings to numbers, `String` and `Char` now (a small check), and add ordering for lists and records later, with interfaces.
- **The cost of adding methods:** each class gets three Python methods, which adds about 7 lines per class. The translator's own Python grew by that.

Tick, or comments?

## Owner

> Tick

## Claude Code

*ran: Tick B142 and add the mypy literal gap to the type-level leaks*

B142 is ticked. I also added the mypy literal gap to the type-level leaks in `doc/hl_rqmt/multi_target.md`.

**B143, step 4: `Maybe` a sum, missing values gone.** This is the step just committed. The write-up is at `doc/hl_rqmt/semantics.md:420`.

**1. `Maybe` is the prelude's `(deft (Maybe a) (Some ((v a))) (None))`.**
- **Built on it:** `find`, `index-of` and `with-default` are prelude Candy, over two new built-ins, `find-index` and `elem-index`, which give `-1` for none.
- **Nesting:** a `(Maybe (Maybe Int))` keeps both layers, so `(Some None)` is not `None`.
- **Showing:** it prints as any variant does: `(Some 4)` and `None`.

**2. The checker's special rules are gone.** A plain `t` is no longer accepted as a `(Maybe t)`, and `nil` is only `Unit`'s value. You take a `Maybe` apart with `match` or `with-default`.

**3. An `if` with no `else` needs a `Unit` then** (Question 7, *for now*, B138): `if: with no else, the then is Int, not Unit`. For effects, `(if loud (put x))` still works.

**4. emit annotates the variables a `match` binds from a generic variant** (`v: a = t0.v`). Without it, mypy narrows them to `Any`.

**Found:**
- **B154, defect, fixed:** one module's local variables could get another module's Python names inside a top-level function. It predates the branch.
- **B155, defect, open:** a `cond` with no `else` gives `if: the branches are Int and Unit`, not the "with no else" message.

**What I'd look at:**
- **B155's place:** it's open, and you rated it as not minor. It could be fixed before the step 5 checkpoint, as part of step 5 or as a small step 4b, rather than left in the backlog. Fixing the check is small: the macro leaves its last `if` without an `else`. The message naming `cond` rather than `if` is a wider question about how errors in a macro's expansion are reported.
- **The names `Some` and `None`:** `None` shadows nothing in Candy. But in the generated Python, `prelude__None` sits next to Python's `None`. It's harmless now that the prefix keeps them apart, but it can confuse anyone reading the Python.

Tick, or comments?

## Owner

> I guess I meant "irritating" instead of "not minor" for b155... Tick

## Claude Code

*ran: Reword B155's note, tick B143*

B143 is ticked, which makes B140–B143 all `done`.

I reworded B155's note to "an irritating inconsistency", and said the wording was corrected in this review. The HLD's step 4 note says the same now (`doc/hl_rqmt/semantics.md:420`).

None of the review changes are committed:
- the four ticks;
- the reword of `checking.any` and the note on B133;
- the type-level leaks section in `doc/hl_rqmt/multi_target.md`;
- B155's wording.

Say gawc to commit them as "semantics: review of steps 1–4". None of them touch `bin`, so it needs no `boot/` tag.

Next is step 5: narrowing (B121) and field constraints (B120), then the checkpoint where the branch merges. B155 can go into step 5 or wait in the backlog.

## Owner

> Gawc

## Claude Code

*ran: Commit the review of steps 1–4*

I committed the review as `0e3dd8e`, "semantics: review of steps 1-4". It doesn't touch `bin`, so there's no `boot/` tag. The commit is all mine; there were no edits of yours in the working tree. Nothing is pushed.

Next is step 5: narrowing (B121) and field constraints (B120), then the checkpoint where the branch merges. Say go when you want to start, and whether B155 goes into step 5.

## Owner

> Go, and go with b155 if it's a small step

## Claude Code

*ran: Read step 5's question, task and items*

*ran: Read the HLD's narrowing design and check.cdy's outline*

*ran: Read check.cdy's context types, field lookup and match*

*ran: Find how lower and emit handle match*

*ran: Read lower-match and emit-match*

*ran: Read check-top, infer-node and the helpers*

*ran: Read emit's Env and how it writes Field, Assoc, Local and SMatch*

*ran: Find where Env is constructed and how Field and Assoc are written*

*ran: Find Env's constructor calls*

*ran: Read the cond macro and is-missing-else*

The B155 fix is small, so it goes in this step: `cond` will write its last clause as an `if` with no `else`, so the checker's missing-else rule sees it. Now writing the checker changes.

*ran: Find field-type's callers and helper definitions*

*ran: Add narrowing and field constraints to the checker*

*ran: Fix the show call in solve-each*

Now emit: inside a clause, a `get` or `assoc` on the subject local reads the narrowed temporary instead.

*ran: Find emit-match's callers and local-py*

*ran: Read the comment above Env*

*ran: Narrow in emit, fix cond's missing else, build T1*

*ran: Try narrowing, field constraints and cond with T1*

*ran: Translate the trial program with T1, run it and mypy it*

The generic case gives mypy an `Any`: it narrows the temporary to `N[Any]`. Checking what mypy does when narrowing the parameter itself:

*ran: Test how mypy narrows a generic union parameter vs a temporary*

*ran: Cast a narrowed generic get, rebuild T1, retry*

Under `--strict`, mypy flags a cast it finds redundant. So the cast must apply only to fields whose declared type mentions a type variable. I'll record those in emit's `generic` map.

*ran: Read generic-variants and its uses*

*ran: Find emit's type-variable helpers*

*ran: Read Core's Variant and emit's field-types*

*ran: Record each generic variant's type-variable fields*

*ran: Narrow per case, rebuild T1, retry*

That works and mypy is clean. Now the error cases:

*ran: Check the error messages for narrowing, constraints and cond*

With `Any`, the field's type stays an unsolved variable; it should become `Any`, as the variable it was read from did. Fixing:

*ran: Mark a field constraint's type Any when its value met only Any*

Now the full build and tests:

*ran: Rebuild bin and run all tests*

*ran: Find the spec text on narrowing and unknown types*

*ran: Read the rest of match.sum-types*

*ran: Write checking.narrowing and update the spec's records, order, if and match rules*

Now the backlog. First I'll check whether an item already covers errors reported in a macro's expansion:

*ran: Search the backlog for items about macro expansions*

*ran: Close B120, B121, B155, move B144 to review, add B156*

The checker won't let a closed item keep its repro. The same case is already in `checking.if`'s errors table, so I'll move the repro section into the note, verbatim:

*ran: Move B155's repro into its note and regenerate the index*

The old `checking.if` text in the note is missing its last line. Fixing:

*ran: Complete the old text in B155's note and check B120's and B121's*

Now the HLD's Done note for step 5:

*ran: Write step 5's Done note in the HLD*

*ran: Note the cast in multi_target.md, rebuild, run all tests and linters*

Everything passes. Checking that `bin`'s diff is only what I expect:

*ran: Look at the diff of the rebuilt translator*

*ran: Rewrite generic-variants as a fold, rebuild and test*

Step 5 is done and ready to commit: all 539 tests pass (6 expected failures), the linters are clean, and `bin` is rebuilt with the fixpoint holding.

**Narrowing (B121).** In a `match` clause whose subject is a local, `get` and `assoc` on it now read that variant's own fields:
```
(defn f (s) (match s ((A _ _) (get s x)) ...))
```
- **Checker:** it keeps a map from local to variant while checking a clause; it doesn't make variants into types. Outside `get` and `assoc`, the local is still the sum, and the `else` isn't narrowed.
- **Python side:** in a clause, `get s x` reads the match's temporary, which `isinstance` has already narrowed (`_cdy_t1.x`).
- **A mypy gap:** for a generic sum, mypy narrows `isinstance(t, N)` on a `T[int]` to `N[Any]`, even on a parameter. So a field whose type has a type variable gets a cast to the checker's type, and only that field, because `--strict` rejects a redundant cast. Every generated file now imports `cast`. I added this to the type-level leaks section in `doc/hl_rqmt/multi_target.md`.

**Field constraints (B120).** A `get` or `assoc` on a value whose type isn't known yet is now checked once the definition is: `(let ((name-of (fn (p) (get p name)))) (name-of (P "ann")))` works.
- **When it's still an error:** if the type is still unknown at the end, the old error stays: `the type of p isn't known here`.
- **Wrong field type:** `get: field name of P is String, not Int`.
- **Met only `Any`:** the field is `Any`.

**B155 (`cond` with no `else`).** `cond` now writes its last clause as an `if` with no `else`, so `(cond (false 1))` gives the same message as an `if`. The message still names the `if` rather than `cond`. I filed that as **B156**, an idea about how errors inside a macro's expansion are reported in general.

**Spec:**
- `checking.narrowing` is new.
- I updated `checking.records`, `checking.order`, `checking.if` and `match.sum-types`.
- The old text is in the notes of B120, B121 and B155.
- B155's repro is now an example in `checking.if`'s errors table.

**Backlog:** B120, B121 and B155 are `done`, B144 is in `review`, and B156 is new.

The step's write-up is in `doc/hl_rqmt/semantics.md`, under step 5.

On gawc I'll commit "semantics step 5: narrowing and field constraints" and tag boot/52. That brings us to the checkpoint you chose: merge `semantics` into master now, after reviewing B144 and running `pytest -m bootstrap`, or go on to step 6 (numbers).

## Owner

> Gawc

## Claude Code

*ran: Commit step 5, check the bootstrap step and tag boot/52*

Step 5 is committed as `8b34dd8`, "semantics step 5: narrowing and field constraints". The bootstrap step passes, `boot/52` is an annotated tag, and there were no edits of yours in the working tree. Nothing is pushed.

This is the checkpoint. The two options:
- **Merge now:** review B144 first, then run `pytest -m bootstrap`, merge `semantics` into master with `--no-ff`, and tag it. Steps 6–10 (numbers, `at`/`slice` bounds, `def` order, errors, docs) would then go on a second branch.
- **Go on to step 6, numbers:** `/` on floats, `mod`, and literal ranges. The branch then merges after step 10.

My recommendation is to merge now. Steps 1–5 already hang together as one piece: types, `show`, equality, `Maybe` and narrowing. Steps 6–9 are mostly separate from them, and a merge here keeps the branch from carrying ten steps' worth of changes.

Merge or go on?

## Owner

> merge

## Claude Code

*ran: Read the HLD's checkpoint decision and the merge process*

*ran: Read the merge steps and the chat-archive script's usage*

*ran: Read the later step tasks, the HLD status and the archive script's usage*

*ran: Run the bootstrap chain tests before the merge*

I started `pytest -m bootstrap` in the background. By `doc/process.md`, a merge needs a few things first, so this is the plan:

1. **Review B144 (step 5).** It's the last item in `review`. The summary I gave before the commit covers it, and the write-up is under step 5 in `doc/hl_rqmt/semantics.md`.
2. **A docs commit for steps 1–5.** This is the process's docs step, done now rather than as step 10:
   - **`CLAUDE.md`:** the "Type checking" and "Sum types" bullets, which describe `Maybe` rules that no longer exist and no narrowing. I'd also add `semantics` to the branch history.
   - **The HLD:**
     - its status becomes *done*, with the scope cut at step 5;
     - steps 6–9 are marked as moved to `semantics-2`;
     - a short "Looking back" section is added.
   - **The four open step tasks:** B145–B148 stay open, re-pointed to `semantics-2`. B149 (docs) becomes this commit's task.
3. **Archive the branch's chat** with `script/chat_archive.py`, as `doc/archive/chat_semantics.md`.
4. **Merge** with `git merge --no-ff refs/heads/semantics`, then tag `semantics`, annotated. Pushing waits until you ask.

Tick B144, and I'll do steps 2–4 and show you the docs commit before merging.

## Owner

> <task-notification>
> <task-id>b61ae4lqf</task-id>
> <tool-use-id>toolu_01SfTXn3rnwa1SASUiQZwgov</tool-use-id>
> <output-file>/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/tasks/b61ae4lqf.output</output-file>
> <status>completed</status>
> <summary>Background command "Run the bootstrap chain tests before the merge" completed (exit code 0)</summary>
> </task-notification>

## Claude Code

*ran: Read the bootstrap test result*

The bootstrap chain passes: `pytest -m bootstrap` ran in 2 min 22 s. That covers the check needed before merging.

I'm waiting on your tick for B144 (step 5) before the docs commit, the chat archive and the merge.

## Owner

> can you put b144 back up again?

## Claude Code

**B144, step 5: narrowing and field constraints.** The write-up is under step 5 in `doc/hl_rqmt/semantics.md`. It's in commit `8b34dd8`, tagged `boot/52`.

**1. Narrowing (B121, done).** In a `match` clause whose subject is a local, `get` and `assoc` on it read that variant's own fields:
```
(defn f (s) (match s ((A _ _) (+ (get s x) (get s id))) ((B _ _) (len (get s y))) ((C) 0)))
```
- **How the checker does it:** it keeps a map from local to clause variant in its context. There are no variant types, so outside `get` and `assoc` the local is still the sum, for instance when it's passed or returned.
- **What isn't narrowed:** the `else` clause, an `if` on a test (B136, *for now*), and a subject that isn't a local.
- **Python:** in a clause, `get s x` reads the match's temporary, which `isinstance` has already narrowed (`_cdy_t1.x`).
- **The mypy gap:** for a generic sum, mypy narrows `isinstance(t, N)` on a `T[int]` to `N[Any]`, even on a parameter. So a field whose type has a type variable gets a cast to the checker's type, for example `_cdy_cast('int', _cdy_t3.v)`. Only those fields get one, because `--strict` rejects a redundant cast. Every generated file now imports `cast as _cdy_cast`. This is listed in the type-level leaks section of `doc/hl_rqmt/multi_target.md`.
- **Errors:** `get: A has no field y` inside an `A` clause, and `get: S has no field x` in the `else`.

**2. Field constraints (B120, done).** A `get` or `assoc` on a value whose type isn't known yet now gives a fresh type and records a constraint. Constraints are solved after each definition is checked:
```
(let ((name-of (fn (p) (get p name)))) (name-of (P "ann")))
```
- **Wrong field type:** `get: field name of P is String, not Int`, and likewise for `assoc`.
- **Missing field:** `get: P has no field age`.
- **Still unknown at the end:** the old error, `get: the type of p isn't known here (name)`.
- **Met only `Any`:** the field's type is `Any`.

**3. B155 (done).** `cond`'s last clause, when there's no `else`, now expands to an `if` with no `else`. So `(cond (false 1))` gives the same message as an `if`: `if: with no else, the then is Int, not Unit`. Its repro moved into `checking.if`'s errors table. The message still names the `if`, not `cond`: that's **B156**, a new idea about errors in a macro's expansion in general.

**4. Spec:**
- `checking.narrowing` is new.
- `checking.records` lost its *for now*, and its old error example is now a run example.
- `checking.order` describes the constraints, with a run example and three errors.
- I also updated `checking.if` and `match.sum-types`.
- The old text is in the notes of B120, B121 and B155.

**5. Bootstrap:** one step, `boot/52`. The translator itself never narrows a `match` subject, and never takes a field of a value whose type isn't known yet. One fix came out of the step: `generic-variants` is now a `fold`, so it doesn't recurse once per top-level definition.

**What I'd look at:**
- **The cast:** it is the first place emit trusts the checker over mypy inside an expression; emit-binds already trusts it in an annotation.
- **Late errors:** constraints are solved at the end of a definition, so one of their errors can now come after an error that is later in the source.

Tick, or comments?

## Owner

> everything looks good, but can we go over "narrowing" in some more detail?

## Claude Code

Before explaining, I'll check one case I haven't tested: a `fn` inside a narrowed clause, in a function that `lower` turns into a loop.

*ran: Test narrowing with closures, tail loops and nested matches*

Those cases all work and pass `mypy --strict`: a `fn` inside a clause, a function that becomes a loop, and nested matches. Here is narrowing in detail.

## What it is

A sum's value is one of its variants, but only a `match` finds out which one. Before step 5, a clause knew which variant it had, but the checker forgot that for the subject:

```
(deft S (A ((x Int) (id Int))) (B ((y String) (id Int))) (C))
(defn f (s) (match s ((A _ _) (get s x)) ...))   ; was: get: S has no field x
```

`get` on a sum only allowed a field every variant has (`id`), so you had to name the field in the pattern instead: `((A x _) x)`. Narrowing means that inside the `A` clause, `s` is known to be an `A`, so `(get s x)` works. This is the same idea as TypeScript's or Kotlin's narrowing after a check, except that only a `match` clause does it.

## What narrows and what doesn't

| Case | Narrowed? |
|---|---|
| A clause whose subject is a local (parameter, `let` name, pattern name) | yes, to the clause's variant |
| Nested matches on two locals | each is narrowed on its own (`nest` above) |
| A `fn` inside the clause that uses the local | yes, it sees the narrowing |
| The `else` clause | no: it could be any of the remaining variants |
| A subject that isn't a local, `(match (make) ...)` | no: there is no name to narrow, and the pattern's names read the fields |
| After an `if` test | no: Candy has no `is-a` test yet. Question 8 chose clauses only, *for now* (B136) |

## What "narrowed" means to the checker

Only `get` and `assoc` see the narrowing. Everywhere else the local keeps the sum's type:
- passing `s` to a function that wants an `S` is fine;
- returning it is fine;
- `(= s other)` compares two `S` values.

A variant is never a type a program can write. The HLD imagined a type per variant, `S.A`, accepted wherever an `S` is. I built something simpler: the checker's context holds a map from the local to the clause's variant. When `get` or `assoc` sees a sum-typed local that's in the map, it looks the field up in that variant, with the sum's type arguments: in a `(T Int)`, the variant `N`'s field `v` is an `Int`. This needed no change to unification, and `get` and `assoc` are the only places a variant type would have made a difference.

## The Python side

mypy has to agree, and it can't see Candy's map. emit already writes a `match` as an `isinstance` chain on a temporary:

```python
_cdy_t1: object = s
if isinstance(_cdy_t1, A):
    return (_cdy_t1.x + _cdy_t1.id_)
```

`s` itself is typed `S` (the union), so `s.x` would fail mypy. `_cdy_t1` has been narrowed by `isinstance`, so a narrowed `get` reads the temporary instead. `walk` above shows it works inside a loop too, since the temporary is set again on each pass, before the test.

**The generic case is where mypy falls short:**
- **The gap:** for `(deft (T a) (L ((v a))) (N ((v a) (n Int))))`, mypy narrows `isinstance(t, N)` on a `T[int]` to `N[Any]`, even when narrowing the parameter itself. I checked it on its own.
- **The fix:** a field whose type contains a type variable gets a cast to the type the checker found, `_cdy_cast('int', _cdy_t3.v)`. Other fields, like `n: int`, don't, because `--strict` rejects a redundant cast.
- **What it trusts:** like the annotations step 4 added on match bindings, it trusts Candy's checker where mypy is blind.

## Things to know

- **Only the subject local is narrowed,** not other names for the same value. In `(let ((t s)) (match s ((A _) (get t x)) ...))`, `t` isn't narrowed, so that is an error. Flow typing would handle it; Question 8's choice doesn't.
- **B136 is the revisit.** The alternatives are narrowing after a test (needs an `is-a`), or no narrowing plus patterns without every field (`(A x)` for a variant with more fields).
- **It doesn't come from ML.** ML, Haskell and Elm have no narrowing: you use the pattern's names, or Haskell's `s@(A x)`. Candy's `get` makes narrowing worth having.

Tick, or something to change?

## Owner

> tracking now, forgot.. tick

## Claude Code

*ran: Tick B144 and find CLAUDE.md text the branch outdated*

*ran: Read the CLAUDE.md lines to update in full*

B144 is ticked. Now the docs commit, starting with `CLAUDE.md`:

*ran: Update CLAUDE.md, and read the HLD's status and outline*

*ran: Find the epic's and iMVP doc's text on this branch*

*ran: Read the epic's branch list and the iMVP doc's Maybe text*

Now the HLD (status, steps 6–9 moved, step 10 done, "Looking back") and the other docs:

*ran: Write the HLD's status, moved steps, docs note and Looking back; update the other docs*

The docs are updated and their links check out. Next is the chat archive. I'll look at how the last branch's archive was written:

*ran: Read the last chat archive's header and the script's options*

*ran: See how the script's since/until/branch filter messages*

*ran: Archive the branch's chat*
