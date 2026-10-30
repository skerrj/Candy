# Python complete (epic HLD)

**Status: proposal (2026-10-29), questions open. An epic: its steps are branches, each
with an HLD of its own; this one sets their order, their scope, and when the epic is
done.** Written after tag `type-checker`.

Candy runs on one host and writes one target, Python, and the backlog's 85 open items
mix what a second target needs with what only Python's backend does. This HLD sorts
them, and plans the branches that make the Python version *complete*.

**Complete** (a draft, Question 1): *the Python version is a solid push-off point to a
Rust target, and eventually a Rust host.* Nothing Candy relies on is Python's, so the
Rust target is a new backend and runtime, not a rework of the language, and the Rust
host is the translator built for that target. The exit test in "Goals" is how to tell.

## Where things stand

- **The translator** is self-hosting on Python, typed by its own checker since
  `type-checker` (mypy is a second check, [[B15]]). Its layers, forms → Core → the
  lowered IR → Python, are the target-independent pipeline `multi_target.md` asks for,
  but the types the checker infers aren't kept in Core.
- **Semantics borrowed from Python:** values print as Python shows them ([[B36]]), `=`
  is `==` ([[B27]]), `/` is true division ([[B23]]), `and`/`or` return an operand
  ([[B26]]), missing values are `None` ([[B20]], [[B21]]), `at` and `slice` are Python's
  subscripts ([[B35]]), integers are unbounded ([[B22]]), a `Char` is a `str`
  ([[B28]]), a value used before its `def` fails at run time ([[B31]]).
- **What a static target can't take:** `Any` ([[B18]]), the nested `fn`s typed `Any`
  ([[B19]]), the operators, `tup` and `put` with no Candy type ([[B48]], [[B99]]), host
  objects with none ([[B49]]), no `Collection` ([[B34]]).
- **Special forms standing in for missing features:** `tup` (no list literal, no tuple
  types, [[B17]], [[B29]]) and `format` (an f-string hack, [[B16]]).
- **Variadics, by special case:** the operators, `tup`, `put` and `format` take any
  number of arguments, as special forms or untyped built-ins; macros are variadic and
  untyped; a function can't be ([[B48]], [[B99]]).
- **Namespaces:** one per program, flat. Every top-level name of every module, every
  built-in and every macro is seen unqualified ([[B47]], [[B108]]); types and values share
  it ([[B40]]); a variant can take a macro's name ([[B11]]); Python's names are the
  module's stem and the name (`util__greet`), and the tests reach them so ([[B65]]).
