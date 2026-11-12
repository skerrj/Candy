*Archived 2026-11-11, from the Claude Code session that built branch `collections-2`
(2026-11-10 to 2026-11-11; HLD `doc/hl_rqmt/collections_2.md`, tag `collections-2`), by
`script/chat_archive.py`, before the merge.* The owner's messages and Claude's replies on
the branch, verbatim; each tool call is a one-line marker, and thinking and tool output
are left out. The HLD's proposal and acceptance were on `master`, earlier in the same
session, and the branch `collections` before that (`chat_collections.md`); neither is in
this file. What came of it: step 1, `map-acc` ([[B167]]); steps 2 to 5, the translator's
loops onto the list operations ([[B177]] to [[B180]], [[B123]] closed, with [[B184]] and
[[B185]] found); step 6, `to-list` gone ([[B181]], [[B174]]); step 7, `equatable`
([[B182]], [[B173]] fixed, [[B186]] found and fixed); step 8, the docs ([[B183]]).

# collections-2

## Claude Code

Committed on `master` as `eb0f7b0`, and branch `collections-2` is created. Starting step 1, `map-acc`.

*ran: Read how fold is declared, spelled and specified*

*ran: Read the list primitives, sigs and spellings*

*ran: Read the library.lists spec rule*

*ran: Read the rest of library.lists and runtime tests*

Adding the built-in, its primitive, the spec rule and a runtime test.

*ran: Add map-acc to library, runtime, tests and spec*

*ran: Stage library and run the library spec and runtime tests*

The built-in works and the spec example passes. Next I'll look at the 16 loops that carry a state.

*ran: List the threaded loops*

*ran: Print the threaded loops in check.cdy*

*ran: Print the other threaded loops*

*ran: Find the callers of each threaded loop*

*ran: Check tests use these internals and Low's shape*

*ran: Rewrite the 12 threaded loops onto map-acc and fix callers*

*ran: Rebuild T1, T2 and bin*

*ran: Time the build and run all tests*

Tests pass (626), and the build got faster: 1.02 s down to 0.93 s. Running the linters.

*ran: Run all linters and type checkers*

*ran: Show and fix the ruff finding*

*ran: Look at the emitted infer-all*

The generated Python is clean: a typed nested `def` and no copies. Now the step's notes.

*ran: Read primitives header and HLD step 1*

*ran: Write as-built note, put B167 in review, note B123*

Step 1 (`map-acc`, B167) is built and in `review`; nothing is committed. pytest passes (627 with the new spec example), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and the fixpoint holds.

- **The built-in:**
  - `(sig map-acc (Fn ((Fn (s a) (Tup s b)) s (List a)) (Tup s (List b))))` is at `src/cdy/system.cdy:96`.
  - It's spelled `list_map_acc`, a primitive that builds a Python list and returns a tuple, so it doesn't copy (`primitives.py`).
  - It has a runtime test in `test_primitives.py`.
- **Spec:** `library.map-acc` is a new rule (`spec/60-library.md`), with an example that numbers words; `library.builtins` lists it.
- **12 of the 16 loops** became one `map-acc` each:
  - `check.cdy`: 7, from `check-tops` and `infer-all` to the `retype-*`s;
  - `core.cdy`: `analyse-all` and `bind-params`, whose state is a `(Tup Scope Int)`;
  - `lower.cdy`: `lower-cases`, `low-all` and `effect-all`, the last a `map-acc` then `concat`.
- **Each keeps its name and its result's order, `(Tup items state)`.** It loses only its `acc` argument, which all 30 callers passed as `empty-list`. In Python the `fn` becomes a typed nested `def` (`check__infer_all` in `bin`).
- **The other four aren't over a list:** `fresh-types` counts down, and `format-parts`, `read-list` and `read-str` walk a text.
- **Build time:** 1.02 s → 0.93 s.
- **Boot step:** one, `boot/63` on commit, with no staging; `boot/62` reads the new library.

The as-built note is under step 1 in `doc/hl_rqmt/collections_2.md`, and B123 has a note.

## Owner

> Can we walk thru the  `map-acc` sig real quick... If you can print it in a more understandable way that would be great

## Claude Code

Here it is, split into its three arguments and its result:

```
(sig map-acc
  (Fn ( (Fn (s a) (Tup s b))    ; 1. f: takes the state and one item,
                                ;    gives back the next state and that item's result
        s                       ; 2. the starting state
        (List a) )              ; 3. the items
      (Tup s (List b))))        ; result: the final state and all the results
```

`a` is the item type, `b` the result type and `s` the state type.

It's `map` and `fold` in one call:
- like `map`, each item `a` becomes a result `b`, and the results come back in order as a `(List b)`;
- like `fold`, a state `s` is passed from item to item, and you get its final value.

`fold` is the same shape without the per-item results:

```
fold:    (Fn ((Fn (s a) s)         s (List a))  s)
map-acc: (Fn ((Fn (s a) (Tup s b)) s (List a))  (Tup s (List b)))
```

**The spec example** (`library.map-acc`), numbering words from 1:

```
(defn number-words (n w) (Tup (+ n 1) (format "{n}:{w}")))
(map-acc number-words 1 (List "a" "b" "c"))
```

Here `s` = `Int` (the counter), `a` = `String` (a word) and `b` = `String` (the numbered word).

| step | state in | item | `f` gives | results so far |
|---|---|---|---|---|
| 1 | 1 | "a" | `(Tup 2 "1:a")` | ("1:a") |
| 2 | 2 | "b" | `(Tup 3 "2:b")` | ("1:a" "2:b") |
| 3 | 3 | "c" | `(Tup 4 "3:c")` | ("1:a" "2:b" "3:c") |

The result is `(Tup 4 (List "1:a" "2:b" "3:c"))`.

**In the translator**, `infer-all` is the typical case. `s` is the checker's state `St` (the substitution, the next fresh variable number, the errors), `a` is an `Expr`, and `b` is the `CType` inferred for it. Each expression is inferred with the state the previous one left, which is why a plain `map` couldn't do it.

**Why the state comes first:** both in `f`'s arguments and in the result, it's in the same place as `fold`'s accumulator. That's why the translator's loops return `(Tup items state)` on the outside but swap it back from `map-acc`'s `(Tup state items)` inside. Changing those loops' own order too would have meant touching every caller's pattern, so I kept their order.

## Owner

> step 1, tick, gawc

## Claude Code

*ran: Tick B167, commit step 1, tag boot/63*

I ticked B167 and committed step 1 as `ab2edbb`, with no edits of yours to include. `bootstrap.py --tag` ran the new step first and it passed, then tagged it `boot/63` with no staging; the tag is annotated. Nothing is pushed.

Next is step 2 (B177): the loops in `core.cdy` and `lower.cdy`, about 45 of them.

## Owner

> go

## Claude Code

*ran: Extract the acc loops in core and lower*

*read: `tmp/c7/core_loops.txt`*

*read: `tmp/c7/lower_loops.txt`*

Of the 40 loops here, most are a plain `map` or `fold`. I'll check each caller's last argument to see which `acc`s always start empty.

*ran: Show each loop's call sites*

*ran: Read the binder loops' sigs and helpers*

*ran: Rewrite core and lower loops onto map, filter, fold, map-acc*

*ran: Check the inlined and changed calls*

The calls look right. Building.

*ran: Check remaining callers, rebuild bin*

*ran: Time the build and run all tests*

Tests pass. The build looks about 5% slower (0.93 s → 0.98 s), so I'll measure it properly: 7 runs each of the step 1 `bin` and the new one.

*ran: Compare build times of step 1 and step 2 bins*

The new `bin` is about 3% slower: median 1.00 s against 0.97 s for step 1's `bin`. The machine is slower today too, since that same step 1 `bin` measured 0.93 s yesterday. Running the linters.

*ran: Run all linters and type checkers*

