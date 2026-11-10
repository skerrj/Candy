# The library

status: stable, since: system-prelude

The built-ins (`src/cdy/system.cdy`), the prelude (`src/cdy/prelude.cdy`) and `format`
(`doc/hl_rqmt/system_prelude.md`, `doc/hl_rqmt/library.md`). The operators are in
`40-expressions.md`.

Lists, tuples, strings and maps are the host's, so their operations are built-ins, which
the runtime provides (`src/cdy_rt/primitives.py`); the prelude holds what is built on
them. A value prints as Candy shows it ([[library.show]]).

<a id="library.builtins"></a>
## Built-ins

`system.cdy` declares each built-in with a `sig` that has no definition: the runtime
provides it, with that type. Only there may a `sig` have no definition. A built-in's
arity is its type's (`40-expressions.md`). A built-in typed `Any` takes any number of
arguments, or works on lists, strings and maps alike, or returns a host object (*for
now*: Candy can't write those types yet, [[B34]], [[B48]], [[B49]]).

| Group | Built-ins |
|---|---|
| output | `put`, `print`, `display` (any number of arguments, with a space between), `put-err` |
| files | `slurp`, `spit`, `file-put-lines`, `file-exists`, `make-dirs`, `path-stem`, `path-dir`, `path-join`, `path-resolve` |
| collections | `len`, `at`, `slice`, `in` (a list, a tuple or a string), `to-list`, `empty-list`, `is-coll` |
| lists | `map`, `filter`, `fold`, `any`, `all`, `find`, `reverse`, `range`, `take`, `drop`, `concat`, `zip`, `index-of`, `contains`, `with-default`, `join` |
| maps | `empty-map`, `map-get`, `map-has`, `map-set`, `map-keys`, `map-from` |
| strings | `split`, `starts-with`, `ends-with`, `repeat`, `strip`, `replace`, `to-int`, `to-float`, `char-code`, `hex-char`, `is-empty-str`, `is-decimal`, `is-digit`, `is-alpha`, `is-str`, `is-neg-int`, `isspace`, `isspace-at` |
| regular expressions | `re-search`, `re-findall`, `re-compile` (Python's match and pattern objects, `Any`) |
| math | `PI`, `sin`, `cos`, `tan` |
| the program | `SYS_ARGS`, `fail`, `nil` |

```candy run
(put (path-stem "dir/file.cdy") (to-int "7") (len (range 0 3)))
```
```expect
file 7 3
```

`fail` is a panic: the program stops with its message ([[library.errors]]). Five built-ins are only for the
translator: `py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name`.

<a id="library.lists"></a>
## Lists

A list is typed `(List a)`; `List` ([[types.constructors]]) and `range` make one, and
`empty-list` is the empty one. The functions take the list last. `map`, `filter` and `fold` are built in for
speed, since Candy adds to a list by copying it. `find` and `index-of` give a `(Maybe a)`
([[library.maybe]]): `None` when nothing is found, which `with-default` replaces.

```candy run
(sig nums (List Int))
(def nums (range 1 6))
(sig none (List Int))
(def none empty-list)

(put nums (range 3 3))
(put (map (fn (n) (* n n)) nums) (filter (fn (n) (> n 2)) nums))
(put (fold (fn (acc n) (+ acc n)) 0 nums))
(put (any (fn (n) (> n 4)) nums) (any (fn (n) (> n 5)) nums) (any (fn (n) true) none))
(put (all (fn (n) (> n 0)) nums) (all (fn (n) (> n 1)) nums) (all (fn (n) false) none))
(put (with-default 0 (find (fn (n) (> n 2)) nums)) (with-default 0 (find (fn (n) (> n 9)) nums)))
(put (reverse nums) (reverse none))
(put (take 2 nums) (take 9 nums) (take -1 nums))
(put (drop 2 nums) (drop 9 nums))
(put (concat (List (List 1 2) none (List 3))))
(put (with-default -1 (index-of 3 nums)) (with-default -1 (index-of 9 nums)))
(put (contains 3 nums) (contains 9 nums))
```
```expect
(List 1 2 3 4 5) (List)
(List 1 4 9 16 25) (List 3 4 5)
15
true false false
true false true
3 0
(List 5 4 3 2 1) (List)
(List 1 2) (List 1 2 3 4 5) (List)
(List 3 4 5) (List)
(List 1 2 3)
2 -1
true false
```

<a id="library.zip"></a>
`zip` pairs two lists' items into tuples, up to the shorter one's length:

```candy run
(sig pairs (List (Tup Int String)))
(def pairs (zip (range 1 6) (List "a" "b" "c")))
(put (len pairs) (join (map (fn (p) (let (((n s) p)) (format "{n}{s}"))) pairs) " "))
```
```expect
3 1a 2b 3c
```

<a id="library.rest"></a>
The prelude's `rest` is all of a list but its first item; the empty list's rest is empty,
as `drop`'s is:

```candy run
(put (len (rest (List 1 2 3))) (len (rest (List "only"))) (rest (rest (List 1))))
```
```expect
2 0 (List)
```

<a id="library.bounds"></a>
## at and slice

`(at xs i)` is the item at index `i` of a list, a tuple or a string, counting from 0, and
`i` must be `0 <= i < (len xs)`. `(slice xs i j)` is the items from index `i` up to, not
including, `j`, and needs `0 <= i <= j <= (len xs)`; a string's slice is a string. Out of
range is a panic, *lasting* ([[library.errors]]): the program stops, with `index out of
range` in its message (for an index written as a number, the rest of the message is the
target's, *for now*: [[B160]]). A negative index doesn't
count from the end, and a slice isn't cut short.

The functions that take a count, or a list that may be empty, stop at the ends instead,
*lasting*: `(take n xs)` is all of `xs` when `n` is past its end, and empty when `n` is
negative; `(drop n xs)` the reverse; `rest` of the empty list is empty; `zip` stops at the
shorter list; `(range a b)` is empty when `b <= a`; and `(repeat s n)` is `""` when `n`
is negative.

```candy run
(sig xs (List Int))
(def xs (List 10 20 30))
(sig i Int)
(def i 2)
(put (at xs 0) (at xs i) (slice xs 1 3) (slice xs 3 3) (at "abc" i) (slice "candy" 1 3))
```
```expect
10 30 (List 20 30) (List) c an
```

```candy run
(sig none (List Int))
(def none empty-list)
(put (take 5 (List 1 2)) (take -1 (List 1 2)) (drop 5 (List 1 2)) (drop -1 (List 1 2)))
(put (rest none) (zip (List 1 2 3) (List "a")) (range 3 1) (len (repeat "ab" -1)))
```
```expect
(List 1 2) (List) (List) (List 1 2)
(List) (List (Tup 1 "a")) (List) 0
```

```candy panic
(sig i Int)
(def i -1)
(put (at (List 1 2) i))
```
```expect-panic
at: index out of range: -1, for length 2
```

```candy panic
(put (at (List 1 2) 2))
```
```expect-panic
index out of range
```

```candy panic
(put (slice "abc" 2 4))
```
```expect-panic
slice: index out of range: 2 to 4, for length 3
```

```candy panic
(put (slice "abc" 2 1))
```
```expect-panic
slice: index out of range: 2 to 1
```

<a id="library.strings"></a>
## Strings

```candy run
(sig yes (Fn (Bool) String))
(defn yes (b) (if b "yes" "no"))

(put (yes (starts-with "candy" "can")) (yes (starts-with "candy" "dy")) (yes (starts-with "" "")))
(put (yes (ends-with "candy" "dy")) (yes (ends-with "candy" "can")))
(put (join (split "a,b,,c" ",") "|") (len (split "a,b,,c" ",")) (len (split "abc" ",")))
(put (repeat "ab" 3) (len (repeat "ab" 0)))
(put (to-int "42") (char-code "A") (slice "candy" 1 3))
```
```expect
yes no yes
yes no
a|b||c 4 1
ababab 0
42 65 an
```

<a id="library.maps"></a>
## Maps

A map is typed `(Map k v)`, and immutable: `map-set` returns a new one. `map-from` makes
one from a list of key-value tuples, the later of two equal keys winning; `map-keys`
lists the keys in the order they were first added. The prelude's `map-update` replaces
the value at a key, which must be in the map, by a function of it.

```candy run
(sig ages (Map String Int))
(def ages (map-from (List (Tup "ann" 30) (Tup "bo" 4) (Tup "ann" 31))))

(put (join (map-keys ages) " ") (map-get ages "ann"))
(put (map-get (map-update ages "bo" (fn (n) (+ n 1))) "bo") (map-get ages "bo"))
(put (map-get (map-set ages "cy" 7) "cy") (if (map-has ages "cy") "has cy" "no cy"))
```
```expect
ann bo 31
5 4
7 no cy
```

<a id="library.format"></a>
## format

`(format "text {form} ...")` is a string with Candy forms in `{...}` holes, one form per
hole, each written as `put` writes it ([[library.show]]); `{{` and `}}` are literal braces. It is a hack from smz (*for
now*: [[B16]]). A hole is read from the string's text,
after its escapes, so a form in a hole writes a `"` as `\"`, can't use a char literal
(`00-syntax.md`), and can't hold a brace (so no `format` inside a hole).

```candy run
(sig n Int)
(def n 6)
(put (format "{n} times 7 is {(* n 7)}, in {{braces}}"))
(put (format "{(len \"four\")}"))
```
```expect
6 times 7 is 42, in {braces}
4
```

```candy errors
(put (format "a } b")) => unmatched }
(put (format "a { b")) => unmatched {
(put (format "{1 2}")) => exactly one form
(put (format "{(format \"{1}\")}")) => a {hole} can't hold a brace
```

<a id="library.show"></a>
## show

`(show x)` is the value `x` as an expression that evaluates to it, *lasting*: a literal
as the literal (`42`, `1500l`, `1b`, `3.14f`, `10.0`, `true`, `\a`, `"a \"b\""`, `nil`),
and anything else as its constructor applied to its parts ([[types.constructors]]):
`(List 1 2)`, `(Tup 1 "a")`, `(Map (Tup "k" 1))` (*for now*, until a map literal), a
record or variant `(Vec 1 2)`, one with no fields by its name, `Dot`; a `(Maybe t)` is
`(Some x)` or `None`. It goes by `x`'s type, so `1` as a `Long` is `1l`. A float is
shown with an exponent when Python's `repr` gives one (`1.0e20`, `1.5e-5`); infinity and
not-a-number have no literal, and are shown as `inf` and `nan` (*for now*: [[B158]]). `put` and a
`format` hole show what they are given, but write a `String` or a `Char` as its text.

A function can't be shown, nor a value holding one (a list of them, or a record or variant
with one among its fields); nor can a value whose type is a type variable (*for now*:
interfaces will let a generic function say its type can be shown): all are errors when
translated. A value typed `Any` is shown from what it is when the program runs, which
can't tell a `Char` from a `String`, the integer and float sizes apart, or a `Tup` from a
`List` (*for now*: [[B18]]).

```candy run
(deft Vec ((x Int) (y Int)))
(deft Shape (Circle ((r Double))) (Dot))
(deft (Tree a) (Leaf) (Node ((l (Tree a)) (v a) (r (Tree a)))))

(put 42 1500l 1b 3.14f 10.0 true nil)
(put 1.0e20 -1.5e-5 1.0e20f (* 1.0e300 1.0e300))
(put \a "text" (show \a) (show "say \"hi\""))
(put (List 1 2) (Tup 1 "a") (rest (List 1)) (map-from (List (Tup "k" 1))))
(put (Vec 1 2) (Circle 1.0) Dot (Node Leaf 2 (Node Leaf 3 Leaf)))
(put (find (fn (n) (> n 1)) (List 1 2)) (find (fn (n) (> n 5)) (List 1 2)))
(put (format "a {(List true)} and {\"text\"}"))
(put (map show (List 1 2)))
```
```expect
42 1500l 1b 3.14f 10.0 true nil
1.0e20 -1.5e-5 1.0e20f inf
a text \a "say \"hi\""
(List 1 2) (Tup 1 "a") (List) (Map (Tup "k" 1))
(Vec 1 2) (Circle 1.0) Dot (Node Leaf 2 (Node Leaf 3 Leaf))
(Some 2) None
a (List true) and text
(List "1" "2")
```

```candy errors
(put (fn (x) x)) => show: a function can't be shown
(deft F ((f (Fn (Int) Int)))) (put (F (fn (n) n))) => show: a function can't be shown, and F holds one
(deft F ((f (Fn (Int) Int)))) (deft S (A ((f F))) (B)) (put B) => show: a function can't be shown, and S holds one
(sig f (Fn (a) Unit)) (defn f (x) (put x)) => show: can't show a value of type a, a type variable
(put empty-list) => , a type variable
```

<a id="library.maybe"></a>
## Maybe

The prelude's `(deft (Maybe a) (Some ((v a))) (None))` is a value that may be missing
(*lasting*; [[checking.maybe]]). `(find keep xs)` is the first item `keep` is true of,
`(index-of x xs)` the index of the first item equal to `x`, each `None` when there is
none, and `(with-default fallback m)` is `m`'s value, or `fallback` for `None`. They are
prelude Candy, over the built-ins `find-index` and `elem-index`, which give `-1` for none.

```candy run
(sig xs (List Int))
(def xs (List 3 1 4))
(put (find (fn (n) (> n 2)) xs) (find (fn (n) (> n 5)) xs))
(put (index-of 4 xs) (with-default -1 (index-of 9 xs)))
(put (find-index (fn (n) (= n 1)) xs) (elem-index 9 xs))
```
```expect
(Some 3) None
(Some 2) -1
1 -1
```

<a id="library.errors"></a>
## Errors

**A panic is a bug,** *lasting*: `(fail msg)`, or an index out of range
([[library.bounds]]). The program stops: it writes `candy: ` and the message to standard
error, and exits with 1, with or without `main` ([[programs.main]]). Candy can't catch a
panic, and has no exceptions (a narrow catch for tools is [[B139]]). `fail`'s result is
typed as anything, since it never returns, so it fits where any value does. The other
errors Python can raise (an integer divided by zero, a missing map key) aren't panics yet,
and stop with Python's traceback (*for now*: [[B160]]).

```candy panic
(sig half (Fn (Int) Int))
(defn half (n) (if (= (mod n 2) 0) (quot n 2) (fail (format "half: {n} is odd"))))
(put (half 4))
(put (half 3))
```
```expect-panic
candy: half: 3 is odd
```

**An expected failure is a value,** *lasting*: the prelude's `(deft (Result a e) (Ok ((v
a))) (Err ((err e))))`, either `(Ok v)`, with an `a`, or `(Err err)`, with an `e`, taken
apart with `match` ([[match.sum-types]]).

```candy run
(sig parse-number (Fn (String) (Result Int String)))
(defn parse-number (s)
  (if (is-decimal s) (Ok (to-int s)) (Err (format "not a number: {s}"))))
(sig describe (Fn ((Result Int String)) String))
(defn describe (r) (match r ((Ok v) (format "got {v}")) ((Err err) err)))
(put (parse-number "42") (parse-number "x"))
(put (describe (parse-number "42")) (describe (parse-number "x")))
```
```expect
(Ok 42) (Err "not a number: x")
got 42 not a number: x
```
