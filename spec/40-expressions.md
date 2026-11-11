# Expressions and functions

status: stable, since: imvp-py-translator

Names and calls, the operators, `do`, `if`, `cond`, `let`, `fn` and `defn`, and `Unit`.

```candy
(f arg*)
(do expr*)
(if test then else?)
(cond (test expr)+ (else expr)?)
(let ((name init)*) expr)
(fn (arg+) expr)
(defn name (arg+) expr)
```

<a id="expr.calls"></a>
## Names and calls

A name is a local (a `let` binding, an argument, a pattern's), a top-level definition, an
import's, the prelude's or a built-in. `(f arg ...)` calls `f` with the arguments,
evaluated first, left to right. A special form (`if`, `let`, ...) isn't a value: it can't
be passed, or bound to another meaning. A built-in's arity comes from its type
(`src/cdy/system.cdy`); `put` is a prelude macro ([[library.put]]), so it takes any
number of arguments, and writes them with a space between.

```candy run
(put (str-len "four") (+ 1 2))
```
```expect
4 3
```

```candy errors
(put nope) => unknown name nope
(put (f 1)) => unknown name f
(put if) => special form, not a value
(put (let ((if 1)) if)) => let name must be a name, not a special form
(put (len 1 2)) => takes 1 argument(s), got 2
```

<a id="expr.arithmetic"></a>
## Operators

The operators are typed built-ins, declared in `src/cdy/system.cdy`
([[checking.operators]]). `+`, `-`, `*`, `/`, `quot` and `mod` take two or more numbers
and fold left; `+` adds numbers only, and `++` joins strings and lists
([[expr.append]]). Their arguments have one type, and the number types don't mix
([[checking.operators]]). `/`
divides a `Float` or `Double`, giving the same type, *lasting* (`(/ 7 2)` is an error).
`quot` divides whole numbers rounding down, toward minus infinity, as Haskell's `div` and
Python's `//` do (*lasting*: [[B24]]; a target whose division truncates spells it
otherwise), and `mod` is its remainder, so that `a` is `(+ (* b (quot a b)) (mod a b))`:
it takes `b`'s sign, as Haskell's `mod` (*lasting*). There is no unary minus: a negative
number is a literal (`-5`), and `(- 0 x)` negates (*lasting*: [[B33]]). Overflow isn't
checked (*for now*: [[B22]]; [[syntax.numbers]] has the sizes).

```candy run
(put (- 10 2 3) (* 2 3 4) (+ 1 2 3))
(put (/ 7.0 2.0) (/ 1.0f 4.0f) (quot 7 2) (quot -7 2))
(put (mod 7 2) (mod -7 2) (mod 7 -2) (mod 7l 4l))
```
```expect
5 24 6
3.5 0.25f 3 -4
1 1 -1 3l
```

```candy errors
(put (/ 7 2)) => argument 1 of /: expected float, got Int
(put (quot 7.0 2.0)) => argument 1 of quot: expected integer, got Double
(put (mod 1.0f 2.0f)) => argument 1 of mod: expected integer, got Float
(put (+ "a" "b")) => argument 1 of +: expected number, got String
```

<a id="expr.append"></a>
`++` (since `collections`) joins two strings or more, or two lists or more, of one type,
folding left: an `appendable` ([[checking.constraints]]). `+` is only for numbers,
*lasting*: joining isn't adding, and a target's `+` may not join (Rust's doesn't, on a
`Vec`).

```candy run
(put (++ "a" "b" "c") (++ (List 1) (List 2 3)) (len (++ (to-list 1) (to-list 2))))
```
```expect
abc (List 1 2 3) 2
```

```candy errors
(put (++ 1 2)) => argument 1 of ++: expected appendable, got Int
(put (++ "a" (List "b"))) => argument 2 of ++: expected String, got (List String)
(put (++ (List 1) (List "b"))) => argument 2 of ++: expected (List Int), got (List String)
```

<a id="expr.comparisons"></a>
The comparisons, `=`, `!=`, `<`, `>`, `<=` and `>=`, take two or more and chain:
`(< a b c)` is `a < b` and `b < c`.

