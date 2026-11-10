# Collections (HLD)

**Status: accepted (2026-11-07); proposed 2026-11-07, for branch `collections`. Epic: `python_complete.md`
(its third branch). After tag `semantics-2`.** The operators get types a program can
write, and so can be values and be used by a generic function; a function can take any
number of arguments of one type; lists, tuples and strings each get their own typed
operations, in place of `Any`; and the translator's list loops move onto the list
operations. Much was decided in the epic (its Questions 4, 9, 11 and 12, 2026-10-30) and
is carried over, not reopened; this HLD surveys today's source, settles what the epic
left to it (the spellings, the list literal, `Collection`), and orders the steps.

## Where things stand

Counts from today's source (2026-11-07, after tag `semantics-2`): the translator
(`src/cdy/`, 5,495 lines), counted on its typed Core (each call by its argument's or
result's type), and the spec's and test programs' text.

| Item | Today | Seen where |
|---|---|---|
| [[B124]] the operators polymorphic, programs not | `infer-op` in `check.cdy`, with step 1's kind lists (`INTEGERS`, `FLOATS`, `NUMBERS`, `ORDERED`) | `+`: 150 on lists, 116 on numbers, 78 on strings; the spec and tests 89 |
| [[B48]], [[B99]] no variadic types | the operators are `(op + variadic)` in `special.cdy`, with no type; `put`, `print`, `display` typed `Any` | 16 operators |
| [[B38]] operators aren't values | `(fold + 0 xs)` is an error | — |
| [[B135]] an operator's error at the call | `(+ x "b")` reported at `(+`, not at `"b"` | — |
| [[B34]], [[B18]] no `Collection` | `len`, `at`, `slice`, `in` take `Any` | `at`: 364 on lists, 277 on tuples (264 a pattern's), 20 on strings, 47 on `Any`; `len`: 341 lists, 26 strings; `slice`: 22 strings, 4 lists; `in`: 17 on a `tup` written in place, 10 lists, 6 strings |
| [[B152]], [[B17]], [[B29]] `tup` and lists | `tup` makes a tuple the checker accepts as a list (`checking.tup-lists`) | 181 `tup`s in the translator, 48 in the spec and tests; 13 `List`s written |
| [[B123]], [[B69]] the translator's loops by hand | `defn`s with an `acc` argument, each a copy per item | 124 such `defn`s; `map` 26, `fold` 15, `any` 7, `filter` 3; `(+ acc (to-list x))` most of the 150 list `+`s |
| [[B16]] `format`'s holes | a special form reading its holes from the string | 162 `format`s |

`Any` is written 52 times in the translator: `system.cdy`'s 17 are `print`, `display`,
`put`, `len`, `at`, `slice`, `in`, `is-coll`, `is-str`, the regular expressions (a host
type, [[B49]], `library`'s) and the macro runtime (`load-macros`, `call-macro`,
`Macro`'s `run`, `host-macros`').

## Goals

- **Every operator has a `sig`** (`system.cdy`), with constraint variables for what it
  takes, so a generic function can use it, it can be a value, and its errors are at the
  argument ([[B124]], [[B38]], [[B135]], [[B48]]).
- **Rest parameters:** a function of any number of arguments of one type, written by a
  program too ([[B99]]).
- **`++` appends,** `+` adds: a list's append shows in the code (the epic's Question 4).
- **No `Any` in a collection's operations:** lists, tuples and strings each typed
  ([[B34]] *for now*, [[B18]] cut down).
- **Tuples are tuples:** `tup` gone for `Tup` and `List`, `checking.tup-lists` gone
  ([[B152]], [[B17]], [[B29]]'s `tup` part).
- **The translator on the list operations,** with `map-acc` ([[B123]], [[B69]]).

## Not goals

- **Interfaces** ([[B34]]'s fix): after the epic, in an HLD of their own (the epic's
  Question 4). Constraint variables are fixed sets of built-in types; a program can't
  add one, nor add a type to one.
- **Overflow, `Float`'s size** ([[B22]]), **mutation** (a list's append stays a copy;
  `map-acc` and the others make it rare, not cheap): `porting-surface` and
  `mutation_optimization.md`.
- **Maps' own literal and operations** beyond `len`: `library`'s.
- **Qualified names** (`string/len`): `namespaces`, next; this branch's names are
  prefixed (`str-len`) and rename then.

## Proposal

### Constraint variables

As decided in the epic (its Question 4, Elm's design): a type variable named for a
constraint takes only the types the constraint lists, *lasting* (until interfaces):

| Variable | Takes | Used by |
|---|---|---|
| `number` | `Int`, `Long`, `Byte`, `Float`, `Double` | `+`, `-`, `*` |
| `integer` | `Int`, `Long`, `Byte` | `quot`, `mod` |
| `float` | `Float`, `Double` | `/` |
| `comparable` | the numbers, `String`, `Char` | `<`, `>`, `<=`, `>=` |
| `appendable` | `String`, `(List a)` | `++` |

`integer` and `float` are Candy's beyond Elm's three (Elm has two number types), and are
step 1's kind lists of `semantics-2` given names. A second, independent variable of one
constraint is numbered, as in Elm: `number2`, `comparable2`. A program's own `sig` can
use them: `(sig sum (Fn ((List number)) number))`. `=` and `!=` take any type but a
function's (`semantics`' Question 12), as now. The checker's `infer-op` and its kind
lists go: an operator is checked as any call, argument by argument ([[B135]]).

### Rest parameters

The epic's Question 9: a typed rest parameter, of one type, the rest arriving as a
list; currying stays dropped. The spelling is this HLD's (Question 1): `(Rest t)`, a
type form, last in a `Fn`'s arguments, *lasting*. It names the item's type, as the
callers write it; in the body the parameter is a `(List t)`. The parameters carry no
marker: every top-level `defn` has its `sig`, which says which parameter is the rest.

```candy
(sig sum (Fn (Int (Rest Int)) Int))                  ; one Int or more
(defn sum (first rest) (fold + first rest))          ; rest is a (List Int)
(sig count-all (Fn ((Rest String)) Int))             ; zero or more
(defn count-all (names) (len names))
(sig + (Fn (number number (Rest number)) number))    ; two or more, in system.cdy
```

`(sum 1 2 3)` binds `first` to `1` and `rest` to `(List 2 3)`; `(sum)` is an error (at
least one argument), and so is `(sum (List 1 2))`: a list isn't spread (no `apply`, *for
now*). Each argument from the rest on is checked against `t`, and its error is at that
argument. In Python, `def sum(first: int, *rest: int)`. `(Rest t)` anywhere but last is
an error in the type (`check-type`), and outside a `Fn`'s arguments too. A `fn` can't be
variadic, having no `sig` to say so (*for now*: [[B169]]). Used as a
value, a variadic function is the function of its arguments before the rest: `+` is a
`(Fn (number number) number)`, `sum` an `(Fn (Int) Int)`.

