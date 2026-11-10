# Type checking

status: stable, since: type-checker

The translator checks a program's types before it writes any Python
(`doc/hl_rqmt/type_checker.md`): every top-level name has its `sig` (`20-types.md`),
every built-in its type (`src/cdy/system.cdy`), and the types of locals are inferred. A
type error is the translator's error, at the form where it is found. mypy still checks
the Python the translator writes, as a second check ([[types.checking]]).

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
parameters the parameter types. A type error is reported at the expression it is in,
literals and names too:

```candy error
(sig x Int)
(def x
  "a")
```
```expect-error
line 3, column 3: def x: expected Int, got String
```

```candy errors
(sig x Int) (def x "a") => def x: expected Int, got String
(sig f (Fn (Int) String)) (defn f (n) n) => defn f: expected String, got Int
(sig f (Fn (String) Int)) (defn f (s) (++ s 1)) => argument 2 of ++: expected String, got Int
```

<a id="checking.generics"></a>
## Generic functions

A `sig` with type variables (`(Fn (a a Bool) a)`) is generic: each use gives its type
variables fresh types, so one function works on `Int`s in one call and `String`s in the
next. Inside its own body a type variable is one fixed, unknown type, so the body can't
treat it as an `Int`, nor add or compare it, unless it is a constraint variable
([[checking.constraints]]).

```candy run
(sig pick (Fn (a a Bool) a))
(defn pick (x y left) (if left x y))
(put (pick 1 2 true) (pick "a" "b" false))
```
```expect
1 b
```

```candy errors
(sig f (Fn (a) a)) (defn f (x) (+ x 1)) => argument 1 of +: expected number, got a
(sig pick (Fn (a a Bool) a)) (defn pick (x y left) (if left x y)) (put (pick 1 "a" true)) => argument 2 of pick: expected Int, got String
```

<a id="checking.locals"></a>
## Locals

A local (a `let` binding, a `fn`'s parameter, a pattern's name) has no written type: the
checker infers it from how it is made and used. A local has one type, so a `fn` bound by
`let` isn't generic (*for now*: [[B133]]); a top-level `defn` with a generic `sig` is.

```candy run
(put (let ((n 3) (m (* n n))) (+ m 1)))
(put (join (map (fn (s) (++ s "!")) (to-list "hi")) ""))
(put (let ((sq (fn (x) (* x x)))) (sq 3)))
```
```expect
10
hi!
9
```

```candy errors
(put (let ((n 1)) (+ n "a"))) => argument 2 of +: expected Int, got String
(put (let ((id (fn (x) x))) (do (id 1) (id "a")))) => argument 1 of id: expected Int, got String
```

<a id="checking.if"></a>
## if

An `if`'s test is a `Bool` (no other value counts as true or false), and its two
branches have one type, the `if`'s. With no `else`, the `then` is a `Unit`, and so is the
`if`: it is for an effect, `(if loud (put x))` (*for now*: [[B138]]); a `cond` with no
`else` clause likewise ([[macros.cond]]: its last clause is an `if` with no `else`, which
the message names, *for now*, [[B156]]). A value that may be missing is a `(Maybe t)`
([[checking.maybe]]).

```candy run
(sig half (Fn (Int) (Maybe Int)))
(defn half (n) (if (= (* 2 (quot n 2)) n) (Some (quot n 2)) None))
(put (half 8) (half 7))
(sig loud Bool)
(def loud true)
(if loud (put "loud"))
```
```expect
(Some 4) None
loud
```

```candy errors
(put (if 1 2 3)) => if: the test is Int, not Bool
(put (if "" 2 3)) => if: the test is String, not Bool
(put (if true 1 "a")) => if: the branches are Int and String
(put (if true 1)) => if: with no else, the then is Int, not Unit
(put (cond (false 1))) => if: with no else, the then is Int, not Unit
```

<a id="checking.constraints"></a>
## Constraint variables (since `collections`)

A type variable named for a constraint takes only the types the constraint lists,
*lasting* (until interfaces, [[B34]]), as Elm's do:

| Variable | Takes |
|---|---|
| `number` | `Int`, `Long`, `Byte`, `Float`, `Double` |
| `integer` | `Int`, `Long`, `Byte` |
| `float` | `Float`, `Double` |
| `comparable` | the numbers, `String`, `Char` |
| `appendable` | `String`, `(List a)` |

