# Collections, part 2 (HLD)

**Status: accepted (2026-11-10), with the answers to its questions (tasks [[B167]],
[[B177]] to [[B183]]); proposed 2026-11-10, for branch `collections-2`. Epic: `python_complete.md`
(its third branch, continued). After tag `collections`.** Step 7 of `collections.md`,
moved here at its checkpoint (its Question 5): `map-acc`, and the translator's loops
onto the list operations. Its design was decided there and in the epic (the epic's
Question 11, 2026-10-30; `collections.md`, "The list operations") and is carried over,
not reopened; this HLD adds a fresh survey, the order of the steps, and which of the
items `collections` found come along.

## Where things stand

Counts from today's source (2026-11-10, after tag `collections`): the translator
(`src/cdy/`, 5,651 lines), its loops classified by a one-off script (not kept) on their
text, so the counts are rough.

| Item | Today | Seen where |
|---|---|---|
| [[B123]] the translator's loops by hand | 124 `defn`s with an `acc` argument: about 51 a `map` or `filter` written out (`(++ acc (to-list ...))` over `(rest xs)`), 38 a `fold` (a map or a count built up), 16 threading a state too (a `(Tup s (List b))` result: `infer-all`, `check-tops`, `retype-all`, `let-bindings`), 19 neither (walks over two lists, counters, early exits) | `core.cdy` 33, `emit.cdy` 27, `check.cdy` 20, `expand.cdy` 14, `lower.cdy` 12, `include.cdy` 8, `cdyc.cdy` 5, `read.cdy` 4, `prelude_macros.cdy` 1 |
| the list operations used | `map` 29, `fold` 15, `any` 9, `filter` 5, `all` 4, `find-index` 1, `take` 1; `find`, `zip` 0 | — |
| [[B69]] lists built by copying | `(++ acc (to-list x))` 72, each a copy of `acc` | — |
| [[B174]] `to-list` duplicates `(List x)` | 151 `to-list`s in the translator, 11 in the spec and tests | — |
| [[B173]] a generic `=` compares functions | `(same inc inc)` is `true` | its repro |

The translator builds itself in 1.02 s (`bin` on `src/cdy/cdyc.cdy`, three runs).
[[B19]] is done (a local `fn` is typed with what the checker inferred), so the reason
`library.md` kept the loops (a `fn` typed `Any`) is gone.

Found by `collections` (open), each a candidate here (Question 1): [[B173]] (a generic
`=` on functions), [[B174]] (`to-list`), [[B171]] (`List` not a value), [[B176]] (host
records), [[B170]] (a bracket list literal, an `idea`).

## Goals

- **The translator on the list operations:** each loop that is one of `map`, `filter`,
  `fold`, `any`, `all`, `find` or `map-acc` becomes that call ([[B123]]); with them most
  of the copies go ([[B69]]).
- **`map-acc`,** a `map` threading a state, as the epic decided.
- **One way to make a one-item list** ([[B174]]), and **no generic `=` on functions**
  ([[B173]]): Question 1's.

## Not goals

- **The loops that are none of them** (two lists at once, a counter, an early exit with
  a value): they stay `defn`s, *lasting* for what no operation says better.
