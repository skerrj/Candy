# Type checker (HLD)

**Status: accepted (2026-10-28), with the proposed answers to its questions and its spec
changes (`spec/25-checking.md`), on branch `type-checker`, after tag `field-checks`.**
[[B15]], the backlog's largest `high` item: Candy has no type checker of its own; mypy
checks the Python. This HLD proposes the first one, an MVP that leaves mypy in place, and
lists what it leaves for later.

## Where things stand

- **What the translator checks** about types: each type it reads exists, with its number
  of arguments (`check-type`, since `name-checks`); a `defn`'s `sig` is a function type
  with one parameter per argument; a built-in's and a variant constructor's number of
  arguments. Nothing else.
- **What mypy checks:** everything else, on the Python. `sig`s become annotations, and
  `test_spec.py` and `test_self_host.py` run `mypy --strict` on every translation. A
  program translated and run with `main.py --run` isn't checked at all.
- **What nobody checks** (the items [[B15]] is the root of): what Python's types can't
  tell apart (`Char` and `String` are both `str`, `Int` and `Bool` mix: [[B25]]'s
  truthy tests); what passes through `Any` ([[B18]]: `put`, `at`, `len`, nested `fn`s,
  [[B19]]); a field `get` names, before mypy ([[B30]]); a record constructor's arguments
  ([[B10]]); a macro's result ([[B42]]).
- **Core has no positions.** `analyse` knows where each form is (`scope here`), but the
  `Expr`s it builds don't carry it, so a pass over Core can't say where an error is.
- **Types in Core:** `CType` is `TCon` (a named type with arguments, `Tup` and the
  built-ins among them), `TVar` (a lowercase type variable) and `TFn`. Each top-level
  `def`/`defn` has its type (`TDef`'s `t`); built-ins have theirs (`Typed` in the builtins);
  a `deft`'s fields have theirs.

## Goals

- A type error in a program is the translator's error, with a position, before any Python
  is written.
- The checker accepts every program that is correct by Candy's types, including the
  translator itself, and the spec's and tests' programs.
- Every `if` test is a `Bool` ([[B25]]), every call's arguments match its function's
  parameters, a record constructor gets its fields ([[B10]]), and `get` and `assoc` name
  a field of the record ([[B30]]).
- mypy stays, as a second check, until a later branch decides otherwise.

**Not goals** (later branches, or items of their own): a real `Maybe` and narrowing
([[B20]], [[B51]]); typing what is `Any` today ([[B18]], [[B48]], [[B99]]: the variadic
built-ins, `at`, `len`); emitting the inferred types for nested `fn`s ([[B19]]),
though the checker would know them; overloading or type classes (the operators stay
special); type-checking macro code ([[B42]]); dropping mypy.

## Proposal

### The checker

A new module, `check.cdy`, run on each module's Core after `analyse` and before `lower`.
It is Hindley-Milner's unification, cut down to what Candy needs, since every top-level
name has a `sig`:

- **Top-level names** have their `sig`s; a generic one (`(Fn (a) a)`) is instantiated
  with fresh type variables at each use. Built-ins are the same, from `system.cdy`.
- **Checking a definition:** a `defn`'s parameters get its `sig`'s parameter types and
  its body is checked against the return type; the `sig`'s type variables are *rigid*
  in its own body (a body that needs `a` to be `Int` is an error).
- **Locals** (`let` bindings, `fn` parameters, pattern names) get fresh type variables,
  solved by unification. They aren't generalised (no let-polymorphism): a local `fn`
  used at two types is an error (*for now*; ML has it, and few programs need it).
- **`Any`** unifies with every type and stays `Any` (it is the gradual type, as in
  mypy): nothing that passes through it is checked ([[B18]]).
- **Substitutions** are a map threaded through the pass (Candy has no mutation), from a
  type variable's id to its type.

### The rules beyond functions and calls

- **Literals** have their types; `nil` is `Unit`, and also any `(Maybe a)` (the one
  place a value has two types, *for now*: [[B20]], [[B21]]); a value of type `t` is
  accepted where `(Maybe t)` is expected, as mypy accepts it.
- **`if`:** the test is `Bool`; both branches have one type, the `if`'s; with no else,
  an `if` whose `then` is a `t` is a `(Maybe t)`, or `Unit` if the `then` is (*for now*,
  as `nil` is: [[B21]]).
- **Operators** (`special.cdy`; no type classes): `+` takes arguments of one type, a
  number type or `String`; `-`, `*` and `quot` one number type; `/` numbers, giving
  `Double`; the comparisons any one type, giving `Bool`; `and`, `or`, `not` take `Bool`s.
  The number types don't mix (`(+ 1 1.0)` is an error), unless the survey finds the
  translator or the tests rely on it.
- **`deft`:** a record's or variant's constructor is a function from its fields' types,
  its type variables instantiated; `get` needs its object's type known (a record, or a
  variant inside the `match` clause that binds it) and gives the field's type; `assoc`
  likewise, each value of its field's type.
