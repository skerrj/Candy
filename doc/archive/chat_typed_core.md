*Archived 2026-10-31, from the Claude Code session that built branch `typed-core`
(2026-10-31; HLD `doc/hl_rqmt/typed_core.md`, tag `typed-core`), by
`script/chat_archive.py`, before the merge.* The owner's messages and Claude's replies on
the branch, verbatim; each tool call is a one-line marker, and thinking and tool output
are left out. The branch began on `master` (the HLD's questions, in
`doc/archive/chat_python_complete.md`). What came of it: types and positions on every
Core node, nested Python `def`s typed ([[B19]]), the messages ([[B119]], [[B14]]),
[[B15]] closed and split ([[B133]], [[B134]]); and from the review, [[B135]] (an
operator's error at the call), [[B136]] (a pattern names every field, with notes from term
rewriting), the goal of no operators in the language ([[B124]]'s note) and "Looking back".

# typed-core

## Claude Code

Now the HLD's status, then the start commit.

*ran: `sed -n 3,4p doc/hl_rqmt/typed_core.md`*

*ran: `python - <<'EOF'`*

Branch `typed-core` is started (`707c515`). Step 1 next: first, every place that builds or takes apart a literal form.

*ran: `grep -rnE "\((Txt|IntLit|LongLit|ByteLit|FloatLit|DoubleLit|CharLit|BoolLit)[ )]`*

*ran: `grep -nE "\((Txt|IntLit|LongLit|ByteLit|FloatLit|DoubleLit|CharLit|BoolLit)[ )]"`*

*ran: `sed -n 600,660p src/cdy/core.cdy && sed -n 350,365p src/cdy/core.cdy`*

*ran: `sed -n 40,73p src/cdy/form.cdy && grep -n "NOWHERE\|form-pos\|at-pos" src/cdy/ex`*

*ran: `sed -n 350,369p src/cdy/expand.cdy && sed -n 105,125p src/cdy/core.cdy`*

*ran: `grep -n "(defn resolve\b\|(defn resolve " -A30 src/cdy/core.cdy | head -45`*

*ran: `grep -nE "\(\(?(Local|Global|Prim|Do)[ )]" src/cdy/*.cdy | grep -v "^src/cdy/che`*

Mapping the 57 places that build or match a Core leaf, before changing them.

*ran: `grep -nE "\(\(?(Local|Global|Prim|Do)[ )]" src/cdy/*.cdy`*

*ran: `grep -n "NIL" src/cdy/*.cdy | grep -v "^src/cdy/core.cdy:5[56]"`*

*ran: `grep -rn "core__\|form__\(Txt\|IntLit\|Sym\|Lst\)\|read__" tst/py_cdy src/py_cdy`*

*ran: `sed -n 380,440p src/cdy_rt/primitives.py && sed -n 530,560p tst/py_cdy/test_self`*

*ran: `sed -n 60,200p src/cdy/read.cdy`*

Now the edits, starting with `form.cdy` and the reader.

*ran: `sed -i 's/^state: open$/state: in-progress/' backlog/B126-typed-core-step-1.md &`*

*ran: `sed -i 's/^(defn number-form (word kind at)$/(defn number-form (word kind where)`*

Now Core's leaves. First, how the checker finds a node's position:

*ran: `sed -n 150,240p src/cdy/check.cdy`*

*ran: `python - <<'EOF'`*

Patterns done. Now the type definitions and every place that builds a leaf:

*ran: `python - <<'EOF'`*

*ran: `for l in 255 280 440 452 568 1378 && do sed -n "${l},$((l+10))p" src/cdy/core.cd`*

*ran: `sed -n 266,275p src/cdy/core.cdy && python - <<'EOF'`*

Now line 270, the `at-use` helper, and the checker's `node-pos`:

*ran: `python - <<'EOF'`*

The macro expander's `stamp` gives an expansion's NOWHERE forms the call's position. Literals need that too now:

*ran: `python - <<'EOF'`*

Now a first build with T1:

*ran: `printf '(sig x Int)\n(def x\n  "a")\n' > tmp/leaf.cdy 2>/dev/null || { mkdir -p `*

The leaf error is now reported at `3:3`. Next, the full rebuild of `bin` and the test suite:

*ran: `time python src/py_cdy/self_host.py 2>&1 | tail -5`*

*ran: `timeout 1200 pytest -q -x -n auto 2>&1 | tail -25 || timeout 1200 pytest -q 2>&1`*

*ran: `time timeout 1500 pytest -q 2>&1 | tail -30`*

Everything passes except the backlog index (B126 is now `in-progress`). Next is the spec example for an error at a leaf. First, how `candy error` blocks match:

*ran: `grep -n "expect-error\|match=" tst/py_cdy/test_spec.py | head && grep -n "expect`*

*edited: `spec/25-checking.md`*

*ran: `python script/backlog.py >/dev/null && pytest -q tst/py_cdy/test_spec.py -k "25-`*

*ran: `printf '(sig f (Fn (Int) Int))\n(defn f (n) n)\n(sig g (Fn (String) Int))\n(defn`*

Errors in names are reported where the name is used, too. Now a reader test for literal positions:

*edited: `tst/py_cdy/test_self_host.py`*

*ran: `pytest -q tst/py_cdy/test_self_host.py -k reader_positions 2>&1 | tail -2 && ruf`*

*ran: `sed -i "s|literals = t1.read__read_source(\"f.cdy\", '(\"s\" 1 2.0\\\\n \\\\\\\\`*

*ran: `grep -rn "only .Sym. and .Lst.\|Only symbols and lists\|leaf is reported\|report`*

Now B59 and B122 get closed (this step fixes both), the task moves to `review`, and the HLD gets its *Done* note:

*ran: `tail -5 backlog/B122*.md && tail -4 backlog/B59*.md && sed -n '/^1\. \*\*Positio`*

*ran: `grep -n "Done" doc/hl_rqmt/type_checker.md | head -3 && sed -n '/^2\. \*\*Positi`*

Before writing the *Done* note, a check of what this step changes in the generated Python: old `bin` against new `bin`, on every test program.

*ran: `rm -rf tmp/oldbin tmp/cmp && mkdir -p tmp/oldbin tmp/cmp/old tmp/cmp/new && git `*

*ran: `grep -n "(= \|(!= " src/cdy/lower.cdy | head -40`*

*ran: `sed -n 494,505p src/cdy/lower.cdy && sed -n 425,437p src/cdy/lower.cdy`*

*ran: `python - <<'EOF'`*

Nested patterns inside a `tup` pattern probably aren't supported, so I'll write it with two matches:

*ran: `python - <<'EOF'`*

The rest of the translator's diff is its own source changing, as expected. Now the test programs again, all of them this time:

*ran: `rm -rf tmp/cmp/old/* tmp/cmp/new/* && n=0 && d=0 && for f in $(find tst/cdy -nam`*

I'll write into a fresh directory rather than clearing the old one:

*ran: `O=tmp/cmp2/old && N=tmp/cmp2/new && mkdir -p $O $N && n=0 && d=0 && for f in $(f`*

*ran: `find tst/cdy -name '*.cdy' | wc -l && find tst/cdy -name '*.cdy' -not -path '*/l`*

*ran: `python script/backlog.py >/dev/null && timeout 1500 pytest -q 2>&1 | tail -3 && `*

Everything is green. Now the bookkeeping: the *Done* note, closing B59 and B122, and moving B126 to `review`.

*ran: `python - <<'EOF'`*

Step 1 (positions on literal forms and Core's leaves) is ready to commit, but not committed: say gawc and I'll commit it, then give it its `boot/NN` tag. The full suite passes (485 passed, 5 expected failures), the linters are clean, and `bin` is rebuilt.

- **What changed for errors:** a type error is now reported at the literal or name it's in, not at the enclosing call. `(def x\n  "a")` now says `3:3`, where it said `2:1`. In `(f\n    s)`, a wrong argument is reported at the `s`, on line 2.
- **How:**
  - Every literal form now carries a position, which the reader fills in.
  - `Local`, `Global`, `Prim` and `Do` in Core got a position field; `Lit` takes its form's.
  - A local's use is rebuilt with the position where it's used.
  - The macro expander gives a macro's literals the call's position, as it already did for symbols and lists.
- **A bug the change caused, which I caught and fixed:**
  - **The cause:** `lower` turns a self tail call into a loop, and it found a parameter passed unchanged by comparing whole `Local` nodes. With positions in them, no parameter matched any more, so the loop rebound every parameter (`text, pos, acc = (text, …)`).
  - **The fix:** it now compares name and id.
  - **The check:** old `bin` and new `bin` write identical Python for 10 of the 11 test programs. The eleventh, `macro_files.cdy`, can't go through the old `bin` at all, because its macro file now builds the new form shape.
- **The macro API change:** macro code that builds a literal writes its position, `(Txt (sym-name s) NOWHERE)`. I updated the spec's `macros.macro-code` example and the two macro test files.
- **Tests:** a spec example of an error at a string literal, in `checking.definitions`; `test_reader_positions` now checks literals too.
- **Backlog:** B59 and B122 are `done` (`fixed: typed-core`), B126 is in `review`, and the HLD has step 1's *Done* note.

## Owner

> gawc

## Claude Code

*ran: `git status --short | grep -v "^ M" && f=/tmp/claude-1000/-home-skerrj-dev-exp-ca`*

Step 1 is committed as `3d2260d` on `typed-core` and tagged `boot/44` (annotated). There were no edits of yours to include. The bootstrap check passed for that commit. Nothing is pushed.

Next is step 2, types in Core: a `t` field on every `Expr`, with the checker rewritten to elaborate. It's the big one. Say go when you want it.

## Owner

> go

## Claude Code

Starting step 2. First, the whole checker, since every function that infers a type will now also return the typed node.

*read: `src/cdy/check.cdy`*

*read: `src/cdy/check.cdy`*

*ran: `grep -nE "\((Call|If|Do|Lambda|Tuple|Fmt|Field|Assoc|MatchE|Temp|Lit|Local|Globa`*

A tool, then: a small s-expression scanner that finds each `Expr` constructor list in the `.cdy` sources, tells a pattern from a construction, and adds `_` to a pattern or `ANY` to a construction.

*wrote: `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/add_field.py`*

*ran: `python /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043`*

*ran: `python - <<'EOF'`*

The tool had already updated `NIL`. Rerunning without that edit:

*ran: `grep -n 'def NIL' src/cdy/core.cdy && python - <<'EOF'`*

Now `lower`'s rebuilt nodes, which should keep their types:

*ran: `sed -n 84,125p src/cdy/lower.cdy && sed -n 150,240p src/cdy/lower.cdy && sed -n `*

*ran: `grep -n "value-call\|value-if\|value-fn\|value-boolop" src/cdy/lower.cdy`*

*ran: `python - <<'EOF'`*

*ran: `grep -n "def map_set" -A12 src/cdy_rt/primitives.py`*

*ran: `sed -n 1,30p src/cdy/check.cdy && sed -n 44,80p src/cdy/check.cdy && sed -n 452,`*

*ran: `python - <<'EOF'`*

One fix: the callee `Lambda` of a `let` is recorded in `infer-call`, like the other callees. Then the new "typed Core" section:

*ran: `python - <<'EOF'`*

T1 builds, and checking works as before. Next, the full rebuild and the tests:

*ran: `time python src/py_cdy/self_host.py 2>&1 | tail -3 && timeout 1500 pytest -q 2>&`*

All green, and the self-host build takes 3.6s, up from 3.0s. Now the test that every node of the translator's own Core has a type after checking:

*ran: `grep -n "^def test_\|^from\|^import\|^ROOT\|^SRC" tst/py_cdy/test_self_host.py |`*

*ran: `sed -n 370,380p tst/py_cdy/test_self_host.py && grep -n "library-builtins" src/c`*

*edited: `tst/py_cdy/test_self_host.py`*

*ran: `timeout 600 pytest -q tst/py_cdy/test_self_host.py -k every_node 2>&1 | tail -15`*

It passed on the first try, so I'll check that the walk really sees the nodes and that their types look right:

*ran: `python - <<'EOF'`*

*ran: `PYTHONPATH=src/py_cdy:script:tst/py_cdy python - <<'EOF'`*

*ran: `mkdir -p tmp/bin44 && git archive HEAD bin/py | tar -x -C tmp/bin44 && O=tmp/cmp`*

*ran: `ruff check src tst script 2>&1 | head -12 && pylint tst/py_cdy/test_self_host.py`*

*ran: `python - <<'EOF'`*

A quick mutation check that the test can fail: I'll stop the checker recording callees, expect the test to fail, then restore it.

*ran: `cp src/cdy/check.cdy tmp/check.bak && python - <<'EOF'`*

The test catches the unrecorded callees, and passes again once the code is restored. Now the *Done* note and the task's state, then a last full run:

*ran: `python - <<'EOF'`*

Step 2 (types in Core) is ready to commit, but not committed: say gawc and I'll commit it and tag `boot/45`. The full suite passes (486 passed, 5 expected failures), the linters are clean, and `bin` is rebuilt.

- **Every Core node now has a type field, `t`.** `analyse` fills it with `ANY`, and the checker replaces that with the type it found. `type-check` now returns the typed definitions instead of the untyped ones.
- **How the checker does it, without a rewrite:**
  1. Before a definition is checked, each node's `t` is set to a unique placeholder variable, `?eK`.
  2. As the checker works, it records the type it settles for each node under that name.
  3. After the definition is checked, each node gets its recorded type, fully resolved.

  The checking logic itself is unchanged; only the recording points are new. The recorded types live in a map of their own, not in the substitution, so unification doesn't slow down.
- **A design change from the HLD:** the HLD said "`infer` returns the node rebuilt". This approach gives the same result with a much smaller change to `check.cdy`. I've described it in the step's *Done* note.
- **`lower` keeps the types** on the nodes it rebuilds, so `emit` (in step 3) will see them.
- **The edit itself:** a throwaway script added the field at about 180 places, as `_` in patterns and `ANY` in constructions. I hand-fixed `lower`'s rebuilds.
- **Checks:**
  - **Same output:** the generated Python is byte for byte the same as `boot/44`'s for every test program.
  - **A new test, `test_every_node_is_typed`:** on the translator's own 23,280 nodes, the checker reached every one and every `fn` has a function type. Three nodes keep an unsolved type variable, which Question 2 allows. I checked the test can fail by removing one recording point.
  - **Cost:** the self-host build is 0.6s slower, 3.6s instead of 3.0s.
- **Backlog:** B127 is in `review`, and the HLD has step 2's *Done* note.

*(The context was summarised here; the turns before it are above.)*

## Owner

> gawc

## Claude Code

*ran: Check working tree and latest boot tags*

Only my step 2 files are changed; none of your own edits are in the tree.

*ran: Commit step 2, check bootstrap step, and tag boot/45*

Step 2 is committed as `ddcf686`, "typed-core step 2: types in Core", and tagged `boot/45`. The bootstrap check passed on the new commit, and the tag is annotated. Only my step 2 files were in the commit; I didn't find any edits of yours to add.

Nothing is pushed: the `typed-core` branch, master's `b2c0ad7`, `boot/45` and `boot/44` (which also hasn't been pushed) are still local.

Next is step 3, typing the nested `fn`s (B19): `emit` will give the nested Python `def`s their real types instead of `Any`, and I'll fix or record whatever mypy then finds. Say go when you want it.

## Owner

> go

## Claude Code

*ran: Find step 3 in the HLD and its backlog items*

*ran: Read the HLD's intro and steps*

*ran: Find SLocalFunc and Any annotation sites*

*ran: Read emit's SLocalFunc and type rendering*

*ran: Read emit-type and emit-func*

*ran: Find all SLocalFunc sites and ?N naming*

Step 3 under way: giving `SLocalFunc` its type and having `emit` annotate nested `def`s with it (a `?N` as `Any`).

*ran: Add type to SLocalFunc and annotate nested defs*

*ran: Restore Any fallback, then build T1 with the change*

*ran: mypy-check the translator built with nested types*

*ran: Show the difference in generated translator*

*ran: Try nested defs, generic, and let-bound fns*

*ran: Retry the nested-def experiment*

Nested `def`s now come out typed, generics too, and mypy passes on them. Now checking the remaining B19 case, a `let`-bound `fn` that stays a `lambda`.

*ran: Check naming of same-named let-bound fns in branches*

Locals are renamed apart within a function, so annotating a `let`-bound `lambda`'s assignment is safe. Adding that too, since it's B19's own repro.

*ran: Annotate let-bound lambdas and recheck*

Both cases pass mypy. Now the spec and docs that mention the `Any` annotations, then the full rebuild and tests.

*ran: Find docs referring to B19 or Any annotations*

*ran: See how step 1 and 2 recorded their items*

*ran: Locate the step Done notes in the HLD*

Now the spec example, the CLAUDE.md line, the HLD note and the backlog.

*ran: Update spec, docs, backlog; rebuild bin*

*ran: Run full test suite and all linters*

*ran: Show changed files*

Step 3 (nested `fn`s typed, B19) is built but not committed; say gawc to commit it and tag `boot/46`. The full suite passes (486 passed, 5 expected failures), every linter is clean, and `bin` is rebuilt.

- **Nested `def`s are typed.** `SLocalFunc` now carries its `fn`'s type, and `emit` writes the parameter and return types from it, the same way it does for a `defn`. For example, `def _cdy_t2(acc: int, sh: Shape) -> int:`. Inside a generic `defn`, the nested `def` uses the outer type variables, as in `def _cdy_t3(y: a) -> bool:`.
- **Unsolved types:** a type variable the checker never solved is written as `Any`, as Question 2 decided.
- **Macro code keeps `Any`:** the checker doesn't check it (B42), so its `fn`s have no types to write.
- **One addition beyond the HLD's wording:** a `fn` bound by `let` that stays a Python `lambda` now gets its type on the assignment, `sq: Callable[[int], int] = (lambda x: (x * x))`.
  - This is B19's own repro, which mypy used to reject with "Call to untyped function".
  - Locals are already renamed apart within a function, so no name gets annotated twice.
  - It's the one place where generated Python changes outside nested `def`s; the step's *Done* note says so.
- **What mypy found:** nothing. The translator itself has no nested `def`s or `let`-bound `lambda`s, so `bin` changes only in `emit`'s own code. I checked by hand a small program with nested `def`s in both a plain and a generic `defn`, and the same-name `let`-bound `fn`s in two branches: it passes `mypy --strict`.
- **Spec:** the `checking.locals` example now calls a `let`-bound `fn`, `(put (let ((sq (fn (x) (* x x)))) (sq 3)))`, which the spec couldn't show before.
- **Docs and backlog:**
  - I updated CLAUDE.md's line about `Any` annotations now rather than in step 5, because it was no longer true.
  - The HLD has step 3's *Done* note.
  - B128 is in `review`, and B19 is `done` (`fixed: typed-core`).

## Owner

> gawc, are there now test cases for the unresolved types? and can we go over those cases after this branch?

## Claude Code

*ran: Commit step 3 and tag boot/46*

Committed. Now checking what tests the unresolved types have.

*ran: See what the typed-node test asserts about ?N*

*ran: Read the test's setup to reuse it*

*ran: Read the test's Core-building lines*

*ran: List the translator's nodes with unsolved types*

*ran: List the translator's nodes with unsolved types*

Step 3 is committed as `c5a8b0d` and tagged `boot/46`. The bootstrap check passed and the tag is annotated.

**Tests for unresolved types: no, not directly.** `test_every_node_is_typed` checks that the checker reached every node and that every `fn` has a function type. Nothing tests that an unsolved type variable (a `?N`) stays in Core as a type variable, or that Python writes it as `Any`. I only checked that by hand, in step 3's throwaway programs under `tmp/`.

The translator's own code has 8 nodes with an unsolved type, all of one kind:

- **`map-keys` on a map whose value type is `Any`:** three calls, in `core.cdy` (lines 1065 and 1118). The checker can't tell the value type, so it stays unsolved.
- **`expand.cdy` lines 278–283:** `map-get` on `loaded`, a `(Map String Any)`, gives `run` an unsolved type. That spreads to the `fn` around it, to the call, and to both uses of `run`.

So it's the same cause each time: in the checker, `Any` matches everything without fixing the variable it meets. Other ways a type stays unsolved don't occur in the translator but would in other programs, such as a `fn` that's never called or an `empty-list` nothing is ever added to.

**Going over them after this branch: yes.** I'd add a backlog item, a `task` with its notes on these cases, in step 4's commit. It would cover:

- tests for each case: the type stays a variable in Core, and Python writes `Any`;
- whether `Any` should fix a variable it meets (as `Any`) rather than leave it unsolved.

The second point overlaps `semantics`' plans to cut `Any` down (B18), so it may land there rather than as a separate review.

Step 4 is next: B119's messages, and the rest of B14 (`main`'s position, positions in `format` holes, and marking `lower`'s and `emit`'s errors as internal). Say go when you want it.