```candy run
(sig yes (Fn (Bool) String))
(defn yes (b) (if b "yes" "no"))
(sig one Int)
(def one 1)
(sig two Int)
(def two 2)
(put (yes (< one two 3)) (yes (< one 3 two)) (yes (= two two 2)) (yes (!= one two)))
```
```expect
yes no yes yes
```

<a id="expr.equality"></a>
`=` and `!=` compare two values of one type ([[checking.operators]]) by their structure,
*lasting*: two lists with equal items, two tuples, two records of one type with equal
fields, two maps with equal pairs; two variants only if they are the same variant, with
equal fields. `Float`s and `Double`s compare as IEEE 754 does (`0.0` is `-0.0`).
Functions can't be compared, nor values holding one (a list of functions, or a record or
variant with one among its fields): an error when translated. Ordering (`<` and the
rest) is only for numbers, `String`s (by their characters' code points, as a `Char`) and
`Char`s ([[checking.operators]]).

```candy run
(deft S (A ((x Int))) (B ((x Int))) (C))
(deft V ((x Int) (y Int)))
(sig a S)
(def a (A 1))
(put (= a (A 1)) (= a (B 1)) (!= a (B 1)) (= C C) (= (V 1 2) (V 1 2)) (= (V 1 2) (V 2 1)))
(put (= (List 1 2) (List 1 2)) (= (Tup 1 "a") (Tup 1 "b")) (= 0.0 -0.0))
(put (contains (B 1) (List a (B 1))) (map-get (map-from (List (Tup a "a") (Tup (B 1) "b"))) (B 1)))
```
```expect
true false true true true false
true false true
true b
```

```candy errors
(sig f (Fn (Int) Int)) (defn f (n) n) (put (= f f)) => =: a function can't be compared, got (Fn (Int) Int)
(sig fs (List (Fn (Int) Int))) (def fs empty-list) (put (!= fs fs)) => !=: a function can't be compared
(deft F ((f (Fn (Int) Int)))) (deft S (A ((f F))) (B)) (put (= B B)) => =: a function can't be compared, got S
```

<a id="expr.logic"></a>
`and` and `or` take two or more and short-circuit: they stop at the first argument that
decides the result, and don't evaluate the rest, even when one needs statements first
(a `do`, whose earlier forms run for effect). `not` takes one. Their arguments are
`Bool`s, so the result is a `Bool` (*lasting*): Python's `or`, which gives an operand,
can't be seen.

```candy run
(sig yes (Fn (Bool) String))
(defn yes (b) (if b "yes" "no"))
(sig loud (Fn (String Bool) Bool))
(defn loud (msg val) (do (put msg) val))

(put (yes (and false (loud "and: never" true))))
(put (yes (or true (loud "or: never" false))))
(put (yes (and true (loud "and: second" true) (loud "and: third" false) (loud "and: never" true))))
(put (yes (or false (loud "or: second" false) (loud "or: third" true) (loud "or: never" true))))
(put (yes (not (and (loud "and: first" true) (do (put "and: last") true)))))

(sig check (Fn (Int) String))
(defn check (n) (if (or (< n 0) (do (put "  checking") (> n 10))) "out" "in"))
(put (check -1))
(put (check 5))
```
```expect
no
yes
and: second
and: third
no
or: second
or: third
yes
and: first
and: last
no
out
  checking
in
```

```candy errors
(put (or 1 5)) => or: expected Bool, got Int
(put (and true 5)) => and: expected Bool, got Int
```

<a id="expr.operator-arity"></a>
Each operator takes the number of arguments its type says: two or more, a rest parameter
([[expr.rest]]), and one for `not`.

```candy errors
(put (+ 1)) => (+ ...) takes at least 2 argument(s), got 1
(put (- 5)) => (- ...) takes at least 2 argument(s), got 1
(put (and true)) => (and ...) takes at least 2 argument(s), got 1
(put (not 1 2)) => (not ...) takes 1 argument(s), got 2
```

<a id="expr.operator-values"></a>
**An operator as a value** (since `collections`) is its function of two arguments, the
ones before its rest parameter ([[expr.rest]]), and `not` of one: `+` is an `(Fn (number
number) number)` ([[checking.operators]]), so `(fold + 0 xs)` adds. `and` and `or` as
values evaluate both arguments, as any function does; only a call written out
short-circuits. `=` and `!=` as values are `(Fn (a a) Bool)`, which doesn't keep `a` off
functions, as a generic function's `=` doesn't either (*for now*: [[B173]]).

```candy run
(put (fold + 0 (List 1 2 3)) (fold * 1.0 (List 2.0 3.0)) (fold ++ "" (List "a" "b")))
(put (fold quot 100 (List 2 5)) (fold and true (List true false)) (map not (List true false)))
(sig check (Fn ((Fn (Int Int) Bool) Int Int) Bool))
(defn check (f a b) (f a b))
(put (check < 1 2) (check >= 1 2) (check = 2 2) (check != 2 2) (let ((plus +)) (plus 1 2)))
```
```expect
6 6.0 ab
10 false (List false true)
true false true false 3
```

```candy errors
(put (map + (List 1))) => got (Fn (number number) number)
```

<a id="expr.conditionals"></a>
## do, if and cond

`(do expr ...)` evaluates its forms in order; its value is the last one's. `(if test then
else)` evaluates `then` or `else`; with no `else` the `then` is a `Unit`, an effect, and a
false test gives `nil`. The test is a `Bool`, and the branches have one type
([[checking.if]]).

`cond` is a macro (in `src/cdy/prelude_macros.cdy`, which every file gets), expanding into
nested `if`s: the first clause whose test is true gives the value. The last clause may be
`(else expr)`; with no `else`, the clauses are `Unit`s, and with no match the value is
`nil`.

```candy run
(sig sign (Fn (Int) String))
(defn sign (n) (cond ((< n 0) "negative") ((= n 0) "zero") (else "positive")))
(put (do (put "first") (sign -5)))
(put (if (> 2 1) "then" "else") (sign 0) (sign 7))
```
```expect
first
negative
then zero positive
```

```candy errors
(put (if 1)) => if: expected (if test then else?)
(put (if 1 2 3 4)) => if: expected (if test then else?)
(put (cond)) => cond: needs at least one (test expr) clause
(put (cond (else 1) (true 2))) => must be the last clause
```

<a id="expr.let"></a>
## let

`(let ((name init) ...) expr)` binds each name to its `init`'s value, in order, so an
`init` sees the names bound before it (like Scheme's `let*`), then evaluates `expr`. A
binding shadows an outer name of the same name, *lasting*: an outer local, or a top-level
one (a `def`, a `defn`, a built-in), which inside the `let` is the local and outside it
is unchanged (a `def` is a constant, [[programs.top-level]]). So does a function's
parameter, and a `match` clause's name. A binding `((a b ...) init)` takes a
tuple apart, as a `Tup` pattern does (`30-match.md`).

```candy run
(sig x Int)
(def x 100)
(put (let ((x 1) (y (+ x 1))) (* x y)))
(put x)
(put (let (((q r) (Tup 17 5))) (- q r)))
(sig f (Fn (Int) Int))
(defn f (x) (* x 2))
(put (f 3) (let ((map 7) (f 1)) (+ map f)) (f 3) x)
```
```expect
2
100
12
6 8 6 100
```

```candy errors
(put (let ((x)) x)) => let: binding must be (name init)
(put (let (x 1) x)) => let: binding must be (name init)
(put (let (((a b))) a)) => binding must be
(put (let ((x 1)) 1 2)) => let: expected (let ((name init)*) body)
```

<a id="expr.functions"></a>
## fn and defn

`(fn (arg ...) expr)` is a function, closing over the names it uses. `(defn name (arg
...) expr)` defines a top-level function; its `sig` must be a function type with one type
per argument (`20-types.md`). Both take at least one argument, and their body is exactly
one form (`do` for more). A function with no real input takes a `Unit` argument, as in
ML: `(defn run (_) ...)`, called as `(run nil)`. `defn` may become a macro over `def` and
`fn` (*for now*, a special form).

```candy run
(sig adder (Fn (Int) (Fn (Int) Int)))
(defn adder (n) (fn (m) (+ n m)))
(put ((adder 2) 3))
(put ((fn (x) (* x 2)) 4))