- **What is known when:** a call's arguments that aren't `fn`s are checked first, then
  its `fn`s, so in `(map (fn (p) (get p name)) people)` the `fn`'s `p` is already a
  person. A `get` or `assoc` on a value whose type still isn't known is an error, `get:
  the type of p isn't known here (name)` (*for now*: [[B15]]; a local's type can't be
  written, so the program has to make it known).
- **`match`:** the subject is the sum, each clause's names get their fields' types, all
  clauses have one type; a `tup` pattern takes a `(Tup ...)` of its arity ([[B17]]).
- **`format`** is a `String`, each hole any type; **`tup`** is a `(Tup ...)` of its
  items; **`do`** is its last form's type.

### Positions

The errors need positions, so Core gets them where checking can fail: `Call`, `If`,
`Lambda`, `Field`, `Assoc`, `MatchE`, `Tuple` and `Fmt` gain a `pos`, from `analyse`'s
`scope here` (*lasting*; `emit`'s errors could use them later, [[B14]]). A leaf (a
local, a global, a literal) is reported at its parent. That touches every pattern on
those variants in `lower.cdy` and `emit.cdy` (about 80), mechanically.

### Errors

One shape, at the position: `expected Int, got String`, with what was being checked
when it helps (`argument 2 of f: expected Int, got String`; `if: the test is Int, not
Bool`). A type variable is shown as the program wrote it, or as `t1`, `t2` for one the
checker made.

### The spec

A new file, `spec/25-checking.md` ("Type checking"), `status: draft`, written with this
HLD: the checker's rules in one place, one id each, with their examples. Its `candy run`
examples pass already (they are correct programs); its error rows fail until step 3, as
a draft's may. Its messages are sketches, settled when the checker is built.

| Id | Rule |
|---|---|
| `checking.calls` | arguments have the parameter types; the call, the return type |
| `checking.definitions` | a `def`'s value and a `defn`'s body have the `sig`'s types |
| `checking.generics` | a generic `sig` is instantiated at each use, fixed in its own body |
| `checking.locals` | locals are inferred, one type each (*for now*) |
| `checking.if` | the test is a `Bool` ([[B25]]); one type for both branches; no else gives `(Maybe t)` |
| `checking.operators` | the operators' fixed rules; number types don't mix |
| `checking.records` | constructors ([[B10]]), `get` and `assoc` ([[B30]]) |
| `checking.order` | `fn` arguments last; a `get` on an unknown type is an error |
| `checking.match` | the subject's sum, the clauses' one type, a `tup` pattern's arity ([[B17]]) |
| `checking.maybe` | `t` as `(Maybe t)`, `nil` as `Unit` or a `Maybe`, no narrowing ([[B20]]) |
| `checking.any` | `Any` matches everything, unchecked ([[B18]]) |

The other files change in step 3, when the checker is on: `[[types.checking]]` becomes a
pointer to the new file (mypy as a second check), and `[[types.records]]` loses its
paragraph on [[B10]] and [[B30]]; `[[expr.conditionals]]`, `[[expr.arithmetic]]` and
`[[expr.unit]]` point at their checking rules; `[[match.tup]]` loses its "only mypy
checks the arity" ([[B17]]); `50-macros.md` says macro code isn't type-checked (*for
now*: [[B42]]). The docs step marks `25-checking.md` `stable`.