## Owner

> go

## Claude Code

*ran: Read B119, B14 and B129*

*ran: See what the HLD says about step 4's details*

*ran: Read the HLD's messages proposal*

Starting with B119, the variant-as-type message.

*ran: Find check-type and its import message*

*ran: Read Scope and check-type*

*ran: Read Scope's variants field type*

*ran: Read VInfo and spec's types.exist*

*ran: Fix B119's message, add spec examples, try them*

*ran: See how fixed defects' repros were handled*

B119 now says "A is a variant of S, not a type" / "X is a value, not a type". Checking the process rule for a fixed defect's repro, then on to B14.

*ran: Read the process rule for repros*

*ran: Find main's type error and lower/emit fails*

*ran: See user-reachable lower/emit errors and their output*

*ran: Find how format holes are read*

*ran: Read the reader's position machinery and format analysis*

Now the `format` holes: I'll give the reader a starting position so forms read from a hole get real positions.

*ran: Find all users of read-forms and the parse hook*

*ran: Read how parse is threaded through cdyc*

*ran: Find parse's type sites and string helpers*

*ran: Thread hole positions through the reader and format*

*ran: Check emit's imports for pos-text*

*ran: Position main's errors; mark internal errors*

Main's errors now have positions and the internal errors say so. Next: the operator-as-value error at its position, then build and test.

*ran: Position operator-as-value error; update tests' parse hook*

Now some quick checks of the new positions with T1.

*ran: Build T1 and try the new error positions*

*ran: Find the 1-arg parse function*

*ran: Fix blank-scope's parse and retry*

