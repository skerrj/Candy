# Type checking

status: draft, since: type-checker

The translator checks a program's types before it writes any Python
(`doc/hl_rqmt/type_checker.md`): every top-level name has its `sig` (`20-types.md`),
every built-in its type (`src/cdy/system.cdy`), and the types of locals are inferred. A
type error is the translator's error, at the form where it is found. mypy still checks
the Python the translator writes, as a second check ([[types.checking]]).

The error messages below are sketches until the checker is built.

<a id="checking.calls"></a>
## Calls

A call's arguments have its function's parameter types, and the call has its return
type. Calling something that isn't a function is an error.

```candy run
(sig twice (Fn (Int) Int))
(defn twice (n) (* 2 n))
(put (twice 21))
```
```expect
42
```

```candy errors
(put (to-int 1)) => argument 1 of to-int: expected String, got Int
(sig twice (Fn (Int) Int)) (defn twice (n) (* 2 n)) (put (twice "a")) => argument 1 of twice: expected Int, got String
(sig one Int) (def one 1) (put (one 2)) => expected a function, got Int
```

<a id="checking.definitions"></a>
## Definitions

A `def`'s value has its `sig`'s type, and a `defn`'s body its return type, its
parameters the parameter types.

```candy errors
(sig x Int) (def x "a") => def x: expected Int, got String
(sig f (Fn (Int) String)) (defn f (n) n) => defn f: expected String, got Int
(sig f (Fn (String) Int)) (defn f (s) (+ s 1)) => +: expected String, got Int
```

<a id="checking.generics"></a>
## Generic functions

A `sig` with type variables (`(Fn (a a Bool) a)`) is generic: each use gives its type
variables fresh types, so one function works on `Int`s in one call and `String`s in the
next. Inside its own body a type variable is one fixed, unknown type, so the body can't
treat it as an `Int`.

```candy run
(sig pick (Fn (a a Bool) a))
(defn pick (x y left) (if left x y))
(put (pick 1 2 true) (pick "a" "b" false))
```
```expect
1 b
```

```candy errors
(sig f (Fn (a) a)) (defn f (x) (+ x 1)) => expected a, got Int
(sig pick (Fn (a a Bool) a)) (defn pick (x y left) (if left x y)) (put (pick 1 "a" true)) => argument 2 of pick: expected Int, got String
```

<a id="checking.locals"></a>
## Locals

A local (a `let` binding, a `fn`'s parameter, a pattern's name) has no written type: the
checker infers it from how it is made and used. A local has one type, so a `fn` bound by
`let` isn't generic (*for now*: [[B15]]); a top-level `defn` with a generic `sig` is.

```candy run
(put (let ((n 3) (m (* n n))) (+ m 1)))
(put (join (map (fn (s) (+ s "!")) (to-list "hi")) ""))
```
```expect
10
hi!
```

```candy errors
(put (let ((n 1)) (+ n "a"))) => +: expected Int, got String
(put (let ((id (fn (x) x))) (do (id 1) (id "a")))) => argument 1 of id: expected Int, got String
```

<a id="checking.if"></a>
## if

An `if`'s test is a `Bool` (no other value counts as true or false), and its two
branches have one type, the `if`'s. With no `else`, an `if` whose `then` is a `t` is a
`(Maybe t)` (*for now*: [[B21]]), or `Unit` if the `then` is.

```candy run
(sig half (Fn (Int) (Maybe Int)))
(defn half (n) (if (= (* 2 (quot n 2)) n) (quot n 2)))
(put (with-default -1 (half 8)) (with-default -1 (half 7)))
```
```expect
4 -1
```

```candy errors
(put (if 1 2 3)) => if: the test is Int, not Bool
(put (if "" 2 3)) => if: the test is String, not Bool
(put (if true 1 "a")) => if: the branches are Int and String
```

<a id="checking.operators"></a>
## Operators

The operators have fixed rules (Candy has no overloading). `+` takes arguments of one
type, a number type, `String` or a list (`+` joins lists, as it joins strings); `-`, `*`
and `quot` one number type; `/` numbers of one type, and gives a `Double`. The comparisons take arguments of one type and give a
`Bool`; `and`, `or` and `not` take `Bool`s. The number types don't mix: `(+ 1 1.0)` is
an error.

```candy run
(put (+ 1 2) (+ "a" "b") (/ 7 2) (if (< 1 2 3) "yes" "no"))
(put (len (+ (to-list 1) (to-list 2) (to-list 3))))
```
```expect
3 ab 3.5 yes
3
```

