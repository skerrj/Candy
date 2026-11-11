# Collections (HLD)

**Status: done (2026-11-10), steps 1 to 6 and the docs (tag `collections`); step 7 goes
to `collections-2` (Question 5's checkpoint). Accepted 2026-11-07, with the answers to its
questions (tasks [[B161]] to [[B168]]); proposed 2026-11-07, for branch `collections`. Epic: `python_complete.md`
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

*As built (step 4):* `++` and its uses were one boot step, not two (step 4's note): a
built-in is the library's, so a staged library is enough. *As built (step 2):* the other
way round too: a step's check runs the translator before
it with the step's own library, so a library that translator can't read needs `old-library`
staging (`script/bootstrap.py`: the parent step's library next to it), or two steps if
`src/` needs the new library as well. Step 2's operator `sig`s were the first (`boot/58`).
`test_newest_step_reads_the_library` (`tst/py_cdy/test_bootstrap.py`) finds it before the
commit, and `bootstrap.py --tag` tags a step only once it passes.

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

   *Done (2026-11-09). As built:* the constraints are a table in `core.cdy`
   (`CONSTRAINTS`, `constraint-of`, shared with `emit`); a sig's `number2` is `number`'s.
   A fresh variable made from one is named `?N:number`, so `unify` stays a function of
   the substitution: binding one (`bind-constrained`) checks the type is one the
   constraint takes (a tuple as a list, for now), binds an unconstrained variable to it,
   and meets another constrained one at the narrower (`within`), or at the one type they
   share (`appendable` and `comparable` at `String`); a sig's own variable only if its
   constraint is within. A message shows an unsolved one as its constraint (`expected
   number, got String`). The operators are bodiless `sig`s in `system.cdy`, with rest
   parameters (step 1); `special.cdy` has only the special forms, `Op` is gone from
   `Builtin`, and `spelling.py`'s operator kinds are a typed built-in's (`OPERATOR_KINDS`).
   `and` and `or` are typed built-ins too, not special forms as this HLD said: their
   short-circuit was always `lower`'s, by name, so a `sig` costs nothing; as values they
   are step 3's question. `+` takes `addable` (the numbers, `String`, a list), *for now*,
   until `++` (step 4). `=` and `!=` are `(Fn (a a (Rest a)) Bool)`, with the function
   check after the call (`infer-compare`). In Python, `integer` and `float` are `int` and
   `float`, and the other constraint variables constrained type parameters
   (`[number: (int, float)]`). [[B124]] and [[B135]] are done (an error is at its
   argument), [[B48]] is the operators' part done. The spec: `checking.constraints`
   (new), `checking.operators` rewritten, `checking.generics`, `expr.arithmetic`,
   `expr.operator-arity`. The translator's build: 0.98 s to 1.00 s. One boot step,
   `boot/58`, staged `old-library` (Bootstrap, above).
3. **Operators as values** ([[B163]]; [[B38]]): the runtime's functions, emit's spelling.

   *Done (2026-11-09). As built:* each operator's `spelling.py` entry has a third field,
   `value`, the function it is as a value (`operator("+", "binop", "add")`: a primitive,
   `cdy_rt.primitives.add`), so `py-spellings` is a map of triples; `emit-prim` writes it
   for an operator used as a value, and a call is still Python's operator. The
   primitives are typed as the `sig`s, a constraint variable a constrained type variable
   (`def add[T: (int, float, str, tuple[Any, ...])]`). The checker needed nothing: since
   step 2 an operator's value has its type, the function of its arguments before the
   rest (step 1's rule). `and` and `or` are values too: their arguments are values
   already, so there is nothing to short-circuit. `=` and `!=` are values too, an `(Fn (a
   a) Bool)` that doesn't keep `a` off functions; not being values ([[B172]], dropped)
   closed nothing, since a generic function's `=` compares functions already, a defect
   found here ([[B173]]: an `equatable` constraint, later). The spec:
   `expr.operator-values` (new). One
   boot step, `boot/59`, no staging (the library change, `py-spellings`' type, is one
   `bin` reads: `test_newest_step_reads_the_library`).
4. **`++`**, and `+` on numbers only ([[B164]]): two boot steps, a script rewriting the
   translator's `+`s by type.

   *Done (2026-11-09). As built:* one boot step, not two: a built-in is the library's
   (`system.cdy`, `spelling.py`), not the translator's code, so `bin` (`boot/59`), with
   the library staged next to it, translates a `src/` that uses `++` (and needs no
   `old-library` staging: `test_newest_step_reads_the_library`). `++` is `(Fn (appendable
   appendable (Rest appendable)) appendable)`, spelled Python's `+`, its value
   `primitives.append`; `+` is a `number`'s, and `addable` is gone (the table, `emit`'s
   type parameters, `primitives.add`). The rewrite was a one-off script (not kept), which
   read each `+` call's type from the typed Core and wrote `(++` at its position: 233 of
   the translator's 349 `+`s (none of unknown type; one in a `format` hole, one at a
   line's end), 7 in `tst/cdy/`'s programs, and by hand the `quasi` lists' join
   (`join-parts`, macro code, unchecked) and one in a macro file; the spec's by hand. The
   editor grammar highlights `++` (and `quot`, `mod`). The spec: `expr.append` (new),
   `expr.arithmetic`, `expr.operator-values`, `checking.operators`, `checking.constraints`,
   `checking.generics`, `checking.locals`, `checking.definitions`, `checking.order`,
   `checking.maybe`. One boot step, `boot/60`.
5. **Tuples** ([[B165]]; [[B152]], [[B17]], [[B29]]'s part): `tup` to `Tup` or `List`,
   `checking.tup-lists` gone, `at` on a tuple an error, then `tup` gone.

   *Done (2026-11-09). As built:* the translator's 203 `tup`s became `Tup`s, then, with
   the checker strict (`accepts` is `unify`: `accepts-each`, `as-list`, `tup-list-type`
   and `join-types`' and `bind-constrained`'s tuple branches gone), the 43 that were lists
   became `List`s, found by one-off scripts (not kept) from the typed Core: 27 where a
   `(List t)` is typed, 15 passed to `in` (an `Any`), one by hand; the tests' and the
   spec's likewise. `at` on a tuple is an error (`check-at`: "at doesn't take a tuple, a
   (Tup Int String): take it apart with a pattern"), the pattern's own read excepted
   (`is-tup-item`); the translator had 70 such `at`s, not 13, since its `tup`s were now
   `Tup`s too, mostly `infer-all`'s `(Tup (List CType) St)` and `unify`'s `(Tup Bool
   ...)`: all patterns now (`args-st` for a call whose arguments' types aren't needed). A
   `Tup` pattern on a typed value that isn't a tuple (a record, a function) is an error
   too, "a Tup pattern takes a tuple, not a P" ([[B17]]'s part). `tup` is gone, with
   `(special tup)` and the editor grammar's keyword. `checking.tup-lists` keeps its id
   (other docs link it), its rule now the opposite: "Tuples aren't lists", *lasting*.
   [[B175]] came along: `spelling-py`, `spelling-kind` and `spelling-value` in
   `core.cdy` read a spelling, where `emit` read it by position; `lower`'s `and`/`or`
   stay by name, since short-circuiting is the language's ([[expr.logic]]), not the
   spelling's. The spec: `types.tuples`, `checking.tup-lists`, `checking.match`,
   `match.tup`, `expr.let`, `library.zip`, `library.rest`, `library.maps`, and
   `programs.prelude`'s example. One boot step, `boot/61`.
6. **Typed collection operations** ([[B166]]; [[B34]] *for now*, [[B18]], [[B48]]): lists',
   strings' and maps' own operations, `in` gone, `put` a macro over `text`; two boot
   steps. *Checkpoint* (as `semantics`' Question 1): merge here, and do step 7 as
   `collections-2`, or go on.

   *Done (2026-11-10). As built:* `len`, `at` and `slice` take a `(List a)`; a string has
   `str-len`, `char-at` (a `Char`), `substring` and `(str-contains part s)`, a map
   `map-size`; `in` is gone (`contains` was there already). The translator's calls were
   renamed by a one-off script (not kept) from their argument's type in the typed Core,
   101 of them (`in` on a list to `contains`, the string ones to their names), and the
   nested `(at (at fields 0) 0)`s, which `at`'s `Any` had hidden, became patterns. The
   reader compares `char-at`'s `Char`s with `Char` literals (`\(`, `\;`); a newline has
   no `Char` literal, so it has `char-text`, the char as a `String` (`text`). `put` is a
   prelude macro, `(put a b)` to `(put-line (++ (text a) " " (text b)))`; `text` is
   written by its argument's type as `show` is (`text-of` in `emit.cdy`, and as a value),
   spelled `text_any` for a translator that doesn't; `print` and `display`, unused, are
   gone. Macro code isn't expanded, so it has `put-line` and `text`, not `put`. With
   `put`'s arguments now checked against `text`'s variable, an `if` checked against an
   unsolved variable is inferred instead, so its branches still say they differ.
   `check-at` (step 5) went: `at`'s type rejects a tuple. `char-at` and `substring` have
   their own primitives, so a panic names them. One boot step, `boot/62`, not two:
   `boot/61` reads the new library (no staging); the runtime keeps `in_`, which
   `boot/61` calls, until a following commit, which doesn't change `bin`. The spec:
   `library.builtins`, `library.bounds`, `library.strings`, `library.maps`,
   `library.format`, `library.put` (new), `syntax.chars`, `types.tuples`,
   `checking.narrowing`'s example, `checking.any`, `expr.calls`, `macros.macro-code`'s example.
7. **The list operations** ([[B167]]; [[B123]], [[B69]]): `map-acc` and `reduce`, and the
   translator's loops onto them, file by file, measured (the build's time).

   *Moved (2026-11-10):* to branch `collections-2`, with its task ([[B167]]), as the
   owner chose at Question 5's checkpoint, after step 6. [[B174]] (`to-list`) and
   [[B173]] (a generic `=` on functions) go with it, to be placed in its HLD.
8. **Docs** ([[B168]]): CLAUDE.md, the epic's third branch *done*, `multi_target.md` (the operators'
   types, constraint variables), the iMVP doc's operator rows; "Looking back".

   *Done (2026-11-10). As built, for steps 1 to 6:* CLAUDE.md's history (the branch, and
   `collections-2` next), the macros (`put`), the built-ins (an operator as a value) and
   the library (each collection's own operations, `text`); `python_complete.md`'s third
   branch, `multi_target.md`'s operators and the iMVP doc's "Operators" each get a
   *since* note. The spec files were already `stable`; their new rules came with their
   steps.

## Looking back

What steps 1 to 6 taught, and the costs a later branch will meet again:

- **`Any` hides code, not just types.** Each `Any` taken out found more behind it than
  "Where things stand" counted from the typed Core: 70 `at`s on tuples, not 13, once
  `tup`s were `Tup`s (step 5), and nested `(at (at fields 0) 0)`s once `at` took a list
  (step 6). A count made on a typed Core counts only what is already typed; the next
  `Any` cut down ([[B18]], the macro runtime, [[B49]]) will meet the same.
- **Renames from the typed Core work.** 203 `tup`s and 101 `len`/`at`/`slice`/`in` calls
  were renamed by one-off scripts reading each node's type, not by hand. The cost: the
  script runs the old translator, which needs the old runtime first on its path, since
  the new one has lost what the old one calls. [[B167]]'s loops will be moved the same
  way.
- **The runtime outlives `bin`'s calls.** A runtime function the new `bin` stops calling
  (`in_`) stays until the commit after its boot step, since the step before it still
  calls it; and a library the parent translator can't read needs `old-library` staging
  (step 2, `boot/58`), which this branch added to `bootstrap.py`, with `--tag` checking
  each new step first. Twice a step planned as two boot steps was one (steps 4 and 6):
  the library is read when the translator runs, so a new built-in costs a boot step only
  when the old translator can't read its declaration.
- **A generic built-in moves an error.** Checking `put`'s arguments against `text`'s type
  variable turned an `if`'s "the branches are Int and String" into one about `text`'s
  argument, until an `if` checked against an unsolved variable was inferred instead
  (step 6). Every generic built-in a macro expands into can do this, as `semantics`
  found for `cond`'s expansion ([[B155]], [[B156]]).
- **New built-ins take names programs use.** `text`, added in step 6, was the reader's
  parameter name, and a local shadows a built-in, so the call failed ("expected a
  function"). Every built-in added before `namespaces` risks this; `namespaces` is where
  it ends.

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