Any other lowercase name is an ordinary type variable, which takes any type. Like one,
each use of a constraint variable is one type in a `sig`: `(Fn (number number) number)`
takes two numbers of one type. A second, independent one is numbered: `number2`,
`comparable2`. A program's own `sig` can use them, so a generic function can add or
compare its arguments; inside its body, a `number` is one unknown number type, so it
isn't an `Int` (a literal is, so `(+ x 1)` on a `number` is an error).

```candy run
(sig total (Fn ((List number) number) number))
(defn total (xs zero) (fold (fn (a b) (+ a b)) zero xs))
(sig biggest (Fn (comparable comparable) comparable))
(defn biggest (a b) (if (> a b) a b))
(sig scale (Fn (number number2) number))
(defn scale (x n) x)
(put (total (List 1 2 3) 0) (total (List 1.5 2.5) 0.0) (biggest "ab" "b") (biggest 3 2) (scale 1 2.0))
```
```expect
6 4.0 b 3 1
```

```candy errors
(sig total (Fn ((List number) number) number)) (defn total (xs z) z) (put (total (List "a") "b")) => argument 1 of total: expected (List number), got (List String)
(sig big (Fn (comparable comparable) comparable)) (defn big (a b) a) (put (big true false)) => argument 1 of big: expected comparable, got Bool
(sig f (Fn (number) number)) (defn f (x) (+ x 1)) => argument 2 of +: expected number, got Int
(sig f (Fn (a) a)) (defn f (x) (+ x x)) => argument 1 of +: expected number, got a
(sig f (Fn (comparable) Int)) (defn f (x) (quot x 2)) => argument 1 of quot: expected integer, got comparable
(sig f (Fn (number Int) Bool)) (defn f (x n) (< x n)) => argument 2 of <: expected number, got Int
```

<a id="checking.operators"></a>
## Operators

The operators are typed built-ins, as any function, with constraint variables and rest
parameters ([[expr.rest]]), declared in `src/cdy/system.cdy`; Candy has no overloading.
`+`, `-` and `*` take a `number`, `/` a `float`, `quot` and `mod` an `integer`, and `++`
an `appendable`, a `String` or a list ([[expr.append]]). The comparisons take arguments
of one type and give a `Bool`: `=` and `!=` any type but a function's ([[expr.equality]]),
the orderings (`<`, `>`, `<=`, `>=`) a `comparable` (lists and records aren't ordered,
*for now*, until interfaces: [[B34]]). `and` and `or` take two `Bool`s or more, and `not`
one. Each argument is checked as a function's is, and its error is at it. The number
types don't mix: `(+ 1 1.0)` is an error.

```candy run
(put (+ 1 2) (++ "a" "b") (/ 7.0 2.0) (if (< 1 2 3) "yes" "no") (< "ab" "b") (< \a \b))
(put (len (++ (to-list 1) (to-list 2) (to-list 3))))
```
```expect
3 ab 3.5 yes true true
3
```

```candy errors
(put (+ 1 "a")) => argument 2 of +: expected Int, got String
(put (+ 1 1.0)) => argument 2 of +: expected Int, got Double
(put (- "a" "b")) => argument 1 of -: expected number, got String
(put (< 1 "a")) => argument 2 of <: expected Int, got String
(put (/ 7 2)) => argument 1 of /: expected float, got Int
(put (quot 1.0 2.0)) => argument 1 of quot: expected integer, got Double
(put (< true false)) => argument 1 of <: expected comparable, got Bool
(put (> (List 1) (List 2))) => argument 1 of >: expected comparable, got (List Int)
(deft V ((x Int))) (put (<= (V 1) (V 2))) => argument 1 of <=: expected comparable, got V
(put (>= nil nil)) => argument 1 of >=: expected comparable, got Unit
(put (and 1 true)) => argument 1 of and: expected Bool, got Int
(put (not "a")) => argument 1 of not: expected Bool, got String
(put (+ 1 2 (- 3 "x"))) => argument 2 of -: expected Int, got String
```

The error is at the argument, not the call ([[B135]]):

