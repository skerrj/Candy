# Semantics, part 2 (HLD)

**Status: accepted (2026-11-06; proposed 2026-11-04), for branch `semantics-2`. Epic: `python_complete.md`
(its second branch, continued). After tag `semantics`.** Steps 6 to 9 of
`semantics.md`, moved here at its checkpoint (its Question 1): numbers, `at` and
`slice`, a `def`'s order, and errors. Their design was decided there (its Questions 4,
5, 9, 10 and 11, 2026-11-01 and 2026-11-02) and is carried over, not reopened; this HLD
adds a fresh survey, the order of the steps, and which of the items `semantics` found
come along.

## Where things stand

Counts from today's source (2026-11-04, after tag `semantics`): the translator
(`src/cdy/`), its test programs (`tst/cdy/`) and the spec's examples.

| Item | Today | Seen where |
|---|---|---|
| [[B23]] `/` is true division | `(/ 7 2)` is `3.5`, a `Double` | translator 0; the spec 2 (`expr.arithmetic`, `checking.operators`) |
| [[B22]] unbounded integers | `Int`, `Long`, `Byte` are Python `int`s; `300b` is accepted; a `Float` is 64 bits | byte literals: the spec 7, all in range |
| [[B35]] `at` and `slice` are subscripts | a negative index counts from the end; an out-of-range `slice` is cut short | translator: `at` 483, none negative (the 4 `semantics.md` counted are gone); `slice` 37 |
| [[B71]] the `at` and `slice_` helpers | used only when `at` or `slice` is a value | — |
| [[B31]] a value used before its `def` | Python's `NameError` when run | — |
| [[B39]] `fail` stands in for errors | raises `CandyFail`; nothing catches it in Candy | translator 130 |

Found by `semantics` (open, `low`), each a candidate here (Question 1): [[B150]] (a
function inside a record is found by `show` only when run), [[B151]] (a float with no
Candy literal, `1e+20`, shown as Python writes it), [[B152]] (`tup` and `Tup` one form),
[[B153]] (`<` and the other orderings Python's on records, lists and `Bool`s; on `nil`
a failure when run), [[B156]] (a macro's errors in its expansion's words).

## Goals

- **Each borrowed meaning in the table decided in the spec** and done by the Python
  target, as `semantics.md` decided it.
- **No negative index, and no silent cut,** anywhere a program can see.
- **`fail` a panic, and `Result` for expected failure,** in the prelude.

## Not goals

What `semantics.md` ruled out stays out: types for the untyped built-ins and `Any` cut
down (`collections`), mutation, the translator's `fail`s turned into values. Also:

- **Overflow** in arithmetic (trap or wrap) and a 32-bit `Float` on Python: *for now*,
  [[B22]], for `porting-surface`.
- **A second form of `at` giving a `Maybe`:** left until one is needed (`semantics.md`,
  Question 9).

## Proposal

As decided in `semantics.md`, "Proposal" (each heading there):

