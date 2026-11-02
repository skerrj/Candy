# Semantics (HLD)

**Status: proposal (2026-11-01), questions open. Epic: `python_complete.md` (its second
branch). After tag `typed-core`.** Where Candy's behaviour is Python's, borrowed rather
than decided, this branch decides it, in the spec, and makes the Python target do what
the spec says: how values print ([[B36]], the backlog's last `high`), `=`, `/`, `and`
and `or`, `Maybe` and missing values, `at` and `slice`, the numbers' sizes, `Char`, a
`def`'s order and constancy, and errors. Most of it needs the types `typed-core` keeps
in Core: a value is shown, or compared, by its static type.

## Where things stand

The group S items the epic gives this branch (`python_complete.md`, "The triage"), with
the checker items that come with them. Counts are from typed Core (2026-11-01): the
translator's own, and its 27 test programs (`tst/cdy/`, without `lib/` and macro files).

| Item | Today | Seen where |
|---|---|---|
| [[B36]] values print as Python's | `put` is `print`, a `format` hole `str()`: `True`, `None`, `(1, 2)`, `V(x=1)` | the spec prints only numbers and text (`spec/README.md`); the test programs `put` 2 `Bool`s, 3 lists and tuples |
| [[B27]] `=` is `==` | structural, and the checker makes both sides one type; but two variants of one sum with the same fields are equal (`(= (A 1) (B 1))` is true: [[B137]], found writing this) | translator: `=` on `Int` 281, `String` 130, `Any` 49, a record or sum 2 |
| [[B23]] `/` is true division | `(/ 7 2)` is `3.5`; `quot` floors | translator 0, tests 5 |
| [[B26]] `and`/`or` return an operand | the checker now makes every operand a `Bool`, so only `Any` can see it ([[B18]]) | translator 106 |
| [[B20]] `Maybe` is `a \| None` | the checker accepts a `t` as a `(Maybe t)` and `nil` as any `Maybe`; `(Maybe (Maybe t))` collapses | translator: 6 mentions, all `system.cdy`'s (`find`, `index-of`, `with-default`); no node is a `Maybe` |
| [[B21]] missing values are `None` | an `if` with no `else` is a `(Maybe t)`; `cond` with no match, `None` | translator 0, tests 2 |
| [[B121]] no narrowing in a clause | the subject is still the sum inside a clause | rare: the clause's names read the fields |
| [[B120]] `get` before a type is known | an error, not a constraint | never fired (`type-checker`'s survey) |
| [[B35]], [[B71]] `at` and `slice` are subscripts | negative indexes count from the end, an out-of-range slice is cut short | translator: `at` 681 (4 negative), `slice` 36 |
| [[B22]] unbounded integers | `Int`, `Long`, `Byte` are Python `int`s; `300b` is accepted | — |
| [[B28]] a `Char` is a `str` | the checker keeps `Char` and `String` apart; `at` is `Any`, so the hole is `Any`'s | — |
| [[B31]] a value used before its `def` | Python's `NameError` at run time | — |
| [[B80]] `def`: constant or variable | undefined: no form changes one | — |
| [[B39]] `fail` stands in for errors | raises `CandyFail`; nothing catches it in Candy | translator 127 |
| [[B132]] the unsolved types | eight in the translator, all `Any` meeting a variable; no test | — |

The epic's answers that bind this branch: `=` and `show` are declared for every type,
`=` on function types an error (Question 12); `Maybe` decided here, leaning to a real
sum, `(deft (Maybe a) (Some ((v a))) (None))` in the prelude, `nil` only `Unit` (Question
7); the spec's runner, later in the epic, needs errors as values (Question 8).

## Goals

- **Every value prints as Candy shows it,** by its type: `true`, `nil`, `(1 2 3)`,
  `(V 1 "a")`; the spec's examples print anything ([[B36]]).
- **Each borrowed meaning decided**, in the spec, *lasting* or *for now* with its item,
  and the Python target doing it: the items in the table above.
- **`Maybe` a real sum,** missing values gone: an `if` without `else` only for effects.
- **The checker's three leaks closed:** narrowing in a clause ([[B121]]), field
  constraints ([[B120]]), the unsolved types covered by tests ([[B132]]).

## Not goals

- **Types for the untyped built-ins** (`put`, `at`, `len`, `tup`), the operators as
  values, `and`/`or` as macros ([[B100]]): `collections`, with typed rest parameters
  and the constraint variables (B124's goal of no operators in the language).
- **Cutting `Any` down** ([[B18]]): `collections`.
- **Mutation** (`doc/hl_rqmt/mutation_optimization.md`): a `def` is decided constant
  here, nothing more.
- **Converting the translator's `fail`s** to values: Question 11.

## Proposal

### Showing values

A built-in `show`, typed `(Fn (a) String)`, gives a value in Candy's syntax, as a reader
would read it back where Candy has a literal (Question 2):

| Type | Shown | |
|---|---|---|
| `Bool`, `Unit` | `true`, `nil` | |
| numbers | `42`, `1500l`, `1b`, `3.14f`, `10.0` | as written |
| `Char`, `String` | `\a`, `"text"` (escaped) | |
| `(List t)` | `(1 2 3)` | |
| `(Tup ...)` | `(tup 1 "a")` | |
| a record or variant | `(V 1 "a")`, `(None)` | its constructor |
| `(Map k v)` | `{"a" 1, "b" 2}` | *for now*, until `collections` decides a map literal |
| a function | an error at translation | Question 12 of the epic: every value shown is data |

`put` and a `format` hole show their values, except a `String` or `Char`, written as its
text: `(put "a" 1 true)` prints `a 1 true`.

**How:** the translator knows each node's type (typed Core), so `emit` chooses the
printer: a `String` hole stays a plain f-string hole; any other type calls a show for it,
built from the type (a record's show calls its fields'). A **type variable** (in a
generic function) has no type to choose by (Question 3): proposed, a show that inspects
the Python value at run time, which is exact except that it can't tell a `Char` from a
`String` or a `Byte` from an `Int` (*for now*, a new item), with the hidden-parameter
way (each generic function given its type variables' shows) left for when interfaces
come.

### Equality

`=` and `!=` are structural, on two values of one type (as the checker already
requires): two lists with equal items, two records of one type with equal fields, two
variants only if they are the same variant ([[B137]]). Python: each record and variant
class gets `__eq__`, `__ne__` and `__hash__` comparing the class too (methods in the
class body, no decorators). On a function type `=` is an error (the epic's Question 12).
A type variable's `=` is Python's `==` with the classes' `__eq__`, so it is exact.
`Float` and `Double` compare as IEEE does (`nan` isn't equal to itself), *lasting*.

### Numbers

- **`/`** (Question 4): proposed, `/` on `Float` and `Double` only, giving the same type;
  `quot` (floor, *lasting*: [[B24]]) and a new `rem` for the integers. `(/ 7 2)` becomes
  an error, `(quot 7 2)` or `(/ 7.0 2.0)`.
- **Sizes** (Question 5): proposed, `Byte` 8 bits unsigned, `Int` 32 and `Long` 64
  signed, `Float` 32 and `Double` 64, *lasting*, as Java and Kotlin have them (Candy's
  `Int` and `Long` already say there are two). A literal out of its range is an error at
  translation (`300b`). Overflow in arithmetic is unchecked on Python, which has no
  sizes, *for now* (a new item): each target's choice, wrap or trap, is the porting
  surface's.

### `and`, `or`, `Char`, `def`

- **[[B26]]** closes: the checker makes every operand of `and` and `or` a `Bool`, so the
  result is a `Bool`; what `Any` lets through is [[B18]]'s. They stay operators here;
  as macros, [[B100]] moves to `collections` with B124's goal.
- **[[B28]]** closes, *lasting*: a `Char` is its own type in the checker, spelled `str`
  in Python as a target's choice; `show` gives `\a`. What reaches it through `at` (typed
  `Any`) is `collections`'.
- **[[B80]]:** a `def` is a constant, *lasting*; a mutable cell, if one comes, is a
  form of its own.
- **[[B31]]:** a top-level value's initial value may use only values defined before it,
  directly or through the functions it calls, an error at translation (`x is used
  before its def`); functions may still call each other in any order (Question 10).

### `Maybe` and missing values

As the epic leans (Question 6): `(deft (Maybe a) (Some ((v a))) (None))` in the prelude,
an ordinary generic sum. The checker's `Maybe` rules go (a `t` is no longer a `(Maybe
t)`; `nil` is only `Unit`), `with-default` becomes prelude Candy over `match`, and `find`
and `index-of` give a `Some` or a `None` (prelude Candy over built-ins, since the runtime
can't build the prelude's classes). `(Maybe (Maybe t))` no longer collapses; it is
Rust's `Option`. The variant `None` is spelled `None_` in Python, as `py-mangle` already
spells a Python keyword.

**Missing values** ([[B21]]): an `if` without `else` is allowed only when its `then` is
`Unit` (an effect, `(if verbose (put x))`), and is `Unit`; otherwise an error, `if: no
else, and the then is Int`. `cond` without `else` likewise. The value of a `def` form is
never seen (a `def` is top level only), so it isn't a value at all.

**Narrowing** ([[B121]]): in a `match` clause whose subject is a local, the local has
the variant's type in the clause's body, so `get` reads that variant's own fields. The
checker gets a type per variant, internally (`S.A`, accepted wherever an `S` is); the
language doesn't. This is also `Maybe`'s narrowing: `((Some v) ...)` names the value.

### The checker's other leaks

- **Field constraints** ([[B120]]): a `get` or `assoc` on a value whose type is a
  variable records the constraint (the variable must be a record with that field, of
  that type) and solves it when the variable is bound; a constraint still open when the
  definition is checked is the error it is today.
- **The unsolved types** ([[B132]]): a test per case (`Any` meeting a variable; nothing
  fixing one), the type in Core and its Python; whether `Any` should bind what it meets
  is decided with [[B18]], in `collections` (Question 13).

### `at` and `slice`

Proposed (Question 9), *lasting*: `(at xs i)` needs `0 <= i < (len xs)`, else it fails;
`(slice xs i j)` needs `0 <= i <= j <= (len xs)`. A negative index is an error, not "from
the end" (the translator's 4 become `(- (len xs) 1)`, or a prelude `last`). Python: a
checked helper, unless `i` is a literal that can't be out of range on the low side
(`(at xs 0)` stays `xs[0]`, Python's `IndexError` covering the high side); the helpers
replace B71's.

### Errors

Proposed (Question 11): `fail` is a **panic**, *lasting*: a bug, not caught in Candy;
the program stops with the message (Rust's `panic!`, Go's `panic`). Expected failure is
a value: `(deft (Result a e) (Ok ((v a))) (Err ((e e))))` in the prelude, taken apart
with `match`. No exceptions. The translator keeps its `fail`s (each is a translation
error the driver reports); the spec's runner, later, runs it as a process.

## The spec

- `spec/README.md`: examples print anything; the rule "only numbers and text" goes.
- New rules: `show` and printing (`library.show`, in `60-library.md`), equality
  (`expr.equality`), integer sizes and literal ranges (`types.numbers`), `at`'s and
  `slice`'s bounds, `def` order (`programs.def-order`), panics and `Result`
  (`library.errors`).
- Changed: `checking.maybe` (a sum; the rows on `t` as `(Maybe t)` go),
  `checking.if` and `expr.conditionals` (no `else` only for `Unit`), `expr.arithmetic`
  (`/` on floats, `rem`), `checking.records` (narrowing in a clause), `checking.order`
  (field constraints).
- The examples that print through Python's `str()` today print Candy's.

## Pros and cons

- **For:** the spec can show every value, and say what each operation means rather than
  what Python does; a second target or host implements a decided language; `Maybe`
  and `Result` as sums make the checker smaller (its `Maybe` rules go) and programs
  exact.
- **Against:** it is a big branch, fifteen items; programs change (`/`, an `if` without
  `else`, `Maybe` written `Some`, a negative `at`), though the translator barely; `at`'s
  check costs on its 681 uses (to measure); a runtime show for type variables is a stopgap.
- **Timing:** after `typed-core`, which it needs, and before `collections`, which builds
  `put` and `format` as macros over `show`.

## Bootstrap

Each step that changes `src/cdy/` rebuilds `bin`. A step that changes what the
translator's own source may write (a negative `at`, `/`, `Maybe`) goes in two: the new
rule built first with the source still accepted, then the source changed; the survey
says only `at`'s four uses need it.

## Steps

1. **The small ones:** [[B132]]'s tests; [[B26]], [[B28]] and [[B80]] decided in the
   spec, closed.
2. **`show` and printing** ([[B36]]): `show`, `put` and `format` by type; the spec's
   examples print anything.
3. **Equality** ([[B27]], [[B137]]): records and variants compared with their class;
   `=` on a function an error.
4. **`Maybe` a sum, missing values gone** ([[B20]], [[B21]]): the prelude's `Maybe`,
   the checker's rules out, `if`/`cond` without `else` only for `Unit`.
5. **Narrowing and field constraints** ([[B121]], [[B120]]).
6. **Numbers** ([[B23]], [[B22]]): `/` on floats, `rem`, literal ranges.
7. **`at` and `slice`** ([[B35]], [[B71]]): bounds checked, in two boot steps.
8. **`def` order** ([[B31]]).
9. **Errors** ([[B39]]): `fail` a panic, `Result` in the prelude.
10. **Docs:** CLAUDE.md, the iMVP doc, `multi_target.md` ("Open: showing values"
    closed), `python_complete.md`; "Looking back".

## Questions

1. **One branch or two?** Ten steps is twice `typed-core`'s. Split after step 5
   (`semantics`: printing, `=`, `Maybe`, the checker; `semantics-2`: numbers, `at`,
   `def`, errors), or keep one? **Proposed: one branch,** the steps as listed: each is a
   commit and a review item, and the split adds a merge, an HLD and a triage pass.
2. **`show`'s format:** Candy's syntax as a reader would read it back (the table above),
   or a display format (`3` for `3l`, no quotes inside lists)? **Proposed: read back**,
   *lasting*: `show` for programs and tests, `put` and `format` for people (text
   unquoted); maps `{k v, ...}` *for now*.
3. **`show` and `=` on a type variable:** a run-time show of the Python value (exact but
   for `Char` against `String` and `Byte` against `Int`); hidden parameters (each generic
   function gets its type variables' shows, as Haskell's dictionaries); or
   monomorphising (a copy per type). **Proposed: run-time,** *for now* (a new item),
   hidden parameters with interfaces. `=` needs nothing: the classes' `__eq__` is exact.
4. **`/`:** floats only, `quot` and `rem` for integers (Elm, OCaml's `/.`); or `/` on
   integers truncating (C, Rust, Java); or as now, `/` giving a `Double` (*lasting*).
   **Proposed: floats only**, since a typed language shouldn't change an operand's type
   silently, and `quot` already floors.
5. **Number sizes:** `Byte` 8 unsigned, `Int` 32, `Long` 64, `Float` 32, `Double` 64
   (Java, Kotlin, C#); or `Int` 64 (Rust's `i64`, Go's `int`), `Long` then 128 or
   gone? Overflow: unchecked on Python *for now*, each target's choice later?
   **Proposed: the Java sizes, literal ranges checked, overflow *for now*.**
6. **`Maybe`:** the real sum (the epic's lean), with the costs above (the translator 6
   mentions, the spec's `checking.maybe` and `60-library.md`'s `find` and `index-of`
   rows, 2 test programs); or `a | None` kept *lasting* with narrowing after `(= m nil)`.
   **Proposed: the real sum,** `Some` and `None` (Rust's names; Elm's `Just` and
   `Nothing`, Haskell's too, are the other choice).
7. **An `if` without `else`:** only for `Unit` (proposed); always an error (Elm, Rust
   unless `()`); or `Unit` whatever the `then` (discarding it)? **Proposed: only for
   `Unit`.**
8. **Narrowing:** in a clause, the subject local narrowed to the variant (proposed); or
   also after an `if` on a test (`(if (is-a s A) ...)`, which Candy doesn't have)?
   **Proposed: clauses only.**
9. **`at` and `slice` out of range:** an error, *lasting*, negative indexes too
   (proposed; Rust, Go, Elm's `Array.get` gives a `Maybe`); `at` giving a `Maybe`
   (Elm), which would make every `at` a `match`; or Python's meaning kept *lasting*?
   **Proposed: an error,** checked as cheaply as the survey allows.
10. **`def` order:** checked through the functions an initial value calls (proposed), or
   only directly (simpler, *for now*, the transitive case a run-time `NameError` still)?
   **Proposed: transitively,** since the direct check alone leaves the common case
   (a helper reading a later `def`).
11. **Errors:** `fail` a panic and `Result` a prelude sum (proposed); exceptions with a
   `try` form; or `Result` only, `fail` gone? And the translator: keeps its `fail`s
   (proposed), or moves to `Result`, so that a host can run it in-process? **Proposed:
   panic and `Result`; the translator unchanged,** its errors the driver's to report.
12. **[[B137]] and the defect's fix:** classes compare their class (proposed), or a
   runtime `eq` function generated code calls (one place, slower)? **Proposed: the
   classes,** as Python's own `==` then is Candy's `=`.
13. **`Any` and the variables it meets** ([[B132]]): decided here (bind them to `Any`),
   or with [[B18]] in `collections`? **Proposed: tests here, the decision with
   [[B18]],** since what `Any` does is that branch's.
14. **Order of the steps:** `show` early (proposed: it unlocks the spec for every later
   step's examples), or `Maybe` first (the biggest change)? **Proposed: as listed.**
