# Typed Core (HLD)

**Status: accepted (2026-10-31), with the proposed answers to its questions and its
spec changes; on branch `typed-core` (tasks [[B126]] to [[B130]]). Epic:
`python_complete.md` (its first branch). After tag `type-checker`.** The checker
(`check.cdy`) works out every expression's type, then throws the types away: `lower` and
`emit` see the Core `analyse` made, untyped, and a `fn` that becomes a nested Python
`def` is annotated `Any` ([[B19]]). This HLD keeps the types, writes them into Core, and
gives Core's leaves the positions they lack ([[B122]], [[B59]]), so that what comes next
in the epic (`show` and `format` by type, `Any` cut down, the translator's loops on
`map` and `fold`, [[B123]]; a backend for a statically typed target) has them.

## Where things stand

- **Core's `Expr`** (`core.cdy`) has fourteen node kinds: four leaves (`Lit`, wrapping
  its literal form; `Local`; `Global`; `Prim`), nine compound nodes, eight of them
  ending with a `pos` since `type-checker` and `Do` without one, and `Temp`, made only by
  `lower`.
  No node has a type.
- **The checker** infers a type for each node (`infer`, `check-expr`), threading a
  substitution (`St`), and returns only the errors: `type-check` gives back the `tops`
  it was given. Its types are `CType`s (`TCon`, `TVar`, `TFn`); a variable it makes is
  `?N`, one a `sig` writes is rigid in its definition.
- **The types that reach Python** are the `sig`s' (top-level `def`s and `defn`s) and the
  records' fields. A local bound by `let` becomes a plain assignment, which mypy infers;
  a `fn` that stays an expression becomes a Python `lambda`, which mypy types from its
  context; a `fn` whose body needs statements becomes a nested `def` (`SLocalFunc`), its
  parameters and result `Any` ([[B19]]), so mypy checks nothing inside it, and its
  callers lose the type.
- **Positions:** only `Sym` and `Lst` forms carry a `Pos` (`form.cdy`); a literal form
  doesn't ([[B59]]), and Core's leaves don't, so an error in a leaf is reported at its
  parent ([[B122]]: `(def x\n  "a")` says `2:1`, not `3:3`). The forms are part of the
  macro API: macro code builds them (`(Txt (sym-name s))`, [[macros.macro-code]]), and
  an error in a macro's expansion is reported at the call ([[macros.errors-at-call]]). A `Top` for `main` has no
  position for its type's error, forms read from a `format` hole have none, and `lower`'s
  and `emit`'s internal errors say none ([[B14]]).
- **Pattern sites:** a `match` on `Expr` names every field, so a new field touches every
  clause that takes that node apart: about 70 in `core.cdy`, 40 in `check.cdy`, 55 in
  `lower.cdy` and 20 in `emit.cdy` (counted 2026-10-30), most of them binding the new
  field as `_`.

## Goals

- **Every `Expr` has its type after checking,** for `lower`, `emit` and any later
  backend to read: the type the checker inferred, with the final substitution put in.
- **Nested `fn`s typed** ([[B19]]): a nested `def`'s parameters and result get their
  types, so mypy checks its body and its callers.
- **Every `Expr` has its position,** leaves too, and literal forms carry one, so an error
  is reported where it is ([[B122]], [[B59]]); and the positions [[B14]] lacks.
- **The defect [[B119]]:** a variant or a value written as a type says what it is.

## Not goals

- **Let-polymorphism, field constraints ([[B120]]) and narrowing in a clause ([[B121]]):**
  checker features, each with its item; none is needed here (Question 3). The two
  items go to `semantics`, with `Maybe`'s narrowing ([[B20]]); let-polymorphism after
  the epic.
- **New rules:** this branch changes what Core carries, not what type-checks. Every
  program that translates today translates the same, and its Python changes only in the
  nested `def`s' annotations.
- **Using the types** for `show`, `format`, `=` or `Any` (`semantics`, `collections`).

## Proposal

### Types in Core

Each `Expr` node gets a type, `t`, its last field (Question 1). `analyse` builds Core with
a placeholder, `ANY` (or a fresh `?N`, if that is simpler), and the checker
**elaborates**: `infer` and `check-expr` return the node rebuilt with its type, besides
the type and the state, and once a definition is checked, a pass puts the final
substitution into every type in it (`zonk`, in the literature). `type-check` returns the
typed `tops`, which `python-of` already takes.