```candy error
(sig x Int)
(def x 1)
(put (+ x
  "b"))
```
```expect-error
line 4, column 3: argument 2 of +: expected Int, got String
```

<a id="checking.tup-lists"></a>
## Tuples aren't lists

A `(Tup t ...)` isn't a `(List t)`, even with its items all one type, *lasting*: a
tuple's size is its type's, a list's isn't. `(List item*)` writes a list, its items one
type ([[types.constructors]]). (Until `collections`, such a tuple was accepted as a list,
and `tup` wrote both.)

```candy run
(sig names (List String))
(def names (List "ann" "bo"))
(put (len names) (join names ","))
```
```expect
2 ann,bo
```

```candy errors
(sig xs (List String)) (def xs (Tup "ann" "bo")) => def xs: expected (List String), got (Tup String String)
(sig xs (List Int)) (def xs (Tup 1 "a")) => def xs: expected (List Int), got (Tup Int String)
```

<a id="checking.records"></a>
## Records

A record's constructor takes its fields' types, in order, and gives the record; `get`
names a field the record has, and has the field's type; `assoc` names fields it has,
each with a value of the field's type. A variant's constructor gives its sum, so `get` on
a sum names a field every variant has, with one type (*lasting*: a sum's value is one of
its variants, not known until it is matched, [[match.sum-types]]); in a `match` clause
on a local, the local is narrowed to the clause's variant ([[checking.narrowing]]).

```candy run
(deft V ((x Int) (y String)))
(put (get (V 1 "a") y))
(put (get (assoc (V 1 "a") x 2) x))
(deft (T a) (L ((v a))) (N ((v a) (n Int))))
(sig t (T Int))
(def t (N 3 4))
(put (+ (get t v) 1) (get (L "b") v))
```
```expect
a
2
4 b
```

```candy errors
(deft V ((x Int))) (put (get (V 1 2) x)) => (V ...) takes 1 field(s), got 2
(deft V ((x Int))) (put (V "a")) => argument 1 of V: expected Int, got String
(deft V ((x Int))) (put (get (V 1) z)) => get: V has no field z
(deft V ((x Int))) (put (get (assoc (V 1) x "a") x)) => assoc: field x of V: expected Int, got String
(put (get 1 x)) => get: Int has no fields
(deft S (A ((x Int))) (B ((y Int)))) (put (get (A 1) x)) => get: S has no field x
(deft S (A ((x Int))) (B)) (put (get (A 1) x)) => get: S has no field x
(deft S (A ((id Int) (x Int))) (B ((id String)))) (put (get (A 1 2) id)) => get: field id of S has different types in its variants
```

<a id="checking.narrowing"></a>
## Narrowing