Writing it found one thing: a `fn` bound by `let` and called fails `mypy --strict` (a
Python lambda, "Call to untyped function"), so the spec can't show one until [[B19]].

## Pros and cons

- **Pro:** errors are Candy's, with positions, in Candy's terms; types Python can't tell
  apart are told apart; a program is checked without running mypy.
- **Pro:** positions in Core are groundwork for [[B14]], and the inferred local types for
  [[B19]].
- **Con:** the largest branch yet: a new module (500 lines, by the size of `core.cdy`'s
  parts), a change to Core that touches `lower` and `emit`, and the translator itself
  must pass, so step 1 may find code to change.
- **Con:** two checkers, Candy's and mypy, until mypy goes; they may disagree (Candy's is
  stricter on `Bool` and `Char`, mypy on generic narrowing).
- **Why now:** it is `high`, the root of seven items; every other type item waits on it.
  **Why wait:** it is large; [[B36]] (printing values) is the other `high` item, and
  smaller.

## Bootstrap

No new declaration forms, so no staging: each step that changes `src/cdy/` is one
rebuild. The checker checks the translator from the step that turns it on, so that step
first fixes whatever in the translator it rejects.

## Steps

1. **A survey:** the checker, written to report rather than fail, run over the
   translator, the test programs and the spec; what it rejects is sorted into the
   checker's bugs, rules to change here, and real type errors (fixed, or recorded as
   items). Nothing changes for a user yet.

   *Done.* As built:
   - **`check.cdy`** (about 800 lines): unification over Core's `CType`, a variable the
     checker makes named `?N` (shown `t1`), a `sig`'s own variables rigid; the
     substitution, the next N and the messages threaded as `St`. It checks against the
     expected type where there is one (`check-expr`: an `if`'s branches, a `do`'s last
     form, a `let`'s body, a `fn` against a function type), and infers otherwise. For now
     it returns its messages (`check-program`), without positions: each names the
     definition (`defn f: ...`).
   - **The survey:** `type-survey` in `cdyc.cdy` checks a file's program
     (`program-tops`, split out of `translate-modules`, which doesn't call the checker
     yet). Run over the translator (all 4,000 lines), the test programs and every spec
     example. Two tests keep its result: `test_the_translator_type_checks`, and
     `test_programs_type_check` with the two known messages below.
   - **What it found, the translator:** one real error, which mypy can't see: `emit-lit`
     passed a `CharLit`'s `Char` to `py-str`, a `String` function (fixed:
     `(py-str (format "{v}"))`).
   - **Rules changed:** `+` joins lists too (the translator does it everywhere; the
     stable spec says only strings, so `[[expr.arithmetic]]` gets it in step 3); a `(Tup
     t ...)` of one type is accepted as a `(List t)` (*for now*, [[B29]]: there is no
     list literal, and the translator writes lists with `tup`). Both are in
     `spec/25-checking.md` (`checking.operators`, the new `checking.tup-lists`).
   - **Rules confirmed:** checking `fn` arguments last is enough: "the type of p isn't
     known here" never fires on the translator or the tests (Question 4). No program
     mixes number types.
   - **To settle in step 3:** a test program's `(or false nil)` (`tst/cdy/t1/basics.cdy`,
     truthiness: [[B25]]); `get` on a variant's value (Question 8); the messages' wording
     (16 of the 31 error rows of `25-checking.md` differ only in it: `if: the test:
     expected Bool, got Int` for `if: the test is Int, not Bool`, `+ are Int and
     String` for `+: expected Int, got String`).
   - **Tried and dropped:** a variant's constructor giving the variant, a type of its
     own accepted as its sum (as mypy has it). Inside other types it needs variance:
     `(List SAssign)` where `(List Stmt)` is expected, `(Tup Lst Int)` for `(Tup Form
     Int)`, 60 places in the translator.
   - **Bootstrap:** one rebuild (`emit-lit`; the checker is in `bin`, unused).