*ran: Write step 2 notes, B177 to review*

*edited: `doc/hl_rqmt/collections_2.md`*

Step 2 (the loops in `core.cdy` and `lower.cdy`, B177) is built and in `review`; nothing is committed. pytest passes (626), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and the fixpoint holds.

A correction to my step 1 report: it said 627 tests, but that run was 626 too. The new spec example replaced nothing; the count was simply 626.

**The 40 functions there with an `acc` argument:**
- Two weren't loops: `add-name` and `read-type`.
- **31 are one call now:**
  - 15 `map`s. Three were already a function per item, so the call sites became `(map sym-name …)`, `(map quoted …)` and `(map analyse-type …)`, and `syms`, `quoted-all` and `analyse-types` are gone.
  - One `filter`: `missing-variants`.
  - 12 `fold`s. Most build a map a name at a time (`top-names`, `read-decls`, `read-sigs`, `put-all`); `deft-fields` folds because it checks each field against the ones so far.
  - Three `map-acc`s:
    - `let-bindings`, then `concat`. Its per-binding work is a new `let-binding` (`core.cdy:278`).
    - `destructure`, over `(zip (range …) names)` for the index.
    - `lower-program`, then `concat`.
- **Seven stay loops:**
  - `tup-binds` and `pattern-binds` check each name against those already bound, and skip `_` while still counting positions.
  - `assoc-fields` takes the forms two at a time.
  - `format-parts` walks a text.
  - `assigns`, `fill-holes` and `refill` each walk two lists at once.

**Signatures:** each function keeps its name. An `acc` that every caller passed empty is gone. An `acc` that a caller fills first (`add-names`, `read-sigs`, `put-all`) is now the fold's `start`.

**Size:** `src/cdy` is 71 lines shorter.

