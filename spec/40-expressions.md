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
(`src/cdy/system.cdy`); `put` is typed `Any`, so it takes any number of arguments and
prints them with a space between.

```candy run
(put (len "four") (+ 1 2))
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

The operators are declared in `src/cdy/special.cdy`. `+`, `-`, `*`, `/`, `quot` and
`mod` take two or more arguments and fold left; `+` also joins strings, and lists. Their
arguments have one type, and the number types don't mix ([[checking.operators]]). `/`
divides a `Float` or `Double`, giving the same type, *lasting* (`(/ 7 2)` is an error).
`quot` divides whole numbers rounding down, toward minus infinity, as Haskell's `div` and
Python's `//` do (*lasting*: [[B24]]; a target whose division truncates spells it
otherwise), and `mod` is its remainder, so that `a` is `(+ (* b (quot a b)) (mod a b))`:
it takes `b`'s sign, as Haskell's `mod` (*lasting*). There is no unary minus: a negative
number is a literal (`-5`), and `(- 0 x)` negates (*lasting*: [[B33]]). Overflow isn't
checked (*for now*: [[B22]]; [[syntax.numbers]] has the sizes).

```candy run
(put (- 10 2 3) (* 2 3 4) (+ "a" "b" "c"))
(put (/ 7.0 2.0) (/ 1.0f 4.0f) (quot 7 2) (quot -7 2))
(put (mod 7 2) (mod -7 2) (mod 7 -2) (mod 7l 4l))
(put (len (+ (to-list 1) (to-list 2))))
```
```expect
5 24 abc
3.5 0.25f 3 -4
1 1 -1 3l
2
```

```candy errors
(put (/ 7 2)) => /: expected a Float or Double, got Int
(put (quot 7.0 2.0)) => quot: expected an Int, Long or Byte, got Double
(put (mod 1.0f 2.0f)) => mod: expected an Int, Long or Byte, got Float
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
Functions can't be compared, nor values holding one (a list of functions): an error when
translated (a function inside a record isn't seen yet: [[B150]]). Ordering (`<` and the
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
Each operator takes the number of arguments `special.cdy` declares: two or more, and one
for `not`.

```candy errors
(put (+ 1)) => needs at least 2 arguments
(put (- 5)) => needs at least 2 arguments
(put (and true)) => (and ...) needs at least 2 arguments, got 1
(put (not 1 2)) => (not ...) takes 1 argument(s), got 2
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
binding shadows an outer name of the same name. A binding `((a b ...) init)` takes a
tuple apart, as a `tup` pattern does (`30-match.md`).

```candy run
(sig x Int)
(def x 100)
(put (let ((x 1) (y (+ x 1))) (* x y)))
(put x)
(put (let (((q r) (tup 17 5))) (- q r)))
```
```expect
2
100
12
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

<a id="expr.tail-calls"></a>
A `defn` that calls itself in tail position runs as a loop, so it can recur any number of
times. Other recursion (not in tail position, mutual, or in a `defn` that makes a `fn`)
uses the host's stack, about 1000 calls deep (*for now*:
[[B37]]).

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