- **What a type can still hold:** a rigid variable (`a`, inside a generic definition),
  which is a real type; and a `?N` the definition never fixed (a `fn` never called, an
  `empty-list` never added to). A `?N` stays in Core as a `TVar` (Question 2); each
  backend decides: Python writes it `Any`.
- **`Any` stays `Any`** (gradual, [[B18]]).
- **`Temp`**, made by `lower` after the checker, gets `ANY`; `lower` reads the types, it
  doesn't need to make new ones.

### Nested functions

`SLocalFunc` gets the `Lambda`'s type (`TFn` of its parameters' types and its result);
`emit` writes them as annotations, as it does `SFunc`'s, a `?N` as `Any`. Inside a
generic definition the rigid variables are in scope in Python too (PEP 695's `def
f[a]`), so a nested `def` can name them. mypy then checks the nested `def`s' bodies,
which may find what `Any` hid; what it finds is fixed in the translator or recorded.

### Positions

- **Literal forms** get a `pos` (`Txt`, `IntLit`, ... in `form.cdy`), last, as `Sym`
  and `Lst` have; the reader gives them theirs. Macro code that builds one writes the
  position, `(Txt "x" NOWHERE)`, as it does for a `Sym`, and an error in it is still
  reported at the call (Question 4).
- **Core's leaves** get a `pos` too: `Local`, `Global` and `Prim` their `Sym`'s, `Lit`
  its form's (read from the form; no field of its own); `Do` gets one, the `(do ...)`
  form's. Every node then has one, before its type (Question 1).
- **The checker** reports at the node: the "leaf is reported at its parent" rule
  goes ([[B122]]).
- **[[B14]]'s rest:** `main`'s `Top` gets a position; forms read from a `format` hole
  get positions offset from the string's (the hole's line and column, plus its place in
  the text); `lower`'s and `emit`'s internal errors, which a program shouldn't be able
  to reach, keep none, *lasting*, and say so ("internal error").

### The defect

[[B119]]: `check-type` asks, before the import check, whether the name is a variant
(`A is a variant of S, not a type`) or a value of this module (`X is a value, not a
type`). Its repro becomes a `checking` example.

### The spec

No rule changes what type-checks. `spec/25-checking.md` gains a sentence on where an
error is reported (at the expression, `file:line:col`), with an example whose position
is a leaf's; [[B119]]'s message is an example in `types.exist` (`spec/20-types.md`). The
error tables give messages without positions, so they don't change. One rule changes
for macro writers, [[macros.macro-code]]: a literal form has a position, so its
example becomes `(Txt (sym-name s) NOWHERE)`.

## Pros and cons

- **For:** everything after it in the epic reads types (`show` per type, `format` as a
  macro, the translator's `fn`s typed so its loops can become `map` and `fold`), and a
  second target needs them; the positions are the same churn, done once; nested `def`s
  get checked; it changes no program's meaning.
- **Against:** the churn: about 185 pattern sites, and the checker rewritten to return
  what it checks (its 850 lines, most of them touched); a bigger Core in memory; mypy
  may find errors the `Any`s hid, which cost time now.
- **Timing:** first in the epic (Question 2 of `python_complete.md`), and best now,
  while `check.cdy` is fresh and before more code takes Core apart.

## Bootstrap

Each step changes `src/cdy/`, so `bin` is rebuilt and the step gets its `boot/NN`. The
form change (step 1) also changes the forms macros see: `form.cdy` is copied next to the
translator ([[B64]]), and macro code that builds or takes apart a literal (`(Txt v)`)
needs the new field: `expand.cdy`, the macro test program
(`tst/cdy/cdyc/macro_code/quoting.cdy`) and the spec's example change in the same step.

## Steps

1. **Positions on literal forms and Core's leaves** ([[B59]], [[B122]]): `form.cdy`,
   the reader, `Lit`/`Local`/`Global`/`Prim`/`Do` with positions, the checker reporting
   at the node; the macro code that takes literal forms apart; the spec's position
   example.

   *Done.* As built:
   - **`form.cdy`, `read.cdy`:** every literal form ends with a `pos`, the reader's (a
     string's at its opening `"`); `form-pos` gives every form's.
   - **`core.cdy`:** `Local`, `Global`, `Prim` and `Do` end with a `pos`; `Lit` reads its
     form's. A `Local` is bound with its name's position and, where it is used, rebuilt
     with the use's (`at-use`). What the translator makes (`NIL`, a quoted form's
     builders, `format`'s joins) is `NOWHERE`; a `tup` pattern's `at` reads are at the
     pattern.
   - **`check.cdy`:** `node-pos` gives the leaves' positions, so an error is reported at
     the literal or name it is in: `(f\n  s)` says `2:3: argument 1 of f: ...`.
   - **`expand.cdy`:** `stamp` gives an expansion's literals the call's position too
     (`form-at`), as it did its symbols and lists.
   - **`lower.cdy`:** a self tail call's unchanged parameters are found by name and id
     (`same-local`), not by comparing whole `Local`s, which now differ in position;
     without it a loop rebound them all.
   - **Macro code:** `expand.cdy` and `include.cdy` build literals with a position;
     `macros.macro-code`'s example writes `(Txt (sym-name s) NOWHERE)`, and the macro
     test programs (`lib/control.cdy`, `macro_code/quoting.cdy`) take the new field.
   - **Output:** the old `bin` and the new one write the same Python for every test
     program but `macro_files.cdy`, whose macro file now builds the new forms (so the
     old `bin` can't translate it).
   - **Tests:** a `checking.definitions` example with the error at a string literal;
     `test_reader_positions` checks literals' positions. [[B59]] and [[B122]] done.
   - **Bootstrap:** one rebuild.
2. **Types in Core:** a `t` on every `Expr`; the checker elaborates and puts in the
   final substitution; `type-check` returns the typed `tops`; a test that every node of
   the translator's own Core has a type after checking.

   *Done.* As built:
   - **`core.cdy`:** every `Expr` variant ends with `t`, a `CType`; `analyse` makes `ANY`
     (moved here from `check.cdy`). The field was added by a throwaway script that reads
     the `.cdy` files as forms: `_` in each `match` pattern, `ANY` in each construction
     (about 180 sites).
   - **`check.cdy`, not rewritten but extended:** rather than have every `infer` rebuild
     its node, each definition is first numbered (`retype-top`: each node's `t` becomes a
     name of its own, `?eK`); the checker records the type it finds under that name
     (`typed`), in a map of its own in `St` (`types`, not the substitution, which stays
     small: `map-set` copies); then each node gets its recorded type with the
     definition's substitution put in (`node-type`). Recorded: every `infer` (now
     `infer` around `infer-node`); `check-expr`'s check-mode `if`, `do`, applied `fn` and
     `fn` (the type wanted); every binder (`fn` and `defn` parameters, a `let`'s, a
     clause's names); a callee the checker doesn't infer (an operator, a `tup`
     pattern's `at`, a `let`'s `fn`) as the function from its arguments' types to the
     result's. `type-check` returns the typed `tops`.
   - **`lower.cdy`:** a node it rebuilds keeps its type (`value-call`, `value-if`,
     `value-fn` and `value-boolop` take it), and so does the `Temp` that stands for a
     `match` or a nested `fn`; other `Temp`s, and the `not` it makes, are `ANY`.
   - **Output:** the same Python, byte for byte, as `boot/44` for every test program.
   - **Tests:** `test_every_node_is_typed` checks the translator's own Core (23,280
     nodes): none keeps its `?eK` name, so the checker reached every node, and every
     `fn` has a function type; three are a `?N` nothing solved, as Question 2 allows.
     Breaking the callees' recording makes it fail.
   - **Cost:** `self_host.py` takes 3.6 s, from 3.0 s.
   - **Bootstrap:** one rebuild.
3. **Nested functions typed** ([[B19]]): `SLocalFunc` with its type; `emit`'s
   annotations; what mypy then finds, fixed or recorded.

   *Done.* As built:
   - **`lower.cdy`:** `SLocalFunc` ends with `t`, its `fn`'s type.
   - **`emit.cdy`:** a nested `def` is annotated from its `TFn` (`emit-params`, as a
     `defn`'s), inside a generic `defn` with its type variables, which PEP 695 puts in
     scope; a `fn` the checker didn't see (macro code, [[B42]]) keeps `Any`. `emit-type`
     writes a `?N` as `Any` (Question 2). Also, beyond the step as written: a `let`-bound
     `fn` that stays a Python `lambda` (B19's own repro, "Call to untyped function") gets
     its type on the assignment, `sq: Callable[[int], int] = (lambda x: ...)`; locals
     are renamed apart within a function, so no name is annotated twice.
   - **What mypy found:** nothing; the translator itself has no nested `def` or bound
     `lambda`, so `bin` changes only in `emit`'s own code. Its spec example,
     [[checking.locals]], now has a bound `fn` called.
   - **Bootstrap:** one rebuild.
4. **The messages:** [[B119]]; [[B14]]'s rest (`main`'s position, `format` holes'
   positions, `lower`'s and `emit`'s errors as internal ones).
5. **Docs:** CLAUDE.md ("How the translator works": typed Core), the iMVP doc's
   layers, `multi_target.md` (a backend reads Core's types), `type_checker.md` and
   `python_complete.md`'s triage; [[B15]] as Question 5 decides.

## Questions (answered: the proposals, 2026-10-31)

1. **How Core carries types and positions:** a field on every node (proposed: `pos`
   then `t`, last, on all fourteen); a side table, from each `Local`'s key to its type
   (enough for [[B19]], not for a `format` hole's type or a backend's); or types only
   where a backend is known to need them (a `Lambda`'s, a hole's), added as needs come.
   The side table is the least churn; the field is the only one that gives "every `Expr`
   its type" and needs no change per new use. **Proposed: a field on every node,**
   *lasting*.
   *Answered:* the proposal.
2. **A `?N` left unsolved:** kept as a `TVar` in Core, each backend choosing (Python:
   `Any`); replaced by `Any` in Core; or an error ("can't tell the type of ..."), as
   Rust's `type annotations needed`. An error would reject programs that translate
   today (an unused `fn`, `(put empty-list)`). **Proposed: kept as a `TVar`, Python
   writing `Any`,** *for now*; whether a target needs an error is the porting surface's.
   *Answered:* the proposal.
3. **Which of the checker's leaks:** [[B122]] (it comes with the positions), and also
   [[B120]] (field constraints) and [[B121]] (narrowing in a clause)? Neither has fired
   on the translator or the tests, and [[B121]] needs variants as types inside the
   checker. **Proposed: [[B122]] only;** [[B120]] and [[B121]] stay open, `low`.
   *Answered:* the proposal; the two go to `semantics`, with `Maybe`'s narrowing
   ([[B20]]), since the epic's exit test leaves no T item open.
4. **Literal forms' positions, and the macro API:** a `pos` field on each literal form
   (macro code writes `(Txt "x" NOWHERE)`); or the literal forms left as they are, so
   only symbols' leaves get positions (`Local`, `Global`, `Prim`) and an error in a
   literal stays at its parent ([[B59]] kept, *lasting*); or a helper per literal
   (`txt`, giving `NOWHERE`) besides the field, so macro code doesn't spell positions.
   Macro code mostly quotes (`quasi`), which builds the forms itself, so few macros build
   a literal by hand. **Proposed: the field,** as `Sym` and `Lst` have, no helpers.
   *Answered:* the proposal.
5. **[[B15]]:** it is the checker's MVP item, with five parts left: mypy (the epic's
   Question 3, `porting-surface`), let-polymorphism, field constraints ([[B120]]),
   narrowing ([[B121]]) and one error at a time. Close it with this branch, the parts
   without an item getting one (let-polymorphism an `idea`; one error at a time a
   `leak`, `low`), or keep it open as their parent? **Proposed: close it here,** with
   the two new items, so the backlog's `high` items are what is really left.
   *Answered:* the proposal.
6. **Steps 1 and 2 together or apart:** the same pattern sites change twice. Apart is
   two reviewable commits, each with its own bootstrap; together is one pass. **Proposed:
   apart,** positions first (they are smaller and need no checker rewrite).
   *Answered:* the proposal.