**Build time: about 3% slower**, 0.97 s → 1.00 s (median of seven runs each, against step 1's `bin`). Most likely a function call per item now costs more than the copies saved: these lists are short (a form's items, a `deft`'s fields). Step 1 was faster because its loops carried the checker's state over long lists. I'll keep measuring; if steps 3–5 add up to a real slowdown, that's a question for you.

The as-built note is under step 2 in `doc/hl_rqmt/collections_2.md`, and B123 has a note. On commit this is one boot step, `boot/64`.

*(The context was summarised here; the turns before it are above.)*

## Owner

> tick, gawc

## Claude Code

*ran: Show B177 header and notes, and git status*

No edits from you in the tree beyond mine.

*ran: Tick B177, commit step 2, tag boot/64*

I've ticked and committed step 2 as `6c1f572`.

- **Tick:** B177 is `done`, with the note "ticked in review", and the backlog index is regenerated.
- **Commit:** your tree had no edits besides mine, so the commit holds only step 2's files.
- **Boot step:** `boot/64` is tagged on it and is an annotated tag. The bootstrap check passed for this step without staging, and the working tree is clean.

Nothing is pushed. Next is step 3 (B178), the loops in `check.cdy`, when you say go.

## Owner

> go

## Claude Code

*ran: List check.cdy functions with an acc argument*

*ran: Find check.cdy functions recursing on rest*

*ran: Show check.cdy loop candidates, part 1*

*ran: Show check.cdy loop candidates, part 2*

*ran: Find callers of the candidate functions*

*ran: Look at step 2's fold style for reference*

Step 3 in progress: the loops in `check.cdy`. I've picked out 13 to convert, and I'm editing them now.

*read: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

*edited: `src/cdy/check.cdy`*

Now I'll rebuild `bin` and run the test suite.

*ran: Save boot/64 bin copy, rebuild bin*

*ran: Inspect the generated Python mypy rejects*

*ran: Search backlog for empty-literal mypy issue*

*ran: Seed solve-each and check-order from parameters, rebuild*

`bin` rebuilt, and the fixpoint holds. Next I'll fix a comment that still names `defined`, then run pytest. I'm also running a candidate repro for the mypy bug.

*ran: Fix the comment; try mypy repros*

Both repros fail mypy, so the bug is real and doesn't depend on the translator's code. Next I'll reflow the comment and file a defect, using B173's format.

*ran: Reflow comment; show a defect item's format*

*ran: Find next backlog id and repro style*

Next id is B184. I'll file it as a defect with r1 as its repro.

*ran: File B184 defect with repro*

B184 is filed. Next: the build timing against `boot/64`'s `bin`, then the full test suite.

*ran: Time the build, boot/64 bin vs new bin*

Build time is unchanged: medians of 0.98 and 0.99 s for the old `bin`, 0.99 and 0.98 s for the new. Next: rebuild after the comment fix, then pytest and the linters.

*ran: Rebuild bin, run tests and all linters*

*ran: See why the B184 repro test fails*

The repro passes under the spec runner. Probably that runner doesn't run mypy on a defect's repro; I'll check.

*ran: Look at how test_spec handles mypy and backlog*

*ran: Read test_spec's mypy and repro handling*

*ran: List fence info strings used in docs*

*ran: Make B184's repro a non-running block*

*ran: Find the spec rule covering fold*

*ran: Point B184 at library.lists, run full pytest*

*ran: See which doc link is broken*

The mypy message I quoted contains `[[tuple[`, which the link checker reads as a link. I'll paraphrase the message instead.

*ran: Rephrase B184 and rerun doc tests*

The tests pass. Next: the HLD note, B178 and B123.

*ran: Line counts and B123's last notes*

*edited: `doc/hl_rqmt/collections_2.md`*

*ran: Move B178 to review with notes, B123 note, full pytest*

*ran: Show working tree status*

Step 3 (the loops in `check.cdy`, B178) is built and in `review`; nothing is committed. pytest passes (626 tests, 5 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and reproduces itself.

**14 of the 20 list loops are one call now:**
- **13 `fold`s:**
  - the maps built from the program's top-level definitions: `top-types`, `top-shapes`, `top-sums`, and from a sum's variants: `variant-types`, `variant-shapes`;
  - the checker's state threaded through a list: `infer-do`, `infer-holes`, `join-all`, `solve-each`, `report-pending`, `assoc-values`, `typed-binds`;
  - a pattern's names put into the environment: `bind-fields`.
- **One `map-acc`:** `check-order`. Its state is the names defined so far; it collects each definition's errors, then `concat`s them.
- `order-of` was already a `fold`; it only loses its `acc` argument.

**Six stay loops:**
- `fresh-types` counts down.
- `find-field` exits early.
- `zip-map`, `typed-all` and `unify-all` walk two lists at once, and `unify-all` also exits early.
- `reach` walks a work list that grows as it goes.

`rigid-vars`, `uses` and `uses-all` have an `acc`, but they walk a type or an expression, not a list.

**New bug, B184 (a defect):** an empty list or map as the start of a `fold` or `map-acc` can fail `mypy --strict`. mypy types `()` as `tuple[()]` and `{}` as `dict[Never, Never]` when nothing around them gives the type.
- It hit `solve-each`'s `(Tup start empty-list)` and `check-order`'s `empty-map`.
- I worked around it: both starts stay parameters typed by the `sig`, and their callers pass them empty.
- A 4-line program reproduces it: it prints the right answer and fails mypy.
- The repro doesn't run as a test. `test_spec.py` runs mypy only on the spec's own files, so a `candy run` block in a backlog item would XPASS. It's a plain `candy` block, and the item says why.
- A suggested fix is in its text: `emit` writes an empty literal with the type the checker found.

**Size and speed:** `src/cdy` is 2 lines longer, because a `fold`'s `fn`, start and list each get their own line. The build is unchanged at 0.98 s (medians of seven runs, measured twice against step 2's `bin`).

The as-built note is under step 3 in `doc/hl_rqmt/collections_2.md`, and B123 has a note. On commit this is one boot step, `boot/65`.

## Owner

> tick, gawc

## Claude Code

*ran: Tick B178, commit step 3, tag boot/65*

I've ticked and committed step 3 as `9e3d677`.

- **Tick:** B178 is `done`, with the note "ticked in review", and the backlog index is regenerated.
- **Commit:** your tree had no edits besides mine. The commit holds step 3's files and the new B184, which stays open.
- **Boot step:** `boot/65` is tagged on it and is an annotated tag. The bootstrap check passed for this step without staging, and the working tree is clean.

Nothing is pushed. Next is step 4 (B179), the loops in `emit.cdy`, when you say go.

## Owner

> go

## Claude Code

*ran: Save boot/65 bin; list emit.cdy loop candidates*

*ran: Show emit.cdy loops, part 1*

*ran: Show emit.cdy loops, part 2*

*ran: Callers of each emit.cdy loop*

*ran: Find name-set uses*

*ran: See the end of PY_RESERVED*

*ran: See how PY_RESERVED calls name-set*

I'm converting `emit.cdy`'s loops now, all in one edit script.

*ran: Apply step 4 conversions to emit.cdy and cdyc.cdy*

*ran: Fix the closing parens, rebuild bin*

*ran: Fix paren count, rebuild bin*

`bin` rebuilt, and the fixpoint holds. Next: other loop shapes, then timing and tests.

*ran: Check for counter loops, diff stat*

*ran: Time build, boot/65 bin vs new*

*ran: Run full pytest*

The two timings disagree (old 0.93 and 0.94 s, new 0.93 and 0.96 s), so I'm running two more pairs.

*ran: Time again; run linters*

*edited: `doc/hl_rqmt/collections_2.md`*

*ran: B179 to review, notes, doc tests*

Step 4 (the loops in `emit.cdy`, B179) is built and in `review`; nothing is committed. pytest passes (626 tests, 5 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and reproduces itself.

**25 of the 29 loops are one call now:**
- **9 `map`s:**
  - the lists of Python text: `emit-exprs`, `emit-types`, `emit-fields`, `emit-parts`, `emit-any-params`, `variant-refs`;
  - `field-types`, `bind-locs`, `variant-list-names`.
- **5 a `map` then `join`:** the strings built a line at a time: `emit-stmts`, `emit-binds`, `emit-record-fields`, `emit-variants`, `emit-imports`.
- **One `filter`:** `used-tvars`.
- **One `find`:** `holder`, with `with-default`.
- **9 `fold`s:**
  - `name-set`;
  - the environment: `global-names`, `add-globals`, `bind-locals`;
  - `bound-locals`, `bound-in-cases`, `bound-in-lists` and `type-vars`. These keep a `start` argument, because they call each other recursively, each passing on what it has so far.
  - `check-py-fields`. It folds only to catch a clash and `fail`; it ignores the fold's result and returns `true` as before.
- `generic-variants` and `deft-field-types` were already `fold`s; they lose their `acc` argument.

**Four stay loops:**
- `mangle-chars` and `escape-chars` walk a text.
- `emit-params` walks two lists at once.
- `emit-match` writes the first case with `if` and the rest with `elif`, and may write the last case as an `assert`.

**Size and speed:** `src/cdy` is 74 lines shorter. The build went from 0.94 s to 0.93 s, which is within the noise (medians of seven runs, measured four times against step 3's `bin`).

The as-built note is under step 4 in `doc/hl_rqmt/collections_2.md`, and B123 has a note. On commit this is one boot step, `boot/66`.

## Owner

> tick, gawc

## Claude Code

*ran: Tick B179, commit step 4, tag boot/66*

I've ticked and committed step 4 as `2d8101e`.

- **Tick:** B179 is `done`, with the note "ticked in review", and the backlog index is regenerated.
- **Commit:** your tree had no edits besides mine, so the commit holds only step 4's files.
- **Boot step:** `boot/66` is tagged on it and is an annotated tag. The bootstrap check passed for this step without staging, and the working tree is clean.

Nothing is pushed. Next is step 5 (B180), the loops in `expand.cdy`, `include.cdy`, `cdyc.cdy` and `read.cdy`, when you say go.

## Owner

> go

## Claude Code

*ran: Save boot/66 bin; list loop candidates in step 5's files*

*ran: Read expand.cdy loops*

*ran: Read include.cdy and cdyc.cdy loops*

*ran: Read read.cdy and prelude_macros.cdy loops*

*ran: Write a paren-aware script to strip dropped acc args*

*ran: Find tests calling these modules' functions*

None of the tests call the functions I'm changing. Next, the new definitions:

*ran: Rewrite step 5's loop definitions*

Next I'll drop the now-unused `acc` from those 18 functions: from each `defn`, its `sig`, and every call.

*ran: Drop acc from defns, sigs and call sites*

*ran: Fix the sig lookup and rerun the scripts*

The one call the script skipped, `(imported (macro-map …))`, is a `let` binding named `imported` in `expand-file`, not a call. Skipping it was right. Next, `put-parts` in the library:

*ran: Convert put-parts, stage library, rebuild bin*

`bin` rebuilt, and the fixpoint holds. Next: remaining `acc`s, timing, and the full test run.

*ran: Leftover accs, diff stat, timing*

*ran: Full pytest and linters*

*edited: `doc/hl_rqmt/collections_2.md`*

*ran: B180 to review, notes, doc tests*

Step 5 (B180) is built and in `review`; nothing is committed. pytest passes (626 tests, 5 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and reproduces itself.

**29 of the 33 loops are one call now:**
- **11 `map`s:**
  - `expand-all`, `expand-defs`, `each-clause`, `stamp-all`, `macro-list`, `imp-list`, `exports-of`, `imported`;
  - `arg-binds` and `expand-modules`, which need each item's index, map over `(zip (range …) xs)`;
  - `stems-of` is now `(map path-stem …)` at its one call, and its `defn` is gone.
- **4 a `map` then `concat`:** `helper-forms`, `macro-program`, `analyse-modules` and `put-parts`.
- **`filter`:** `pick-forms` is one `filter`. `module-imports` and `other-forms` are each a `filter` then a `map`: one keeps the imports, the other everything else.
- **One `all`:** `all-names`.
- **One `find-index`:** `cycle-text` (`include.cdy:94`), which now takes the stack from the repeated key on.
- **9 `fold`s:**
  - `macro-map`, `import-all`, `add-helpers`, `load-imports` and `include-forms` start from a value their caller passes in;
  - `mangled-names` and `exports-by-key` start from an empty map;
  - `unique-names` and `unique-stems` fold only to catch a clash and `fail`, then return `true`, as `check-py-fields` did in step 4.

**Four stay:** `read.cdy`'s `line-starts`, `read-all`, `read-list` and `read-str`, which walk a text.

**One loop outside the step's four files:** `put-parts` in `prelude_macros.cdy`. The survey counted it, but no step had it, so I took it here. It's a library file, so its copy in `bin` is updated too. `boot/66` builds with the new copy, so no `STAGING` entry is needed.

**Size and speed:** `src/cdy` is 51 lines shorter. The build went from 0.95 s to 0.94 s (medians of seven runs, measured twice against step 4's `bin`).

**All four loop steps:** 111 loops are now calls and 21 stay, each with its reason in the HLD's notes. B123 has a note saying so.

**Decision for you: B123 ("the translator writes its list loops by hand").**
- **Close it with this step (recommended):** its work is done, and the 21 loops left are kept on purpose (*lasting*).
- **Keep it open until step 8:** the docs step, alongside B69's update.

On commit this is one boot step, `boot/67`.

## Owner

> tick, close B123, note 21 loops left, gawc, then go over `macro-map` real quick

## Claude Code

*ran: Tick B180, close B123 with its note, verify names*

*ran: Commit step 5, tag boot/67, show macro-map*

Step 5 is committed as `659870f`, and `boot/67` is tagged on it. That's an annotated tag, and the bootstrap check passed without staging.
- **Ticks:** B180 is `done`.
- **B123:** closed, with a note naming the 21 loops left and why each stays: two lists walked at once, walking a text, a count, an early exit, a growing work list, the name checks, forms taken two at a time, and the `if`/`elif` chain.
- **Commit:** your tree had no edits besides mine. Nothing is pushed.

## `macro-map` (`src/cdy/expand.cdy:93`)

**What it does:** it adds a list of macros to a map from name to macro. A name already in the map is an error.

**Before**, a loop by hand:
```
(defn macro-map (macros acc)
  (if (= (len macros) 0)
    acc
    (let ((macro (at macros 0))
          (name (get macro name)))
      (if (map-has acc name)
        (fail (format "...defmacro: {name} is already a macro"))
        (macro-map (rest macros) (map-set acc name macro))))))
```

**Now**, a `fold`:
```
(defn macro-map (macros start)
  (fold
    (fn (acc macro)                       ; the map so far, the next macro
      (let ((name (get macro name)))
        (if (map-has acc name)
          (fail ...)                      ; a clash panics, ending the fold
          (map-set acc name macro))))     ; else the map with it added
    start                                 ; the map to start from
    macros))
```

`(fold f start xs)` calls `(f acc x)` for each item in turn. `acc` begins as `start`, and each result becomes the next `acc`. The old loop did the same steps: the `len`/`at`/`rest` handling is gone, and the per-item work is now the body of the `fn`.

**Why it takes a `start` instead of always starting from `empty-map`:** `expand-file` calls it twice, and the second call starts from a map that already has entries.
- `expand.cdy:54`: `(macro-map (get imports macros) empty-map)` builds the imported macros from nothing.
- `expand.cdy:62`: `(macro-map own imported)` adds the file's own `defmacro`s on top of those.

So a file that defines a macro with the same name as an imported one fails here, and so do two imports that define the same name. That's why `start` stays a parameter rather than becoming a fixed `empty-map`.

**In Python**, the `fn` becomes a nested Python `def`, typed `(acc: Mapping[str, expand__Macro], macro: expand__Macro) -> Mapping[str, expand__Macro]`. The `fold` becomes `cdy_rt.primitives.list_fold(...)`, which is `functools.reduce`.

Next is step 6 (B181): replace the `to-list`s with `(List x)`, then remove the `to-list` declaration, in two boot steps. I'll start when you say go.

## Owner

> got it... miss read it... next

## Claude Code

Starting step 6. First, a count of the `to-list`s left:

*ran: Count to-list uses; read B174*

*ran: Show to-list in spec, tests, library*

*ran: Find to-list used as a value or in the editor grammar*

Every use is a call, so a regex will do. Next: replace them all except the declaration, then rebuild.

*ran: Replace (to-list x) with (List x) everywhere but system.cdy*

*ran: Stage library, rebuild bin*

*ran: Inspect the mypy errors*

*ran: Show read-type; try a user-level repro*

*ran: Reorder read-type's clauses, file B185, rebuild*

The rebuild passes mypy. Step 6 is two boot steps, and this is the first: the translator stops calling `to-list`. Next: the tests, timing and linters for it.

*ran: Full tests, linters, to_list count in bin, timing*

*ran: Diff stat, HLD step 6 text, B181 state*

*ran: HLD note for step 6 part 1, B181 in-progress, index*

The first half of step 6 (B181) is built: the translator no longer calls `to-list`. Nothing is committed. pytest passes (626 tests, 5 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt, reproduces itself, and contains no `to_list` calls.

**What changed:** a script turned all 108 remaining `(to-list x)` calls into `(List x)`.
- **98 in the translator:** `lower.cdy` 43, `core.cdy` 19, `emit.cdy` 10, `check.cdy` 7, `expand.cdy` 7, `read.cdy` 5, `include.cdy` 4, and `prelude_macros.cdy` 2. That last one is a library file, so its copy in `bin` is updated too.
- **8 in the spec's examples**, in `25-checking.md` and `40-expressions.md`.
- **2 in the test programs.**
- Every use was a call, never a value. The declaration in `system.cdy` and `library.builtins`'s listing of it stay until the second half.

**New bug, B185 (a defect):** `(List x)` can fail `mypy --strict` in a `match` that produces a value.
- mypy types the Python temporary from its first assignment, and `(x,)` is a one-item tuple to it. A later clause with a list of a different length then fails.
- `to-list` returned `tuple[T, ...]`, which hid this in the translator. A 4-line user program reproduces it: `(match m ((Some v) (List v)) ((None) (List 1 2)))`.
- **Workaround:** `read-type` (`core.cdy:1005`) now lists its clause that gives a whole list first, with a comment pointing to B185.
- Its repro is a plain `candy` block for the same reason as B184's. The item says one fix in `emit` would likely close both: annotate Python with the type the checker found.

**Speed:** the build is unchanged at 0.94 s.

B181 stays `in-progress`, with a note on the first half, and the HLD has the matching note under step 6.

**Next:**
- On "gawc", I commit this half and tag it `boot/68`.
- Then I build the second half: remove `to-list` from `system.cdy` and `spelling.py`, and `to_list` from `primitives.py` and its test. That becomes `boot/69`, and B181 goes to `review` then.
- The second half has to wait for this commit: `boot/67`'s `bin` still calls `to_list`.

## Owner

> so, `(map List xs)` works now?

## Claude Code

I'll test it rather than guess:

*ran: Try (map List xs); read B171*

No, it doesn't. `(map List (List 1 2 3))` fails with `unknown name List`.

**Why:** `(List x …)` isn't a function. The analyser recognises it as its own form and builds the list directly, so `List` on its own isn't a value. That's B171, still open, low priority.

**Making it a value wouldn't help either.** B171's text points out that a function with a rest parameter, used as a value, takes only its arguments before the rest ([[expr.rest]]). `List` has nothing before its rest, so as a value it would take no arguments, and `(map List xs)` still wouldn't wrap each item.

**What does work:** `(map (fn (x) (List x)) xs)`.

**What removing `to-list` costs:** `(map to-list xs)` did work, since `to-list` is an ordinary built-in. That's the one thing `(List x)` doesn't replace. Nothing in the translator, spec or tests used `to-list` as a value; I checked before replacing. It's a small loss, but worth recording.

**Decision for you: record it, or bring `to-list` back?**
- **Record it (recommended):** when I remove the declaration, I'll add a note to B174 and B171 saying `(map to-list xs)` is gone and `(fn (x) (List x))` replaces it.
- **Bring it back:** if you'd rather keep a one-item list as a value, that undoes B174, which you chose to fix.

Step 6's first half still waits on "gawc".

## Owner

> record it, i guess my current comment is that `operators` and `type construction` are very different things... and there expressions are different...and how this "kinda" breaks regular lisp/scheme families sematics... thoughts?

## Claude Code

I'll add the `(map to-list xs)` note to B174 and B171 when I remove the declaration.

On your point: I'd put the line in a slightly different place. Operators and type construction differ less than it looks. The real split is between functions and syntax, and Candy has moved operators to the function side but left `List` and `Tup` on the syntax side.

**Operators now behave like Lisp.** Since `collections`, `+` is an ordinary built-in with a type, `(Fn (number number (Rest number)) number)`, and it's a value: `(fold + 0 xs)` works. That's Scheme's model, apart from the static types.

**`List` and `Tup` are syntax.** `(List 1 2)` isn't a call: the analyser turns it into its own node (`ListOf`, `Tuple`). That's the ML or Haskell model, where `[1, 2]` and `(a, b)` are syntax, not function calls. So in Candy, `List` is the one constructor that isn't a value: a record's or variant's constructor is a value, and so is `+`. In Scheme, `list` is just a procedure, and `(map list xs)` works.

Three things cause this, and they're worth keeping apart:

1. **One name for a type and a value.** `List` is a type in a `sig` and a constructor in an expression. Haskell has the same punning (`data P = P String`), but keeps types and values in separate namespaces, so both can exist. Candy's built-ins map and `spelling.py` have one entry per name, and `List` is used by its type. That's an implementation limit (B171 says so), not a design one.

2. **A rest function used as a value loses its rest.** This rule ([[expr.rest]]) is the real departure from Lisp. In Scheme a procedure that takes any number of arguments stays that way when passed around, so `(map list xs)` and `(apply + xs)` work. In Candy the value takes only its parameters before the rest, so even a real `List` function would be `(Fn () (List a))` as a value.
   - **Possible fix:** give the value the number of arguments that its expected type asks for. The checker already checks a call's `fn` arguments after the others, so in `(map List xs)` it knows by then that it wants `(Fn (Int) ?b)`. It would use `List` with one argument, and Python would get `lambda x: (x,)`.
   - With no expected type, it would fall back to the current rule.
   - That would make `(map List xs)` work, and `(fold + 0 xs)` would keep working.

3. **`Tup` can't be a function.** Its result type depends on how many arguments it gets and what each one's type is. Static typing can't express that without much heavier machinery. ML makes tuples syntax for the same reason. I'd call this one *lasting*.

**My suggestion:** make `List` an ordinary function, as `+` already is, rather than calling constructors a different category. That needs fixes 1 and 2. `Tup` stays syntax, and the spec would say why. Operators are already right.

**Decision for you: what to file.** This is a language design question, not part of `collections-2`.
- **An `idea` item (recommended):** "rest functions as values take the number of arguments their expected type gives; types and values in separate namespaces", linked from B171. It would go in a later HLD, probably alongside interfaces ([[B34]]), which also touches the operators' types.
- **Just a note on B171.**
- **Nothing for now.**

Step 6's first half still waits on "gawc".

## Owner

> i just want to note this "a script turned all 108 remaining (to-list x) calls into (List x)." don't respond

## Claude Code

Noted.

## Owner

> still reading, "So in Candy, List is the one constructor that isn't a value: a record's
>   or variant's constructor is a value, and so is +. In Scheme, list is just a procedure, and (map list xs) works."... and i know ive asked this before.... if `List` is a `very special` constructor... then why can't it just be a `procedure`?

## Claude Code

*ran: Check why List was made a form*

*ran: Read the HLD passages on List as a constructor*

It can be a procedure. The plan was for it to become one, and it was deferred, not ruled out.

**How it got here:**
- **`semantics`** made `(List …)` a form because Candy had no way then to type a function taking any number of arguments. Rest parameters didn't exist yet, so the analyser built the list itself (`ListOf`).
- **`collections`** added rest parameters, and its HLD proposed the change: `List` as an ordinary built-in, `(sig List (Fn ((Rest a)) (List a)))` (`collections.md:142`).
- **In step 1** you chose to keep it a form, *for now*, on 2026-11-08: option A, recorded in B171's notes. That's probably the earlier conversation you're remembering.

So the original reason, no rest parameters, is gone. Two reasons remain (`collections.md:237`):

1. **One name can't be both a type and a value yet.** The built-ins map and `spelling.py` have one entry per name, and `List`'s entry is its type's. That's an implementation limit. B171 plans to fix it when the symbol table next changes (the `namespaces` branch): one name with a type entry and a value entry.

2. **The value rule.** A rest function used as a value keeps only its parameters before the rest, so a procedure `List` would be `(Fn () (List a))` as a value. With only this fix, `(map List xs)` still fails. It needs the expected-arity rule I described: the value takes as many arguments as its expected type asks for, here one.

**With both fixed,** `List` is a procedure like `+`:
- A call `(List 1 2)` still emits the tuple literal `(1, 2)`, so it's no slower.
- As a value it's a function, `lambda x: (x,)` or `*xs`.
- `(map List xs)` works, as in Scheme.
- `Tup` stays syntax, because its type depends on how many items it has.

Fix 1 is plumbing. Fix 2 is a language rule and needs a decision, which is why I'd file it as an idea for a later HLD rather than fold it into `collections-2`.

**Decision for you: what to file.**
- **The `idea` item (recommended):** it would name B171's fix plus the expected-arity rule as the way to make `List` a procedure.
- **A note on B171.**
- **Nothing for now.**

Step 6's first half still waits on "gawc".

## Owner

> gawc

## Claude Code

*ran: Commit step 6 part 1, tag boot/68*

Committed as `34da27d`, with `boot/68` tagged on it. That's an annotated tag, and no staging was needed. I'm building the second half now: taking `to-list`'s declaration out.

*ran: Find the remaining to-list declarations and docs*

*ran: Remove to-list from system, spelling, spec*

*ran: Remove to_list primitive and test; stage library; rebuild*

*ran: Check bin library, run tests and linters*

Everything passes, and `bin`'s library no longer has `to-list`. Next, the notes:

*ran: HLD done note, B181 review, B174 done, B171 note*

The second half of step 6 (B181) is built, and B181 is in `review`; nothing is committed. pytest passes (626 tests, 5 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean.

**`to-list` is gone from:**
- `system.cdy`, its declaration;
- `spelling.py`, its Python spelling;
- `primitives.py`, the `to_list` function, along with its test.

`bin/py/cdy_translator.py` comes out byte for byte the same, since `boot/68` already made no `to-list` calls. Only `bin/py/system.cdy`, the library copy, changes. That's still a change in `bin`, so it gets `boot/69`.

**Spec:**
- `types.constructors` (`spec/20-types.md:198`) now says `(List x)` is the one way to make a list of one item, linking B174.
- `library.builtins` no longer lists `to-list`.

**Backlog and HLD notes:**
- **B174 is `done`.** Its note records what you asked: `(map to-list xs)` is lost, and it's now `(map (fn (x) (List x)) xs)`.
- **B171 has a note** with your question about why `List` can't be a procedure, and my answer: it can, given its own fix plus the expected-arity rule. It also says the idea isn't filed as its own item yet.
- **The HLD's step 6** has a *Done* note covering both boot steps.

On commit this is `boot/69`, and step 6 is finished. Step 7 is next: `equatable` (B182, which fixes B173).

## Owner

> gawc

## Claude Code

*ran: Commit step 6 part 2, tag boot/69*

I've committed step 6's second half as `441eeb0`. `boot/69` is tagged on it and is an annotated tag; the bootstrap check passed for this step without staging. The working tree is clean, and nothing is pushed.

You said "gawc" without "tick", so B181 is still in `review`. A later "tick" will mark it `done`, in a commit of its own or folded into step 7's.

Step 7 is next: `equatable` (B182, fixing B173), when you say go.

## Owner

> go

## Claude Code

Starting step 7. First, how the constraint variables work today:

*ran: Find constraint machinery in check.cdy and system.cdy*

*ran: Read the constraint and compare code*

*ran: Find CONSTRAINTS and constraint-of*

*ran: Read St, Pending and the per-definition check*

*ran: Find instantiate callers, St constructions*

*ran: Read Global/Prim inference; current spec messages*

*ran: Find comparing built-ins and prelude functions*

*ran: Apply the equatable changes*

`assoc` takes several field/value pairs, as `emit.cdy` already uses it. Next: stage the library and build.

*ran: Stage library, rebuild bin*

The build passes, so the translator has no generic function comparing a sig's type variable. Next: the full test suite, with B173's repro.

*ran: Run full pytest*

B173's repro now passes as an error, so it XPASSes. Under the process, a closed defect's repro moves to the spec. Next, the spec rules the HLD names:

*ran: Read the spec rules to update*

*ran: Update spec rules; run their tests*

The new examples all pass. The one failure left is B173's repro, which needs to leave the item now that the spec has it. I'll check how an earlier closed defect recorded its moved repro:

*ran: See how closed defects record their moved repro*

*ran: See B137's note header for the moved repro*

*ran: Move B173's repro into its note, set review*

*ran: Find stale mentions of the old = type*

*ran: Full tests, linters, timing*

The old timing is 0.28 s because the run fails: `tmp/c7/b68`'s library still declares `to-list`, which the current `spelling.py` no longer has. I'll time against `boot/69`'s `bin`, taken from git:

*ran: Extract boot/69 bin and time against it*

The build is 0.94 s → 0.95 s, about 1.5% slower: each name now looks for `equatable` variables, and each definition runs one more check. Next, the notes:

*ran: HLD step 7 note, B182 review, B172 note*

Step 7 (`equatable`, B182) is built and in `review`, and it fixes B173; nothing is committed. pytest passes (631 tests, 4 expected failures; one fewer, since B173's repro now passes). ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and reproduces itself.

**What it is:** `equatable` is a new constraint variable, for any type except one that is or holds a function.
- It's declared in `CONSTRAINTS` (`core.cdy:763`) with an empty type list, because no finite list describes it.
- `=`, `!=`, `contains` and `elem-index` (`system.cdy`) and the prelude's `index-of` now take it.

**How it's checked** (`check.cdy`): in two places, because finding a function inside a record or sum needs the type shapes in `Ctx`, and `unify` doesn't have them.
- **When a variable is bound** (`bind-equatable`):
  - Any concrete type is accepted for now.
  - A sig's own type variable is accepted only if its constraint is `equatable`, or one of the constraints whose types are all `equatable`. That's every constraint except `appendable`, since its lists may hold functions. So `(sig same (Fn (a a) Bool)) (defn same (x y) (= x y))` fails with "argument 1 of =: expected equatable, got a", which is B173's repro.
- **When the definition is done** (`check-compared`, run after `solve-pending`): each use of a name whose type contains an `equatable` variable has been recorded with its position. `has-fn` checks what the variable finally became.
  - A function, a list of functions, or a record or variant holding one gives "NAME: a function can't be compared, got T", reported at the use.
  - This covers a direct `(= f f)`, a generic `(same inc inc)`, and `=` passed as a value.

**One change from the accepted HLD:** it said `infer-compare` would stay for concrete types. I removed it instead, as B173's own fix proposed, because the end-of-definition check covers that case with the same message. The HLD's as-built note says so.

**What wasn't affected:**
- **The translator** needed no `sig` changes: none of its generic functions compare a type variable.
- **Map keys** aren't constrained to `equatable`, as before: Python hashes them, and a function key is hashed by identity.

**Spec:**
- **`checking.constraints`:** the new table row, its explanation, an example, and four error rows: an `appendable` compared, `(same inc inc)`, a list of functions through `contains`, and B173's repro moved here.
- **`expr.equality`:** it now says a generic function's comparison is checked too.
- **`expr.operator-values`:** `=` as a value is `(Fn (equatable equatable) Bool)`, and its *for now* link to B173 is gone. It gained an error row for `(let ((eq =)) (eq f f))`.

**Speed:** about 1.5% slower, 0.94 s → 0.95 s (medians of seven runs, measured twice against `boot/69`'s `bin`). That's the cost of looking for `equatable` variables at each name and the extra check per definition.

**Backlog:**
- B173 is in `review`, with its old repro kept verbatim in its note, and B182 is in `review` too.
- B172 (dropped) has a note that `infer-compare` is gone.
- B181 (step 6) is also still in `review`, since you haven't ticked it.

On commit this is `boot/70`. Step 8, the docs, is next.

## Owner

> This is an aside, process aside, don't respond, can you put the title of the issue in parentheses after the issue number

## Claude Code

*wrote: `~/.claude/projects/-home-skerrj-dev-exp-candy/memory/backlog-ids-with-titles.md`*

*ran: Add memory index line*

Noted.

## Owner

> I.e. for the issues that only ref the issue number

## Claude Code

*edited: `~/.claude/projects/-home-skerrj-dev-exp-candy/memory/backlog-ids-with-titles.md`*

Got it. I'll add the title only where a backlog id stands on its own, and leave it off where the sentence already says what the item is.

## Owner

> Once per response....

## Claude Code

*edited: `~/.claude/projects/-home-skerrj-dev-exp-candy/memory/backlog-ids-with-titles.md`*

Got it: each item gets its title once per response, at the first mention that doesn't already say what it is.

## Owner

> Can we walk thru, pipeline complete, example of an `equatable` constraint?

## Claude Code

I'll run a real example through the pipeline, so every stage below is actual output:

*ran: Run good and bad equatable examples*

*ran: Line numbers for the walkthrough*

Here is one small program, run through the translator:

```
(sig has (Fn (equatable (List equatable)) Bool))
(defn has (x xs) (contains x xs))

(put (has 2 (List 1 2)))
```
It prints `true`, and the generated Python passes `mypy --strict`.

## 1. Read, include and expand
Nothing here knows about `equatable`. The reader makes it a symbol, and `include.cdy` adds the prelude. `expand.cdy` expands `put` into `(put-line (text …))`.

## 2. Analysis (`core.cdy`)
- The `sig` is checked by `check-type`. `equatable` is lowercase, so it's a type variable, like `a`.
- `constraint-of` (`core.cdy:779`) finds `"equatable"` in `CONSTRAINTS` (`core.cdy:773`), so it counts as a constraint variable.
- `contains` is a built-in typed in `system.cdy:112` as `(Fn (equatable (List equatable)) Bool)`.

## 3. Type check (`check.cdy`): the work happens here
Each definition is checked on its own (`check.cdy:89`).

**Inside `has`'s body**, the sig's `equatable` is *rigid*: one fixed, unknown type.
1. Analysis makes `contains` a `Prim` (a built-in), so `name-type` instantiates it. `keep-constraint` (`:1190`) gives each `equatable` in its sig a fresh `?7:equatable`, so its type becomes `(Fn (?7:equatable (List ?7:equatable)) Bool)`.
2. `noted` (`:317`) records `Compared ?7:equatable "contains" 2:19` in the state.
3. Argument `x` has the rigid type `equatable`, so `unify` calls `bind-equatable` (`:1101`). For a rigid variable, its constraint must be within `equatable`. `equatable` is within itself, so `?7` is bound to `equatable`, and `xs` matches as well.
4. At the end of the definition, `check-compared` (`:584`) resolves `?7` to the rigid `equatable`. `has-fn` (`:598`) finds no function in it, so there's no error.

**At the top-level call `(has 2 (List 1 2))`:**
1. `has` is instantiated as `(Fn (?12:equatable (List ?12:equatable)) Bool)`, and `noted` records `?12` with the position of `has`, 4:6.
2. Argument `2` is an `Int`. `bind-equatable` accepts any concrete type, so `?12` is bound to `Int`, and `(List 1 2)` matches as `(List Int)`.
3. At the end, `check-compared` resolves `?12` to `Int`. `has-fn` finds no function, so there's no error.

## 4. Lower (`lower.cdy`)
Nothing special. The types are carried through as they are.

## 5. Emit (`emit.cdy`)
`type-param` (`emit.cdy:648`) gives the Python bracket entry. `number` would get a constrained entry, `[number: (int, float)]`. `equatable` has none to give, so it's a plain one:
```python
def has[equatable](x: equatable, xs: tuple[equatable, ...]) -> bool:
    return cdy_rt.primitives.list_contains(x, xs)
print(cdy_rt.primitives.show(has(2, (1, 2)), 'Bool'))
```
Python can't express "not a function", so `equatable` is enforced only by Candy's checker. mypy sees an ordinary type variable.

## The two ways it fails

**A function passed in** (`(has inc (List inc))`): `?12` is bound to `(Fn (Int) Int)`. `bind-equatable` accepts it, because at that point it can't see into records, so it checks nothing yet. `check-compared` then finds it:
```
eq_bad.cdy:7:6: has: a function can't be compared, got (Fn (Int) Int)
```
The error is reported at the use of `has`, because `noted` saved that position.

**A plain `a` compared** (`(sig has (Fn (a (List a)) Bool))`): inside the body, `contains`'s `?7:equatable` meets the rigid `a`. `a` has no constraint, so `bind-equatable` refuses, and the error comes at the argument:
```
eq_rigid.cdy:2:28: argument 1 of contains: expected equatable, got a
```
This is B173 (A generic function's `=` compares functions), now fixed.

**Why it takes two places:** a function type could be rejected at binding. A record or sum that holds a function can only be found with the type shapes in `Ctx`, which `unify` doesn't have. So binding accepts everything except a sig variable without the constraint, and the end-of-definition check decides the rest.

## Owner

> I'm already stuck on step 1

## Claude Code

I'll go through step 1 slowly. It's three stages before any type checking, and none of them gives `equatable` a meaning yet.

**Read** (`read.cdy`) turns the text into *forms*: nested lists of symbols, numbers and strings. The `sig` line becomes:
```
(sig has (Fn (equatable (List equatable)) Bool))
  ↓
Lst [ Sym "sig", Sym "has",
      Lst [ Sym "Fn",
            Lst [ Sym "equatable", Lst [ Sym "List", Sym "equatable" ] ],
            Sym "Bool" ] ]
```
At this point `equatable` is only `Sym "equatable"`, a name, the same as `has` or `Bool`. The reader doesn't know it's a type, let alone a constraint. Each form also carries its position (line:col), which the error messages use later.

**Include** (`include.cdy`) reads the program's imports. This program has none, but every file implicitly imports `prelude.cdy`, so that's read too. That doesn't affect this example; it's why `index-of` or `Some` would be available if we used them.

**Expand** (`expand.cdy`) replaces macro calls with what they expand to. The only macro here is `put`, from `prelude_macros.cdy`:
```
(put (has 2 (List 1 2)))
  ↓
(put-line (text (has 2 (List 1 2))))
```
`put` with one argument means "print its text as a line". The `sig` and `defn` aren't macro calls, so they pass through unchanged.

**After step 1** there are three forms, all still plain nested lists:
```
(sig has (Fn (equatable (List equatable)) Bool))
(defn has (x xs) (contains x xs))
(put-line (text (has 2 (List 1 2))))
```
Nothing has decided what any name means. Step 2 (analysis) is the first place `equatable` is recognised as a type variable, and as a constraint.

Is it one of these three stages that's unclear, or the forms themselves?

## Owner

> What are the other cases where a type variable gets used in this way... And what are the other cases where a type variable, that's also a constraint, gets used in this way?

## Claude Code

I'll check a few facts before answering: which built-ins use each constraint, and whether a `deft`'s type variable can be one.

*ran: List constraint uses; test a deft with a constraint name*

*ran: Check whether deft constraint variables are specified*

*ran: See mypy errors for a constrained deft*

Type variables are used in three places, and constraint variables in four. Checking that turned up a bug, at the end.

## Ordinary type variables (any lowercase name)

1. **In a `sig`, a program's or the library's.** `equatable` takes the same path, minus the constraint.
   - Examples: `(sig map (Fn ((Fn (a) b) (List a)) (List b)))` in `system.cdy`, `(sig len (Fn ((List a)) Int))`, a user's `(sig f (Fn (a) a))`.
   - Inside the definition, `a` is rigid: one fixed, unknown type.
   - At each use, `instantiate` replaces it with a fresh `?N`, which unification then solves.
2. **As a `deft`'s parameters**, which make a generic type.
   - Examples: `(deft (Maybe a) (Some ((v a))) (None))` in `prelude.cdy`, `(deft (Result a e) …)`, and the built-in types `(deft (List a))` and `(deft (Map k v))` in `system.cdy`.
   - The type's arguments come from here, and so does the constructor's type: `Some` is `(Fn (a) (Maybe a))`, instantiated fresh at each use, as in case 1.
3. **The checker's own `?N`s**, for locals and anything else not yet known. A program never writes these.

## Constraint variables (a name in `CONSTRAINTS`, `core.cdy:763`)

There are six: `number`, `integer`, `float`, `comparable`, `appendable` and `equatable`. Numbering one makes an independent second one, as in `number2`.

1. **The built-ins' `sig`s** in `system.cdy`:
   - `number`: `+`, `-`, `*`
   - `float`: `/`
   - `integer`: `quot`, `mod`
   - `comparable`: `<`, `>`, `<=`, `>=`
   - `appendable`: `++`
   - `equatable`: `=`, `!=`, `contains`, `elem-index`
2. **The prelude:** `index-of`, which takes `equatable`.
3. **A user's `sig`:** the spec's examples include `total` (`number`), `biggest` (`comparable`), `scale` (`number` and `number2`) and `same` (`equatable`).
4. **A `deft`'s parameters.** This works, but nothing specifies it; see below.

**How `equatable` differs:** the other five each list their types. They're checked as soon as they're bound (`bind-listed`), with the error at the argument. `equatable` can't be listed, so it's the only one whose check waits for the end of the definition.

**They differ in Python too**, in what goes in the brackets after the name (`emit.cdy:648`):

| Constraint | Python |
|---|---|
| `number` | `[number: (int, float)]` |
| `comparable` | `[comparable: (int, float, str)]` |
| `appendable` | `[appendable: (str, tuple[Any, ...])]` |
| `integer`, `float` | no type variable: written as plain `int` and `float` |
| `equatable` | `[equatable]`, plain |

## The bug: a constraint variable as a `deft`'s parameter

I tested `(deft (Box number) ((v number)))`.
- **Candy enforces it:** `(Box "a")` fails with "argument 1 of Box: expected number, got String", because the constructor is instantiated through the same `keep-constraint`.
- **No rule says this is allowed.** No spec text or backlog item mentions it.
- **`(Box 1)` runs and prints `(Box 1)`, but fails `mypy --strict`** with three errors. `emit` writes `class Box[number: (int, float)](NamedTuple)`, and mypy rejects a constrained type variable on a NamedTuple class that has these `__eq__`, `__ne__` and `__hash__` methods ("The erased type of self … is not a supertype of its class").
- The same `deft` with a plain `a` passes mypy.

**Decision for you: what to do about it.**
- **File a defect, B186 (recommended):** the program type-checks and runs right but fails mypy, as B184 and B185 do. The fix to decide later: make a constraint variable an error as a `deft`'s parameter, or specify it and emit something mypy accepts.
- **Leave it:** no program uses it today.

Step 7 is still in `review`, and B181 (step 6) is still unticked.

## Owner

> How would having a candy language level syntax for constraint variables help and hurt?

## Claude Code

*ran: Get B34's title; see why names were chosen*

Today a constraint is carried by the variable's name, as in Elm: `number`, `number2`. Explicit syntax would move it into the `sig`: something like `(sig same (Fn (a a) Bool) (where (equatable a)))`, or Haskell's `Eq a =>`.

## How explicit syntax would help

- **One variable could have several constraints.** A name carries exactly one, so there's no way to say "a list I can append and compare". I hit this in step 7: an `equatable` variable meeting an `appendable` one keeps only the `appendable`, and the end-of-definition check has to make up the difference. With syntax, it's `(where (appendable a) (equatable a))`.
- **The names would be free.** `number`, `comparable` and the other four can't be ordinary variable names today, and an independent second one needs the numbering trick. With syntax, a variable can be called `n` or `k`, with its constraint stated.
- **Constraints would be declared, not hard-coded.** Today they're a fixed table in `core.cdy` (`CONSTRAINTS`). A syntax could name a constraint declared in the library, the way `system.cdy` declares types. That's the road to user-defined constraints, and to interfaces (B34, No `Collection` interface).
- **Accidents would become decisions.** The `deft` bug I just found exists because any type variable with a constraint's name gets the constraint, wherever it appears. With syntax, whether a `deft` may constrain its parameters becomes a rule someone writes.
- **The checker would be simpler.** It encodes constraints in variable names (`?7:equatable`) and reads them back out. With syntax, the constraint would be stored with the variable instead of inside its name.

## How it would hurt

- **Sigs get longer.** `(sig + (Fn (number number (Rest number)) number))` reads at a glance. With `where` clauses, all 17 constrained built-in `sig`s, and every user generic that compares or adds, get longer. Elm chose names for exactly this reason.
- **It could be designed twice.** Interfaces are planned after this epic, and the HLDs call the naming convention *lasting* until then. A syntax built now would likely be replaced by interface syntax.
- **Open questions follow.**
  - The checker would have to solve several constraints at once: two lists of types meeting gives their intersection, plus `equatable`'s rule.
  - Python can't say "int-or-float *and* not a function" (mypy can't express `equatable` at all), so `emit` would have to give up some of mypy's checking.
- **Bootstrap cost.** Changing the shape of `sig` means the previous translator must read the new `system.cdy`. That's a staged, two-boot-step change, like `to-list`'s removal.

## My take

Keep names through this epic, and bring in the syntax with interfaces, where it's needed anyway: interfaces are named constraints with operations.

The two real problems seen so far are worth recording for that design:
- one constraint per variable;
- the `deft` accident.

**Decision for you: what to record.**
- **A note on B34 (recommended):** it would name those two problems as input for the interfaces design.
- **Nothing for now.**

The `deft` defect (B186, if filed) is still waiting on your decision, step 7 is still in `review`, and B181 (collections-2 step 6: `to-list` gone) is still unticked.

## Owner

> Was thinking of `where` too.... Still reading... Wait

## Claude Code

I'll wait.

## Owner

> Ok, wait for interfaces

## Claude Code

*ran: Record the decision on B34*

I've recorded your decision as a note on B34 (No `Collection` interface): the `where` syntax waits for interfaces, and the constraint names stay until then. The note also lists the two problems from step 7 for that design to answer. A variable can carry only one constraint, and a `deft`'s parameter named for a constraint gets it without any rule saying so.

The note is in the working tree with step 7, uncommitted. Still open:
- **Step 7 (`equatable`):** in `review`, waiting on your tick.
- **B181 (collections-2 step 6: `to-list` gone):** still in `review`, not yet ticked.
- **B186:** whether to file the `deft` bug as its own defect.

## Owner

> Your thoughts on 186?

## Claude Code

*ran: Check for deft constraint uses; find the deft tvar check*

I'd make it an error: "a `deft`'s type variable can't be a constraint". I wouldn't make it a feature.

**The reasons:**
- **Constraints belong on functions, not data.** Haskell tried constraints on data types (`data Ord a => Set a`) and removed them in Haskell 2010 as a misfeature. They don't keep a bad value from being built any better than the functions' own constraints do, and every function that uses the type then has to repeat the constraint. Elm doesn't allow them either.
- **It fits your decision.** Constraints wait for interfaces. Shutting this off now, *lasting* until interfaces revisit it, means nobody comes to rely on an accident in the meantime.
- **Nothing uses it.** The translator, the spec and the tests have no such `deft`; the only occurrence anywhere is the note I just wrote on B34 (No `Collection` interface).
- **It's small.** `core.cdy:1320` already checks a `deft`'s type variables for repeats, and the error would sit next to it: `deft Box: a type variable can't be a constraint (number)`. One spec row would go in `types.records`, at the same rule as the repeated-variable error.
- **The other fix costs more.** Making the Python pass mypy would mean writing plain type variables for classes, with Candy alone enforcing the constraint. That's more code for a feature we'd want to remove anyway.

**When to do it:** I'd file B186 as a defect and fix it within step 7. Step 7 is the constraints step and isn't committed yet, the fix is a few lines, and it would close before the branch merges. The alternative is to file it open, for after the epic.

**Decision for you:** file B186 and fix it in step 7 (recommended), or file it open for later.

## Owner

> Go with your recommendation... Tick all...6 and 7...

## Claude Code

*ran: Read the deft tvar check and its spec row*

*ran: Read the types.records rule text*

Next: the check in `top-deft`, its spec row, and B186, filed with its repro already in the spec and closed in review. Then the ticks.

*ran: Add the deft check, spec rows, B186; tick all; rebuild; test*

The check is in, and pytest passes (633 tests, including the 2 new spec rows). B181, B182, B173 and B186 are all `done`. Next: the HLD note and the linters.

*ran: HLD note for B186; doc tests and linters*

I've ticked steps 6 and 7, and the fix for B186 (A `deft`'s type variable named for a constraint gets it, unspecified) is in step 7; nothing is committed. pytest passes (633 tests, 4 expected failures), and ruff, ruff format, mypy, pyright and pylint are clean. `bin` is rebuilt and reproduces itself.

**B186 fixed:**
- **The check:** `top-deft` (`core.cdy`) now rejects a `deft` type variable named for a constraint, reporting at that variable: `deft Box: a type variable can't be a constraint (number)`. A numbered one like `comparable2` is caught too.
- **The spec:** `types.records` (`spec/20-types.md`) now says a constraint belongs on the functions that need it, not on the type, *lasting* until interfaces, and it gained two error rows.
- **The item:** B186 is filed as a defect and closed. Its would-be repro went straight into the spec; the item keeps it verbatim in its note, and says why the error was chosen.
- No existing program used it.

**Ticked, all `done`:**
- B181 (collections-2 step 6: `to-list` gone)
- B182 (collections-2 step 7: `equatable`)
- B173 (A generic function's `=` compares functions), fixed by step 7
- B186

**Also in the tree, uncommitted:**
- Your decision on constraint syntax, as a note on B34 (No `Collection` interface).
- The HLD's step 7 note, now covering B186 and that decision.

On "gawc" this is one commit with `boot/70`. Step 8, the docs, is the last step before the merge.

## Owner

> Gawc

## Claude Code

*ran: Commit step 7, tag boot/70*

I've committed step 7 as `344e31b`. It holds the step 6 and 7 ticks, the B186 fix and the note on B34 (No `Collection` interface).

`boot/70` is tagged on it and is an annotated tag. The bootstrap check passed for this step without staging, and the working tree is clean. Nothing is pushed.

Next is step 8 (B183): the docs for the branch. That covers:
- `CLAUDE.md`;
- the epic, marking its third branch *done*;
- `library.md`, closing its Question 6's *for now*;
- `mutation_optimization.md`, recording where B69 stands;
- a "Looking back".

Then, before the merge, the chat archive with the token scrub, and `pytest -m bootstrap`. Say go when you want them.

## Owner

> Go

## Claude Code

Starting step 8. First, its task, and what `collections`' docs step touched, as a pattern:

*ran: Read B183 and the previous docs step's footprint*

*ran: Read collections' Looking back and its status line change*

*ran: Read the epic, library.md Q6, mutation_optimization and B69*

*ran: Read epic branch 3, library.md questions, B69 notes, B167 state*

*ran: Read the doc passages step 8 updates*

*ran: Read more doc passages for step 8*

*ran: Read multi_target operators and CLAUDE.md built-ins/checking bullets*

I have the full list of what step 8 updates. Next, the edits:

*ran: Update CLAUDE.md, epic, library, mutation, multi_target, iMVP, collections docs*

Next, the HLD itself: its status line, step 8's note, and "Looking back".

*ran: HLD status, step 8 note, Looking back; B183, B69 notes; tests*

pytest passes. In `collections`, the docs commit also carried the branch's chat archive. I'll check how `chat_archive.py` picks out a branch's part of the transcript:

*ran: Read chat_archive.py usage and the last archive's head*
