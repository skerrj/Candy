# Semantics (HLD)

**Status: accepted (2026-11-02), with the answers to its questions and its spec changes;
on branch `semantics` (tasks [[B140]] to [[B149]]); proposed 2026-11-01. Epic:
`python_complete.md` (its second branch). After tag `typed-core`.** Where Candy's behaviour is Python's, borrowed rather
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

- **Every value prints as Candy shows it,** by its type: `true`, `nil`, `(List 1 2 3)`,
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

A built-in `show`, typed `(Fn (a) String)`, gives a value as an expression that
evaluates to an equal value: a literal as the literal, anything else as its
constructor applied to its parts (Question 2). Every type's name is its constructor,
the built-in ones' too: `List` and `Tup` become variadic built-in constructors (`tup`
staying as an alias, *for now*), `Maybe`'s are `Some` and `None` (step 4).

| Type | Built and shown | |
|---|---|---|
| `Bool`, `Unit` | `true`, `nil` | |
| numbers | `42`, `1500l`, `1b`, `3.14f`, `10.0` | as written |
| `Char`, `String` | `\a`, `"text"` (escaped) | |
| `(List t)` | `(List 1 2 3)` | |
| `(Tup ...)` | `(Tup 1 "a")` | |
| `(Maybe t)` | `(Some 3)`, `None` | step 4 |
| a record or variant | `(V 1 "a")` | its constructor |
| `(Map k v)` | `(Map (Tup "a" 1) (Tup "b" 2))` | *for now*, until `collections` decides literals |
| a function | an error at translation | Question 12 of the epic: every value shown is data |