2. **Positions in Core:** the `pos` fields, set by `analyse`, matched through `lower` and
   `emit`; no output changes.
3. **The checker on:** its errors fail translation, with positions; the spec's
   `[[types.checking]]` and its rows; [[B25]], [[B10]] and [[B30]] closed (or narrowed),
   and [[B15]] narrowed to what is left.
4. **Docs:** CLAUDE.md, the iMVP doc, `multi_target.md` (the checker is the front end's,
   not the target's).

## Questions (answered: the proposals, 2026-10-28)

1. **Inference or checking only?** Required `sig`s make a checker without inference
   possible for top-level code, but `let` and `fn` locals have no types written, so
   their types have to be inferred somehow. **Proposed: unification (HM without
   let-polymorphism)**, the standard answer, and the one that gives [[B19]] its types
   later.
   *Answered:* unification, no let-polymorphism (*for now*).
2. **`Any`: gradual (accepts everything) or an error?** **Proposed: gradual** (*for
   now*, [[B18]]): the built-ins depend on it, and so does the translator.
   *Answered:* gradual, *for now*.
3. **`Maybe`: a value of type `t` accepted as `(Maybe t)`, and `nil` as `Unit` and any
   `Maybe`?** That is mypy's rules without its narrowing; the alternatives are those
   rules with narrowing after `(= m nil)` (flow-sensitive types), or the real sum
   ([[B20]]), which changes programs. **Proposed: mypy's rules, no narrowing, for now**
   ([[B20]]). The translator doesn't use `Maybe`.
   *Answered:* the proposal.
4. **`get` on a value whose type isn't known yet** (a `fn`'s parameter, read before the
   argument that fixes it): an error; deferred, as a constraint solved later; the
   arguments that aren't `fn`s checked first; or the field looked up by name (OCaml's
   rule; the translator reuses field names). A local's type can't be written, so an
   error can't ask for a `sig`. **Proposed: `fn` arguments last, and an error for what
   is still unknown, for now**; step 1 counts how often the error fires, and deferring
   is the next answer if it is often.
   *Answered:* the proposal ("What is known when").
5. **Positions: in Core, a wrapper node, or check during `analyse`?** A `pos` field on
   the compound nodes changes about 80 patterns, but the translator finds every one (a
   variant pattern lists every field); a wrapper (`At`) leaves `lower` and `emit` alone,
   but a missed one silently takes an `else`; checking while analysing mixes two jobs
   into the translator's largest module. **Proposed: positions in Core** (*lasting*).
   *Answered:* the proposal.
6. **mypy: keep it?** As now, in the tests; or only on `bin` and the test programs; or
   drop it. It still checks what Candy's checker can't: the Python `emit` writes, and
   the checker's own gaps. **Proposed: keep it as now**, until a branch of its own
   decides.
   *Answered:* the proposal.
7. **One branch or two?** Positions could be a branch of their own first, or the survey
   too. **Proposed: one branch**, with the survey first, so the checker's design meets
   the translator's code before anything else is built on it.
   *Answered:* the proposal.

### From the survey (answered: the proposal, 2026-10-29)

8. **`get` on a variant's value.** A constructor gives the sum, so `(get (Rect 4 5) h)`
   is `get` on a `Shape`, and not every variant has an `h`: rejected, though
   `30-match.md` shows it ("A variant's fields are named, as a record's are, so `get`
   reads one") and `tst/cdy/sums.cdy` does it. The options:
   - **A.** `get` on a sum needs a field every variant has, with one type; the example
     and the test change to read a field inside `match` (*lasting*: a sum's value is one
     of its variants, unknown until matched).
   - **B.** A variant is its own type, accepted as its sum, as in mypy: needs variance
     inside lists and tuples (the survey's 60 places), a larger checker.
   - **C.** A for now, B later with real subtyping (a backlog item).
   **Proposed: A** (*lasting*); `match` is how a sum is taken apart.
   *Answered:* A (*lasting*); the example and the test change in step 3, when the
   checker is on.