(sig seven (Fn (Unit) Int))
(defn seven (_) 7)
(put (seven nil))
```
```expect
5
8
7
```

<a id="expr.rest"></a>
**A rest parameter** (since `collections`): a `defn` whose `sig`'s last argument type is
`(Rest t)` takes any number of `t`s there, zero or more, after the arguments before it,
*lasting*. The parameter carries no marker: the `sig` says which it is. In the body it is
a `(List t)` of the arguments from there on; each of those is checked against `t`, and
too few arguments is an error. A list isn't spread over it: `(sum (List 1 2))` passes one
argument (no `apply`, *for now*). `(Rest t)` is only for the last argument of a `sig`'s
function type, and only a `defn` takes one: a `fn` has no `sig` to say so (*for now*:
[[B169]]). Used as a value, a function with a rest parameter is the function of its
arguments before the rest: `sum` below is an `(Fn (Int) Int)`.

```candy run
(sig sum (Fn (Int (Rest Int)) Int))
(defn sum (first more) (fold (fn (a b) (+ a b)) first more))
(sig names (Fn ((Rest String)) (List String)))
(defn names (ns) ns)
(sig twice (Fn ((Fn (Int) Int)) Int))
(defn twice (f) (f (f 1)))
(put (sum 1) (sum 1 2 3) (names) (names "a" "b") (twice sum))
```
```expect
1 6 (List) (List "a" "b") 1
```

```candy errors
(sig sum (Fn (Int (Rest Int)) Int)) (defn sum (n ns) n) (put (sum)) => (sum ...) takes at least 1 argument(s), got 0
(sig sum (Fn (Int (Rest Int)) Int)) (defn sum (n ns) n) (put (sum 1 2 "x")) => argument 3 of sum: expected Int, got String
(sig sum (Fn (Int (Rest Int)) Int)) (defn sum (n ns) n) (put (sum (List 1 2))) => argument 1 of sum: expected Int, got (List Int)
(sig f (Fn ((Rest Int) Int) Int)) (defn f (ns n) n) => (Rest t) is only for the last argument of a sig's function type
(sig f (Fn ((Fn ((Rest Int)) Int)) Int)) (defn f (g) 1) => (Rest t) is only for the last argument of a sig's function type
(sig f (Fn ((Rest Int Int)) Int)) (defn f (ns) 1) => bad rest type: expected (Rest Type)
(sig f (Fn ((Rest Int)) Int)) (def f (fn (n) 1)) => def f: only a defn can take a rest parameter
```

<a id="expr.tail-calls"></a>
A `defn` that calls itself in tail position runs as a loop, so it can recur any number of
times, unless it has a rest parameter. Other recursion (not in tail position, mutual, in
a `defn` that makes a `fn`, or with a rest parameter) uses the host's stack, about 1000
calls deep (*for now*: [[B37]]).

```candy run
(sig count (Fn (Int Int) Int))
(defn count (n acc) (if (= n 0) acc (count (- n 1) (+ acc 1))))
(put (count 100000 0))
```
```expect
100000
```

<a id="expr.function-shape"></a>
A `fn` or `defn` with no argument, or a body of more than one form, is an error:

```candy errors
(put (fn () 1)) => at least one
(put (fn (x) 1 2)) => fn: expected (fn (args+) body), with exactly one body form
(sig f (Fn (Int) Int)) (defn f () 1) => defn f: at least one argument is needed
(sig f (Fn (Int) Int)) (defn f (x) 1 2) => with exactly one body form
```

<a id="expr.unit"></a>
## Unit and nil

`Unit` is the type with one value, `nil`: the value of an effect, such as `put`, of an
`if` with no `else` (whose `then` is a `Unit`, [[checking.if]]), of `(do)`, and of a
`def` form itself. A value
that may be missing is a `(Maybe a)`, whose missing value is `None`, not `nil`
([[checking.maybe]]).

```candy run
(sig loud Bool)
(def loud false)
(put (if loud (put "never")) (do))
(sig m (Maybe Int))
(def m None)
(put (= m None))
```
```expect
nil nil
true
```
