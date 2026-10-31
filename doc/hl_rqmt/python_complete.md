# Python complete (epic HLD)

**Status: accepted (2026-10-30), questions answered; step 1 done, the branches next,
`typed-core` first. An epic: its steps are branches, each with an HLD of its own; this
one sets their order, their scope, and when the epic is done.** Written after tag `type-checker`.

Candy runs on one host and writes one target, Python, and the backlog's 84 open items
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
    add or compare in order, though the operators themselves can ([[B124]]);
    constraint variables could, then interfaces ([[B34]], Question 4);
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
Candy runs it):

- **a second implementation:** `test_spec.py` runs every example on both, and the
  spec becomes a conformance suite ([[B101]]);
- **the macro runner:** macros are interpreted, not compiled to Python and `exec`ed
  ([[B41]], [[B70]]), which is what a second host needs from macros;
- **a REPL**, later, nearly for free.

What it takes:

- **Its own values:** a sum (`VInt`, `VStr`, `VList`, `VRecord`, `VFn` with its
  closure, ...), and an environment. A macro's arguments and result cross between its
  values and the translator's `Form`s, by a conversion each way.
- **Its own built-ins:** every system built-in, written over its values. Each hands its
  leaf work to the host (`split` on a `VStr`'s text), but what it means (`=` on records,
  `/` on `Int`s, printing) is written from the spec. So it shares nothing with the
  Python target by design, which is the point of a second implementation, and the
  system's list is its porting surface too.
- **A settled language:** it implements the spec as it is, so it comes after the
  branches that change the language (semantics, collections, namespaces), and is
  written once. It doesn't discover borrowed semantics by itself: where it hands the
  host a meaning, it inherits it as the Python target does. What it checks is that the
  spec says enough to implement it twice.

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
separate operators, constraint variables or interfaces ([[B124]], [[B34]]) is
Question 4.

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
- **The first bounds come** (`collections`): `number`, `comparable` and `appendable`,
  constraint variables a `sig` can use (Question 4); Rust's spelling of each is a trait
  bound (`Add`, `PartialOrd`).
- **Left:** let-polymorphism ([[B15]]), bounds as interfaces (Question 4), higher kinds.
  None blocks a Rust target; each is a feature for later.

### Variadics

What takes any number of arguments falls in two kinds:

- **One type for every argument:** `+`, `-`, `*`, the comparisons, `and`, `or`. A typed
  rest parameter covers them: `(Fn (Int ...) Int)`, the rest arriving as a list
  ([[B99]]). It maps to every likely target (Rust: a slice). It would let them be
  ordinary built-ins in `system.cdy`, with types ([[B48]]): with Question 4's proposal,
  `(Fn (number ...) number)` for `+` and `(Fn (appendable ...) appendable)` for `++`.
- **Mixed types:** `put`, `format`, `tup`. A rest parameter can't type them. `put` and
  `format` need a `show` per argument's type, so they become macros over a typed `show`
  (see "`tup` and `format`"); `tup`'s type is its arity, so it stays a special form, or
  becomes literal syntax. Rust draws the same line: no variadic functions, and
  `println!` is a macro.

A user's `defn` could take a rest parameter too (`(defn sum (& xs) ...)`, the spelling
open, Question 9), which is the same feature. Against it: **currying** ([[B93]],
dropped): a curried type, and partial application, need a fixed arity, so Candy has
variadic functions or curried ones, not both (Question 9). Clojure's `map` takes several lists (`(map + xs ys)`); with rest
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
- **In the interpreter,** they are its own built-ins, over its values, so the two
  implementations agree because the spec says what each does.

### The branches

Each is a branch with its own HLD, in this order (Question 2), the groups it closes in
brackets:

1. **`typed-core`:** the checker writes each `Expr`'s type into Core; nested `fn`s get
   their types ([[B19]]); the checker's own leaks as wanted ([[B120]], [[B121]],
   [[B122]]). First, since `show`, `format`, `Any`'s cut and the translator's loops
   ([[B123]]) all need it. (T)