```candy errors
(put (+ 1 "a")) => +: expected Int, got String
(put (+ 1 1.0)) => +: expected Int, got Double
(put (- "a" "b")) => -: expected a number, got String
(put (< 1 "a")) => <: expected Int, got String
(put (and 1 true)) => and: expected Bool, got Int
(put (not "a")) => not: expected Bool, got String
```

<a id="checking.tup-lists"></a>
## Tuples as lists

A `(Tup t ...)` whose items are all `t`s is accepted where a `(List t)` is expected, so
`tup` writes a list (*for now*: Candy has no list literal, and a tuple is a list in
Python, [[B29]]).

```candy run
(sig names (List String))
(def names (tup "ann" "bo"))
(put (len names) (join names ","))
```
```expect
2 ann,bo
```

```candy errors
(sig xs (List Int)) (def xs (tup 1 "a")) => def xs: expected (List Int), got (Tup Int String)
```

<a id="checking.records"></a>
## Records

A record's constructor takes its fields' types, in order, and gives the record; `get`
names a field the record has, and has the field's type; `assoc` names fields it has,
each with a value of the field's type.

```candy run
(deft V ((x Int) (y String)))
(put (get (V 1 "a") y))
(put (get (assoc (V 1 "a") x 2) x))
```
```expect
a
2
```

```candy errors
(deft V ((x Int))) (put (get (V 1 2) x)) => (V ...) takes 1 field(s), got 2
(deft V ((x Int))) (put (V "a")) => argument 1 of V: expected Int, got String
(deft V ((x Int))) (put (get (V 1) z)) => get: V has no field z
(deft V ((x Int))) (put (get (assoc (V 1) x "a") x)) => assoc: field x of V is Int, got String
(put (get 1 x)) => get: Int has no fields
```

<a id="checking.order"></a>
## What is known when

The checker reads a call's arguments that aren't `fn`s first, then its `fn`s, so a
`fn`'s parameters already have types when its body is read: in `(map (fn (p) ...)
people)`, `p` is a person. A `get` or `assoc` on a value whose type isn't known yet is
an error (*for now*: [[B15]]).

```candy run
(deft P ((name String)))
(put (join (map (fn (p) (get p name)) (to-list (P "ann"))) ","))
```
```expect
ann
```

```candy errors
(put (fn (p) (get p name))) => get: the type of p isn't known here (name)
```

<a id="checking.match"></a>
## match

A `match`'s subject is of the sum its clauses take apart; each clause's names have their
fields' types; all the clauses (and the `else`) have one type, the `match`'s. A `tup`
pattern takes a `(Tup ...)` with as many items as it has names.

```candy run
(deft Shape (Circle ((r Int))) (Sq ((s Int))))
(sig size (Fn (Shape) Int))
(defn size (sh) (match sh ((Circle r) (* 3 r r)) ((Sq s) (* s s))))
(put (size (Circle 1)) (size (Sq 2)))
```
```expect
3 4
```

```candy errors
(deft S (A ((x Int))) (B)) (sig f (Fn (S) Int)) (defn f (s) (match s ((A x) x) ((B) "none"))) => match: the clauses are Int and String
(deft S (A) (B)) (put (match 1 ((A) 1) ((B) 2))) => match: the subject is Int, not S
(put (match (tup 1 2) ((tup a b c) a))) => match: a (Tup Int Int) has 2 items, not 3
```

<a id="checking.maybe"></a>
## Maybe and nil

A `t` is accepted where a `(Maybe t)` is expected, and `nil` where a `Unit` or any
`(Maybe t)` is. A `(Maybe t)` isn't a `t`: `with-default` takes the `t` out (*for now*:
no narrowing after `(= m nil)`, and `Maybe` isn't a sum, [[B20]]).

```candy run
(sig some (Maybe Int))
(def some 5)
(sig none (Maybe Int))
(def none nil)
(put (with-default 0 some) (with-default 0 none))
```
```expect
5 0
```

```candy errors
(sig m (Maybe Int)) (def m 5) (put (+ m 1)) => +: expected a number or String, got (Maybe Int)
(sig n Int) (def n nil) => def n: expected Int, got Unit
```

<a id="checking.any"></a>
## Any

`Any` matches every type, both ways, and nothing passing through it is checked (*for
now*: [[B18]]). The built-ins Candy can't type yet are `Any`: `put`, `at`, `len`.

```candy run
(put (+ (at (to-list 41) 0) 1))
```
```expect
42
```