- **Lists' copies made cheap:** what a `fold` building a list, or a `map-set` per key,
  still copies stays, for `mutation_optimization.md` ([[B69]]'s fix).
- **`reduce`:** the epic allowed it once `Maybe` was decided; nothing in the translator
  needs it (Question 2).
- **Interfaces, qualified names:** as `collections.md` (after the epic; `namespaces`).

## Proposal

- **`map-acc`** (`collections.md`, "The list operations"): `(sig map-acc (Fn ((Fn (s
  a) (Tup s b)) s (List a)) (Tup s (List b))))`, the state first as `fold`'s start
  value is, *lasting*. In Python a primitive with a loop, building a Python list and
  returning a tuple, so it doesn't copy. Taken apart with a `Tup` pattern: `(let (((st
  ys) (map-acc f st xs))) ...)`.
- **The loops,** by layer, each step one boot step, measured (the build's time before and
  after): a loop becomes a call when it is exactly one operation; its `fn` is written in
  place, or names a function that was the loop's per-item work. A loop kept says why
  only when that isn't plain (two lists, an early exit).
- **[[B174]]** (Question 1): after the loops, the `to-list`s left become `(List x)` by
  script, and `to-list` goes from `system.cdy` and `spelling.py`, in two boot steps
  (the translator off it, then its declaration out, since the step before still calls
  it: `collections.md`, "Looking back").
- **[[B173]]** (Question 1): `equatable`, a constraint variable for every type but one
  that is or holds a function, as its text proposes; `=` and `!=` take it, and a generic
  function that compares says so in its `sig`: the built-ins that compare (`contains`,
  `elem-index`), the prelude's `index-of`, and the translator's few. `infer-compare`'s look into the argument type stays
  for a concrete type; a type variable bound to `equatable` is checked when solved.

### The spec

| Rule | File | Step |
|---|---|---|
| `library.map-acc` (new): its type, an example threading a counter | `60-library.md` | 1 |
| `library.builtins`: `map-acc`; `to-list` gone | `60-library.md` | 1, 6 |
| `types.constructors`: `(List x)` the one way | `20-types.md` | 6 |
| `checking.constraints`: `equatable`; `expr.equality`, `expr.operator-values`: a generic `=` | `25-checking.md`, `40-expressions.md` | 7 |

The loop steps change no rule.

## Pros and cons

- **For:** the translator reads as the language it is written in; a `map` says what a
  loop is for, and the 72 copies' cost goes from quadratic to linear where they become
  `map` or `filter`.
- **Against:** a mechanical rewrite of about 105 functions, each a chance to change what
  a loop does; the tests (the fixpoint, T1 against T2 on every program) are the guard.
  A `fn` in a call becomes a nested Python `def` or a `lambda`, a call per item, so the
  build may not get faster: measured, not assumed.

## Bootstrap

Each step that changes `src/cdy/` rebuilds `bin`, one `boot/NN` each (from `boot/63`).
`map-acc` is a built-in, so its step needs no staging if `boot/62` reads its
declaration (`test_newest_step_reads_the_library`); the translator's first `map-acc`
calls come in that step or the next. `to-list`'s removal is two steps (above).

## Steps

1. **`map-acc`** ([[B167]]): the built-in, its primitive and rule; the translator's 16
   threaded loops onto it where each is one.

   *Done (2026-11-10). As built:* `map-acc` is a built-in (`system.cdy`), spelled
   `list_map_acc`, a primitive that builds a Python list and returns a tuple; the rule
   is `library.map-acc` (new), and `library.builtins` lists it. 12 of the 16 loops were
   one `map-acc`: `check-tops`, `infer-all`, `infer-clauses`, `retype-all`,
   `retype-pairs`, `retype-parts` and `retype-clauses` (`check.cdy`), `analyse-all`
   and `bind-params` (`core.cdy`, the latter's state a `(Tup Scope Int)`), and
   `lower-cases`, `low-all` and `effect-all` (`lower.cdy`, the last a `map-acc` then
   `concat`). Each keeps its name and its result's order, `(Tup items state)`, and loses
   its `acc` argument, which every caller passed as `empty-list` (30 calls). The other
   four aren't over a list: `fresh-types` counts down, and `format-parts`, `read-list`
   and `read-str` walk a text. In Python each `fn` is a nested `def`, typed with what
   the checker inferred. The translator's build: 1.02 s to 0.93 s. One boot step,
   `boot/63`, no staging (`boot/62` reads the new library).
2. **The loops in `core.cdy` and `lower.cdy`** ([[B177]]; 45).

   *Done (2026-11-11). As built:* 40 functions there had an `acc` argument, not 45 (step
   1 took five); two weren't loops (`add-name`, `read-type`). Of the 38 loops, 31 are
   one call now: 15 `map`s (three inlined where the per-item work was a function already,
   `(map sym-name ...)`, `(map quoted ...)`, `(map analyse-type ...)`, their `defn`s gone),
   one `filter` (`missing-variants`), 12 `fold`s (the maps built a name at a time:
   `top-names`, `read-decls`, `read-sigs`, `put-all`, `stems-for`; `deft-fields`, which
   reads the fields so far; `holes`), and three `map-acc`s: `let-bindings` (each binding's
   pairs, then `concat`; its per-binding work is `let-binding`, new), `destructure` (over
   `(zip (range ...) names)` for the index) and `lower-program` (then `concat`). A
   function keeps its name; an `acc` every caller passed empty goes, and one a caller
   seeds (`add-names`, `read-sigs`, `put-all`) is the fold's `start`. Seven stay loops:
   `tup-binds` and `pattern-binds` (each name checked against those bound so far, `_`
   skipped but counted), `assoc-fields` (two forms at a time), `format-parts` (a text),
   and `assigns`, `fill-holes` and `refill` (two lists at once). `src/cdy` is 71 lines
   shorter. The translator's build: 0.97 s to 1.00 s (medians of seven, against step
   1's `bin`), likely a `fn` call per item costing more than the copies saved, these
   lists being short (a form's items, a deft's fields).
3. **The loops in `check.cdy`** ([[B178]]; 20).

   *Done (2026-11-11). As built:* 20 loops over a list, 14 of them one call now: 13
   `fold`s (the maps from the tops, `top-types`, `top-shapes`, `top-sums`, and from a
   sum's variants, `variant-types`, `variant-shapes`; the checker's state through a list,
   `infer-do`, `infer-holes`, `join-all`, `solve-each`, `report-pending`, `assoc-values`,
   `typed-binds`; a pattern's names into the env, `bind-fields`) and one `map-acc`,
   `check-order` (the names defined so far its state, each top's errors, then `concat`).
   `order-of` was a `fold` already and loses its `acc`. Six stay: `fresh-types` (a
   count), `find-field` (an early exit), `zip-map`, `typed-all` and `unify-all` (two
   lists, the last with an early exit), and `reach` (a work list that grows). `rigid-vars`,
   `uses` and `uses-all` have an `acc` but walk a type or an expression, not a list. Found:
   an empty literal as the start ([[B184]], a defect): `(Tup start empty-list)` and
   `empty-map` fail mypy, so `solve-each`'s `left` and `check-order`'s `start` stay
   parameters, their callers passing them empty. `src/cdy` is 2 lines longer (a `fold`'s
   `fn`, start and list each on a line). The translator's build: 0.98 s, unchanged
   (medians of seven, twice, against step 2's `bin`).
4. **The loops in `emit.cdy`** ([[B179]]; 27).

   *Done (2026-11-11). As built:* 29 loops, 25 of them one call now: 9 `map`s (the
   lists of Python texts, `emit-exprs`, `emit-types`, `emit-fields`, `emit-parts`,
   `emit-any-params`, `variant-refs`; `field-types`, `bind-locs`, `variant-list-names`),
   5 a `map` then `join` (the strings built line by line, `emit-stmts`, `emit-binds`,
   `emit-record-fields`, `emit-variants`, `emit-imports`), one `filter` (`used-tvars`),
   one `find` (`holder`, with `with-default`), and 9 `fold`s (`name-set`; the env,
   `global-names`, `add-globals`, `bind-locals`; the locals a body binds, `bound-locals`,
   `bound-in-cases`, `bound-in-lists`, and `type-vars`, each from a `start` its recursion
   seeds; `check-py-fields`, the Python names so far, its result dropped for `true`).
   `generic-variants` and `deft-field-types` were `fold`s already and lose their `acc`.
   Four stay: `mangle-chars` and `escape-chars` (a text), `emit-params` (two lists), and
   `emit-match` (each case's keyword differs from the first's, and the last may be an
   assert). `src/cdy` is 74 lines shorter. The translator's build: 0.94 s to 0.93 s
   (medians of seven, four times, against step 3's `bin`), unchanged within the noise.
5. **The loops in `expand.cdy`, `include.cdy`, `cdyc.cdy`, `read.cdy`** ([[B180]]; 31).

   *Done (2026-11-11). As built:* 32 loops in the four files, and the survey's one in
   `prelude_macros.cdy` (`put-parts`, in no step), 29 of them one call now: 11 `map`s
   (`expand-all`, `expand-defs`, `each-clause`, `stamp-all`, `macro-list`, `imp-list`,
   `exports-of`, `imported`; `arg-binds` and `expand-modules` over `(zip (range ...) xs)`
   for the index; `stems-of`, inlined as `(map path-stem ...)`, its `defn` gone), 4 a
   `map` then `concat` (`helper-forms`, `macro-program`, `analyse-modules`, `put-parts`),
   one `filter` (`pick-forms`) and two a `filter` then `map` (`module-imports`,
   `other-forms`: an import, or not), one `all` (`all-names`), one `find-index`
   (`cycle-text`, the stack from the key on), and 9 `fold`s (`macro-map`, `import-all`,
   `add-helpers`, `load-imports` and `include-forms` from a `start` a caller seeds;
   `mangled-names`, `exports-by-key`; `unique-names` and `unique-stems`, the names so far,
   their result dropped for `true`). Four stay, `read.cdy`'s: `line-starts`, `read-all`,
   `read-list` and `read-str` walk a text. `import-file`, `add-module` and `include-file`
   have an `acc` but aren't loops. `prelude_macros.cdy` is a library file, staged in `bin`
   (`boot/66` reads it: no staging). `src/cdy` is 51 lines shorter. The translator's
   build: 0.95 s to 0.94 s (medians of seven, twice, against step 4's `bin`).
6. **`to-list` gone** ([[B181]]; [[B174]]): the rest to `(List x)`, then the
   declaration out (two boot steps).

   *First boot step done (2026-11-11). As built:* the 108 `(to-list x)` calls left are
   `(List x)`, by script: 98 in the translator (`lower.cdy` 43, `core.cdy` 19, `emit.cdy`
   10, `check.cdy` and `expand.cdy` 7 each, `read.cdy` 5, `include.cdy` 4, and
   `prelude_macros.cdy` 2, a library file, staged in `bin`), 8 in the spec's examples
   (`25-checking.md`, `40-expressions.md`) and 2 in the test programs; `bin` no longer
   calls `to_list`. Found: `(List x)` is a fixed-length tuple to mypy, so a `match` whose
   first clause gives one fails `mypy --strict` once a later clause gives another length
   ([[B185]], a defect, which `to-list`'s `tuple[T, ...]` hid); `read-type` (`core.cdy`)
   has its whole-list clause first. The translator's build: 0.94 s, unchanged.
7. **`equatable`** ([[B182]]; [[B173]]).
8. **Docs** ([[B183]]): CLAUDE.md, the epic's third branch *done*, `library.md` (its Question 6's
   *for now* closed), `mutation_optimization.md` ([[B69]]'s state); "Looking back".

## Questions

1. **The found items:** which of `collections`' come along? [[B174]] (`to-list`) is
   mechanical and mostly about the same `(++ acc (to-list x))`s; [[B173]] (`equatable`)
   is a defect in what `collections` built (constraint variables, `=` as a value).
   [[B171]] (`List` as a value) gains little (its text), [[B176]] (host records) is
   `library`'s, [[B170]] (brackets) waits for the map literal. **Proposed: [[B174]] and
   [[B173]];** the rest stay. *Answer (2026-11-10, the owner): as proposed.*
2. **`reduce`:** add it, `(Fn ((Fn (a a) a) (List a)) (Maybe a))`, as the epic allowed,
   or not until something needs it? **Proposed: not now,** *for now*: nothing in the
   translator needs it, and a built-in no program uses is a spelling to keep for every
   target. *Answer (2026-11-10, the owner): as proposed.*
3. **The tasks:** reuse [[B167]], retitled "collections-2 step 1", with new tasks for
   steps 2 to 8; or close it as moved and open new ones? **Proposed: reuse, retitled,**
   as `semantics-2` did, its notes saying where it came from. *Answer (2026-11-10, the
   owner): as proposed;* steps 2 to 8 are [[B177]] to [[B183]].
4. **The loop steps:** by layer, as above (four steps, 20 to 45 loops each), or one step
   per file (eight), or one step for all? **Proposed: by layer,** each small enough to
   review, with the build's time measured at each. *Answer (2026-11-10, the owner): as
   proposed.*