`and` and `or` stay special forms (they don't evaluate every argument); `not` is a
one-argument function. `tup` and `put` aren't rest parameters (mixed types): `tup` goes
(below), and `put` becomes a macro.

### Operators as values

An operator used as a value is its two-argument function: `(fold + 0 xs)`, where `+`
is a `(Fn (number number) number)` ([[B38]]). Python spells each value as a runtime
function (`cdy_rt.primitives.add`), and a call as now (`a + b`).

### `++` and `+`

`++` appends strings and lists, `appendable`; `+` adds numbers only, *lasting* (the
epic's Question 4). The translator's 228 `+`s on lists and strings become `++`, by a
script reading each `+`'s type from the checker, as in the epic's estimate; most of the
list ones are `(+ acc (to-list x))`, which `map-acc` and the others take away (step 7).
Two boot steps: `++` into `bin`, then the translator's uses.

### Lists, tuples and strings

A collection's operations are typed by what they take, *for now* until interfaces
([[B34]]; Question 2):

- **Lists:** `len`, `at`, `slice` and `contains` take a `(List a)`; `in` goes for
  `contains` (its 17 uses on a `tup` written in place become a `List`).
- **Strings:** `str-len`, `char-at` (a `Char`, so a `Char` read from a string is no
  longer `Any`, [[B18]]), `substring` and `str-contains`; `namespaces` renames them
  (`string/len`). The reader's 20 `at`s on strings compare `Char`s.
- **Tuples:** taken apart by a pattern only, *lasting*: no `at` on a `Tup` (13 in the
  translator), since its result type depends on the index; `len` on a tuple is its
  type's. `checking.tup-lists` goes: a `(Tup Int Int)` isn't a `(List Int)`.
- **`tup`:** its 181 uses become `Tup` or `List`, as each means ([[B152]]), then `tup`
  goes, *lasting*, and with it `(special tup)` in `special.cdy`.
- **`Tup` and `List`:** `Tup` stays the analyser's own constructor, since its type is
  its number of items, which no `sig` can say; `List` becomes an ordinary built-in, `(sig
  List (Fn ((Rest a)) (List a)))`, zero items or more. (*As built,* step 1: `List`
  stays the analyser's constructor, *for now*: [[B171]].)
- **Maps:** `map-size` for `len`.

`is-coll` and `is-str` are the translator's (forms read as `Any` before `Form`, [[B79]]);
they go if nothing uses them, or stay `Any` *for now*.

### The list literal

`semantics` made the type's name the constructor: `(List 1 2 3)` is a list, and a
literal's job is done. The question left (Question 3) is sugar: `[1 2 3]` for `(List 1
2 3)`, as Clojure's vector. Proposed: **no sugar in this branch,** *for now*: brackets
are better decided with the map's literal and the reader macros (`'`), and the
constructor reads plainly.

### `put` and `format`

`put` becomes a prelude macro over a typed `text` built-in (`show`, but a `String` or
`Char` as its text), `(put a b)` to `(put-line (++ (text a) " " (text b)))`, so `put`,
`print` and `display` lose `Any` ([[B48]]). `format` stays a special form, typed by the
checker as now, *for now* (Question 4): a macro would have to read its holes from the
string, which is the reader's job ([[B16]]), and macro code doesn't get the prelude
([[B52]]); both are `host-macros`'.

### The list operations

`map-acc`, a `map` threading a state, `(Fn ((Fn (s a) (Tup s b)) s (List a)) (Tup s
(List b)))`, as the epic's Question 11 decided; and `reduce`, which it left for when
`Maybe` was decided, `(Fn ((Fn (a a) a) (List a)) (Maybe a))`. The translator's
`acc` loops move onto `map`, `filter`, `fold`, `any`, `find` and `map-acc` where each is
one of them ([[B123]]); most of its quadratic copies go with them ([[B69]]).

### The spec

| Rule | File | Step |
|---|---|---|
| `types.table`, `types.sig`, `expr.rest` (new; *as built*, for `expr.functions`): rest parameters, `(Rest t)` | `20-types.md`, `40-expressions.md` | 1 |
| `checking.constraints` (new): the constraint variables; `checking.operators` rewritten as `sig`s; `checking.generics` | `25-checking.md` | 2 |
| `expr.arithmetic`, `expr.comparisons`: the operators' `sig`s; as values | `40-expressions.md` | 2, 3 |
| `expr.append` (new): `++`; `+` numbers only | `40-expressions.md` | 4 |
| `types.tuples`, `checking.tup-lists` (goes), `match.tup` | `20-types.md`, `25-checking.md`, `30-match.md` | 5 |
| `library.lists`, `library.strings`, `library.bounds`, `library.builtins`: the typed operations | `60-library.md` | 6 |
| `library.put` (new): `put` a macro over `text` | `60-library.md` | 6 |
| `library.lists`: `map-acc`, `reduce` | `60-library.md` | 7 |

## Pros and cons

- **For:** the last of the operators' special rules go, which a second target would
  otherwise need the checker's types for (`+` on a Rust `Vec`); `Any` leaves the
  collection operations, the translator's commonest calls; generic code can add and
  compare; the translator's loops get shorter and lose their quadratic copies.
- **Against:** the most churn of the epic so far: 228 `+`s, 181 `tup`s, 20 string
  `at`s, about 124 loops, each a boot step or two; prefixed string names that
  `namespaces` renames soon after. The checker's unification grows a constraint on a
  type variable (a mark, as `Any` is).
- **Timing:** `namespaces` is independent and could go first (the epic's Question 2),
  which would spell the string operations `string/len` at once; proposed after, as the
  epic orders it, since this branch is about types and `namespaces` about names.

## Bootstrap

Each step that changes `src/cdy/` rebuilds `bin`, one `boot/NN` each (from `boot/57`).
Two need two: `++` (step 4: the operator into `bin`, then the translator's uses), and
the typed collection operations (step 6: the new names into `bin`, then the translator
onto them, then the old names out). A step that changes `system.cdy` or the prelude
stages the library next to `bin` before building.

## Steps

1. **Rest parameters** ([[B161]]; [[B99]]): `(Rest t)` in a `Fn` type, last; the checker (the
   arguments from the rest on, each against `t`; as a value, the arguments before it)
   and emit (Python's `*rest: T`); `List` a built-in over it.

   *Done (2026-11-08). As built:* `(Rest t)` is a type form (`analyse-type`), held as a
   `TCon "Rest"`, so no other part of the translator needs a new kind of type; a `sig`'s
   type may end its function type's arguments with one (`check-sig-type`), and anywhere
   else it is an error (`check-type`: a field, a nested `Fn`, a value's type), as is a
   `def` with a variadic type. The checker reads a call's callee with its rest
   (`infer-callee`), spreading the item type over the arguments from there on
   (`spread-rest`), with "takes at least N argument(s)" when too few; a name used as a
   value loses it (`as-value`); in the body the parameter is a `(List t)`
   (`body-types`). A built-in's call checks the same arity in `core.cdy`
   (`check-call`), for those to come. Python writes `*name: T` (`emit-param`). A
   variadic `defn` isn't made a loop (`lower-top`): its self call would rebind the rest
   from a list. `List` stays the analyser's constructor, *for now* ([[B171]], the
   owner's choice): an ordinary built-in needs one built-in name to be a type and a
   value, which the built-ins map and `spelling.py` can't hold, and its value would be
   only an `(Fn () (List a))` by the value rule. The spec: `expr.rest` (new),
   `expr.tail-calls`, `types.table`, `types.sig`, `types.constructors`. One boot step,
   `boot/57`.
2. **Constraint variables and the operators' `sig`s** ([[B162]]; [[B124]], [[B135]], [[B48]]):
   `number`, `integer`, `float`, `comparable`, `appendable` in the checker; the
   operators move from `(op ...)` to `system.cdy` `sig`s, `infer-op` goes.
3. **Operators as values** ([[B163]]; [[B38]]): the runtime's functions, emit's spelling.
4. **`++`**, and `+` on numbers only ([[B164]]): two boot steps, a script rewriting the
   translator's `+`s by type.
5. **Tuples** ([[B165]]; [[B152]], [[B17]], [[B29]]'s part): `tup` to `Tup` or `List`,
   `checking.tup-lists` gone, `at` on a tuple an error, then `tup` gone.
6. **Typed collection operations** ([[B166]]; [[B34]] *for now*, [[B18]], [[B48]]): lists',
   strings' and maps' own operations, `in` gone, `put` a macro over `text`; two boot
   steps. *Checkpoint* (as `semantics`' Question 1): merge here, and do step 7 as
   `collections-2`, or go on.
7. **The list operations** ([[B167]]; [[B123]], [[B69]]): `map-acc` and `reduce`, and the
   translator's loops onto them, file by file, measured (the build's time).
8. **Docs** ([[B168]]): CLAUDE.md, the epic's third branch *done*, `multi_target.md` (the operators'
   types, constraint variables), the iMVP doc's operator rows; "Looking back".

## Questions

1. **A rest parameter's spelling:** `&` in the type and the parameters (`(Fn (Int &
   Int) Int)`, `(defn sum (first & rest) ...)`, as Clojure's `&`); `...` after the type
   and the name (`(Fn (Int Int ...) Int)`, `(defn sum (first rest ...) ...)`, as the
   epic wrote it); or `&rest` (Common Lisp)? **Proposed: `&` in both,** one marker,
   read before the name or type it marks, *lasting*.
   *Answer (2026-11-07, the owner): `(Rest t)` in the type, and no marker in the
   parameters,* *lasting*: the `sig` already says which parameter is the rest, so a
   marker would say it twice. Weighed on the way: `&` followed by the list's type
   (`(Fn (Int & (List Int)) Int)`, the type the body sees, as TypeScript's), which needs
   a rule that after `&` the type is a list; `&` followed by the item's type, which reads
   as two `Int`s; `((List Int))`, which is a list argument, not a variadic one; and
   `(& Int)` or a keyword (`(vari Int)`), the wrapping form chosen, Capitalised as type
   forms are (a lowercase name is a type variable). The cost: a `fn` can't be variadic,
   *for now*.
2. **`Collection`:** typed operations per collection, *for now* until interfaces
   (proposed: `len`, `at` on lists, `str-len`, `char-at` on strings); a built-in
   constraint variable `sequence` for lists and strings (but `at`'s result, an item or a
   `Char`, then depends on which, which a constraint variable can't say); or `Any` kept
   for them, *for now*? **Proposed: per collection,** since they are the translator's
   commonest calls and the one place `Any` hides real types.
   *Answer (2026-11-07, the owner): per collection,* *for now* until interfaces
   ([[B34]]).
3. **The list literal:** `[1 2 3]` as sugar for `(List 1 2 3)` now, or none in this
   branch, decided with maps and reader macros? **Proposed: none now,** *for now*, an
   `idea` item for brackets with the map literal.
   *Answer (2026-11-07, the owner): none now,* *for now*; [[B170]].
4. **`format`:** stays a special form, typed as now, *for now* ([[B16]], to
   `host-macros`), or becomes a macro here? **Proposed: stays;** `put` becomes a macro.
   *Answer (2026-11-07, the owner): `format` stays a special form,* *for now* ([[B16]]);
   `put` becomes a prelude macro over `text`.
5. **The checkpoint:** merge after step 6 and do the loops (step 7) as `collections-2`,
   or one branch? **Proposed: decide at the checkpoint,** as `semantics` did; step 7 is
   the translator's own (X), and the language is settled by step 6.
   *Answer (2026-11-07, the owner): decide at the checkpoint.*
6. **The string names:** prefixed (`str-len`, `char-at`, `substring`, `str-contains`)
   until `namespaces` gives `string/len`, or `namespaces` first, so they are spelled
   once? **Proposed: prefixed, `namespaces` after,** as the epic orders it; the rename
   is mechanical.
   *Answer (2026-11-07, the owner): prefixed, `namespaces` after.*