- **Generics:** a `deft` takes type variables (`(deft (Box a) ((v a)))`, a generic sum
  `(deft (T a) (L ((v a))) (N))`), and a `sig` with type variables is a generic function
  (`(Fn (a a Bool) a)`, `checking.generics`): each use instantiates it, and inside its
  body a type variable is rigid. Python gets PEP 695 generics (`class Box[a]`, `def
  pick[a]`, `type T[a] = L[a] | N`), and a generic sum's `match` skips the typed
  temporary, since mypy loses the arguments in class patterns. What isn't there:
  - **let-polymorphism:** a `fn` bound by `let` has one type (`checking.locals`,
    [[B15]]);
  - **bounds:** a type variable takes any type, with no way to say "one with `+`"
    (`(+ x 1)` on an `a` is an error, `checking.generics`), so a generic function can't
    add or compare in order; that is interfaces' job ([[B34]], Question 4);
  - **but `=` and `format` take a type variable** (`(= x y)` and `"{x}"` on an `a`
    pass), because Python can compare and show anything: an unwritten bound, which a
    Rust target must make a real one (`PartialEq`, `Display`), or the checker must
    reject;
  - **higher kinds** (a type variable that takes arguments, `(f a)`), explicit type
    arguments at a call, and generic `fn`s inside a body: none, and none needed yet;
  - **variadic types** (a type over any number of types, as `Tup`'s): only `Tup`
    ([[B99]]).
- **The list operations:** `map`, `filter`, `fold` and the rest are built-ins, for speed
  (`library.md`: a host type's operations are the host's, *for now*). The translator
  hardly uses them: its list work is `acc` loops written by hand, kept *for now* until a
  `fn` is typed ([[B123]], [[B19]]), and building a list item by item is quadratic
  ([[B69]]).
- **Macros run on the host:** compiled to Python and run with `exec` ([[B41]]); their
  results aren't checked ([[B42]]); macro files are included, not imported ([[B45]]);
  templates aren't hygienic across modules ([[B46]]); macro code has no prelude
  ([[B52]]).
- **The library is one flat set:** `special.cdy` (the special forms and operators),
  `system.cdy` (every other built-in, typed; the runtime gives each a Python spelling),
  `prelude.cdy` (Candy on top, imported by every file), `prelude_macros.cdy`. Every
  file sees every built-in, unqualified ([[B108]], [[B47]]), the translator's own five
  among them ([[B50]]); some built-ins are Python's in disguise (regexes, [[B32]];
  `slurp`'s search, [[B54]]); I/O is thin wrappers ([[B95]]). There is no standard
  library beyond the prelude, and no place for a target's own built-ins ([[B97]]).
- **One implementation:** the spec runs through the translator only, so nothing tells
  Candy's semantics from Python's but reading ([[B101]]).
- **The tests are Python's:** pytest runs everything. `test_spec.py` reads the spec's
  fences (with `script/doc_links.py`) and runs each example through T1, mypy and T2;
  `test_self_host.py` runs the test programs (`NAME.cdy` against `NAME.out`) and checks
  the fixpoint. A Candy program can't test itself: there is no assertion, no test
  module, and a second host would have to port the runners.

## Goals

- **The exit test** (Question 1): the epic is done when
  1. the spec runs on two implementations, the Python target and an interpreter, with
     the same output;
  2. no item in the groups *borrowed semantics*, *static types* or *macros on the host*
     (below) is open, each fixed or decided *lasting*;
  3. the **porting surface**, what a new target or host must supply, is written down,
     specified, and small: the system built-ins, the runtime's primitives, the host
     built-ins;
  4. what only one target has lives in that target's extension modules, never in what
     portable code sees.
- **Typed Core:** every `Expr` has its type after checking, for every backend to read.
- **A layered library:** system, prelude, standard library, target extensions, each
  with its own rule for what goes in it (see "The library").
- **An interpreter**, in Candy, over Core: the second implementation, and what runs
  macros.
- **A start at testing in Candy:** a `test` module programs use to test themselves, and
  the spec's runner in Candy, so a new host runs the conformance suite without
  Python (see "Testing in Candy").

## Not goals

- **A Rust target or host.** Each is the next epic, after this one.
- **Performance**, beyond what keeps the suite fast ([[B37]], [[B69]] and the like stay
  where they are unless a branch needs them).
- **Mutation** (`doc/hl_rqmt/mutation_optimization.md`).
- **Replacing the hand-written reader** (but see Question 6, parsec in Candy).

## Proposal

### The groups

Every open item goes in one group (the full table is "The triage", at the end):

| Group | What | Before a second target? |
|---|---|---|
| **S** borrowed semantics | Candy's behaviour is Python's | yes: fix, or decide *lasting* |
| **T** static types | something a statically typed target can't express | yes |
| **M** macros on the host | macros depend on Python to run | yes, for a second host |
| **L** library | the system, the prelude, the standard library, target extensions | the layering, yes; each module as needed |
| **P** Python's backend | how Python is written, invisible in Candy | no: it stays in `emit` |
| **D** defects | wrong by Candy's own rules | any time, in any branch near them |
| **X** the translator's own | internals, tests, tools | any time |
| **I** ideas | not yet wanted | no, unless a branch takes one up |

### The library

The layers, from the bottom, and the revisit each needs:

1. **The special forms** (`special.cdy`): the language. A new target implements them
   in its backend. Revisit: which are special only for want of a feature (`tup`,
   `format`, the operators: [[B48]], [[B99]], [[B100]]).
2. **The system** (`system.cdy`): the built-ins a target or host supplies, each typed,
   each spelt by the runtime (`spelling.py`, `primitives.py` for Python). This is the
   porting surface, so it should be **small and portable**. Revisit:
   - what can be Candy moves up, to the prelude or the standard library (`with-default`,
     [[B51]]; much of the list and string set, once it can be written well: [[B69]]);
   - the translator's host built-ins (`load-macros`, `py-spellings`, ...) move to a
     declaration only the translator imports ([[B50]]);
   - what is Python's moves out, to the Python extension (regexes, [[B32]], [[B49]];
     `slurp`'s search, [[B54]]);
   - each built-in gets a spec rule, so the surface is specified, not just declared.
3. **The prelude** (`prelude.cdy`, `prelude_macros.cdy`): Candy every file sees without
   importing it. Kept small: what nearly every program uses. Revisit: macro code gets
   it ([[B52]]); a program carries only what it uses, and it is read once
   ([[B68]], [[B66]], [[B62]]).
4. **The standard library:** Candy modules imported by name, qualified (`(import
   string)`, `string/split`): `list`, `string`, `map`, `math`, `io`, `test`, perhaps
   `parse` (Question 6). It needs qualified imports (see "Namespaces") and is how the
   flat set is split ([[B108]]). The I/O refactor ([[B95]]) is the `io` module's design. Portable:
   written in Candy, over the system, so every target gets it for free.
5. **Target extensions:** a target's (or host's) own built-ins and modules, such as `py`
   (Python interop, opaque host types: [[B49]]) or, later, `rust`. A program that
   imports one isn't portable, and says so by importing it. Each target has its own
   `system` additions and spec files for them ([[B97]]). How a module picks a
   target's code, a module per target or reader conditionals as Clojure's
   (`multi_target.md`), is Question 5.