2. **`semantics`:** the borrowed semantics, one by one, each decided in the spec and
   fixed in the Python target: `show` and printing ([[B36]], the backlog's other
   `high`), `=`, `/`, `and`/`or`, `Maybe` and missing values, `at` and `slice`, numbers'
   bounds, `Char`, `def` order and constancy ([[B80]]), errors ([[B39]]); `=` and
   `show` on a type variable (Question 12). (S)
3. **`collections`:** the list literal, tuple types, variadics (typed rest
   parameters; `put` and `format` as macros over `semantics`' `show`; the operators as
   values, [[B38]]), `++` and the constraint variables `number`, `comparable` and
   `appendable` ([[B124]], Question 4), `Any` cut down to what is still needed,
   `Collection` (as Question 4 decides); the list operations' set, and the translator
   moved onto them ([[B123]]).
   (T)
4. **`namespaces`:** qualified names, the import forms, types and values, macros'
   names, shadowing, private names, each target's mapping. Independent of 2 and 3, so
   it could swap with them. (L)
5. **`library`** (perhaps two branches: the layering first, then the modules): the
   system revisited, each built-in specified; the prelude trimmed, the standard
   library's first modules, the I/O refactor, the target-extension mechanism and the
   `py` extension; the `test` module. (L)
6. **`interpreter`:** the interpreter over typed Core, written once against the
   language as the branches before it leave it; the spec runs on both, and a
   difference is a gap in the spec or a bug in one of them. (S, checked)
7. **`host-macros`:** macros run on the interpreter; macro code gets the prelude
   ([[B52]]); their results checked ([[B42]]); macro files as modules ([[B45]]);
   hygiene ([[B46]]); the macro leaks that remain ([[B43]], [[B44]]). (M)
8. **`test-runner`:** the spec's runner in Candy, on the interpreter, called from
   `test_spec.py`; the spec runs on both implementations through it. (X)
9. **`porting-surface`:** the per-target files (`system`, spelling, runtime, spec
   extensions) in a layout a second target fills in; the porting surface's own doc;
   whether mypy stays ([[B15]], Question 3), and each target's own checker as an
   option ([[B125]]); the exit test checked. (L, P)

Defects (D) and the translator's own items (X) go into whichever branch is near them.

## Pros and cons

- **For:** the backlog gets an order and an end; each branch is the size the last ones
  were; the language settles before its second implementation is written, so that is
  written once; the interpreter pays for itself three ways (conformance, macros, a
  REPL); the library gets a design before it grows, rather than after.
- **Against:** it is long, nine or more branches, before anything runs on Rust; some
  answers (interfaces, `Maybe` as a sum, qualified names) change many programs, the
  translator most, and the semantics are checked by one implementation until the
  sixth branch.
- **Why now:** the type checker was what the rest waited on (typed Core, `show`, `Any`).
  And the longer the translator is the only big Candy program, the more of it is written
  against Python's semantics.

## Steps

1. **Accept this HLD,** with its triage; add to `doc/process.md` what an epic is (an
   HLD whose steps are branches; "Design docs"), and an `epic` reference from each
   branch's HLD back to it.
   *Done:* accepted 2026-10-30; epics are in `doc/process.md` ("Design docs",
   "Kinds"). [[B93]] (currying) was dropped by Question 9's answer.
2. **The branches,** in order, each with its own lifecycle. This HLD gets a *Done* note
   per branch, and its triage is updated as items close or are found.
3. **The exit test,** checked in the last branch; the HLD becomes *done*.

## Questions (answered: the proposals, 2026-10-30)