- **Numbers** ("Numbers"; its Questions 4 and 5): `/` on `Float` and `Double` only,
  giving the same type, *lasting*; `mod` beside `quot` for the integers, both rounding
  down (`a` = `b`·`(quot a b)` + `(mod a b)`, the result with `b`'s sign). `Byte` 8 bits
  unsigned, `Int` 32 and `Long` 64 signed, `Float` 32 and `Double` 64, *lasting*; a
  literal out of its type's range is an error when translated (`300b`).
- **`at` and `slice`** ("`at` and `slice`"; its Question 9): `(at xs i)` needs `0 <= i <
  (len xs)`, `(slice xs i j)` needs `0 <= i <= j <= (len xs)`, else a panic, *lasting*.
  In Python, a checked helper, except `at` on a literal index that can't be negative
  (`(at xs 0)` stays `xs[0]`: Python's `IndexError` covers the high side, as a panic).
  The helpers replace [[B71]]'s. The translator has no negative index left, so one boot
  step does (`semantics.md`, "Bootstrap", planned two).
- **`def` order** ("`and`, `or`, `Char`, `def`"; its Question 10): a top-level value's
  initial value may use only the values defined before it, directly or through the
  functions it calls, a `fn` written in it counted as called; a cycle is the same
  error, `x is used before its def`. Functions still call each other in any order.
- **Errors** ("Errors"; its Question 11): `fail` is a panic, *lasting*: the program stops
  with the message, and Candy can't catch it. `(deft (Result a e) (Ok ((v a))) (Err ((err
  e))))` in the prelude, taken apart with `match`. No exceptions. The translator keeps
  its `fail`s; a `catch-panic` for tools is [[B139]]'s.

### The spec

The rules each step changes or adds (`semantics.md`, "The spec", for steps 6 to 9):

| Rule | File | Step |
|---|---|---|
| `expr.arithmetic`: `/` on floats, `mod` beside `quot` | `40-expressions.md` | 1 |
| `checking.operators`: `/` a float's, `mod` an integer's | `25-checking.md` | 1 |
| `syntax.numbers`, `types.table`: the sizes, a literal's range an error; overflow and `Float` *for now* ([[B22]]) | `00-syntax.md`, `20-types.md` | 1 |
| `library.bounds` (new): `at` and `slice` out of range a panic, negative indexes too | `60-library.md` | 2 |
| `programs.def-order` (new): a value used before its `def`, directly or through a call | `10-programs.md` | 3 |
| `library.errors` (new): `fail` a panic; `Result` | `60-library.md` | 4 |
| `programs.prelude`: `Result` in it | `10-programs.md` | 4 |

And the found items Question 1 takes: [[B153]] `expr.comparisons` (step 1), [[B151]]
`library.show` (step 1), [[B150]] `library.show` and `expr.equality` (step 2).

## Pros and cons

- **For:** each step is small and decided; the epic's next branch, `collections`,
  builds on `/`, `at` and `Result` (typed rest parameters, the list operations), and
  the spec's runner (`test-runner`) needs a panic it can tell from a type error.
- **Against:** `at`'s check costs on every index the translator writes (483); step 2
  measures it. A panic can't be caught, so a tool that runs Candy in-process (the
  macros, the spec's runner) depends on [[B139]] or a process per run.
- **Timing:** now, while `semantics`' context is fresh; nothing waits on another branch.

## Bootstrap

Each step that changes `src/cdy/` rebuilds `bin`, one `boot/NN` each (from `boot/53`).
The translator writes no `/` and no negative index, so no step needs two. A step that
changes `system.cdy` or the prelude stages the library next to `bin` before building
(`semantics.md`, "Looking back").

## Steps

1. **Numbers** ([[B145]]; [[B23]], [[B22]]): `/` on floats, `mod`, literal ranges; with Question
   1's [[B153]] and [[B151]].

   *Done (2026-11-06). As built:* `infer-op` (`src/cdy/check.cdy`) gives `/` a float
   type (`FLOATS`), `quot` and `mod` an integer type (`INTEGERS`), and the orderings a
   number type, `String` or `Char`, each `needs-kind`'s error (`/: expected a Float or
   Double, got Int`); `mod` is declared in `special.cdy` and spelt `%` in `spelling.py`.
   The reader (`read.cdy`) checks a literal's range in `number-form` (`number-range`, the
   bounds written as `to-int` and `to-float` of strings, so that the translator's own
   source has no literal it can't read), a parse error `300b is out of range: a Byte is 0
   to 255`; and reads an exponent (`exponent-end`: `e`, an optional `-`, digits, after
   the fraction), so [[B151]]'s fix is `show_float` (`primitives.py`) writing Python's
   `1e+20` as `1.0e20`. Infinity, not-a-number and `(/ 1.0 0.0)`, which fails on Python,
   are a new item, [[B158]]. The spec: `expr.arithmetic`, `expr.equality`,
   `checking.operators`, `syntax.numbers` (the sizes, now with a run example and the range
   errors), `types.table` and `library.show`; [[B22]] is reworded to what remains. One
   boot step, `boot/53`: the translator used no `/`, no `quot` on a float and no
   ordering on anything but numbers and strings.
2. **`at` and `slice`** ([[B146]]; [[B35]], [[B71]]): bounds checked, the cost measured on the
   translator's build; with [[B150]].
3. **`def` order** ([[B147]]; [[B31]]).
4. **Errors** ([[B148]]; [[B39]]): `fail` a panic, `Result` in the prelude.
5. **Docs** ([[B157]]): CLAUDE.md, `semantics.md` (a pointer to here), the epic's second branch
   *done*, `multi_target.md` (sizes, panics); "Looking back".

## Questions

1. **The found items:** which of `semantics`' come along? [[B153]] (orderings: restrict
   `<` and the rest to numbers, `String` and `Char` for now, the rest an error, until
   interfaces), [[B151]] (a float shown as its literal, `1.0e20`), [[B150]] (`show` and
   `=` refusing a record with a function field when translated) are each small and
   about what a value means. [[B152]] (`tup` and `Tup`) is `collections`' (the list
   literal and tuple types); [[B156]] (a macro's error messages) a macros question.
   **Proposed: [[B153]], [[B151]] and [[B150]];** [[B152]] and [[B156]] stay.
   *Answer (2026-11-06, the owner): as proposed.*
2. **The tasks:** reuse [[B145]] to [[B148]], retitled "semantics-2 step N", with a new
   task for the docs step; or close them as moved and open new ones? **Proposed: reuse,
   retitled,** their notes saying where they came from. *Answer (2026-11-06, the
   owner): as proposed;* the docs step is [[B157]].
3. **`at`'s cost:** if the checked `at` makes the translator's own build noticeably
   slower, keep it, or check only where the index isn't a literal or a loop's counter?
   **Proposed: measure in step 2, and decide there** with the numbers (the literal case
   is exempt already). *Answer (2026-11-06, the owner): as proposed.*