### The interpreter

A tree-walking interpreter over typed Core, written in Candy (so any host that runs
Candy runs it), using the system built-ins as the Python target does:

- **a second implementation:** `test_spec.py` runs every example on both, and a
  difference is a borrowed semantic found ([[B101]]: the spec becomes a conformance
  suite);
- **the macro runner:** macros are interpreted, not compiled to Python and `exec`ed
  ([[B41]], [[B70]]), which is what a second host needs from macros;
- **a REPL**, later, nearly for free.

It doesn't need to be fast: the suite's programs are small, and the translator stays
compiled.

### Testing in Candy

The tests' Python is the last of the host a second host would have to port, after the
runtime. A start, in two parts:

- **A `test` module** in the standard library: `check` (an assertion with a message and
  a position), `deftest` (a macro naming a test), and a runner that runs a module's
  tests and reports them, exiting non-zero on a failure. Programs and the standard
  library's own modules test themselves with it; the test programs' `.out` files stay
  for what is about output.
- **The spec's runner in Candy:** reading a spec file's fences (`candy run` with its
  `expect`, `candy error`, `candy errors`), running each example on the interpreter, or
  translating it and running the result, and reporting by `file:line`, as
  `test_spec.py` does. It needs Markdown read well enough for fences (a `string`
  module's work), the interpreter (to run an example without a Python process each),
  and errors as values, not only `fail` ([[B39]]), to catch an example's error.

pytest stays the driver for what is about Python (mypy on the translation, the
bootstrap chain, the fixpoint), and calls the Candy runners. Moving the rest (the test
programs, the backlog's and links' checks) waits for a second host to need it
(Question 8).

### `tup` and `format`

Both are special forms because Candy has no variadic functions, no list literal and no
tuple types ([[B48]], [[B99]], [[B29]]):

- a **list literal** and real **tuple types**: `tup` builds a tuple only, a list is
  written as a list, and the `Tup`-as-`List` rule (`checking.tup-lists`) goes;
  patterns take tuples apart properly ([[B17]]);
- **`format` as a macro** over string joining and a **`show` per type**, chosen by the
  checker from the hole's type: the same `show` is how values print in Candy's syntax
  ([[B36]], [[B28]]), so it needs typed Core.

Whether `+` and the comparisons stay special (one rule per type, as now), become
overloaded, or wait for interfaces ([[B34]]) is Question 4.

### Generics

What this epic does to them, and what it leaves:

- **The hidden bounds go** (`semantics`): `=` and `show` on a type variable are the
  borrowed semantics in generic form. Either the checker rejects them, as it rejects
  `+`, until interfaces come, or `=` and `show` are declared for every type, *lasting*,
  each target supplying them for every type it has (Rust: by deriving `PartialEq` and
  `Debug` on every Candy type). **Proposed: the second** (Question 12): every Candy value
  is data (no functions compared, no host objects shown, [[B49]]), so structural `=` and
  a `show` per type are always possible, and generic code needs them.
- **For Rust:** Candy's generics map onto Rust's (`struct Box<A>`, `fn pick<A>(...)`,
  `enum T<A>`), with the derived bounds above; no monomorphising needed in the
  translator. Values are immutable and shared, so a target clones or counts references
  (`Rc`) as it likes: a backend's business, not the language's.
- **Left:** let-polymorphism ([[B15]]), bounds as interfaces (Question 4), higher kinds.
  None blocks a Rust target; each is a feature for later.

### Variadics

What takes any number of arguments falls in two kinds:

- **One type for every argument:** `+`, `-`, `*`, the comparisons, `and`, `or`. A typed
  rest parameter covers them: `(Fn (Int ...) Int)`, the rest arriving as a list
  ([[B99]]). It maps to every likely target (Rust: a slice). It would let them be
  ordinary built-ins in `system.cdy`, with types ([[B48]]), but for `+` on several types,
  which is overloading (Question 4).
- **Mixed types:** `put`, `format`, `tup`. A rest parameter can't type them. `put` and
  `format` need a `show` per argument's type, so they become macros over a typed `show`
  (see "`tup` and `format`"); `tup`'s type is its arity, so it stays a special form, or
  becomes literal syntax. Rust draws the same line: no variadic functions, and
  `println!` is a macro.

A user's `defn` could take a rest parameter too (`(defn sum (& xs) ...)`), which is the
same feature. Against it: **currying** ([[B93]]): a curried type, and partial
application, need a fixed arity, so Candy has variadic functions or curried ones, not
both (Question 9). Clojure's `map` takes several lists (`(map + xs ys)`); with rest
parameters Candy's could, but it would need the function's arity to match the number of
lists, which a type can't say: `map2` or `zip` is the simpler answer.

### Namespaces

A design of its own, before the library is split, since the standard library and the
target extensions are modules found by name. What its HLD settles (Question 10):

- **Qualified names:** `string/split`, as Clojure's. `/` is the division operator, so
  the reader takes a lone `/` as the operator and `m/name` as a qualified name.
- **The import forms:** `(import m)` as now, an alias (`(import m :as s)`), chosen names
  (`(import m (split join))`), and what stays unqualified everywhere: the prelude, the
  operators, the special forms ([[B47]], [[B108]]).
- **Types and values:** one namespace, as now, or two, as Haskell's ([[B40]]). Variants
  are values named like types, so a type and a variant can't share a name in one
  namespace; with two, `(sig a A)` for a variant `A` is plainly an unknown type
  ([[B119]]).
- **Macros:** global to a program now; imported and qualified like values, or kept
  global ([[B11]], [[B45]]).
- **Shadowing:** a program's own definition of a built-in wins today ([[B50]]); whether
  that is *lasting*, and whether a local can shadow a global.
- **Fields:** `get` finds a field by its value's type (`checking.records`); fields
  aren't in any namespace, and stay so.
- **Private names:** export lists or a naming rule (`modules.md`, "After the MVP"), so a
  library module can have helpers.
- **Each target's names:** a target maps Candy's qualified names to its own (Python's
  `stem__name`, Rust's modules); the mapping is part of the porting surface, and the
  tests reach Candy names, not Python ones ([[B65]]).

### The list operations

`map`, `filter`, `fold`, `any`, `find` and the rest are built-ins, each a native
operation of the host (`functools.reduce`, `tuple(map(...))`): every target supplies
them, and every likely target has them natively (`brainstorm.md`: "optimized target
implementations"). That stays: they are part of the porting surface, and a target makes
them fast its own way. What changes in this epic:

- **The set:** `fold` is a left fold with a start value; there is no `reduce` (no start
  value, on a list that can't be empty), no right fold, and no `map-acc`, a `map` that
  threads a state (a counter, a scope) and returns it with the list, which many of the
  translator's loops are. Which to add is the `collections` HLD's (Question 11).
- **The translator on them:** once `fn`s are typed (`typed-core`), its `acc` loops can
  become `map`, `filter`, `fold` and `map-acc` calls ([[B123]]); that also takes most of
  them off the quadratic copies ([[B69]]).
- **Their types:** each takes a `(List a)` today; with `Collection` (Question 4) they
  would take any collection.
- **In the interpreter,** they are its built-ins too, so the interpreter and the
  Python target agree by sharing them, not by accident.

### The branches

Each is a branch with its own HLD, in this order (Question 2), the groups it closes in
brackets:

1. **`typed-core`:** the checker writes each `Expr`'s type into Core; nested `fn`s get
   their types ([[B19]]); the checker's own leaks as wanted ([[B120]], [[B121]],
   [[B122]]); whether mypy stays ([[B15]], Question 3). (T)
2. **`interpreter`:** the interpreter over Core; the spec runs on both; differences are
   recorded as S items, not fixed here. (S, found)
3. **`semantics`:** the borrowed semantics, one by one, the interpreter checking each:
   `show` and printing, `=`, `/`, `and`/`or`, `Maybe` and missing values, `at` and
   `slice`, numbers' bounds, `Char`, `def` order and constancy ([[B80]]), errors
   ([[B39]]); `=` and `show` on a type variable (Question 12). (S)
4. **`collections`:** the list literal, tuple types, variadics (typed rest
   parameters; `put` and `format` as macros), `Any` cut down to what is still needed,
   `Collection` (as Question 4 decides); the list operations' set, and the translator
   moved onto them ([[B123]]). (T)
5. **`namespaces`:** qualified names, the import forms, types and values, macros'
   names, shadowing, private names, each target's mapping. (L)
6. **`library`** (perhaps two branches: the layering first, then the modules): the
   system revisited, the prelude trimmed, the standard library's
   first modules, the I/O refactor, the target-extension mechanism and the `py`
   extension; the `test` module. (L)
7. **`host-macros`:** macros run on the interpreter; their results checked ([[B42]]);
   macro files as modules ([[B45]]); hygiene ([[B46]]); the macro leaks that remain
   ([[B43]], [[B44]]). (M)
8. **`test-runner`:** the spec's runner in Candy, on the interpreter, called from
   `test_spec.py`; the spec runs on both implementations through it. (X)
9. **`porting-surface`:** the per-target files (`system`, spelling, runtime, spec
   extensions) in a layout a second target fills in; the porting surface's own doc; the
   exit test checked. (L, P)

Defects (D) and the translator's own items (X) go into whichever branch is near them.

## Pros and cons

- **For:** the backlog gets an order and an end; each branch is the size the last ones
  were; the interpreter pays for itself three ways (conformance, macros, a REPL); the
  library gets a design before it grows, rather than after.
- **Against:** it is long, nine or more branches, before anything runs on Rust; some
  answers (interfaces, `Maybe` as a sum) may change many programs, the translator most.
- **Why now:** the type checker was what the rest waited on (typed Core, `show`, `Any`).
  And the longer the translator is the only big Candy program, the more of it is written
  against Python's semantics.

## Steps

1. **Accept this HLD,** with its triage; add to `doc/process.md` what an epic is (an
   HLD whose steps are branches; "Design docs"), and an `epic` reference from each
   branch's HLD back to it.
2. **The branches,** in order, each with its own lifecycle. This HLD gets a *Done* note
   per branch, and its triage is updated as items close or are found.
3. **The exit test,** checked in the last branch; the HLD becomes *done*.

## Questions

1. **What "complete" means, and its exit test:** "a solid push-off point to a Rust
   target, and eventually a Rust host" (the draft above), tested by the four conditions
   in "Goals"? Or less (no interpreter: the second implementation waits for Rust), or
   more (the standard library's modules written, not just designed)? **Proposed: the
   draft, and the four.**
2. **The order:** typed Core, the interpreter, semantics, collections, namespaces,
   library, host macros, test runner, porting surface? The library could come earlier (it is independent of
   typed Core but for `show`), and macros could move to the interpreter in its own
   branch. **Proposed: as listed**, since the interpreter finds the S items the
   semantics branch fixes.
3. **mypy:** keep it as a second check through the epic, or drop it once Core is typed?
   **Proposed: keep it** until `semantics` is done, then decide (it catches the
   backend's mistakes, which the interpreter doesn't).
4. **Overloading:** `+` on numbers and strings, `=` on everything, `Collection`: special
   rules per operator (as now), interfaces (traits, type classes), or plain
   per-type functions (`str-concat`)? Rust has traits, so interfaces map well, but they
   are a big feature. It is decided with variadics (Question 9): a variadic `+` on
   several types is overloading either way. **Proposed: special rules for now**
   ([[B34]]), and an HLD for interfaces of its own, after this epic.
5. **Target extensions:** a module per target (`py.cdy`, found in the target's library
   directory), or reader conditionals in one file? **Proposed: a module per target**:
   simpler, and a program says it isn't portable by importing it.
6. **parsec in Candy:** a parser-combinator module in the standard library (the reader
   stays hand-written), as a proving ground for generics and closures? **Proposed: yes,
   as `parse`, in the `library` branch's second half, if it is cheap there.**
7. **`Maybe`:** a real sum (`(Some x)`, `None`), changing programs, or `a | None` kept
   *lasting* with narrowing? It is the biggest S item ([[B20]], [[B21]]). **Proposed:
   decided in the `semantics` HLD**, with the interpreter's evidence.
8. **Testing in Candy: how far?** The `test` module only; or that and the spec's
   runner (the conformance suite, which a second host needs); or everything, pytest
   kept for the Python-only checks. **Proposed: the `test` module and the spec's
   runner**, the rest when a second host needs it. The spec's runner could move into
   `interpreter` (its first user), or wait for `library`'s `string` module; as listed
   it comes after both.

9. **Variadics or currying?** Typed rest parameters (`(Fn (Int ...) Int)`, user
   `defn`s with `&`), or curried types and partial application ([[B93]]), which need a
   fixed arity; not both. Partial application can be a macro or a `fn` either way.
   **Proposed: rest parameters**, of one type, in `collections`; currying dropped
   (*lasting*), `fn` covering partial application. `put`, `format` and `tup` are not
   rest parameters in any answer.
10. **Namespaces' scope:** a branch of its own before `library` (proposed), or the first
   half of `library`? And types and values: one namespace (as now) or two? **Proposed:
   its own branch; one namespace, *lasting*,** since the translator and the tests rely on
   it and two would make `A` mean two things; [[B40]] and [[B119]] become a rule and a
   message.
11. **The list operations:** add `map-acc` (a `map` threading a state), a right fold,
   `reduce` (no start value)? **Proposed: `map-acc` only**, as the translator's loops
   need it; `reduce` needs a non-empty list, which Candy can't type; a right fold isn't
   used.

12. **`=` and `show` on a type variable:** declared for every type, *lasting* (each
   target supplies structural equality and a printer for all its types), or rejected
   until interfaces come? **Proposed: declared for every type**, in `semantics`; the
   rest of a type variable's operations wait for interfaces.

## The triage

Every open item on 2026-10-29, by group; the branch is where it is expected to close.

| Item | Group | Branch |
|---|---|---|
| [[B15]] the checker is an MVP | T | `typed-core` |
| [[B19]] nested `fn`s typed `Any` | T | `typed-core` |
| [[B120]] `get` before a type is known | T | `typed-core` |
| [[B121]] no narrowing in a clause | T | `typed-core` |
| [[B122]] a leaf's error at its parent | X | `typed-core` |
| [[B59]] only symbols and lists carry positions | X | `typed-core` |
| [[B67]] the built-ins' types unused | X | `typed-core` (likely done already) |
| [[B101]] an interpreter | I → taken up | `interpreter` |
| [[B36]] values print as Python's | S | `semantics` |
| [[B27]] `=` is `==` | S | `semantics` |
| [[B23]] `/` is true division | S | `semantics` |
| [[B26]] `and`/`or` return an operand | S | `semantics` |
| [[B100]] `and` and `or` as macros | I | `semantics` (with B26) |
| [[B20]] `Maybe` is `a \| None` | S | `semantics` |
| [[B21]] missing values are `None` | S | `semantics` |
| [[B35]] `at` and `slice` are subscripts | S | `semantics` |
| [[B22]] unbounded integers | S | `semantics` |
| [[B28]] a `Char` is a `str` | S | `semantics` |
| [[B31]] a value used before its `def` | S | `semantics` |
| [[B80]] `def`: constant or variable | S | `semantics` |
| [[B39]] `fail` stands in for errors | S | `semantics` |
| [[B38]] operators aren't values | S | `semantics` or `collections` |
| [[B40]] types and values share a namespace | S | `namespaces` |
| [[B16]] `format` is an f-string hack | T | `collections` |
| [[B17]] taking a `tup` apart | T | `collections` |
| [[B48]] operators, `tup`, `put` untyped | T | `collections` |
| [[B123]] the translator's loops by hand | X | `collections` |
| [[B99]] variadic types | I → taken up | `collections` |
| [[B18]] `Any` turns checking off | T | `collections` (cut down; *lasting* for what stays) |
| [[B34]] no `Collection` | T | `collections` (Question 4) |
| [[B49]] host objects untyped | T | `library` (the `py` extension) |
| [[B93]] curried types, partial application | I | `collections` (Question 9) |
| [[B47]] only `(import m)` | L | `namespaces` |
| [[B108]] one flat namespace | L | `namespaces`, `library` |
| [[B51]] `with-default` is a built-in | L | `library` |
| [[B52]] macro code has no prelude | L | `library` |
| [[B50]] the translator's host built-ins | L | `library` |
| [[B95]] the I/O refactor | L | `library` |
| [[B32]] regexes are Python's | L | `library` (the `py` extension) |
| [[B54]] `slurp`'s search | L | `library` |
| [[B68]] the whole prelude in every program | L | `library` |
| [[B66]] the built-ins read every time | L | `library` |
| [[B62]] every module compiles the prelude's macros | L | `library` |
| [[B97]] a library per target | L | `library`, `porting-surface` |
| [[B72]] parsec.py v4 unpublished | X | not this epic (the bootstrap chain) |
| [[B41]] macros run with `exec` | M | `host-macros` |
| [[B70]] `load-macros` finds names by Python name | M | `host-macros` |
| [[B64]] `form.cdy` copied next to every translator | M | `host-macros` |
| [[B42]] a macro's result unchecked | M | `host-macros` |
| [[B45]] macro files use inclusion | M | `host-macros` |
| [[B46]] templates not hygienic across modules | M | `host-macros` |
| [[B43]] `gensym` is impure | M | `host-macros` |
| [[B44]] a macro can't expand into `import` | M | `host-macros` |
| [[B61]] `expand.cdy` knows special forms' shapes | M | `host-macros` |
| [[B63]] a macro file compiled per importer | M | `host-macros` |
| [[B104]] `up`, `down` for quoting | I | later |
| [[B29]] records are `NamedTuple`s | P | stays (the `tup` part: `collections`) |
| [[B113]] a field can't start with `_` | P | stays, or `porting-surface` |
| [[B114]] a field named like a tuple method | P | stays, or `porting-surface` |
| [[B55]] `match` is an `isinstance` chain | P | stays |
| [[B56]] every `match` subject gets a temporary | P | stays |
| [[B57]] the translator's Python is plain | P | stays |
| [[B74]] `py-str` is close to `repr` | P | stays |
| [[B76]] `PY_RESERVED` is 3.14's | P | stays |
| [[B71]] `at` and `slice_` helpers | P | `semantics` (with B35) |
| [[B37]] only self tail calls are loops | P | not this epic |
| [[B98]] trampolines, `loop`/`recur` | I | not this epic |
| [[B69]] building a list is quadratic | X | `collections` (with B123) |
| [[B58]] the reader builds one item at a time | X | not this epic |
| [[B65]] tests reach internals by Python names | X | `namespaces` |
| [[B75]] `mypy --strict` one program at a time | X | `typed-core` (Question 3) |
| [[B60]] three directories of test programs | X | any |
| [[B79]] `read_sexpr.cdy` types forms as `Any` | X | `collections` |
| [[B1]] highlight `candy` fences | X | any |
| [[B94]] doc strings and metadata | I | later |
| [[B96]] "no code changes" commits | I | any (process) |
| [[B102]] the book | I | later |
| [[B4]] `(def (x) 1)`'s message | D | any |
| [[B7]] a lowercase record name | D | any |
| [[B8]] the same argument twice | D | any |
| [[B9]] `nil` can be defined | D | any |
| [[B11]] a variant named like a macro | D | `namespaces` |
| [[B13]] a 200-clause `cond` | D | `semantics` (deep nesting) |
| [[B14]] errors without positions | D | `typed-core` |
| [[B119]] a variant written as a type | D | `typed-core` |