All the positions are right (the hole one checked against the column count by hand). Adding tests for them, then rebuilding.

*ran: Look at existing error-position tests*

*ran: Add tests for the new error positions*

*ran: Check next backlog id and item format*

*ran: Update backlog: B119, B14 done, B129 review; add B131, B132*

*ran: Check the item endings*

Now the HLD's step 4 note, then rebuild and the full run.

*ran: Rebuild bin and run all tests and linters*

*ran: Show the two failures and the pylint warning*

*ran: Register new items; show the hole test's actual message*

*ran: Reproduce the failing hole-position case*

The translator is right here: the error is at the symbol `f`, column 5; my expected column was wrong.

*ran: Fix the expected column and format the test*

*ran: Rerun the full suite and linters*

My sed also hit an existing test case's expected text. Restoring it.

*ran: Find the accidentally changed test line*

*ran: Restore the original expectation and rerun tests*

Step 4 (the messages) is built but not committed; say gawc to commit it and tag `boot/47`. The full suite passes (494 passed, 4 expected failures, one fewer because B119's repro now passes and moved into the spec), the linters are clean, and `bin` is rebuilt.

- **B119:** a variant or a value written as a type now says what it is. `(sig a A)` gives `A is a variant of S, not a type`, and a capitalised value gives `X is a value, not a type`. Both are now examples in the spec's `types.exist` rule.
- **`main`:** "main must be a defn" and "main must be typed …" now say where `main` is defined.
- **`format` holes:** forms inside a `{…}` hole now have their own positions, so an error in a hole points into the string. For example, `(+ x "b")` in a hole now reports at `2:18` instead of at the `(format …)` form.
  - This is right on later lines of a multi-line string too.
  - An escape (`\"`, `\n`) before a hole on its line puts the column one short per escape, *for now*. This is because the position is counted from the string's value, not its source text.
  - The brace errors ("unmatched {", "a hole can't hold a brace") are now at the `(format …)` form; before, they had no position at all.
- **Internal errors:** `lower`'s and `emit`'s errors, which no program should reach, now start with `internal error:` and keep no position, as the HLD decided (*lasting*).
- **One extra:** "the operator + can't be used as a value" is now at the operator.
- **Tests:** four new cases in `test_errors_say_where` (two hole errors, an unmatched brace, the operator), and a new `test_main_errors_say_where`.
- **Backlog:**
  - B14 and B119 are `done`, and B129 is in `review`.
  - **New, B131 (defect, low):** what B14 leaves. `emit`'s errors for two names that are one Python name, and for a field Python can't spell, still have no position, because a `deft` has none. B131 also tracks the escape-column issue.
  - **New, B132 (task):** the review of unsolved types you asked for, for after this branch. It lists the translator's eight cases, all `Any` meeting a type variable, and the cases where nothing fixes a variable. It asks for a test for each and a decision on whether `Any` should fix the variable it meets.

## Owner

> need some help w/ b119... where's the `sum` ref'd a `S`?

## Claude Code

*ran: Find where VInfo's sum is filled*

*ran: Read find-variants*

The `S` in the message is the sum's name as written in its `deft`. The new check doesn't work it out; it reads it from a table that `core.cdy` builds before analysing anything.

**The message** (`check-type`, `src/cdy/core.cdy`):

```
((map-has (get scope variants) name)
  (fail (located scope (format "{name} is a variant of {(get (map-get (get scope variants) name) sum)}, not a type"))))
```

In `(get … sum)`, `sum` isn't a variable. It's the name of a field, which `get` reads from the record that `map-get` returns. Reading from the inside out:

1. `(get scope variants)` is the scope's `variants` field, a `(Map String VInfo)` (`core.cdy:71`).
2. `(map-get … name)` looks up `A` and gives its `VInfo`.
3. `(get … sum)` reads that record's `sum` field, which here is `"S"`.

**The record type**, at `core.cdy:105`:

```
(deft VInfo ((sum String) (fields (List String))))
```

**Where it's filled:** `find-variants` (`core.cdy:827`) runs over a module's forms before analysis (it's called at `core.cdy:1022`). For each `(deft S (A …) (B …))` whose body lists variants:

- it reads the sum's name from the `deft`'s second item, `(deft-name (at items 1))`, which gives `"S"`;
- `add-variants` then stores `(VInfo "S" fields)` under each variant's name, `A` and `B` (`core.cdy:853`):

  ```
  (assoc scope variants (map-set (get scope variants) name (VInfo sum fields)))
  ```

  There, `sum` is `add-variants`' parameter, the `"S"` passed down from `find-variants`.

So for `(deft S (A ((x Int))) (B ((y Int))))`, the scope ends up with `variants = {A: (VInfo "S" ("x")), B: (VInfo "S" ("y"))}`. The `match` code already reads this map for its own errors, the same way: `match-sum` at `core.cdy:509` and "clauses mix variants" at `core.cdy:571`. So the B119 check reuses it rather than adding anything new.

If the problem is that the inline `get`/`map-get` chain in the `format` hole is hard to read, I can pull it out into a small helper like `variant-sum`, next to `variant-fields` at `core.cdy:112`.

## Owner

> so, can you repro or reference that `deft` of `S` in the bug...?

## Claude Code

*ran: Show B119's original repro and run it before and after*

The stash didn't run, so the working tree is untouched. `bin` is already rebuilt, so that first run shows the new message. Getting the old behaviour from `boot/46` instead:

*ran: Run B119's repro with boot/46's translator*

Yes, it reproduces. `S` is defined on the first line of B119's own repro, which I moved out of the item in this step. That's why the item no longer shows the `deft`.

**The repro**, as it was in B119's `## Repro` section (the version committed at `boot/46`):

```
(deft S (A ((x Int))) (B ((y Int))))
(sig a A)
(def a (A 1))
```

That `deft` defines a sum `S` with two variants, `A` and `B`. `(sig a A)` then uses the variant `A` as if it were a type.

**Before (`boot/46`'s translator):**
```
candy: tmp/s3/b119.cdy:2:1: A is not defined here; b119 defines it, but this file doesn't import b119
```
This is the bug: it names the file itself, `b119`, as a module it should import.

**After (this step's translator):**
```
candy: tmp/s3/b119.cdy:2:1: A is a variant of S, not a type
```

**Where it lives now:** the process says that once a defect's repro passes, the example moves into its spec file and the item is `done`. So I removed the `## Repro` section from B119, and the same program is now an example in `spec/20-types.md:64`, under `types.exist`:

```
(deft S (A ((x Int))) (B ((y Int)))) (sig a A) (def a (A 1)) => A is a variant of S, not a type
```

The catch is that B119 now reads "A is a variant of S" without showing where `S` comes from. Its prose only mentions "`A` a variant of `S`", and its new note just says the repro moved. I can fix the item in either of two ways before the commit:

1. Keep the `## Repro` block in B119 as history, but with a plain `cdy` fence so it no longer runs as an expected failure.
2. Give the spec example in B119's note directly, such as "the repro, `(deft S (A ((x Int))) (B ((y Int)))) (sig a A)`, is now in `spec/20-types.md`'s `types.exist`".

I'd go with option 2, since it keeps one runnable copy, in the spec. Which do you want?

## Owner

> option 2, but can we add part(s) that was removed to the notes... leaning toward verbose... this might be a bad idea... again, and am sorry, navigation is still poor... so whatever we can do... even if its' a note in your summaries in this cli as a hint until we figure a better solution

## Claude Code

*ran: Check B119's ending and how fences are read*

*ran: Check B119's ending and how fences are read*

*ran: Write B119's verbose note and recheck docs tests*

*ran: Tidy the note's wording and recheck*

Now saving the navigation preference to memory so it carries over between sessions.

*wrote: `~/.claude/projects/-home-skerrj-dev-exp-candy/memory/navigation-hints.md`*

*ran: Index the memory; get line hints for the summary*

*ran: Get line numbers for the summary*

I've expanded B119's note as you asked; it's all still uncommitted with the rest of step 4. The backlog and doc-link tests pass.

The note (under `## Notes` in `backlog/B119-variant-as-type-message.md`, line 19) now has:
- **How it was fixed:** `check-type` looks the name up in the scope's `variants` map, which `find-variants` fills and which gives the sum's name. For a value, it looks in `top`. The fix is at `src/cdy/core.cdy:1256`.
- **Where the repro went:** both spec rows, copied out:
  - `spec/20-types.md:64` is the `deft S` case.
  - Line 65 is the value case.
- **The removed `## Repro` section, word for word,** including the `(deft S (A ((x Int))) (B ((y Int))))` line that `S` comes from.
- **Before and after:**
  - At `boot/46` it said `A is not defined here; b119 defines it, but this file doesn't import b119`.
  - Now it says `A is a variant of S, not a type`.

The copies sit in plain `text` blocks, so the spec runner doesn't treat them as tests. Only the spec rows run.

About navigation, no need to apologise; it's a fair point. I've saved it to my memory for this project, so it carries into later sessions. From now on:
- When something is moved or removed, I'll keep it word for word in a dated note and say where it went.
- My summaries will give `file:line` pointers, with rule and backlog ids, so you can jump straight there.

Step 4 is still ready for gawc, which commits it and tags `boot/47`.

## Owner

> gawc

## Claude Code

*ran: Commit step 4 and tag boot/47*

Step 4 is committed as `806e499`, "typed-core step 4: the messages", and tagged `boot/47`. The bootstrap check passed, the tag is annotated, and the working tree is clean. The commit holds only the step 4 files; I found no edits of yours to include.

What went in:
- **The fixes:**
  - B119's message: `src/cdy/core.cdy:1256`.
  - `main`'s positions: `is-main`, in `core.cdy`.
  - Positions in `format` holes: `read-hole` in `src/cdy/read.cdy`, plus `text-pos` and `format-parts` in `core.cdy`.
  - Internal errors marked: in `src/cdy/lower.cdy` and `src/cdy/emit.cdy`.
- **The spec:** the two rows are at `spec/20-types.md:64-65`, under `types.exist`.
- **The backlog:**
  - B14 and B119 are `done`; B119's note keeps the old repro word for word.
  - B129 is in `review`.
  - B131 and B132 are new.
- **The HLD:** step 4's *Done* note is in `doc/hl_rqmt/typed_core.md`.

Nothing is pushed: the `typed-core` branch, `boot/44` to `boot/47`, and master's `b2c0ad7` are all local.

Step 5, the docs (B130), is the last one. It brings CLAUDE.md's "How the translator works", the iMVP doc's layers, `multi_target.md`, `type_checker.md` and `python_complete.md`'s triage up to date. It also closes B15 and splits off its two new items, let-polymorphism (an `idea`) and one error at a time (a `leak`). Say go when you want it.

## Owner

> go

## Claude Code

*ran: Read B130, B15 and where B15 is linked*

*ran: Read the epic's triage and mypy plans*

*ran: Locate the doc sections to update*

*ran: Read type_checker header and iMVP layers section*

Writing the two new items and closing B15, then the doc updates.

*ran: Add B133/B134, close B15, repoint links*

*ran: See how the triage table marks groups and later items*

*ran: Read the groups table and the triage's end*

*ran: Update the triage, HLD headers, layers and CLAUDE.md*

*ran: Find remaining stale lines and step 5 in HLD*

*ran: Check when an HLD's status becomes done*

Docs for step 5 are mostly updated (B15 closed and split into B133/B134). Checking when the HLD's status turns "done", then the step's note and the tests.

*ran: Read the status-word rule and merge steps*

*ran: Read the lifecycle steps before merge*

*ran: Write step 5's note, B130 to review, run everything*

*ran: Gather file:line pointers for the report*

Step 5 (the docs) is done but not committed; say gawc to commit it. It changes nothing in `bin/`, so it gets no `boot/NN` tag. The full suite passes (494 passed, 4 expected failures) and the linters are clean.

**B15 is closed and split.** Its note (`backlog/B15-no-type-checker.md:35`) maps each part it listed to the item that now tracks it:

| B15's part | Now |
|---|---|
| mypy still checks the Python | B125 (each target's own checker, as an option), and whether mypy stays is decided in `porting-surface` |
| no let-polymorphism | **B133**, new: an `idea`, low, for after the epic |
| a type not known yet when `get` uses it | B120, in `semantics` |
| no narrowing in a `match` clause | B121, in `semantics` |
| it stops at the first error | **B134**, new: a `leak`, low. The checker already collects its errors in a list, so reporting them all is mostly a driver change |

**Links that pointed at B15** as a *for now* now point at its successors:
- `spec/25-checking.md:81` → B133;
- `spec/20-types.md:73` → B125;
- CLAUDE.md's note on mypy → B125.

**Docs:**
- **`CLAUDE.md`:**
  - line 35, "Type checking", describes typed Core: every node ends with a position and then its type; how the checker fills the types; an unsolved type becomes `Any` in Python. It links B133 and B134.
  - line 36, "Errors", says every form and node has a position, and internal errors say `internal error`.
  - "History" names the epic and this branch.
- **`python_complete.md`:** a note in "Where things stand" (line 21). The triage's intro says what this branch closed and found (line 519), and its table has the four new items, each marked *(typed-core)* (lines 537, 602, 603, 607).
- **`type_checker.md:8`, `multi_target.md`, the iMVP doc's layers (line 524):** each gets a dated *(Since `typed-core` …)* aside. I didn't rewrite their history.
- **`typed_core.md:245`:** step 5's *Done* note. B130 is in `review`.

After this commit, the branch's next stage is your review of the five `review` tasks (B126–B130). Then I'd:
1. set the HLD's status to *done*;
2. run `pytest -m bootstrap`;
3. merge into master and tag `typed-core`;
4. push when you say.

## Owner

> gawc

## Claude Code

*ran: Commit step 5*

Step 5 is committed as `5562418`, "typed-core step 5: docs", and the working tree is clean. It doesn't touch `bin/`, so it gets no `boot/NN` tag.

All five steps of `typed-core` are now committed:

| Step | Commit | Tag |
|---|---|---|
| 1, positions | `3d2260d` | `boot/44` |
| 2, types in Core | `ddcf686` | `boot/45` |
| 3, nested `fn`s typed | `c5a8b0d` | `boot/46` |
| 4, the messages | `806e499` | `boot/47` |
| 5, docs | `5562418` | none |

Nothing is pushed: the branch, `boot/44` to `boot/47`, and master's `b2c0ad7` are all local.

Next is your review of B126 to B130, the five step tasks now in `review` (the list is in `backlog/README.md`). Tick each one and I'll mark it `done` with your note. After that:
1. I set `typed_core.md`'s status to *done*.
2. I run `pytest -m bootstrap`.
3. I merge into master and add the annotated tag `typed-core`.
4. I push when you ask.

## Owner

> let's start the review with B126

## Claude Code

*ran: Read B126, step 1's Done note and its commit stats*

*ran: Gather file:line pointers for B126's review*

*ran: Show leaf-error positions before and after step 1*

**B126 is step 1: positions on literal forms and on Core's leaves.** It's commit `3d2260d`, tagged `boot/44`. It fixed two items: B59 (only symbols and lists carried positions) and B122 (an error in a leaf was reported at its parent).

**What it does: an error is now reported at the literal or name it's in, not at the form around it.** I ran both translators on two small programs; "before" is `boot/43`, the last tag before this step:

```
(sig x Int)                before: r1.cdy:2:1: def x: expected Int, got String
(def x                     after:  r1.cdy:3:3: def x: expected Int, got String
  "a")

(sig f (Fn (Int) Int))     before: r2.cdy:3:6: argument 1 of f: expected Int, got String
(defn f (n) n)             after:  r2.cdy:4:3: argument 1 of f: expected Int, got String
(put (f
  "s"))
```

**Where to look, in reading order:**

1. **The forms** (`src/cdy/form.cdy:14-24`): every literal form (`Txt`, `IntLit`, … `BoolLit`) now ends with `(pos Pos)`, like `Sym` and `Lst`. `form-pos` (`form.cdy:46`) gives any form's position.
2. **The reader** (`src/cdy/read.cdy`): it fills those positions. A string's position is its opening `"`. `number-form` (`read.cdy:176`) takes the position as `where`, because `at` would have hidden the built-in of that name.
3. **Core's leaves** (`src/cdy/core.cdy`):
   - `Local`, `Global`, `Prim` and `Do` end with a `pos`; `Lit` reads its form's.
   - A `Local` is bound with the position of its name, and `at-use` (`core.cdy:149`) rebuilds it with each use's position.
   - Nodes the translator makes itself, like `NIL` or a quoted form's builders, are `NOWHERE`.
4. **The checker** (`src/cdy/check.cdy:188`): `node-pos` now covers the leaves, so it reports at the leaf. This is B122's fix.
5. **Macro expansion** (`src/cdy/expand.cdy:366`): `form-at` gives an expansion's literals the call's position, as `stamp` already did for symbols and lists.
6. **A bug this step caused, and its fix** (`src/cdy/lower.cdy:499`):
   - A self tail call becomes a loop that rebinds only the parameters that change. `lower` found the unchanged ones by comparing whole `Local`s.
   - Those now differ in position, so every parameter got rebound.
   - `same-local` compares name and id instead.

**The one change macro writers see** is at `spec/50-macros.md:48-49`, the `macros.macro-code` example. Macro code that builds a literal by hand now passes a position: `(Txt (sym-name s) NOWHERE)`. The test macro files `tst/cdy/cdyc/lib/control.cdy` and `tst/cdy/cdyc/macro_code/quoting.cdy` changed the same way.

**Tests:**
- The spec gained an example (`spec/25-checking.md:39-46`): the error at a string literal, "line 3, column 3".
- `test_reader_positions` (`tst/py_cdy/test_self_host.py:583`) checks the literals' positions.

**Output:** every test program translates to the same Python as before, except `macro_files.cdy`. Its macro file now builds the new forms, so the old `bin` can't translate it.

**The record:**
- the HLD's *Done* note for step 1, in `doc/hl_rqmt/typed_core.md`;
- the notes in `backlog/B59-positions-symbols-lists.md` and `backlog/B122-leaf-error-position.md`.

Say tick if it looks right, or tell me what to look at more closely; then B127.

## Owner

> tick

## Claude Code

*ran: Tick B126 and rewrite the index*

B126 is ticked. Now B127.

*ran: Gather file:line pointers for B127*

*ran: Read the core of step 2's checker changes*

**B127 is step 2: types in Core.** It's commit `ddcf686`, tagged `boot/45`. It changes no behaviour on its own: every Core node now carries its type, for `emit` (step 3) and the epic's later branches to read.

**Where to look, in reading order:**

1. **The field** (`src/cdy/core.cdy:20-35`): every `Expr` variant ends with `(t CType)`, for example `(Lit ((form Form) (t CType)))`. `analyse` fills it with `ANY` (`core.cdy:38-39`, moved here from `check.cdy`).
   - A throwaway script added the field at about 180 match and construction sites.
   - Those edits are why the diff is wide but shallow: most of it is a `_` added to a pattern, or an `ANY` to a constructor.
2. **How the checker fills it** (`src/cdy/check.cdy:647-700`, the "typed Core" section; its comment at `check.cdy:649-654` explains the scheme). Inference itself wasn't rewritten; it gained recording points, and the work happens in three phases in `check-tops` (`check.cdy:55-61`):
   1. **Numbering:** `retype-top` sets each node's `t` to a unique placeholder, `?e0`, `?e1`, …
   2. **Recording:** as the checker finds each node's type, `typed` (`check.cdy:658`) stores it under that placeholder, in a new map in the checker's state (`St`'s `types`, `check.cdy:30`).
      - It's kept out of the substitution because `map-set` copies the whole map, and the substitution is consulted on every unification.
   3. **Resolving:** `retype-top` runs again with `node-type` (`check.cdy:690`). Each node gets its recorded type with the definition's final substitution applied.
3. **The recording points:**
   - `infer` (`check.cdy:211`) wraps the old `infer-node` and records every inferred node.
   - `check-expr` records its check-mode cases: `if`, `do`, an applied `fn` and a `fn`.
   - Binders are recorded with `typed-all` and `typed-binds` (`check.cdy:664`, `669`): parameters, `let` names, and the names a `match` clause binds.
   - Callees the checker doesn't infer (an operator, a `tup` pattern's `at`, a `let`'s `fn`) are recorded with `typed-callee` (`check.cdy:678`), as the function from their arguments' types to the result's.
4. **The interface:** `type-check` (`check.cdy:43`) now returns the typed tops instead of the ones it was given, and `check-program` (`check.cdy:49`) returns the tops and the errors.
5. **`lower` keeps the types** on the nodes it rebuilds: `value-fn`, `value-call`, `value-boolop` and `value-if` (`src/cdy/lower.cdy:155`, `197`, `213`, `283`) take a `ty`. The `Temp` that stands for a `match` or a nested `fn` gets that node's type; other `Temp`s are `ANY`.

**A deviation from the HLD:** the HLD said "`infer` returns the node rebuilt". Numbering, recording and resolving gives the same result with a much smaller change to `check.cdy`. The *Done* note (`doc/hl_rqmt/typed_core.md`, step 2) records this.

**Checks:**
- **The test:** `test_every_node_is_typed` (`tst/py_cdy/test_self_host.py:409`) runs on the translator's own Core, 23,280 nodes:
  - No node keeps its `?eK` placeholder, so the checker reached them all.
  - Every `fn` has a function type.
  - I confirmed it fails when callee recording is removed.
- **Output:** byte for byte the same Python as `boot/44` for every test program.
- **Cost:** `self_host.py` takes 3.6 s, up from 3.0 s.
- **What's left:** eight nodes in the translator end up with an unsolved type variable (the step-2 report said three, but my later count found eight). That's allowed by Question 2; going over them is B132, after the branch.

Say tick, or point me at anything to look into; then B128.

## Owner

> tick; an aside: can we archive each branch chat for this epic?

## Claude Code

*ran: Tick B127; look at the session transcripts*

*ran: Look at the existing chat archives*

*ran: Measure the transcript's chat text by git branch*

B127 is ticked.

On archiving: yes, it's doable, and there's a precedent. `doc/archive/` already holds two side conversations, `chat_get_on_sums.md` and `chat_spec_by_example.md`, and `doc/process.md:187` sets the format: owner and Claude turns verbatim, with a note at the top saying when, where and what came of it.

**The raw material.** This one session's transcript goes back to the project's start, 2026-10-07, and every entry records the git branch it happened on. So it can be split per branch. Counting only owner and Claude text (no tool calls or output), each branch is small:

- `typed-core` so far: about 46 KB (16 owner turns, 64 replies);
- `type-checker`: about 68 KB;
- the largest is `master`'s, about 290 KB, since HLDs, triage and the epic were written there;
- the whole transcript is 210 MB, almost all of it tool output.

**What I'd build:**
- a small script, `script/chat_archive.py`;
- it reads the transcript and keeps your messages and my replies verbatim;
- it drops tool calls, tool output, my thinking and the system's reminders, and marks where a context summary replaced earlier turns;
- it writes one file per branch, `doc/archive/chat_<branch>.md`, with the usual note at the top: the dates, the HLD, and the tag.

For this epic I'd run it as part of each branch's docs step, or just before its merge. `typed-core`'s archive would go in now, before the merge. The epic's own planning chat happened on `master`, so I'd cut that span out by date (from the start of `python_complete.md`) as its own file.

Three decisions for you:
1. **In the repo or not?** Tracked under `doc/archive/` matches the precedent, but the files get pushed to the backup remote. The alternative is somewhere untracked, like `tmp/` or outside the repo.
2. **This epic only, or backfill every branch since `py-py-translator`?** The backfill is the same script, run once.
3. **Tool activity:** leave it out entirely, or keep a one-line marker per tool call (say, "*ran: pytest*") so the replies read in context?

My recommendation: tracked, this epic only plus `type-checker`, and one-line markers. If you agree, I'd add the archive as a small extra commit on `typed-core` before the merge.

Next in the review is B128, nested functions typed.

## Owner

> agree w/ recommended; let's do B128

## Claude Code

*ran: Gather file:line pointers for B128*

Before/after on the step's examples, with `boot/45`'s translator as "before":

*ran: Diff nested-fn output before and after step 3, with mypy*

**B128 is step 3: nested functions typed.** It's commit `c5a8b0d`, tagged `boot/46`, and it fixed B19 (a nested `fn` got `Any` annotations).

**What changes.** A local `fn` used to reach Python as `Any`, so mypy checked nothing inside it. It now gets the type the checker inferred. On the test program from the step (`tmp/s3/a.cdy`, which has nested `fn`s in a plain `defn` and in a generic one, plus two `let`-bound ones), the whole diff between `boot/45`'s translator and today's is:

```
<     def _cdy_t2(acc: _cdy_Any, sh: _cdy_Any) -> _cdy_Any:
>     def _cdy_t2(acc: int, sh: Shape) -> int:            # fn inside total's fold
<     def _cdy_t3(y: _cdy_Any) -> _cdy_Any:
>     def _cdy_t3(y: a) -> bool:                          # inside generic pick[a]
< sq = (lambda x: (x * x))
> sq: _cdy_Callable[[int], int] = (lambda x: (x * x))    # let-bound fn, a lambda
< def _cdy_t4(x: _cdy_Any) -> _cdy_Any:
> def _cdy_t4(x: int) -> int:                             # let-bound fn, a def
```

`mypy --strict` on the old output fails with "Call to untyped function (unknown) in typed context", B19's own repro. On the new output it passes.

**Where to look:**
1. **`src/cdy/lower.cdy:24`:** `SLocalFunc` ends with `(t CType)`, its `fn`'s type. It's set at `lower.cdy:160` from the `Lambda`'s type, which step 2 put there.
2. **`src/cdy/emit.cdy:481`:** a nested `def` takes its parameter and return types from that `TFn`, as a `defn` does. Inside a generic `defn` it uses the outer type variables (`y: a`), which Python's PEP 695 puts in scope.
   - When the type isn't a function type, which happens only for macro code since the checker doesn't check it (B42), it falls back to `Any` (`emit-any-params`, `emit.cdy:524`).
3. **`emit.cdy:406`:** `emit-type` writes an unsolved `?N` as `Any`, as Question 2 decided.
4. **`emit.cdy:497`:** `lambda-annotation`. A local bound to a `fn` that stays a Python `lambda` gets the type on its assignment.
   - This goes beyond the step as written; it's B19's repro.
   - It's safe because locals are renamed apart within a function, so no name is annotated twice. I checked same-named `let`-bound `fn`s in two branches of an `if`: `g` and `_cdy_g_4`.
5. **The spec (`spec/25-checking.md:86`):** the `checking.locals` example now calls a `let`-bound `fn`, `(put (let ((sq (fn (x) (* x x)))) (sq 3)))`. The spec couldn't show that before, because mypy rejected it.

**What mypy found:** nothing new. The translator itself has no nested `def` or bound `lambda`, so `bin` changed only in `emit`'s own code.

**The record:**
- step 3's *Done* note, at `doc/hl_rqmt/typed_core.md:202`;
- B19's closing note.

Say tick, or point me at anything; then B129. I'll do the chat archive (`script/chat_archive.py`, tracked, the epic plus `type-checker`, one-line markers for tool calls) after the review, before the merge.

## Owner

> 2. src/cdy/emit.cdy:481: a nested def... Curious about this... Wondering how it got there

## Claude Code

*ran: Trace how a fn becomes a nested def, and its history*

A nested `def` is how a Candy `fn` reaches Python when its body can't be a single Python expression. The mechanism dates from 2026-10-17 and is older than this branch; step 3 only gave it types.

**Why a `fn` sometimes can't be a `lambda`.** A Python `lambda` holds one expression. Some Candy forms become statements in Python, so a `fn` that uses one needs a real `def`:
- `match` becomes an `isinstance` chain;
- `do` becomes several statements;
- `let` becomes assignments.

In the test program, the `fn` inside `total`'s `fold` has a `match`:

```
(fn (acc sh) (+ acc (match sh ((Circle r) (* 3 r r)) ((Sq s) (* s s)))))
```

**How it gets there, stage by stage:**

1. **`analyse`** (`core.cdy`) makes it a Core `Lambda`, with params `acc`, `sh` and the body.
2. **`type-check`**, as of step 2, records its type in the `Lambda`'s `t`: `(Fn (Int Shape) Int)`.
3. **`lower`** decides between a `lambda` and a `def` in `value-fn` (`src/cdy/lower.cdy:155-160`):
   ```
   (let (((stmts n1) (tail body n)))
     (match (if (= (len stmts) 1) (at stmts 0) (SExpr NIL))
       ((SReturn result) (Low empty-list (Lambda params result pos ty) n1))
       (else
         (Low (to-list (SLocalFunc (Temp n1 ty) params stmts ty)) (Temp n1 ty) (+ n1 1)))))
   ```
   - It lowers the body in tail position. If that comes out as exactly one `return e`, the `fn` stays a `Lambda`, which becomes a Python `lambda`.
   - Otherwise it becomes a statement, `SLocalFunc`, named by a fresh temporary, `Temp n1`, which becomes `_cdy_t2`.
   - The `fn`'s place in the expression is taken by that `Temp`: the statement goes before the expression, and the expression refers to the name.
   - Step 3's change is the last `ty`: `SLocalFunc` now carries the `Lambda`'s type.
4. **`emit`** (`src/cdy/emit.cdy:481`) writes the `SLocalFunc` as `def _cdy_t2(acc: int, sh: Shape) -> int:` with the body indented. The types come from that `ty`, a `TFn`, through `emit-params`, the same helper a `defn` uses. Before step 3 it ignored the type and wrote `_cdy_Any` for everything. The `else` branch still does, for macro code, which isn't checked.

The result (`tmp/s3/after.py`):

```python
def total(shapes: tuple[Shape, ...]) -> int:
    def _cdy_t2(acc: int, sh: Shape) -> int:
        _cdy_t1: object = sh
        if isinstance(_cdy_t1, Circle):
            r = _cdy_t1.r
            _cdy_t0 = (3 * r * r)
        else:
            assert isinstance(_cdy_t1, Sq)
            s = _cdy_t1.s
            _cdy_t0 = (s * s)
        return (acc + _cdy_t0)
    return cdy_rt.primitives.list_fold(_cdy_t2, 0, shapes)
```

The `fold`'s `fn` argument has become `_cdy_t2`, the name the `def` defines just above it.

**Its history:**
- **2026-10-17, `acdcade`** ("Stage 1b: T1 handles let, fn, tup, format, get/assoc and deft records", on `pre-self-host`): `SLocalFunc` first appears, in the Candy translator. It followed the iMVP design, `doc/hl_rqmt/iMVP_py_translator.md`, under "`fn`" (around line 872): a `fn` "becomes a nested `def _cdy_fnN(...)`, which is added to the statements".
- **From then until step 3** it was annotated `Any`, because nothing knew the `fn`'s type. That's what B19 recorded.
- **`2d76e2b`** (Stage 1d, the same day) added the closure check that uses it. `stmts-have-closure` (`lower.cdy:531`) treats an `SLocalFunc` as making a closure, so a `defn` that contains one isn't turned into a tail-call loop.

Say tick if that settles it, or ask more; then B129.

## Owner

> Sorry, a nested python `def`... Read it as a nested candy `def`

## Claude Code

No need to apologise: my wording was ambiguous. That item meant a nested *Python* `def`. Candy has no nested `def`; `def` and `defn` are top level only (CLAUDE.md, "Decisions that fill gaps in the spec"). What I traced above is a Candy `fn` whose body needs statements, which `lower` turns into a Python `def` inside the enclosing Python function.

"Nested `def`" in this branch's docs always means the Python one, and the same ambiguity is in several places:
- the HLD (`doc/hl_rqmt/typed_core.md`, its Goals and step 3's *Done* note);
- B19's and B128's notes;
- CLAUDE.md's checking line, which now says "a nested Python `def`, or a `lambda` bound by `let`";
- the comment at `src/cdy/lower.cdy:23`.

Two ways to make it unambiguous:
1. Say "a nested Python `def`" every time in this branch's docs and comments.
2. Rename the IR statement too: `SLocalFunc` to something like `SNestedPyDef`. That's more churn, and the IR is meant to be target-neutral, so a Python name in it would be odd.

I'd do option 1, as a small fix in the review (no `bin` change, so no boot tag). I'll also say "Python `def`" or "Candy `defn`" explicitly in my summaries from now on.

Want that fix, and then tick B128? Or is there more on it?

## Owner

> Tick b128

## Claude Code

*ran: Tick B128; gather pointers for B129*

Before/after on step 4's cases, with `boot/46`'s translator as "before":

*ran: Run step 4's error cases before and after*

B128 is ticked. I didn't make the "nested Python `def`" wording fix, since your tick didn't mention it; say if you want it done in the review.

**B129 is step 4: the messages.** It's commit `806e499`, tagged `boot/47`. It fixed B119 and the rest of B14. Here are its cases, each run on `boot/46`'s translator and on today's (the programs are in `tmp/s3/`):

| Case | Before (`boot/46`) | After |
|---|---|---|
| `(sig a A)`, `A` a variant of `S` (B119) | `2:1: A is not defined here; b119 defines it, but this file doesn't import b119` | `2:1: A is a variant of S, not a type` |
| `(put (map + (tup 1)))` | no position | `1:11: the operator + can't be used as a value yet; …` |
| `(sig main Int) (def main 1)` | `main must be a defn`, no position | `2:1: main must be a defn` |
| an error inside a `format` hole, `"a {(+ x \"b\")} c"` | `3:6`, the `(format …)` form | `3:18`, the `(+` in the hole |
| a hole on the string's second line | `1:6`, the form | `2:6`, the `x` in the hole |
| `(format "a {x")`, an unmatched brace | no position | `1:6`, the `(format …)` form |

**Where to look:**

1. **B119** (`src/cdy/core.cdy:1243`, `check-type`): two checks now come before the import check.
   - **A variant:** if the name is in the scope's `variants` map, the error names its sum (`core.cdy:1256`). That map is the one `find-variants` fills, which you asked about earlier.
   - **A value:** if the name is in `top`, it's a value.
   - **The spec:** both are rows in `types.exist`, `spec/20-types.md:64-65`. B119's note keeps its old `## Repro` section word for word.
2. **`main`** (`core.cdy:1441`, `is-main`): its two errors use the position of `main`'s definition. `TDef` and `TDefn` have had one since `type-checker`.
3. **`format` holes:**
   - **The reader** (`src/cdy/read.cdy:28`): `Source` gains a `base` field, where the text starts in the file. `read-hole` (`read.cdy:19`) reads a hole's text with `base` set to the hole's position, so the forms in it get real positions.
   - **The hook:** the analyser reads holes through a function passed in (`parse`). Its type is now `(Fn (String Pos) (List Form))`, threaded through `cdyc.cdy` and `core.cdy`'s `Scope`.
   - **Finding the hole:** `text-pos` (`core.cdy:398`) works out the hole's position from the string's opening quote, counting the string value's newlines.
   - **Its limit, for now (B131):** an escape such as `\"` or `\n` before a hole on the same line makes the column one short per escape. That's because the count runs over the value, not the source text.
   - **The brace errors:** `hole-end` (`core.cdy:410`) now reports at the `(format …)` form; before, they had no position.
4. **Internal errors:** `lower`'s and `emit`'s, which no program should reach, now say `internal error: lower: …` or `internal error: emit: …` with no position, as the HLD decided (*lasting*). They're at `src/cdy/lower.cdy:68-69`, `121` and `src/cdy/emit.cdy:244`, `316-317`, `377`.
5. **An extra:** the operator-as-value error is at the operator: `emit-prim` (`emit.cdy:380`) takes the `Prim`'s position.

**What's left goes to B131.** `emit`'s two Python-name errors still have no position: two names that are one Python name, and a field Python can't spell. A Candy `deft` has no position to give them. B131 also has the escape-column limit.

**Tests:** `test_errors_say_where` gains four cases (`tst/py_cdy/test_self_host.py:101-106`), and there's a new `test_main_errors_say_where` (`test_self_host.py:131`).

**The record:**
- step 4's *Done* note in `doc/hl_rqmt/typed_core.md`;
- the notes in `backlog/B14-errors-without-position.md` and `backlog/B119-variant-as-type-message.md`;
- the new items `backlog/B131-errors-without-position.md` and `backlog/B132-unsolved-types-reviewed.md`.

Say tick, or point me at anything; then B130.

## Owner

> an error inside a format hole, "a {(+ x \"b\")} c".... This points to `(+` now... Why?

## Claude Code

*ran: Compare operator vs function argument error positions*

*ran: Read how operator errors get their position*

It points at `(+` because operator errors are always reported at the operator's call, inside a hole or not. What step 4 changed is only that the call inside a hole now has a position of its own, so the error lands on it instead of on the whole `(format …)` form.

The same program outside a hole does the same thing (`tmp/s3/e1.cdy`):

```
(put (+ x
  "b"))        →  e1.cdy:3:6: +: expected Int, got String     (the "(+", not "b" at 4:3)
```

**Why: operators and functions are checked differently** (`src/cdy/check.cdy`):

- **A function call** checks each argument against its parameter's type, one at a time, at that argument's node. So the error lands on the argument. For a function `f` in a hole (`tmp/s3/e2.cdy`):
  ```
  (put (format "a {(f x \"b\")} c"))   →  e2.cdy:5:23: argument 2 of f: expected Int, got String
  ```
  Column 23 is where the `"b"` literal starts.
- **An operator** has no parameter types to check against. `infer-op` (`check.cdy:467`) works in three steps:
  1. it infers all the arguments first (`infer-all`);
  2. it unifies their types with each other (`join-all`): `+` needs all its arguments to be one type;
  3. it checks that type's kind (`needs-kind`: a number, a `String` or a list).

  Steps 2 and 3 happen after every argument is read, with the context still at the call node, so the report goes to the call.

**Is that right?** It's defensible, but it could be better.

- **Why the call is a fair place:** for `(+ x "b")` the checker can't tell which argument is wrong. `x` is an `Int` and `"b"` is a `String`, and either one could be the mistake. That's why the message names the operator rather than an argument.
- **What would be better:** point at the first argument that disagrees with the ones before it, here `"b"`, and keep the message as it is: `+: expected Int, got String` at `4:3`. In `join-all` that's a small change: pass each argument's node along with its type. Elm and Rust both blame the later argument this way.
- **The exception:** the kind check (`(- "a" "b")`, "expected a number, got String") is about all the arguments at once, so it would stay at the call.

The type checker's HLD didn't decide this; reporting operator errors at the call was just how step 3 built it. I'd record it as a low `defect` for now (call it B135, "an operator's type error is at the call, not the argument"), so it doesn't hold up the review, and fix it when we next work on the checker.

Want that item added, and then tick B129?

## Owner

> So, it's because `+` is not polymorphic anymore... I.e not for strings and lists

## Claude Code

Not quite. `+` is still polymorphic today: it takes numbers, `String`s and lists. The spec's `checking.operators` rule (`spec/25-checking.md:122`) has `(+ "a" "b")` giving `ab`, and joining lists. Nothing in this branch changed that.

The cause is that **operators have no type signature**, while functions do, polymorphic or not:

- **A polymorphic function reports at the argument.** `pick` has the generic signature `(Fn (a a Bool) a)`, and the spec shows `(pick 1 "a" true) => argument 2 of pick: expected Int, got String` (`spec/25-checking.md:73`). The checker gives `a` a fresh variable, checks argument 1 (`a` becomes `Int`), then checks argument 2 against `Int` at argument 2's node.
- **An operator reports at the call.** `+` is declared in `special.cdy` as `(op + variadic)`, with no type. Its rule ("all one type, and that type a number, `String` or list") is code in `infer-op` (`check.cdy:467`). That code infers every argument first and compares them afterwards, by which point the context is the call.

So if `+` had a signature, like `(Fn (a a) a)` with a bound on `a`, it would go through the same path as `pick` and report at `"b"`. Candy can't write that bound yet.

That ties to the epic's Question 4 answer: Elm-style constraint variables (`number`, `comparable`, `appendable`) arrive in the `collections` branch, with `++` for appending. Then `+` can get a signature over `number`, and `++` one over `appendable`. Both would be checked like ordinary functions, and the error would point at the argument without special code.

That changes my suggestion. Rather than patching `join-all` now, I'd record it as a low `defect` with `collections` as its branch, as B135, "an operator's type error is at the call, not the argument". Its note would say constraint variables give operators signatures, which fixes it. Shall I add that, and tick B129?

## Owner

> Yes

## Claude Code

*ran: Find collections rows in the triage table*

*ran: Add B135 with a repro, triage row, tick B129*

B129 is ticked, and B135 is added (`backlog/B135-operator-error-at-call.md`); none of it is committed yet.

**B135** is a low defect, "An operator's type error is at the call, not the argument":
- **Text:** the difference between functions and operators. A function call reports at the wrong argument; an operator has no type signature, so `infer-op` reports at the call.
- **Planned fix:** in `collections`, constraint variables give the operators type signatures (B124). The text also gives the stopgap: `join-all` could carry each argument's node.
- **Repro:** `(+ x` with `"b"` on the next line should say `line 4, column 3: +: expected Int, got String`. It now runs as a strict expected failure, the fifth in `test_spec.py`.
- **Note:** your question from this review, with the answer that `+` is still polymorphic.
- **Triage:** a row in the table in `python_complete.md`, next to B124, marked *(typed-core)*. The table's intro now says this branch found five items.

The spec, backlog and doc-link tests pass. These edits wait for the review's commit, along with your ticks.

Next is B130, step 5, the docs.

## Owner

> What's our current definitions, and their differences, of a function call and an operator?

## Claude Code

*ran: Read operator declarations and spec rule ids*

*ran: Find the spec's operator rules and Builtin type*

*ran: Read the spec's calls and operators rules*

Here's what the spec and code say today, side by side. A **function call** is `(f arg ...)` where `f` is something with a type: a user's `defn`, a local `fn`, or a typed built-in from `system.cdy`. An **operator** is one of the fourteen names `special.cdy` declares with `op`. Both are written the same way, as a list with the name first, and both become a Core `Call` node. They diverge at every stage after that.

**What each is** (`src/cdy/special.cdy`, `src/cdy/system.cdy`, `Builtin` at `src/cdy/core.cdy:873`):

| | Function | Operator |
|---|---|---|
| Declared by | a `sig` (user code), or a bodiless `sig` in `system.cdy` (a built-in) | `(op + variadic)` / `(op not unary)` in `special.cdy` |
| Kind in the built-in table | `(Typed type)` | `(Op unary)`, with **no type** |
| The set | open: anyone can define one | closed: `+ - * / quot`, `= != < > <= >=`, `and or not` |
| Arity | from its type: exactly that many parameters | `variadic` = two or more; `unary` = exactly one |

**Spec** (`spec/40-expressions.md`):
- **Calls,** `expr.calls`: arguments are evaluated first, left to right, and a built-in's arity comes from its type. The arity error is `takes 1 argument(s), got 2`.
- **Operators,** `expr.arithmetic`, `expr.comparisons` and `expr.operator-arity`:
  - the arithmetic ones fold left: `(- 10 2 3)` is 5;
  - the comparisons chain: `(< a b c)` means `a < b` and `b < c`;
  - `and` and `or` short-circuit.
  - The arity error is different: `needs at least 2 arguments`.

**Checking** (`src/cdy/check.cdy`):
- **Functions** go through the general path. The callee's type is looked up, a generic one is instantiated fresh, and then **each argument is checked against its parameter, at the argument's node**. The error names it: `argument 2 of pick: expected Int, got String`.
- **Operators** go to `infer-op` (`check.cdy:467`): hand-written rules per group (`checking.operators`, `spec/25-checking.md:122`).
  1. Every argument is inferred, then all their types are joined into one (`join-all`).
  2. For `+`, that type must be a number, `String` or a list; for `- * / quot`, a number (`needs-kind`).
  3. `/` gives a `Double`, the comparisons give a `Bool`, and `and`, `or` and `not` want `Bool`s.
  4. The error is reported at the call: `+: expected Int, got String`. That's B135, which you just reviewed.

**As values:**
- **A function** is a value: it can be passed, as in `(map f xs)`, or bound.
- **An operator** isn't, for now: `(map + xs)` is an error, "the operator + can't be used as a value yet; wrap it in a fn" (B38). Having no type is part of why: there would be nothing to give `+` as a value's type (B48, "operators, `tup`, `put` untyped").

**In Python** (`src/cdy/emit.cdy`, with the spellings in `src/cdy_rt/spelling.py`):
- **A function** becomes a Python call: `f(a, b)` for a user's function, `cdy_rt.primitives.list_fold(...)` for a built-in.
- **An operator** becomes Python's own operator, inline:
  - `(+ a b c)` becomes `(a + b + c)`;
  - `(< a b c)` becomes Python's chained comparison;
  - `and` becomes Python's `and`.

  The short-circuiting comes from Python here. So does what `and` and `or` return: Python's operand, not always a `Bool` (B26, for `semantics`).

**Where it's heading.** In the epic's Question 4 answer, the `collections` branch brings Elm-style constraint variables (`number`, `comparable`, `appendable`):
- the operators get real types, for example `+` over `number`;
- `++` joins strings and lists, over `appendable`;
- `=` works on every type, except function types, where it's an error.

Then most of the differences in the checking and values rows go away: an operator is checked like a call, argument by argument (B124, B135), and can have a type as a value (B38, B48). What should stay different:
- the syntax-level behaviour: fold, chaining and short-circuiting;
- the variadic arity;
- inline Python;
- the closed set, which is declared in `special.cdy` because it's part of the language rather than the library.

## Owner

> In a perfect world... Whether it's user defined or defined by the system, they'd both just be operators... That was my note.. but I get your gist... Thoughts?

## Claude Code

I think you're right, and the epic's own answers already put most of it in place. In a Lisp the distinction barely exists: `+` is just a function with a short name. In Candy, the gap between a function call and an operator is mostly a set of MVP shortcuts, and each one has a planned fix.

Going through the differences:

| Difference | Language or shortcut? | What removes it |
|---|---|---|
| no type | a shortcut | constraint variables (Question 4, `collections`): `(sig + (Fn (number ...) number))` |
| checked by special code, error at the call | a shortcut | a typed `+` goes through ordinary call checking (B124, B135) |
| not a value | a shortcut | with a type, `(map + ...)` just works (B38, B48) |
| variadic arity | looks like language, but isn't special | typed rest parameters (Question 8, `collections`): a user's function can be variadic too |
| folds left, comparisons chain | not special | that's just what the function does with its rest list; a user could write one that does the same |
| closed set in `special.cdy` | a shortcut | once the others go, `+` is a bodiless `sig` in `system.cdy` like `len` |
| inline Python, `(a + b)` | **backend only** | the spelling table can inline any built-in it knows; the language needn't care |
| `and`/`or` short-circuit | **the one real difference** | a function evaluates all its arguments first. These need to be macros (expanding to `if`), which is already B100, in `semantics` |

So after `semantics` and `collections`, the `op` category in `special.cdy` could go away entirely:
- the arithmetic and comparison operators become typed built-in functions;
- `and` and `or` become macros;
- `not` becomes an ordinary one-argument function.

Then "operator" would mean only how a backend spells something: infix in Python, maybe a method in another target. Whether something is built-in or user-defined would make no difference to how it's declared, checked, passed or called.

Two things to keep in mind:
1. **The names.** You said "they'd both just be operators" and I've been saying "functions", but it's one category either way. I'd still call them functions, since that's the Lisp/ML convention and Candy's types already say `Fn`.
2. **The cost is in the backend, not the language.** mypy has to accept the variadic and constrained signatures, which may mean overloads or `Any` in the generated stubs. And the inline spelling has to survive, for speed and readable output. Both belong to `emit` and `spelling.py`, which is where they should live.

I'd record this as a goal for the `collections` HLD rather than act on it now. I'd add it as a note on B124, "the operators polymorphic, programs not", since that's the item the change would close. The note would say: "goal: no operators in the language; `op` leaves `special.cdy`; with B100 for `and`/`or`; inline spelling is the backend's". It would go into the review commit with the other edits. Want that, and then on to B130?

## Owner

> Sure

## Claude Code

*ran: Add the no-operators goal note to B124*

I've added the note to the end of B124's notes (`backlog/B124-*.md`). It records the goal for the `collections` HLD, no operators in the language, and quotes your remark. The backlog and doc-link tests pass, and the note waits for the review commit.

**B130 is step 5: the docs.** It's commit `5562418`, with no boot tag because `bin` didn't change. It updated the docs that described the checker before this branch, and closed B15.

1. **B15 is closed and split** (its note at `backlog/B15-no-type-checker.md:35` has the map):
   - mypy as a second check goes to B125 (each target's own checker as an option). Whether mypy stays is decided in `porting-surface`.
   - No let-polymorphism goes to **B133**, new: an `idea`, for after the epic.
   - A type not known yet when `get` uses it goes to B120, in `semantics`.
   - No narrowing in a `match` clause goes to B121, in `semantics`.
   - Stopping at the first error goes to **B134**, new: a low `leak`. The checker already collects its errors in a list, so reporting them all is mostly a driver change.
2. **The spec's *for now* links moved with the parts:**
   - `spec/25-checking.md:81` (a `let`-bound `fn` isn't generic) now links B133;
   - `spec/20-types.md:73` (mypy as a second check) now links B125.
3. **`CLAUDE.md`:**
   - line 35, "Type checking": a paragraph on typed Core. Every node ends with `pos` and then `t`, filled by the checker, with an unsolved type written as `Any` in Python. Links to B133 and B134.
   - line 36, "Errors": every form and Core node has a position, and internal errors say so.
   - "History": the epic and this branch.
4. **The other HLDs:**
   - **`python_complete.md`:** a note in "Where things stand" (line 21). The triage's intro and table list the new items, marked *(typed-core)*, now five with B135.
   - **`type_checker.md:8`, `multi_target.md`, the iMVP doc's layers (line 524):** each gets a dated *(Since `typed-core` …)* aside, with the history itself left alone.
5. **The record:** step 5's *Done* note, at `doc/hl_rqmt/typed_core.md:245`.

Things the review has added since then, still uncommitted:
- B135 and its triage row;
- the goal note on B124;
- the ticks on B126 to B129.

The docs above don't need to change for them.

Say tick, or point me at anything. After that I'll:
1. set the HLD's status to *done*;
2. commit the review: your five ticks, B135, the B124 note, and the "nested Python `def`" wording fix if you want it;
3. write the chat archive (`script/chat_archive.py`, as agreed) and commit it;
4. run `pytest -m bootstrap`, then merge and tag on your gawc.

## Owner

> Since we recently finished the `type-checker` branch can we "reflect" on how it relates to the `typed-core` branch? Not sure where I'm going on this... It's probably spelled out already... Just wondering it there's more we could add...?

## Claude Code

*ran: Look for existing items on patterns, map copying, retrospectives*

*ran: Read B69 and type_checker.md's design wording*

It's mostly spelled out, but only in passing. `typed_core.md`'s opening says the checker "works out every expression's type, then throws the types away", and `type_checker.md` now has a one-line *(Since `typed-core`)* aside. Neither says why the first branch was built that way, or what building the second taught us. Here's my reflection, with what I think is worth adding.

**How the two relate.** In the literature these are the two halves of a type checker: *checking* (does the program type?) and *elaboration* (writing the types it found into the program). `type-checker` built only the first. `type_checker.md` never mentions keeping the types: its proposal is all rules and messages. So the MVP was "check and discard", without saying so. `typed-core` is the elaboration half, plus the positions that the first branch's messages needed but couldn't get at the leaves (B122, which `type-checker` found).

**What `typed-core` showed about `type-checker`, which isn't written down yet:**

1. **The checker didn't visit every node.** Step 2's test made "the checker reached every node" checkable, and the first run failed on some kinds of node:
   - operators' callees;
   - a `tup` pattern's `at`;
   - a `let`'s `fn`.

   These are places where the checker computed a type without inferring the node itself. The fix was to record their types (`typed-callee`). Nothing was wrongly typed, but `type-checker`'s tests couldn't have told us that.
2. **mypy and the checker didn't disagree once typed nested `fn`s exposed more code.** Nested Python `def`s and `let`-bound `lambda`s now reach mypy with real types, and it found nothing (step 3). That's a small piece of evidence for the epic's Question 3, which keeps mypy as a second check through the epic and decides later whether it stays.
3. **Two costs came from the language, not from the checker.** These are the parts I'd add, because they'll recur on later branches:
   - **Adding a field to Core is expensive.** A `match` pattern names every field, so each new field touched about 180 sites. `type-checker` paid it for `pos` on compound nodes, and `typed-core` paid it twice more, for `pos` on the leaves and for `t`. Step 2 needed a throwaway script to do it. Patterns that don't have to name every field would make this cheap: a "rest" wildcard like `(Call callee ..)`, or matching fields by name. Every later branch that grows Core (`semantics`, a second backend) will hit this again. I found no backlog item for it.
   - **Immutable maps copy on every write.** `map-set` copies the whole dict. That's why step 2 kept the recorded types in their own map, out of the substitution, so unification wouldn't slow down. It's the map version of B69 ("building a list is quadratic"), whose note covers only lists.
4. **Unsolved types aren't the only thing `Any` hides.** B132 already records the eight unsolved nodes, which all come from `Any` meeting a type variable. It's worth a line that this is what typed Core made *visible*: before it, nothing could see an unsolved type at all.

**What I'd add** (all small, all in the review commit):
- **A short "Looking back" section in `typed_core.md`**, after the steps, with points 1 to 4: what elaboration revealed about the checker, the mypy evidence, and the two language costs. `process.md` has no retrospective step. If you like how this one reads, I'd also add one line to the process, "the docs step notes what the branch taught about the ones before it". That would make it a habit for every branch in the epic.
- **A new item, B136, an `idea`:** match patterns that don't name every field, with the field-churn counts as its evidence. Its branch would be open, though `semantics` or `collections` would be natural.
- **A note on B69:** maps copy too, and typed Core worked around it.

Want all three, or just some of them?

## Owner

> All three, thanks that was a great summary

## Claude Code

*ran: Locate sections for the additions*

*ran: Add Looking back, B136, B69 note, process line, triage row*

I put a wrong reference in B136 (B101 is the interpreter), so I'm removing it. Also checking whether `process.md` keeps a dated log of its changes.

*ran: Fix B136's refs; view process.md's change log*

*ran: See the newest process log entry's format*

*ran: Log the process change; rerun doc tests*

*ran: Fix the section name in the log entry; list changes*

All three are written, plus the one-line process change; they wait for the review commit. The backlog, doc-link and spec tests pass.

1. **"Looking back" in `doc/hl_rqmt/typed_core.md:262`,** between Steps and Questions. It has the points from my summary:
   - checking and then elaboration, with "check and discard" as `type-checker`'s unstated MVP;
   - the checker not visiting every node, which step 2's test exposed;
   - mypy finding nothing new once nested Python `def`s were typed;
   - unsolved types becoming visible (B132);
   - the two costs that later branches will meet again, each linked to its item.
2. **B136, an `idea`, "A `match` pattern names every field"** (`backlog/B136-patterns-without-every-field.md`):
   - **The evidence:** about 180 sites per new Core field, paid three times across `type-checker` and `typed-core`.
   - **Ways out:** a rest wildcard, as in Rust's `(Call callee ..)`; fields by name, as in OCaml, Elm and Rust; and `get` on the subject in a clause, which works only for shared fields until B121.
   - **Its branch:** any that grows Core. It's also a triage row in `python_complete.md:609`, and the triage intro now says this branch found six items.
3. **A note on B69** ("building a list is quadratic"): maps copy too. `map-set` copies the whole dict, which is why step 2 kept the recorded types out of the substitution. The fix is the one B69 already points to, in `mutation_optimization.md`.
4. **`doc/process.md:42`:** the docs step now says the HLD gets a short "Looking back": what the branch taught about the earlier ones, and the costs later branches will meet, each with its item. It's in this step or the review. There's an entry for it in the process change log (`process.md:206`).

Since your tick, I've also fixed a wrong reference in B136 (it pointed at B101, the interpreter).

B130 is still waiting for your tick. After that I'll:
1. set the HLD to *done*;
2. commit the review: the ticks, B135, B136, the B124 and B69 notes, "Looking back" and the process line;
3. write the chat archive;
4. run `pytest -m bootstrap` before the merge.

One thing for you to decide: you never replied about the "nested Python `def`" wording fix. Do you want it in this commit, or should I leave the wording as it is?

## Owner

> "nested Python def" , yes add the wording fix, I'd like to talk more about b136 more... But let's go thru b130

## Claude Code

*ran: Find ambiguous nested-def wording*

*ran: Apply the nested Python def wording fix*

*ran: Rebuild bin to confirm comments don't change it; full tests*

The wording fix is done, and since `bin` didn't change it needs no boot tag:
- **Docs:** "nested `def`" is now "nested Python `def`" everywhere it meant the Python one. That's 16 places in `typed_core.md`, 2 in B19 and 2 in B128.
- **Comments:** the three in `src/cdy/lower.cdy` (lines 23, 153 and 520) say "nested Python def" too. The one at line 153 adds "Candy has no nested def or defn".
- **Checks:** I rebuilt `bin` and it came out identical; the full suite passes (494 passed, 5 expected failures).

B136 is noted for after B130.

**B130, step 5: the docs** (commit `5562418`). To review it in one go, `git show 5562418 --stat` lists the 14 files. The ones to read:

1. **`backlog/B15-no-type-checker.md:35`:** the closing note, with a table that sends each of B15's five parts to its item (B125, B133, B120, B121, B134).
2. **The two new items:**
   - `backlog/B133-let-polymorphism.md` (an idea, for after the epic);
   - `backlog/B134-one-type-error-at-a-time.md` (a low leak; reporting every error is mostly a driver change, since the checker already collects them).
3. **`CLAUDE.md:35-36`:** the typed Core paragraph in "Type checking", and "Errors".
4. **The spec's moved links:**
   - `spec/25-checking.md:81` now links B133;
   - `spec/20-types.md:73` now links B125.
5. **The dated *(Since `typed-core`)* asides:**
   - `doc/hl_rqmt/type_checker.md:8`;
   - `doc/hl_rqmt/multi_target.md` (the paragraph on showing values by static type);
   - `doc/hl_rqmt/iMVP_py_translator.md:524`;
   - `doc/hl_rqmt/python_complete.md:21`.
6. **The triage** (`python_complete.md:516-519` and its table): the items this branch closed and found, each marked *(typed-core)*. The review has since added B135 and B136 there.
7. **`doc/hl_rqmt/typed_core.md:245`:** the step's *Done* note.

Say tick, or point me at anything. Then B136.

## Owner

> Tick

## Claude Code

*ran: Tick B130; check nothing is left in review*

B130 is ticked, so all five tasks, B126 to B130, are `done` and nothing is left in `review`.

**B136: a `match` pattern names every field.** Today a variant pattern binds fields by position, so it has to list all of them:

```
((Call callee args _ _) ...)        ; Call has callee, args, pos, t: four slots
```

When `typed-core` added `t`, every clause that takes a `Call` apart gained a `_`, even clauses that only wanted `callee`. That was about 180 sites in the translator. `type-checker` paid the same for `pos`.

**Three ways out, in Candy syntax:**

1. **A rest wildcard: bind the first fields, ignore the rest.**
   ```
   ((Call callee args ..) ...)
   ```
   - Small: one new token in patterns, and existing patterns keep working.
   - Adding a field at the *end* (as `pos` and `t` were) costs nothing.
   - Adding one in the middle still breaks the positional patterns, which is mostly a convention issue, since new fields would go last.
   - Rust has `..`, and Haskell, which lacks it, is often criticised for exactly this.
2. **Fields by name: bind only what you name.**
   ```
   ((Call :callee c :args as) ...)     ; or ((Call (callee c) (args as)) ...)
   ```
   - Robust to any field change, wherever it goes. It reads well for records with many fields.
   - Needs a syntax decision: keywords like `:callee` don't exist in Candy yet, and the parenthesised form looks like a nested pattern.
   - OCaml, Elm and Rust all have it (`Call { callee, .. }`).
3. **No pattern change: `get` inside the clause.**
   ```
   ((Call ..) (... (get e callee) ...))
   ```
   This needs the checker to know `e` is a `Call` in that clause, which is narrowing (B121, in `semantics`). Without narrowing, `get` works only for fields every variant shares.

**My lean:** option 1 first, because it's tiny and covers this branch's case, fields appended at the end. Option 2 later, if records grow big enough that names matter more than positions. They can live together, as they do in Rust.

**Where it fits:**
- **Language or translator?** It's a language feature, a change to the spec's `match` rules (`spec/30-match.md`), so it needs an HLD, or a step in one.
- **Which branch:** `semantics` changes `match` anyway (narrowing, B121) and grows Core. Or it could be its own small branch before `semantics`, to make that branch's Core changes cheap.

What would you like to talk through? It could be the syntax, whether it should come before `semantics`, or something else you had in mind.

## Owner

> I was just wondering if this relates to rewriting systems/languages, such as obj3, maude, pure etc

## Claude Code

Yes, quite directly. Term rewriting systems met exactly this problem and solved it in two ways, and both are worth recording in B136.

**The problem is the same.** In OBJ3, Maude or Pure, a term is a constructor applied to arguments by position: `Call(callee, args, pos, t)`. A rule's left-hand side is a pattern over terms, so it names every argument, just like Candy's `((Call callee args _ _) ...)`. A plain rewriting system has B136's churn too.

**Solution 1: matching modulo a theory (OBJ3, then Maude).** OBJ3 let an operator be declared associative, commutative, with an identity element (`assoc comm id:`), and matching then works *modulo* those equations. Maude uses this for its objects: an object is `< O : C | a1 : v1, a2 : v2 >`, and its attributes form a set, a term built with an associative-commutative operator. So a rule can write

```
< A : Account | bal : N, Atts >  =>  < A : Account | bal : N + M, Atts >
```

Here `Atts` is a variable that matches *the rest of the attributes*, whatever they are and in any order. That's option 2 (fields by name) plus a rest variable, and neither is a special pattern feature: both fall out of matching on sets rather than sequences. Full Maude's object-oriented modules go one step further: a rule can just leave out the attributes it doesn't touch.

For Candy, this suggests an option 4 for B136. A record's fields would be a set of name–value pairs that a pattern matches modulo order, with a variable for the rest, as in `((Call (callee c) . rest) ...)`. It would also give `assoc`-style updates for free.

**Solution 2: generic traversal (Stratego, and in functional languages "Scrap Your Boilerplate" and Uniplate).** This targets a different part of the churn. Many of those ~180 sites weren't clauses that *wanted* a field; they were whole-tree walks that only rebuilt each node: step 2's `retype` family, `has-lambda`, `bound-locals`. Strategic rewriting separates the rules from the traversal. You write one rule for the node you care about, and a combinator such as `all`, `topdown` or `bottomup` applies it everywhere, descending into the other variants without naming their fields. A new field then costs nothing in a traversal, because no traversal mentions it. I haven't counted how many of the 180 sites were traversals like this rather than clauses that needed a field. I can, if the split matters for the decision.

**Pure** is the closest in spirit to Candy: a functional language whose evaluation *is* term rewriting, with a Lisp-like attitude to terms as data. Its patterns are positional constructor patterns, like Candy's today, so it shows the problem rather than a fix.

**How this relates to Candy** (my observations, not decided anywhere): Candy already does rewriting in two places.
- **Macros** rewrite forms to forms.
- **`lower`** is close to a set of rewrite rules over Core: a `let` becomes assignments, and a self tail call becomes a loop.

So taking in rewriting ideas would help the translator's own code at least as much as user programs.

I'd add both solutions to B136 as notes, alongside its current three options, with the systems named:
- option 4, fields matched modulo a theory, from OBJ3 and Maude;
- generic traversal from Stratego, Scrap Your Boilerplate and Uniplate, as a separate way to cut the traversal part of the churn, which may deserve its own `idea` item later.

Want that?

## Owner

> Ya add that... Then let's get back to what we were doing

## Claude Code

*ran: Add the rewriting-systems note to B136*

B136 has the note. Back to the merge path: first, the HLD's status becomes *done*.

*ran: Mark the HLD done; check links and status*

I've added the rewriting-systems note to B136 and set `typed_core.md`'s status to *done*. The status line lists what the branch fixed, what it closed, and what it found. All of it is still uncommitted.

The review commit is ready. It has 15 files, all mine; none are your own edits:

- **Your five ticks:** B126 to B130, all now `done`.
- **New items:** B135 (an operator's error is at the call) and B136 (a pattern names every field, with the OBJ3/Maude/Stratego note).
- **Notes:** the no-operators goal on B124, and maps copying on B69.
- **"Looking back"** in `typed_core.md`, and the matching line in `doc/process.md`.
- **The wording fix:** "nested Python `def`" in `typed_core.md`, B19, B128 and three comments in `src/cdy/lower.cdy`. `bin` came out identical, so there's no boot tag.
- **Elsewhere in `python_complete.md`:** the two new triage rows.

The full suite passed after the wording fix. Since then I've only edited backlog and doc files, and the backlog and doc-link tests pass on them.

On gawc I'll commit it as "typed-core review: ticks, B135, B136, looking back". Then:
1. **Chat archive:** I write `script/chat_archive.py`, generate `doc/archive/chat_typed-core.md`, `chat_type-checker.md` and the epic's planning span from `master`, and show you the result before committing it.
2. **Bootstrap check:** I run `pytest -m bootstrap`.
3. **Merge:** I merge into master with `--no-ff` and add the annotated tag `typed-core`, on your gawc.
4. **Push:** when you ask.

## Owner

> Gawc

## Claude Code

*ran: Commit the review*

Review committed as `0835dbc`. Now the chat archive. First, a look at the transcript's entry shapes:

*ran: Inspect transcript entry types on typed-core*

*ran: Read a script's style and the archive turn format*

Now the script, in the style of the others (`NamedTuple`s, no decorators, typed):

*wrote: `script/chat_archive.py`*

*ran: Lint the script and try it on typed-core*

Two problems: early commands had no description, so they all read "*ran: a command*", and I want to check what the 32 owner turns are. Fixing the first: I'll fall back to the command's first line.

*ran: Fall back to command text; list the owner turns*

The markers still show the shell set-up. Dropping the `cd`/`source`/`conda activate` prefix:

*read: `script/chat_archive.py`*

*edited: `script/chat_archive.py`*

*edited: `script/chat_archive.py`*

*ran: Regenerate; show markers and the owner turns*

The owner turns are right: all 32 are yours, from step 1's gawc to the review's. Now the epic's span on `master`, between `type-checker`'s end and `typed-core`'s start:

*ran: Generate the epic span and type-checker drafts*

The first owner turn there, "Push", belongs to `type-checker`'s merge, so the epic span should start at the next one. Finding its timestamp:

*ran: Find when the epic's planning chat began*

Writing the three top notes, then generating into `doc/archive/`:

*ran: Write the notes, generate the three archives, check links*