In a `match` clause whose subject is a local, the local is of the clause's variant, so
`get` and `assoc` on it name the variant's own fields. Only the clauses narrow: not the
`else`, nor an `if` on a test (*for now*: [[B136]]); a subject that isn't a local isn't
narrowed (the clause's names read its fields). A variant isn't a type a program writes,
so where the local is passed or returned it is still of the sum.

```candy run
(deft S (A ((x Int) (id Int))) (B ((y String) (id Int))) (C))
(sig f (Fn (S) Int))
(defn f (s) (match s ((A _ _) (+ (get s x) (get s id))) ((B _ _) (len (get s y))) ((C) 0)))
(sig bump (Fn (S) S))
(defn bump (s) (match s ((A _ _) (assoc s x (+ (get s x) 1))) (else s)))
(put (f (A 1 2)) (f (B "abc" 1)) (f C) (bump (A 1 2)) (bump C))
(deft (T a) (L ((v a))) (N ((v a) (n Int))))
(sig g (Fn ((T Int)) Int))
(defn g (t) (match t ((N _ _) (+ (get t v) (get t n))) ((L _) (get t v))))
(put (g (N 1 5)) (g (L 3)))
```
```expect
3 3 0 (A 2 2) C
6 3
```

```candy errors
(deft S (A ((x Int))) (B ((y Int)))) (sig f (Fn (S) Int)) (defn f (s) (match s ((A _) (get s y)) (else 0))) => get: A has no field y
(deft S (A ((x Int))) (B ((y Int)))) (sig f (Fn (S) Int)) (defn f (s) (match s ((A _) 0) (else (get s x)))) => get: S has no field x
```

<a id="checking.order"></a>
## What is known when

The checker reads a call's arguments that aren't `fn`s first, then its `fn`s, so a
`fn`'s parameters already have types when its body is read: in `(map (fn (p) ...)
people)`, `p` is a person. A `get` or `assoc` on a value whose type isn't known yet is a
constraint on it, checked once its definition is: then the value's type must be known,
with the field, of the type the constraint found; one that met only `Any` is `Any`.

```candy run
(deft P ((name String)))
(put (join (map (fn (p) (get p name)) (to-list (P "ann"))) ","))
```
```expect
ann
```

```candy run
(deft P ((name String)))
(put (let ((name-of (fn (p) (get p name))) (rename (fn (p) (assoc p name "bo")))) (++ (name-of (P "ann")) (get (rename (P "x")) name))))
```
```expect
annbo
```

```candy errors
(put (fn (p) (get p name))) => get: the type of p isn't known here (name)
(deft P ((name String))) (put (let ((f (fn (p) (+ (get p name) 1)))) (f (P "a")))) => get: field name of P is String, not Int
(deft P ((name String))) (put (let ((f (fn (p) (assoc p name 1)))) (f (P "a")))) => assoc: field name of P is String, not Int
(deft P ((name String))) (put (let ((f (fn (p) (get p age)))) (f (P "a")))) => get: P has no field age
```

<a id="checking.match"></a>
## match

A `match`'s subject is of the sum its clauses take apart; each clause's names have their
fields' types; all the clauses (and the `else`) have one type, the `match`'s. A `Tup`
pattern takes a `(Tup ...)` with as many items as it has names, and only a tuple (or an
`Any`).

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
(put (match (Tup 1 2) ((Tup a b c) a))) => a (Tup Int Int) has 2 items, not 3
(deft P ((a Int) (b Int))) (put (let (((x y) (P 1 2))) x)) => a Tup pattern takes a tuple, not a P
```

<a id="checking.maybe"></a>
## Maybe and nil

A `(Maybe t)` is the prelude's sum, `(Some v)` or `None` ([[library.maybe]]), checked as
any sum (*lasting*): a `t` isn't a `(Maybe t)`, nor is `nil`, which is only `Unit`'s
value; `match` takes one apart, `((Some v) ...)` naming the value, and `with-default`
gives the value or a fallback. A `(Maybe (Maybe t))` is two layers, `(Some None)` not
`None`.

```candy run
(sig some (Maybe Int))
(def some (Some 5))
(sig none (Maybe Int))
(def none None)
(put (with-default 0 some) (with-default 0 none) (match some ((Some v) (+ v 1)) ((None) 0)))
(sig two (Maybe (Maybe Int)))
(def two (Some None))
(put two (= two None))
```
```expect
5 0 6
(Some None) false
```

```candy errors
(sig m (Maybe Int)) (def m 5) => def m: expected (Maybe Int), got Int
(sig m (Maybe Int)) (def m nil) => def m: expected (Maybe Int), got Unit
(sig m (Maybe Int)) (def m (Some 1)) (put (+ m m)) => argument 1 of +: expected number, got (Maybe Int)
(sig n Int) (def n nil) => def n: expected Int, got Unit
(sig m (Maybe Int)) (def m (Some 1)) (put (+ 1 m)) => argument 2 of +: expected Int, got (Maybe Int)
```

<a id="checking.any"></a>
## Any

`Any` matches every type, both ways, and nothing passing through it is checked (*for
now*: [[B18]]). The built-ins Candy can't type yet are `Any`: `put`, `at`, `len`.

`Any` binds no type variable it meets, so a later use can still solve it; one that met
`Any` and nothing else is `Any` once its definition is checked, as gradual inference
defaults it (`(reverse a)` on an `a` typed `Any` is a `(List Any)`). One that met nothing
(a `fn` never called, an `empty-list` never added to) stays a type variable, which
Python writes `Any` (*for now*: [[B133]]). *Tested in* `test_unsolved_types` and
`test_every_node_is_typed` (`tst/py_cdy/test_self_host.py`): the type is in Core and the
Python annotations, not in what a program prints.

```candy run
(put (+ (at (to-list 41) 0) 1))
```
```expect
42
```