Literals for the collections (`[1 2 3]`, Clojure's), and literals overloaded by the
expected type (Haskell's `OverloadedLists`, with interfaces), are `collections`' to
decide, as sugar over the constructors; `show` then writes them.

`put` and a `format` hole show their values, except a `String` or `Char`, written as its
text: `(put "a" 1 true)` prints `a 1 true`.

**How:** the translator knows each node's type (typed Core), so `emit` chooses the
printer: a `String` hole stays a plain f-string hole; any other type calls a show for it,
built from the type (a record's show calls its fields'). A **type variable** (in a
generic function) has no type to choose by (Question 3): showing one is an error at
translation, *for now* (a new item), until interfaces let a function declare that its
type variable can be shown (the hidden-parameter way, each generic function given its
type variables' shows). Step 2 first counts the holes whose type the checker never
solved ([[B132]]), which would be errors too; if they are many, those alone get a show
that inspects the Python value at run time, a leak. A variable that met `Any` and
nothing else is `Any` by then (Question 13), and a value typed `Any` gets that run-time
show, part of `Any`'s leak ([[B18]]).

### Equality

`=` and `!=` are structural, on two values of one type (as the checker already
requires): two lists with equal items, two records of one type with equal fields, two
variants only if they are the same variant ([[B137]]). Python: each record and variant
class gets `__eq__`, `__ne__` and `__hash__` comparing the class too (methods in the
class body, no decorators). On a function type `=` is an error (the epic's Question 12).
A type variable's `=` is Python's `==` with the classes' `__eq__`, so it is exact.
`Float` and `Double` compare as IEEE does (`nan` isn't equal to itself), *lasting*.

### Numbers

- **`/`** (Question 4): `/` on `Float` and `Double` only, giving the same type, *lasting*;
  `quot` (floor, *lasting*: [[B24]]) and a new `mod` for the integers, rounding down as
  `quot` does (`a` = `b`·`(quot a b)` + `(mod a b)`, the result taking `b`'s sign, as
  Python's `%`). `(/ 7 2)` becomes an error, `(quot 7 2)` or `(/ 7.0 2.0)`. A weakness,
  kept: `quot` is Haskell's name for the truncating division, whose partner is `rem`,
  while Candy's floors, as Haskell's `div` (B24's note).
- **Sizes** (Question 5): `Byte` 8 bits unsigned, `Int` 32 and `Long` 64 signed, `Float`
  32 and `Double` 64, *lasting*, as Java and Kotlin have them (Candy's `Int` and `Long`
  already say there are two; `Byte` unsigned as C#'s, Rust's `u8`). A literal out of its
  range is an error at translation (`300b`). Overflow in arithmetic is unchecked on
  Python, which has no sizes, and a `Float` there is 64 bits, *for now* ([[B22]],
  reworded): the potential fix, a rule (trap, as Swift; or wrap, as Java) with each
  target's way to keep it, is `porting-surface`'s.

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

As the epic leans (Question 6, decided): `(deft (Maybe a) (Some ((v a))) (None))` in the prelude,
an ordinary generic sum. The checker's `Maybe` rules go (a `t` is no longer a `(Maybe
t)`; `nil` is only `Unit`), `with-default` becomes prelude Candy over `match`, and `find`
and `index-of` give a `Some` or a `None` (prelude Candy over built-ins, since the runtime
can't build the prelude's classes). `(Maybe (Maybe t))` no longer collapses; it is
Rust's `Option`. The variant `None` is spelled `None_` in Python, as `py-mangle` already
spells a Python keyword.

**Missing values** ([[B21]]): an `if` without `else` is allowed only when its `then` is
`Unit` (an effect, `(if verbose (put x))`), and is `Unit`, *for now* ([[B138]]); otherwise an error, `if: no
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
  fixing one), the type in Core and its Python; a variable that met `Any` and nothing
  else is defaulted to `Any` at the end, one that met nothing stays a variable (Question
  13).

### `at` and `slice`

Decided (Question 9), *lasting*: `(at xs i)` needs `0 <= i < (len xs)`, else it fails;
`(slice xs i j)` needs `0 <= i <= j <= (len xs)`. A negative index is an error, not "from
the end" (the translator's 4 become `(- (len xs) 1)`, or a prelude `last`). Python: a
checked helper, unless `i` is a literal that can't be out of range on the low side
(`(at xs 0)` stays `xs[0]`, Python's `IndexError` covering the high side); the helpers
replace B71's.

### Errors

Decided (Question 11): `fail` is a **panic**, *lasting*: a bug, not caught in Candy;
the program stops with the message (Rust's `panic!`, Go's `panic`). Expected failure is
a value: `(deft (Result a e) (Ok ((v a))) (Err ((err e))))` in the prelude, taken apart
with `match`. No exceptions. The translator keeps its `fail`s (each is a translation
error the driver reports); the spec's runner, later, runs it as a process, or in-process
with a `catch-panic` for tools ([[B139]]).

## The spec

Each step changes its spec file in the same commit (`doc/process.md`, "The spec"); the
rules by file (rule ids new unless they exist; reviewed against the answers 2026-11-02):

- **`spec/README.md`:** examples print anything; the rule "only numbers and text" goes
  (step 2), and the examples that print through Python's `str()` today print Candy's
  (`true`, not `True`).
- **`00-syntax.md`:** `syntax.numbers`, the sizes and `Byte` unsigned, a literal out of
  range an error (`300b`; step 6); `syntax.chars`, a `Char` its own type ([[B28]]
  closed, step 1).
- **`10-programs.md`:** `programs.def-order`, new: an initial value uses only values
  defined before it, through the functions it calls too, a `fn` in it counted as
  called, a cycle the same error (step 8); `programs.top-level`, a `def` a constant
  ([[B80]] closed, step 1); `programs.prelude`, `Maybe` and `Result` in it (steps 4, 9).
- **`20-types.md`:** `types.constructors`, new: every type's name is its constructor,
  `List` and `Tup` variadic built-ins, `tup` an alias *for now* (step 2); `types.table`,
  `Maybe` a prelude sum (step 4); overflow unchecked and `Float` 64 bits on Python, *for
  now* ([[B22]], step 6).
- **`25-checking.md`:** `checking.any`, a variable that met only `Any` defaulted to
  `Any` (step 1); `checking.tup-lists`, `List`'s items one type, as `tup`'s (step 2);
  `checking.maybe`, a sum, the rows on `t` as `(Maybe t)` and `nil` as `Maybe` gone (step
  4); `checking.if`, no `else` only for `Unit`, *for now* ([[B138]], step 4);
  `checking.records`, narrowing in a clause, *for now* ([[B136]], step 5);
  `checking.order`, field constraints (step 5).
- **`30-match.md`:** `match.sum-types`, the subject narrowed in a clause (step 5).
- **`40-expressions.md`:** `expr.equality`, new: structural, a variant equal only to
  the same variant ([[B137]]), `=` on a function an error, floats as IEEE (step 3);
  `expr.arithmetic`, `/` on floats, `mod` beside `quot` (step 6); `expr.logic`, the
  operands `Bool`s ([[B26]] closed, step 1); `expr.conditionals`, no `else` only for
  `Unit` (step 4); `macros.cond` (`50-macros.md`) likewise.
- **`60-library.md`:** `library.show`, new: the constructor rule, `put` and `format`
  writing text unquoted, a function or a type variable an error, `Any` the run-time show
  ([[B18]]); the file's own `show` (line 55, printing `[1 2 3]`) goes for the built-in;
  a program's own `show` still shadows it, as any built-in (step 2); `library.format`
  likewise; `library.bounds`, new: `at` and `slice` out of range an error, negative
  indexes too (step 7); `library.builtins`, `find` and `index-of` giving the sum,
  `with-default` prelude Candy (step 4); `library.errors`, new: `fail` a panic (line 42's
  "no exceptions yet" goes), `Result` (step 9).

Before (2026-11-01), replaced by the list above:

```text
- `spec/README.md`: examples print anything; the rule "only numbers and text" goes.
- New rules: `show` and printing (`library.show`, in `60-library.md`), equality
  (`expr.equality`), integer sizes and literal ranges (`types.numbers`), `at`'s and
  `slice`'s bounds, `def` order (`programs.def-order`), panics and `Result`
  (`library.errors`).
- Changed: `checking.maybe` (a sum; the rows on `t` as `(Maybe t)` go),
  `checking.if` and `expr.conditionals` (no `else` only for `Unit`), `expr.arithmetic`
  (`/` on floats, `mod`), `checking.records` (narrowing in a clause), `checking.order`
  (field constraints).
- The examples that print through Python's `str()` today print Candy's.
```

## Pros and cons

- **For:** the spec can show every value, and say what each operation means rather than
  what Python does; a second target or host implements a decided language; `Maybe`
  and `Result` as sums make the checker smaller (its `Maybe` rules go) and programs
  exact.
- **Against:** it is a big branch, fifteen items; programs change (`/`, an `if` without
  `else`, `Maybe` written `Some`, a negative `at`), though the translator barely; `at`'s
  check costs on its 681 uses (to measure); a generic function can't show its type
  variables' values until interfaces.
- **Timing:** after `typed-core`, which it needs, and before `collections`, which builds
  `put` and `format` as macros over `show`.

## Bootstrap

Each step that changes `src/cdy/` rebuilds `bin`. A step that changes what the
translator's own source may write (a negative `at`, `/`, `Maybe`) goes in two: the new
rule built first with the source still accepted, then the source changed; the survey
says only `at`'s four uses need it.

## Steps

1. **The small ones:** [[B132]]'s tests, and a variable that met only `Any` defaulted
   to `Any` at the end (Question 13); [[B26]], [[B28]] and [[B80]] decided in the spec,
   closed.

   *Done.* As built:
   - **`check.cdy`:** `unify` still binds nothing `Any` meets, but `mark-any` marks
     each flexible variable in the other type, in the substitution under its name with
     `any` before it (`any?4`; no variable is named so, and the substitution is only
     looked up by name). `node-type` resolves with `final-type`: an unsolved variable
     with a mark is `Any`, one without stays a `TVar`. A variable that met `Any` and is
     solved later keeps the later type.
   - **The translator's own Core:** its eight unsolved nodes (all `Any` meeting a
     variable, [[B132]]) are `Any` now, none left; its Python is unchanged but for
     renumbered temporaries, since an unsolved variable was written `Any` already.
   - **Tests** (`tst/py_cdy/test_self_host.py`): `test_unsolved_types`, one case each,
     the type in Core and its Python: met `Any` (`(List Any)`), met `Any` then `Int`
     (`(Fn (Int) Int)`), a `fn` never called and an `empty-list` never added to (still
     variables, Python `Any`); `test_every_node_is_typed` now also checks the
     translator's Core has no unsolved variable (helpers `typed_core`, `unsolved`).
   - **The spec:** [[checking.any]] states the defaulting (*Tested in* the two tests);
     [[expr.logic]] the `Bool` result, with an errors table ([[B26]]); [[syntax.chars]]
     `Char` its own type, with `=: expected Char, got String` ([[B28]]);
     [[programs.top-level]] a `def` a constant, with `defined more than once` ([[B80]]).
     `spec/20-types.md` (`types.sig`) and `mutation_optimization.md` (open question 4)
     follow. All closed with no code change but the defaulting.
   - **Bootstrap:** `bin` rebuilt (`boot/48`); nothing new the source may write.

   The text replaced, verbatim. `spec/20-types.md` (`types.sig`), line 83:

   ```text
   defined once. No form changes a `def`'s value yet, so whether a `def` is a constant or a
   variable is undefined (*for now*: `doc/hl_rqmt/mutation_optimization.md`, open question
   4).
   ```

   `doc/hl_rqmt/mutation_optimization.md`, "Where the iMVP stands", line 10:

   ```text
   - **`def`'s mutability is undefined.** `candy-special.md` called it "not immutable... for
     now", but no form changes a `def`'s value, and defining a name twice is an error, so a
     `def` is neither a constant nor a variable yet (`spec/20-types.md` says it is open). It
     becomes an issue once a form that changes a value arrives, or a target where the two
     differ (a C constant, a JavaScript `const`): open question 4, and an item for the
     backlog (`doc/hl_rqmt/tracking.md`).
   ```
2. **`show` and printing** ([[B36]]): the `List` and `Tup` constructors; `show`, `put`
   and `format` by type; the spec's examples print anything.

   *Done.* As built:
   - **Constructors** (`core.cdy`): `List` and `Tup` aren't in `special.cdy`, since a
     built-in type's name is in the built-ins as a type (one map); `analyse-list` treats
     the names in `BUILTIN_CONSTRUCTORS` (unless a local) as forms. `(Tup ...)` is
     `tup`'s form (and pattern); `(List ...)` is a new Core node, `ListOf`, which
     `check.cdy` types as a `(List t)` with each item a `t` (`infer-list-of`: `List: an
     item: expected Int, got String`) and `lower` turns into a `Tuple`, so `emit` never
     sees one (it says so, for `match`'s exhaustiveness).
   - **`show`** (`system.cdy`: `(sig show (Fn (a) String))`; runtime `show`): `emit`
     writes the value's type for the runtime, from the node's type (`show-type`: `"Int"`,
     `("List", "Int")`), and the runtime shows it. A function, or a type variable (rigid,
     or an unsolved `?N`), is an error when translated, at the call or the `format`;
     `Any` is the runtime's `show_any`. Each record and variant class is registered
     after its definition (`cdy_rt.primitives.register_type(Box, "Box", ("a",),
     ("'a",))`: its Candy name, its type's type variables, its fields' types), so the
     runtime shows records, generic and recursive ones too, by their class; mypy refuses
     class attributes in a `NamedTuple`'s body, hence a registry. A function inside a
     record is found only when run ([[B150]]); a float with no literal (`1e+20`) is
     Python's `repr` ([[B151]]). `show` as a value is a `lambda` over its type.
   - **`put` and `format`:** `emit-text` writes a `String` or `Char` as it is, an `Int`
     with `str` (in `put`, as it is), a value typed `Any` with `text_any` (its text if
     it is a string), and shows the rest. `print` and `display` (unused aliases) are
     `put`'s.
   - **The translator's own holes:** none is a type variable (Question 3's count is 0);
     3 call `show` (two `Double`s in `emit-lit`, and `show-call`'s own text), 26 call
     `text_any`, on values that are strings when run. `emit-lit` wrote a `Bool` literal
     with `(format "{v}")`, Python's `True`, which the new `show` made `true`: it writes
     `True` and `False` itself now, which the old `bin` reads the same, so no two-step
     bootstrap. `lower`'s sequence temporaries keep their value's type (they were
     `Any`, which would have shown values from Python).
   - **Tests:** the runtime's `show` (`tst/cdy_rt/test_primitives.py`: each type,
     records, `Any`); the outputs that changed, as decided (`true`, `1500l`, `(Tup "one"
     1)`, `(Some 7)`, read values as `(List ...)` from `Any`): `basics`, `forms_1b`,
     `read_sexpr`, `macro_files`, `macros`, and `macro_code/quoting`;
     `test_unsolved_types` no longer `put`s its unsolved list (an error now).
   - **The spec:** [[library.show]] (new, with errors: a function, a type variable,
     `(put empty-list)`); [[types.constructors]] (new); [[types.tuples]] (`Tup`, `tup`
     *for now*, [[B152]]); [[checking.tup-lists]]; [[library.lists]]'s example prints
     lists and `Bool`s itself, its own `show` and `yes` gone; [[library.format]]; the
     literals example (`syntax.literals`) prints `1500l 1b` and `3.14f`; `spec/README.md`
     drops "output is numbers and text".
   - **Bootstrap:** `bin` rebuilt with the new library next to the old `bin` (the
     staging the chain does), one step.

   The text replaced, verbatim. `spec/README.md`, line 56:

   ```text
   **Output is numbers and text** (*for now*): an example prints numbers, and strings it
   builds with `format`, never a raw list, `Bool`, `nil` or record, since those print the way
   Python prints them ([[B36]]; `doc/hl_rqmt/executable_spec.md`, question 12).
   ```

   `spec/60-library.md`, the head (line 10) and `library.lists`'s example (line 22):

   ```text
   them. The examples print lists and `Bool`s through small helpers, since a list or a `Bool`
   prints the way Python prints it (*for now*: `spec/README.md`).

   (sig show (Fn ((List Int)) String))
   (defn show (xs) (+ "[" (join (map (fn (n) (format "{n}")) xs) " ") "]"))
   (sig yes (Fn (Bool) String))
   (defn yes (b) (if b "yes" "no"))
   ...
   [1 2 3 4 5] []
   [1 4 9 16 25] [3 4 5]
   ```

   `spec/20-types.md` (`types.tuples`), line 169, and `spec/25-checking.md`
   (`checking.tup-lists`):

   ```text
   `(tup expr+)` makes a fixed-size tuple of at least one item, typed `(Tup a b ...)`. `at`
   reads an item by its position, from 0, and `len` is its size. A tuple is taken apart with
   a `tup` pattern, in `match` or a `let` binding (`30-match.md`).

   A `(Tup t ...)` whose items are all `t`s is accepted where a `(List t)` is expected, so
   `tup` writes a list (*for now*: Candy has no list literal, and a tuple is a list in
   Python, [[B29]]).
   ```
3. **Equality** ([[B27]], [[B137]]): records and variants compared with their class;
   `=` on a function an error.

   *Done.* As built:
   - **`emit.cdy`:** every record and variant class gets `eq-methods`: `__eq__`
     (`type(self) is type(other) and tuple.__eq__(self, other)`), `__ne__` and
     `__hash__` (the class with the fields), in its body, so Python's own `==` is
     Candy's `=` everywhere: in `=`, `contains`, `index-of`, and a map's keys. A variant
     with no fields no longer needs `pass`. Every class gets them: a class without
     would still compare as a tuple from its side (`B(1) == A(1)`, checked on Python
     3.14 for Question 12).
   - **`check.cdy`:** a comparison whose type is, or holds, a function (`has-fn`: a list
     of functions too) is an error at the call, `=: a function can't be compared, got
     (Fn (Int) Int)`; a function inside a record isn't seen ([[B150]], noted).
   - **Found:** the orderings (`<` and the rest) take any one type, so records, lists
     and `Bool`s order as Python's tuples and `nil` fails when run ([[B153]], a leak).
     mypy refuses `(= (List (A 1)) (List (B 1)))` written with literals (`tuple[A]`
     against `tuple[B]`, non-overlapping), though Candy types both `(List S)`; a typed
     value doesn't meet it, so it stays mypy's (the second check, [[B125]]).
   - **The spec:** [[expr.equality]] (new, after [[expr.comparisons]]), with
     [[B137]]'s repro as its `(= a (B 1))` (the repro is kept in B137's note) and the
     errors. [[B27]] and [[B137]] done; [[B29]] noted (equality was one of its
     consequences; the rest stays).
   - **Bootstrap:** `bin` rebuilt, one step; the translator's own classes get the
     methods too.
4. **`Maybe` a sum, missing values gone** ([[B20]], [[B21]]): the prelude's `Maybe`,
   the checker's rules out, `if`/`cond` without `else` only for `Unit`.

   *Done.* As built:
   - **`prelude.cdy`:** `(deft (Maybe a) (Some ((v a))) (None))`, and `find`, `index-of`
     and `with-default` on it, in Candy, over two new built-ins that give `-1` for none,
     `find-index` and `elem-index` (`system.cdy`; `list_find_index` and
     `list_elem_index` in `primitives.py`). `system.cdy`'s `(deft (Maybe a))`, the three
     old `sig`s, their spellings, `with_default` and `show_maybe` are gone: a `Maybe` is
     shown as any variant, `(Some 4)`.
   - **`check.cdy`:** the `Maybe` rules out (`maybe-arg`, `as-maybe`, `is-unit`, and
     `join-types`' `Unit` and `Maybe` branches): `accepts` is a `Tup` of `t`s as a
     `(List t)`, else unification. An `if` whose `else` is missing (`is-missing-else`:
     the `nil` analysis writes, at `NOWHERE`) has a `Unit` then, `if: with no else, the
     then is Int, not Unit`. A `cond` with no `else` expands to a written `nil`, so its
     error is `if: the branches are Int and Unit`, a defect the owner finds irritating
     ([[B155]]; noted in [[B138]]).
   - **`emit.cdy`:** a generic variant's `match` bindings are annotated with their type
     (`v: a = t0.v`), as mypy narrows an `isinstance` on a `Maybe[a]` to `Some[Any]`.
   - **Found:** [[B154]], a defect from before the branch: one module's locals could be
     spelled as another's in a top-level function (the prelude's `rest` read `v` for its
     `xs`), since `python-of` kept every module's locals in one map. Fixed: `emit-func`
     starts from an empty map.
   - **The spec:** [[checking.if]], [[checking.maybe]], [[expr.conditionals]] and
     [[expr.unit]] rewritten (their old text is in [[B20]]'s and [[B21]]'s notes),
     [[library.maybe]] new, `spec/20-types.md`'s `Maybe` row and [[library.lists]] (in
     [[B20]]'s note). [[programs.prelude]] said, before (now: `rest`, `map-update`, and
     `Maybe` with `find`, `index-of` and `with-default`):

     ```text
     on the built-ins (declared in `src/cdy/system.cdy`), `rest` and `map-update` so far.
     ```
   - **Tests:** `test_primitives`' two `Maybe` rows of `test_show` dropped (`(None,
     ("Maybe", "Int"), "None")` and `(3, ("Maybe", "Long"), "(Some 3l)")`), the spec
     covering them; `test_unsolved_types` names an unsolved variable `tN`, as its number
     depends on the prelude; `macros.cdy`'s value `when` dropped (kept in [[B138]]'s
     note). [[B20]] and [[B21]] done.
   - **Bootstrap:** `bin` rebuilt, one step; the translator used neither.
5. **Narrowing and field constraints** ([[B121]], [[B120]]).

   *Done.* As built:
   - **Narrowing** (`check.cdy`): the checker's `Ctx` has `narrowed`, a local's key to
     its clause's variant, set by `infer-clauses` when the subject is a local; `narrow`
     gives `get` and `assoc` on it the variant (with the sum's type arguments), not the
     sum. No variant types: the local is still of the sum everywhere else, as the HLD
     wanted (`S.A` accepted wherever an `S` is) at the cost of nothing new in `unify`.
     The `else` isn't narrowed.
   - **Narrowing in Python** (`emit.cdy`): in a case, a `get` or `assoc` on the subject
     local reads the match's temporary (`_cdy_t1.x`), which `isinstance` has narrowed;
     `s` itself is the sum to mypy. For a generic sum mypy narrows `isinstance(t, N)` on
     a `T[int]` to `N[Any]`, on a parameter too, so a field whose type has a type
     variable is cast to the checker's type (`_cdy_cast('int', _cdy_t3.v)`; `cast` is
     imported as `_cdy_cast`), and only it, as `--strict` refuses a redundant cast
     (`generic` in `Env` now maps each generic variant to those fields). Another
     type-level leak (`multi_target.md`).
   - **Field constraints** (`check.cdy`): `field-type` on a flexible variable gives a
     fresh variable and records a `Pending` in `St`; `check-tops` runs `solve-pending`
     after each definition: a constraint whose value's type is known is checked as the
     `get` or `assoc` would have been (`get: field name of P is String, not Int`), the
     rest again while any was solved, then each left is today's error, and one whose
     value met only `Any` is `Any`.
   - **[[B155]], taken into the step:** `cond`'s last clause with no `else` expands to an
     `if` with no `else` (`prelude_macros.cdy`), so the checker's missing-else rule sees
     it: `if: with no else, the then is Int, not Unit`, as for an `if`. The message
     naming the `if` is [[B156]] (an idea: a macro's errors in the expansion's words).
   - **The spec:** [[checking.narrowing]] (new), [[checking.records]] (its *for now*
     gone, its error example now a run one there), [[checking.order]] (a constraint, a
     run example and three errors), [[checking.if]] (`cond`'s error), [[match.sum-types]].
     The old text is in [[B120]]'s, [[B121]]'s and [[B155]]'s notes. [[B120]], [[B121]]
     and [[B155]] done.
   - **Bootstrap:** `bin` rebuilt, one step; the translator neither narrows nor reads a
     field of an unknown type, and its Python only gains the `cast` import.
6. **Numbers** ([[B23]], [[B22]]): `/` on floats, `mod`, literal ranges.
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
   **Decided (2026-11-01): one branch, with a checkpoint after step 5,** where the owner
   decides whether to merge then and do steps 6 to 9 as `semantics-2`.
2. **`show`'s format:** Candy's syntax as a reader would read it back (the table above),
   or a display format (`3` for `3l`, no quotes inside lists)? **Proposed: read back**,
   *lasting*: `show` for programs and tests, `put` and `format` for people (text
   unquoted); maps `{k v, ...}` *for now*.
   **Decided (2026-11-01): a value shows as its constructor applied to its parts,**
   *lasting*, and every type's name is its constructor (`(List 1 2 3)`, `(Tup 1 "a")`,
   `(Some 3)`; Scala's scheme); `put` and `format` as proposed. The owner asked what
   separates printing a list from printing an expression: the proposal's `(1 2 3)` was
   a Lisp's data notation, a call of `1` in Candy, while `(tup 1 "a")` and `(V 1 "a")`
   were expressions; and why only a user's types have constructors. The other schemes
   weighed: literals per collection (Clojure), lowercase constructor functions (Lisp's
   `list`, Kotlin's `listOf`), lists as a `Nil`/`Cons` sum (ML), typed quoted data,
   literals overloaded by type (Haskell's `OverloadedLists`), and types as values
   (Zig, Idris); the second and fifth are left to `collections` as sugar. The table
   under "Showing values" (line 62) was, before:

   ```text
   | `(List t)` | `(1 2 3)` | |
   | `(Tup ...)` | `(tup 1 "a")` | |
   | a record or variant | `(V 1 "a")`, `(None)` | its constructor |
   | `(Map k v)` | `{"a" 1, "b" 2}` | *for now*, until `collections` decides a map literal |
   ```
3. **`show` and `=` on a type variable:** a run-time show of the Python value (exact but
   for `Char` against `String` and `Byte` against `Int`); hidden parameters (each generic
   function gets its type variables' shows, as Haskell's dictionaries); or
   monomorphising (a copy per type). **Proposed: run-time,** *for now* (a new item),
   hidden parameters with interfaces. `=` needs nothing: the classes' `__eq__` is exact.
   **Decided (2026-11-01): an error, *for now*,** a fourth way: "can't show a value of
   type `a`" (Rust's "doesn't implement `Display`"), a constraint to declare once
   interfaces come. Under Question 2's constructor rule the run-time show is less exact
   than said above: it can't tell `Char` from `String`, `Int`/`Long`/`Byte` apart (`3l`
   shown `3`), `Float` from `Double`, or a `List` from a `Tup` (all Python tuples). An
   unsolved `?N` ([[B132]]) is a type variable too: step 2 counts those holes, and if
   they are many, they alone get the run-time show, as a leak. The text under "Showing
   values" (line 91) was, before:

   ```text
   generic function) has no type to choose by (Question 3): proposed, a show that inspects
   the Python value at run time, which is exact except that it can't tell a `Char` from a
   `String` or a `Byte` from an `Int` (*for now*, a new item), with the hidden-parameter
   way (each generic function given its type variables' shows) left for when interfaces
   come.
   ```
4. **`/`:** floats only, `quot` and `rem` for integers (Elm, OCaml's `/.`); or `/` on
   integers truncating (C, Rust, Java); or as now, `/` giving a `Double` (*lasting*).
   **Proposed: floats only**, since a typed language shouldn't change an operand's type
   silently, and `quot` already floors.
   **Decided (2026-11-01): floats only,** *lasting*, with the integer remainder named
   `mod`, not `rem`: Candy's `quot` floors (Haskell's `div`), so its partner floors too
   (Haskell's and Lisp's `mod`; their `rem` truncates). The name `quot` itself is the
   weakness, noted in [[B24]], not renamed. The bullet under "Numbers" (line 111) was,
   before:

   ```text
   - **`/`** (Question 4): proposed, `/` on `Float` and `Double` only, giving the same type;
     `quot` (floor, *lasting*: [[B24]]) and a new `rem` for the integers. `(/ 7 2)` becomes
     an error, `(quot 7 2)` or `(/ 7.0 2.0)`.
   ```
5. **Number sizes:** `Byte` 8 unsigned, `Int` 32, `Long` 64, `Float` 32, `Double` 64
   (Java, Kotlin, C#); or `Int` 64 (Rust's `i64`, Go's `int`), `Long` then 128 or
   gone? Overflow: unchecked on Python *for now*, each target's choice later?
   **Proposed: the Java sizes, literal ranges checked, overflow *for now*.**
   **Decided (2026-11-01): as proposed,** `Byte` unsigned; overflow left undecided, with
   a note to `porting-surface` (the epic's step 9, and [[B22]]): the potential fix is
   to choose trap (Swift, Rust's debug builds) or wrap (Java, Go) as Candy's rule, and
   on Python either check each operation (slow) or keep the leak; `Float`'s 32 bits
   likewise (Python rounds only with `struct` or numpy). The bullet under "Numbers"
   (line 117) was, before:

   ```text
   - **Sizes** (Question 5): proposed, `Byte` 8 bits unsigned, `Int` 32 and `Long` 64
     signed, `Float` 32 and `Double` 64, *lasting*, as Java and Kotlin have them (Candy's
     `Int` and `Long` already say there are two). A literal out of its range is an error at
     translation (`300b`). Overflow in arithmetic is unchecked on Python, which has no
     sizes, *for now* (a new item): each target's choice, wrap or trap, is the porting
     surface's.
   ```
6. **`Maybe`:** the real sum (the epic's lean), with the costs above (the translator 6
   mentions, the spec's `checking.maybe` and `60-library.md`'s `find` and `index-of`
   rows, 2 test programs); or `a | None` kept *lasting* with narrowing after `(= m nil)`.
   **Proposed: the real sum,** `Some` and `None` (Rust's names; Elm's `Just` and
   `Nothing`, Haskell's too, are the other choice).
   **Decided (2026-11-01): the real sum, `Some` and `None`,** *lasting* (Rust's, OCaml's
   and Scala's names, the better known); shown `(Some 3)` and `None` (Question 2), a
   variant with no fields being a value, not a call (`spec/30-match.md:22`).
7. **An `if` without `else`:** only for `Unit` (proposed); always an error (Elm, Rust
   unless `()`); or `Unit` whatever the `then` (discarding it)? **Proposed: only for
   `Unit`.**
   **Decided (2026-11-01): only for `Unit`, *for now*** ([[B138]]). The attribution above
   is off: Rust (and OCaml) allow an `if` without `else` when it is `()`, which is this
   rule; Elm and Haskell always need the `else`. A fourth way, `if` always with both
   branches and a `when` macro for effects (Lisps), is [[B138]]'s, for later.
8. **Narrowing:** in a clause, the subject local narrowed to the variant (proposed); or
   also after an `if` on a test (`(if (is-a s A) ...)`, which Candy doesn't have)?
   **Proposed: clauses only.**
   **Decided (2026-11-01): clauses only, *for now*** ([[B136]] tracks the revisit). The
   others weighed: flow typing after a test (Kotlin's smart casts, TypeScript; needs an
   `is-a`); no narrowing at all (ML, Haskell, Elm: the pattern's names only, with
   Haskell's as-patterns `s@(A x)`), which [[B136]]'s patterns without every field would
   make easier to live with.
9. **`at` and `slice` out of range:** an error, *lasting*, negative indexes too
   (proposed; Rust, Go, Elm's `Array.get` gives a `Maybe`); `at` giving a `Maybe`
   (Elm), which would make every `at` a `match`; or Python's meaning kept *lasting*?
   **Proposed: an error,** checked as cheaply as the survey allows.
   **Decided (2026-11-01): an error,** *lasting*, negative indexes too. A second form
   giving a `Maybe` (Rust's `xs.get(i)` beside `xs[i]`) is left for when one is needed,
   prelude Candy over `at` and `len`. Step 7 measures the check's cost on the
   translator's own build.
10. **`def` order:** checked through the functions an initial value calls (proposed), or
   only directly (simpler, *for now*, the transitive case a run-time `NameError` still)?
   **Proposed: transitively,** since the direct check alone leaves the common case
   (a helper reading a later `def`).
   **Decided (2026-11-02): transitively,** a `fn` written in an initial value counted as
   called (conservative); a cycle (`x` calls `f`, `f` reads `x`) is the same error. The
   others weighed: the direct check only (Java's static fields), strict order for
   functions too (OCaml's `let rec ... and`, F#), and lazy top-level values (Haskell,
   Kotlin's `by lazy`).
11. **Errors:** `fail` a panic and `Result` a prelude sum (proposed); exceptions with a
   `try` form; or `Result` only, `fail` gone? And the translator: keeps its `fail`s
   (proposed), or moves to `Result`, so that a host can run it in-process? **Proposed:
   panic and `Result`; the translator unchanged,** its errors the driver's to report.
   **Decided (2026-11-02): as proposed,** with a note for `test-runner`: a narrow
   `catch-panic` for tools ([[B139]]; Rust's `catch_unwind`, Go's `recover`), if running
   each `candy error` example as a process is too slow. `Err`'s field is `err`, not `e`
   (a field `e` of type `e` was legal but confusing). The text under "Errors" (line 173)
   was, before:

   ```text
   Proposed (Question 11): `fail` is a **panic**, *lasting*: a bug, not caught in Candy;
   the program stops with the message (Rust's `panic!`, Go's `panic`). Expected failure is
   a value: `(deft (Result a e) (Ok ((v a))) (Err ((e e))))` in the prelude, taken apart
   with `match`. No exceptions. The translator keeps its `fail`s (each is a translation
   error the driver reports); the spec's runner, later, runs it as a process.
   ```
12. **[[B137]] and the defect's fix:** classes compare their class (proposed), or a
   runtime `eq` function generated code calls (one place, slower)? **Proposed: the
   classes,** as Python's own `==` then is Candy's `=`.
   **Decided (2026-11-02): the classes,** every record's and variant's (checked on Python
   3.14: `A(1) == B(1)` and `A(1) == (1,)` are `False`, nested tuples compare item by
   item, `A(1) in {A(1)}` holds; but `B(1) == A(1)` stays `True` if `B` lacks the
   methods, so every class gets them). A runtime `eq` would fix only `=`, not Python's
   `==` inside `in`, `find`, `index-of` and map keys; a frozen dataclass needs a
   decorator.
13. **`Any` and the variables it meets** ([[B132]]): decided here (bind them to `Any`),
   or with [[B18]] in `collections`? **Proposed: tests here, the decision with
   [[B18]],** since what `Any` does is that branch's.
   **Decided (2026-11-02): here, a third way:** a variable stays free while checking,
   and one that met `Any` and nothing else is defaulted to `Any` at the end (`node-type`),
   as gradual type inference treats the dynamic type (Siek and Vachharajani, 2008); one
   that met nothing (`(put empty-list)`) stays a variable, Question 3's error. Binding
   it to `Any` at once was the other way, losing a later, more precise use. `show` on a
   value typed `Any` is the run-time show, part of [[B18]]'s leak; [[B18]] keeps only
   using `Any` less. In step 1, with [[B132]]'s tests.
14. **Order of the steps:** `show` early (proposed: it unlocks the spec for every later
   step's examples), or `Maybe` first (the biggest change)? **Proposed: as listed.**
   **Decided (2026-11-02): as listed.** Between steps 2 and 4 a `Maybe` is still
   `t | None` in Python, but `show` picks by static type, so it prints `(Some …)` or
   `None` from step 2 on and step 4 changes no example's output (only `(Maybe (Maybe
   t))` would show wrong in between, and nothing uses it).