1. **What "complete" means, and its exit test:** "a solid push-off point to a Rust
   target, and eventually a Rust host" (the draft above), tested by the four conditions
   in "Goals"? Or less (no interpreter: the second implementation waits for Rust), or
   more (the standard library's modules written, not just designed)? **Proposed: the
   draft, and the four.**
   *Answered:* the proposal.
2. **The order:** typed Core, semantics, collections, namespaces, library, the
   interpreter, host macros, test runner, porting surface? The other order puts the
   interpreter second, as a probe before the semantics are fixed; but it can't find a
   borrowed semantic by itself (it would hand the host the same meaning), and it would
   be rewritten for each language change after it. **Proposed: as listed**: the
   language changes first, `typed-core` first of all (what the rest needs) and
   `semantics` next (with [[B36]], `high`); the second implementation once, against the
   settled spec. `namespaces` could go before `semantics` and `collections`, if
   qualified names are wanted sooner.
   *Answered:* the proposal, as listed.
3. **mypy:** keep it as a second check through the epic, or drop it once Core is typed?
   **Proposed: keep it through the epic**, and decide in `porting-surface`, once two
   implementations check the semantics: it catches the Python backend's mistakes, which
   neither the checker nor the interpreter sees.
   *Answered:* the proposal; and a target may name a static checker for its output,
   which the driver runs as an option (mypy for Python; for Rust, `rustc` checks
   anyway), part of the porting surface ([[B125]]).
4. **Overloading:** the operators are polymorphic through rules built into the checker,
   and a program can't write a polymorphic function ([[B124]]): `+` on numbers, strings
   and lists, `-` and `*` on numbers, the comparisons and `=` on any one type. Four ways
   out:
   1. **Separate operators** (OCaml, Gleam): one per type, each an ordinary `sig`;
   2. **Constraint variables** (Elm): `number`, `comparable`, `appendable`, type
      variables a program's `sig`s can use, which take only those types;
   3. **Interfaces** (traits, type classes): a big feature, which maps well to Rust;
   4. **Special rules for now**, as today, kept as a leak.

   A survey of option 1, the one with the most churn:
   - **Elsewhere:** Gleam goes furthest (`+` and `+.`, `<` and `<.`, `<>` for strings,
     `list.append`), with two number types, and keeps a structural `==` on every type.
     OCaml has `+` and `+.`, `^`, `@` and `Int64.add`, but `=`, `<` and `compare` stay
     built-in and polymorphic (failing at run time on functions). Standard ML separates
     `^` and `@`, overloads `+` with a default to `int` (option 4), and gives `=`
     equality type variables (option 2). Elm already splits `++` (`appendable`) from
     `+` (`number`); Haskell has `++` and type classes for numbers. Go before 1.18 had
     Candy's leak exactly, and its generics added constraints (`Ordered`). Rust has
     traits (`Add`), and no `+` on `Vec`.
   - **Churn:** about 300 `+`s in the translator (roughly 140 on lists, 80 on strings,
     80 on numbers) and 76 in `spec/` and `tst/cdy/`. A rename, and a mechanical one:
     the checker can list each `+` with its type, and a script rewrite them, in two boot
     steps (the new operators into `bin`, then the translator's uses).
   - **For:** no special rules (`infer-op`'s cases and `needs-kind` go; each operator is
     a `sig`, and can be a value, [[B38]]); `(fn (a b) (+ a b))` infers `Int`; **the
     porting surface**: Python's `+` works on all three, so `emit` needs no types, but
     Rust's doesn't, and a polymorphic `+` would make the checker's types an input to
     every backend, while separate operators have one spelling each per target; and a
     list's append, O(n) on a tuple, shows in the code ([[B69]], [[B123]]).
   - **Against:** five number types (`Int`, `Long`, `Byte`, `Float`, `Double`), so five
     sets of arithmetic, or names qualified by `namespaces` (after `collections`), or
     fewer number types (a bigger change); `=` and the comparisons aren't covered (even
     Gleam and OCaml keep a polymorphic `=`, and Candy has 419), so Question 12 stays
     open; interfaces would usually bring overloaded arithmetic back (Rust's `Add`,
     Haskell's `Num`), though a separate append survives them (Haskell, Elm); and the
     spec's operator rules, examples and error tables change.

   **Proposed: Elm's design, in `collections`**: option 1 for append, `++` on strings
   and lists (`appendable`), most of the churn, and what lasts in every language that
   has it; option 2 for the rest, `number` across the five number types for `+`, `-`,
   `*` and `quot`, and `comparable` for the ordering comparisons, usable in a program's
   `sig`s; `=` for every type (Question 12). Interfaces (option 3, [[B34]]) get an HLD of
   their own after this epic, without undoing either. It is decided with variadics
   (Question 9): a variadic `+` over one `number` is a rest parameter of a constraint
   variable.
   *Answered:* the proposal.
5. **Target extensions:** a module per target (`py.cdy`, found in the target's library
   directory), or reader conditionals in one file? **Proposed: a module per target**:
   simpler, and a program says it isn't portable by importing it.
   *Answered:* the proposal.
6. **parsec in Candy:** a parser-combinator module in the standard library (the reader
   stays hand-written), as a proving ground for generics and closures? **Proposed: yes,
   as `parse`, in the `library` branch's second half, if it is cheap there.**
   *Answered:* the proposal; not part of the exit test, and if it isn't cheap there it
   moves after the epic, as an `idea`.
7. **`Maybe`:** a real sum (`(Some x)`, `None`), changing programs, or `a | None` kept
   *lasting* with narrowing? It is the biggest S item ([[B20]], [[B21]]), and changes
   the most programs if it changes. **Proposed: decided in the `semantics` HLD.**
   *Answered:* the proposal, both costed there (the translator's uses counted, as for
   `+`), leaning to the real sum: `(deft (Maybe a) (Some ((v a))) (None))` in the
   prelude, an ordinary generic sum taken apart with `match`, the checker's `Maybe`
   rules gone and `nil` only `Unit`; `(Maybe (Maybe t))` no longer collapses, and it is
   Rust's `Option`.
8. **Testing in Candy: how far?** The `test` module only; or that and the spec's
   runner (the conformance suite, which a second host needs); or everything, pytest
   kept for the Python-only checks. **Proposed: the `test` module and the spec's
   runner**, the rest when a second host needs it. The spec's runner needs the
   interpreter, `library`'s `string` module and `semantics`' errors as values, so it
   comes after all three.
   *Answered:* the proposal.
9. **Variadics or currying?** Typed rest parameters (`(Fn (Int ...) Int)`, a user
   `defn`'s rest parameter), or curried types and partial application ([[B93]]), which
   need a fixed arity; not both. Partial application can be a macro or a `fn` either way.
   **Proposed: rest parameters**, of one type, in `collections`; currying dropped
   (*lasting*), `fn` covering partial application. `put`, `format` and `tup` are not
   rest parameters in any answer.
   *Answered:* the proposal; a rest parameter's spelling is the `collections` HLD's
   (`&`, `(xs ...)` as in the `sig`, `&rest`, or a dotted tail).
10. **Namespaces' scope:** a branch of its own before `library` (proposed), or the first
   half of `library`? And types and values: one namespace (as now) or two? **Proposed:
   its own branch; one namespace, *lasting*,** since the translator and the tests rely on
   it and two would make `A` mean two things; [[B40]] and [[B119]] become a rule and a
   message.
   *Answered:* the proposal.
11. **The list operations:** add `map-acc` (a `map` threading a state), a right fold,
   `reduce` (no start value)? **Proposed: `map-acc` only**, as the translator's loops
   need it; `reduce` needs a non-empty list, which Candy can't type; a right fold isn't
   used.
   *Answered:* the proposal; `reduce` can come once Question 7 decides `Maybe`, typed
   `(Fn ((Fn (a a) a) (List a)) (Maybe a))`.
12. **`=` and `show` on a type variable:** declared for every type, *lasting* (each
   target supplies structural equality and a printer for all its types), or rejected
   until interfaces come? **Proposed: declared for every type**, in `semantics`;
   ordering (`<`) is `comparable`'s, in `collections` (Question 4), and the rest of a
   type variable's operations wait for interfaces.
   *Answered:* the proposal, with `=` on function types an error, so that every value
   compared is data.

## The triage

Every open item on 2026-10-29, in branch order; the branch is where it is expected to
close. ([[B67]], the built-ins' types unused, was closed by `type-checker`; [[B124]] and
[[B125]] were added on 2026-10-30, and [[B93]] dropped by Question 9.)

| Item | Group | Branch |
|---|---|---|
| [[B15]] the checker is an MVP | T | `typed-core` |
| [[B19]] nested `fn`s typed `Any` | T | `typed-core` |
| [[B120]] `get` before a type is known | T | `typed-core` |
| [[B121]] no narrowing in a clause | T | `typed-core` |
| [[B122]] a leaf's error at its parent | X | `typed-core` |
| [[B59]] only symbols and lists carry positions | X | `typed-core` |
| [[B14]] errors without positions | D | `typed-core` |
| [[B119]] a variant written as a type | D | `typed-core` |
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
| [[B71]] `at` and `slice_` helpers | P | `semantics` (with B35) |
| [[B38]] operators aren't values | S | `collections` |
| [[B16]] `format` is an f-string hack | T | `collections` |
| [[B17]] taking a `tup` apart | T | `collections` |
| [[B48]] operators, `tup`, `put` untyped | T | `collections` |
| [[B123]] the translator's loops by hand | X | `collections` |
| [[B99]] variadic types | I → taken up | `collections` |
| [[B18]] `Any` turns checking off | T | `collections` (cut down; *lasting* for what stays) |
| [[B34]] no `Collection` | T | `collections` (Question 4) |
| [[B124]] the operators polymorphic, programs not | T | `collections` (Question 4) |
| [[B69]] building a list is quadratic | X | `collections` (with B123) |
| [[B79]] `read_sexpr.cdy` types forms as `Any` | X | `collections` |
| [[B40]] types and values share a namespace | S | `namespaces` |
| [[B47]] only `(import m)` | L | `namespaces` |
| [[B108]] one flat namespace | L | `namespaces`, `library` |
| [[B65]] tests reach internals by Python names | X | `namespaces` |
| [[B11]] a variant named like a macro | D | `namespaces` |
| [[B49]] host objects untyped | T | `library` (the `py` extension) |
| [[B51]] `with-default` is a built-in | L | `library` |
| [[B50]] the translator's host built-ins | L | `library` |
| [[B95]] the I/O refactor | L | `library` |
| [[B32]] regexes are Python's | L | `library` (the `py` extension) |
| [[B54]] `slurp`'s search | L | `library` |
| [[B68]] the whole prelude in every program | L | `library` |
| [[B66]] the built-ins read every time | L | `library` |
| [[B62]] every module compiles the prelude's macros | L | `library` |
| [[B97]] a library per target | L | `library`, `porting-surface` |
| [[B125]] the target's own checker, as an option | I → taken up | `porting-surface` |
| [[B101]] an interpreter | I → taken up | `interpreter` |
| [[B52]] macro code has no prelude | L | `host-macros` |
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
| [[B29]] records are `NamedTuple`s | P | stays (the `tup` part: `collections`) |
| [[B113]] a field can't start with `_` | P | stays, or `porting-surface` |
| [[B114]] a field named like a tuple method | P | stays, or `porting-surface` |
| [[B55]] `match` is an `isinstance` chain | P | stays |
| [[B56]] every `match` subject gets a temporary | P | stays |
| [[B57]] the translator's Python is plain | P | stays |
| [[B74]] `py-str` is close to `repr` | P | stays |
| [[B76]] `PY_RESERVED` is 3.14's | P | stays |
| [[B75]] `mypy --strict` one program at a time | X | any (Question 3) |
| [[B60]] three directories of test programs | X | any |
| [[B1]] highlight `candy` fences | X | any |
| [[B96]] "no code changes" commits | I | any (process) |
| [[B4]] `(def (x) 1)`'s message | D | any |
| [[B7]] a lowercase record name | D | any |
| [[B8]] the same argument twice | D | any |
| [[B9]] `nil` can be defined | D | any |
| [[B13]] a 200-clause `cond` | D | any |
| [[B104]] `up`, `down` for quoting | I | later |
| [[B94]] doc strings and metadata | I | later |
| [[B102]] the book | I | later |
| [[B72]] parsec.py v4 unpublished | X | not this epic (the bootstrap chain) |
| [[B37]] only self tail calls are loops | P | not this epic |
| [[B98]] trampolines, `loop`/`recur` | I | not this epic |
| [[B58]] the reader builds one item at a time | X | not this epic |
