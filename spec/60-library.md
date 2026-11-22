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
provides it, with that type. Only a declaration module (`system.cdy`, `translator.cdy`,
`math.cdy`, `string.cdy`, `map.cdy`) may have a `sig` with no definition. A built-in's arity is its type's
(`40-expressions.md`). Lists, strings and maps each have their own operations (`len` a
list's, `string.len` a string's, `map.size` a map's), *for now*, until interfaces let one
name work on each ([[B34]]). None is typed `Any`; only three of `translator`'s are, which
take or give a host function (*for now*: [[B49]]).

Each group's rule names its built-ins with their types, and what they do at the edges (an
empty list, an index out of range, a missing key or file), *lasting*. This table is the
index: every built-in is in it, and in an example that runs (`test_doc_links.py`), and
the prelude's are marked.

| Group | Rules | Built-ins |
|---|---|---|
| the operators | `40-expressions.md`: [[expr.arithmetic]], [[expr.append]], [[expr.comparisons]], [[expr.equality]], [[expr.logic]] | `+`, `-`, `*`, `/`, `quot`, `mod`, `++`, `=`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not` |
| output | [[library.put]], [[library.show]] | `put` (the prelude's, a macro), `put-line`, `text`, `show`, `put-err` |
| files | [[library.files]] | `slurp`, `spit`, `file-exists`, `make-dirs`, `path-stem`, `path-dir`, `path-join`, `path-resolve` |
| lists | [[library.lists]], [[library.map-acc]], [[library.zip]], [[library.rest]], [[library.bounds]], [[library.maybe]] | `len`, `empty-list`, `at`, `slice`, `map`, `filter`, `fold`, `map-acc`, `any`, `all`, `find-index`, `contains`, `reverse`, `range`, `take`, `drop`, `concat`, `zip`; the prelude's `rest`, `find`, `index-of`, `with-default` |
| maps (the module `map`) | [[library.maps]] | `map.empty`, `map.at`, `map.has`, `map.set`, `map.keys`, `map.from`, `map.size`; in Candy, `map.update`, `map.values`, `map.at-or` |
| strings (the module `string`) | [[library.strings]], [[library.bounds]] | `string.len`, `string.at`, `string.slice`, `string.contains`, `string.starts-with`, `string.ends-with`, `string.split`, `string.join`, `string.repeat`, `string.replace`, `string.to-int`, `string.to-float`, `string.code`, `string.hex-char`, `string.is-decimal`, `string.is-space`; in Candy, `string.trim`, `string.lines` |
| lists' Candy (the module `list`) | [[library.list]] | none: `list.last`, `list.sort`, `list.sum`, `list.flat-map`, `list.partition` are Candy |
| math (the module `math`) | [[library.math]] | `math.PI`, `math.sin`, `math.cos`, `math.tan` |
| the program | [[library.errors]], [[expr.unit]] | `fail`, `nil`; the prelude's `Result` |

```candy run
(import string ())
(put (path-stem "dir/file.cdy") (string.to-int "7") (len (range 0 3)))
```
```expect
file 7 3
```

`fail` is a panic: the program stops with its message ([[library.errors]]). Five built-ins are only for the
translator: `py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name`,
declared in `translator.cdy`, a declaration module, and seen only by a file that imports
`translator` ([[programs.import]]).

<a id="library.lists"></a>
## Lists

A list is typed `(List a)`; `List` ([[types.constructors]]) and `range` make one, and
`empty-list` is the empty one. The functions take the list last. `map`, `filter` and `fold` are built in for
speed, since Candy adds to a list by copying it. `find` and `index-of` give a `(Maybe a)`
([[library.maybe]]): `None` when nothing is found, which `with-default` replaces.

| Call | Type | Gives |
|---|---|---|
| `(len xs)` | `(Fn ((List a)) Int)` | the number of items |
| `empty-list` | `(List a)` | the list with no items |
| `(at xs i)` | `(Fn ((List a) Int) a)` | the item at `i`; out of range a panic ([[library.bounds]]) |
| `(slice xs i j)` | `(Fn ((List a) Int Int) (List a))` | the items from `i` up to `j`; out of range a panic |
| `(join strs sep)` | `(Fn ((List String) String) String)` | the strings, `sep` between them; `""` for none |
| `(map f xs)` | `(Fn ((Fn (a) b) (List a)) (List b))` | `f` of each item |
| `(filter keep xs)` | `(Fn ((Fn (a) Bool) (List a)) (List a))` | the items `keep` is true of |
| `(fold f start xs)` | `(Fn ((Fn (b a) b) b (List a)) b)` | `f` of the result so far and each item, from the left; `start` for none |
| `(map-acc f state xs)` | `(Fn ((Fn (s a) (Tup s b)) s (List a)) (Tup s (List b)))` | a `map` that threads a state ([[library.map-acc]]) |
| `(any keep xs)` | `(Fn ((Fn (a) Bool) (List a)) Bool)` | whether `keep` is true of some item; `false` for none |
| `(all keep xs)` | `(Fn ((Fn (a) Bool) (List a)) Bool)` | whether `keep` is true of every item; `true` for none |
| `(find-index keep xs)` | `(Fn ((Fn (a) Bool) (List a)) Int)` | the index of the first item `keep` is true of, or `-1` |
| `(contains x xs)` | `(Fn (equatable (List equatable)) Bool)` | whether an item is equal to `x` |
| `(reverse xs)` | `(Fn ((List a)) (List a))` | the items, last first |
| `(range a b)` | `(Fn (Int Int) (List Int))` | the integers from `a` up to, not including, `b`; empty when `b <= a` |
| `(take n xs)` | `(Fn (Int (List a)) (List a))` | the first `n` items; all past the end, none when `n` is negative |
| `(drop n xs)` | `(Fn (Int (List a)) (List a))` | all but the first `n`; none past the end, all when `n` is negative |
| `(concat xss)` | `(Fn ((List (List a))) (List a))` | the lists, one after another |
| `(zip xs ys)` | `(Fn ((List a) (List b)) (List (Tup a b)))` | the items paired, up to the shorter list ([[library.zip]]) |
| `(rest xs)`, the prelude's | `(Fn ((List a)) (List a))` | all but the first item; empty for none ([[library.rest]]) |
| `(find keep xs)`, the prelude's | `(Fn ((Fn (a) Bool) (List a)) (Maybe a))` | the first item `keep` is true of, or `None` ([[library.maybe]]) |
| `(index-of x xs)`, the prelude's | `(Fn (equatable (List equatable)) (Maybe Int))` | the index of the first item equal to `x`, or `None` |
| `(with-default x m)`, the prelude's | `(Fn (a (Maybe a)) a)` | `m`'s value, or `x` for `None` |

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

<a id="library.map-acc"></a>
`map-acc` is a `map` that threads a state: its function takes the state and an item, and
gives a tuple of the next state and the item's result; `map-acc` gives the last state and
the results. The state comes first, as `fold`'s start value does, and is taken apart with
a `Tup` pattern ([[match.tup]]):

```candy run
(sig number-words (Fn (Int String) (Tup Int String)))
(defn number-words (n w) (Tup (+ n 1) (format "{n}:{w}")))

(let (((n words) (map-acc number-words 1 (List "a" "b" "c"))))
  (put n words))
(put (map-acc number-words 7 empty-list))
```
```expect
4 (List "1:a" "2:b" "3:c")
(Tup 7 (List))
```

<a id="library.zip"></a>
`zip` pairs two lists' items into tuples, up to the shorter one's length:

```candy run
(import string ())
(sig pairs (List (Tup Int String)))
(def pairs (zip (range 1 6) (List "a" "b" "c")))
(put (len pairs) (string.join (map (fn (p) (let (((n s) p)) (format "{n}{s}"))) pairs) " "))
```
```expect
3 1a 2b 3c
```

<a id="library.list"></a>
## The list module

`list` (since `stdlib`) is a library module of Candy built on the list built-ins, which
stay `system`'s (lists are everywhere); an ordinary module, with no built-ins of its own.
A program imports it by convention with no names unqualified, `(import list ())`.

| Call | Type | Gives |
|---|---|---|
| `(list.last xs)` | `(Fn ((List a)) a)` | the last item; the empty list's a panic, as `at`'s ([[library.bounds]]) |
| `(list.sort xs)` | `(Fn ((List comparable)) (List comparable))` | the items smallest first, equal ones in their order (a merge sort) |
| `(list.sum xs)` | `(Fn ((List number)) number)` | the items added; the empty list's a panic ("list.sum: the list is empty") |
| `(list.flat-map f xs)` | `(Fn ((Fn (a) (List b)) (List a)) (List b))` | `f` of each item, a list each, joined |
| `(list.partition keep xs)` | `(Fn ((Fn (a) Bool) (List a)) (Tup (List a) (List a)))` | the items `keep` is true of, and the others |

`sum` needs an item, since a type variable's number type has no zero of its own to start
from (a literal `0` is an `Int`; *for now*: [[B216]]). Each of `sort`'s merges copies its
list as it grows (*for now*: [[B69]]).

```candy run
(import list ())
(put (list.sort (List 3 1 2 5 4 1)) (list.sort (List "b" "a" "c")) (list.sort (List 2.5 1.0)))
(put (list.last (List 1 2 3)) (list.sum (List 1 2 3)) (list.sum (List 1.5 2.0)))
(put (list.flat-map (fn (x) (List x x)) (List 1 2)) (list.partition (fn (x) (> x 1)) (List 1 2 3)))
(put (len (list.sort (reverse (range 0 500)))) (list.last (list.sort (reverse (range 0 500)))))
```
```expect
(List 1 1 2 3 4 5) (List "a" "b" "c") (List 1.0 2.5)
3 6 3.5
(List 1 1 2 2) (Tup (List 2 3) (List 1))
500 499
```

```candy panic
(import list ())
(sig none (List Int))
(def none empty-list)
(put (list.sum none))
```
```expect-panic
list.sum: the list is empty
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

`(at xs i)` is the item at index `i` of a list, counting from 0, and `i` must be `0 <= i
< (len xs)`; `(string.at s i)` is a string's `Char` at `i`, likewise. `(slice xs i j)` is
the items from index `i` up to, not including, `j`, and needs `0 <= i <= j <= (len xs)`;
`(string.slice s i j)` is a string's, a string. Out of
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
(import string ())
(sig xs (List Int))
(def xs (List 10 20 30))
(sig i Int)
(def i 2)
(put (at xs 0) (at xs i) (slice xs 1 3) (slice xs 3 3) (string.at "abc" i) (string.slice "candy" 1 3))
```
```expect
10 30 (List 20 30) (List) c an
```

```candy run
(import string ())
(sig none (List Int))
(def none empty-list)
(put (take 5 (List 1 2)) (take -1 (List 1 2)) (drop 5 (List 1 2)) (drop -1 (List 1 2)))
(put (rest none) (zip (List 1 2 3) (List "a")) (range 3 1) (string.len (string.repeat "ab" -1)))
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
(import string ())
(put (string.slice "abc" 2 4))
```
```expect-panic
string.slice: index out of range: 2 to 4, for length 3
```

```candy panic
(put (slice (List 1 2 3) 2 1))
```
```expect-panic
slice: index out of range: 2 to 1
```

```candy panic
(import string ())
(sig i Int)
(def i 3)
(put (string.at "abc" i))
```
```expect-panic
string.at: index out of range: 3, for length 3
```

<a id="library.strings"></a>
## Strings

`string` (since `stdlib`; before, its built-ins were `system`'s, as `str-len`, `char-at`,
`substring`, `str-contains`, `char-code`, `isspace` and the rest) is a library module, a
declaration module ([[programs.import]]): a string's own operations, named for what they
do, as a list's are (`string.len`, `string.at`, a `Char` ([[syntax.chars]]),
`string.slice`), *for now* until interfaces ([[B34]]); and `trim` and `lines`, in Candy.
A program imports it by convention with no names unqualified, `(import string ())`, so
`len` is still the list's ([[programs.import]]). The predicates on a whole string
(`is-decimal`, `is-space`) are `false` for `""`. Text that isn't a number, to `to-int` or
`to-float`, a `code` of a string that isn't one character, and a `split` on `""` stop
with Python's error, not a panic (*for now*: [[B160]]).

| Call | Type | Gives |
|---|---|---|
| `(string.len s)` | `(Fn (String) Int)` | the number of characters |
| `(string.at s i)` | `(Fn (String Int) Char)` | the character at `i`; out of range a panic ([[library.bounds]]) |
| `(string.slice s i j)` | `(Fn (String Int Int) String)` | the characters from `i` up to `j`; out of range a panic |
| `(string.contains part s)` | `(Fn (String String) Bool)` | whether `part` is in `s`; `true` for `""` |
| `(string.starts-with s prefix)` | `(Fn (String String) Bool)` | whether `s` starts with `prefix` |
| `(string.ends-with s suffix)` | `(Fn (String String) Bool)` | whether `s` ends with `suffix` |
| `(string.split s sep)` | `(Fn (String String) (List String))` | the parts of `s` between each `sep`, empty ones too; `(List s)` when there is none |
| `(string.join parts sep)` | `(Fn ((List String) String) String)` | the strings `parts`, `sep` between each two |
| `(string.repeat s n)` | `(Fn (String Int) String)` | `s` `n` times over; `""` when `n` isn't positive |
| `(string.replace s old new)` | `(Fn (String String String) String)` | `s` with its first `old` replaced by `new` |
| `(string.to-int s)` | `(Fn (String) Int)` | the integer `s` writes, a sign allowed |
| `(string.to-float s)` | `(Fn (String) Double)` | the number `s` writes |
| `(string.code s)` | `(Fn (String) Int)` | the code of the one character in `s` |
| `(string.hex-char s)` | `(Fn (String) String)` | the character whose code `s` writes in hexadecimal |
| `(string.is-decimal s)` | `(Fn (String) Bool)` | whether `s` is all decimal digits |
| `(string.is-space s)` | `(Fn (String) Bool)` | whether `s` is all whitespace |
| `(string.trim s)` | `(Fn (String) String)` | `s` without the whitespace at its start and end |
| `(string.lines s)` | `(Fn (String) (List String))` | `s`'s lines, without their newlines; a last newline ends a line, and `""` has none |

```candy run
(import string ())
(sig yes (Fn (Bool) String))
(defn yes (b) (if b "yes" "no"))

(put (yes (string.starts-with "candy" "can")) (yes (string.starts-with "candy" "dy")) (yes (string.starts-with "" "")))
(put (yes (string.ends-with "candy" "dy")) (yes (string.ends-with "candy" "can")))
(put (string.join (string.split "a,b,,c" ",") "|") (len (string.split "a,b,,c" ",")) (len (string.split "abc" ",")))
(put (string.repeat "ab" 3) (string.len (string.repeat "ab" 0)))
(put (string.to-int "42") (string.code "A") (string.slice "candy" 1 3))
(put (string.len "candy") (string.at "candy" 0) (= (string.at "candy" 0) \c) (string.contains "and" "candy"))
(put (string.replace "a-b-c" "-" "+") (string.to-int "-7") (string.to-float "2.5") (string.hex-char "41"))
(put (string.is-decimal "123") (string.is-decimal "") (string.is-decimal "1a") (string.is-space " \t") (string.is-space ""))
```
```expect
yes no yes
yes no
a|b||c 4 1
ababab 0
42 65 an
5 c true true
a+b-c -7 2.5 A
true false false true false
```

```candy run
(import string ())
(put (string.trim "  a b \n") (string.len (string.trim " \t")) (string.trim "x"))
(put (string.lines "a\nb\n") (string.lines "a\n\nb") (string.lines ""))
(put (len (List 1 2)) (string.len "abc"))
```
```expect
a b 0 x
(List "a" "b") (List "a" "" "b") (List)
2 3
```

<a id="library.maps"></a>
## Maps

`map` (since `stdlib`; before, its built-ins were `system`'s, as `empty-map`, `map-get`,
`map-has`, `map-set`, `map-keys`, `map-from`, `map-size`, and `map-update` the prelude's)
is a library module, a declaration module ([[programs.import]]). A map is typed
`(Map k v)`, and immutable: `map.set` returns a new one. `map.at` gives the value at a
key, as a list's and a string's `at` give the item at an index (`get` is the special form
that reads a record's field). `map.from` makes one from a list of key-value tuples, the
later of two equal keys winning; `map.keys` lists the keys in the order they were first
added. `update`, `values` and `at-or` are Candy. A program imports it by convention with
no names unqualified, `(import map ())`; the list function `map` is still the list's. A
`map.at` of a key that isn't in the map stops with Python's error, not a panic (*for
now*: [[B160]]); ask `map.has` first, or use `map.at-or`.

| Call | Type | Gives |
|---|---|---|
| `map.empty` | `(Map k v)` | the map with no keys |
| `(map.at m k)` | `(Fn ((Map k v) k) v)` | the value at `k`, which must be in `m` |
| `(map.has m k)` | `(Fn ((Map k v) k) Bool)` | whether `k` is in `m` |
| `(map.set m k v)` | `(Fn ((Map k v) k v) (Map k v))` | `m` with `v` at `k`, replacing any value there |
| `(map.keys m)` | `(Fn ((Map k v)) (List k))` | the keys, in the order they were first added |
| `(map.from pairs)` | `(Fn ((List (Tup k v))) (Map k v))` | the map of the pairs, the later of two equal keys winning |
| `(map.size m)` | `(Fn ((Map k v)) Int)` | the number of keys |
| `(map.update m k f)` | `(Fn ((Map k v) k (Fn (v) v)) (Map k v))` | `m` with `f` of the value at `k`, which must be in `m` |
| `(map.values m)` | `(Fn ((Map k v)) (List v))` | the values, in their keys' order |
| `(map.at-or m k fallback)` | `(Fn ((Map k v) k v) v)` | the value at `k`, or `fallback` if `k` isn't in `m` |

```candy run
(import map ())
(import string ())
(sig ages (Map String Int))
(def ages (map.from (List (Tup "ann" 30) (Tup "bo" 4) (Tup "ann" 31))))

(put (string.join (map.keys ages) " ") (map.at ages "ann"))
(put (map.at (map.update ages "bo" (fn (n) (+ n 1))) "bo") (map.at ages "bo"))
(put (map.at (map.set ages "cy" 7) "cy") (if (map.has ages "cy") "has cy" "no cy"))
(put (map.size ages) (map.size (map.set ages "cy" 7)))
(sig none (Map String Int))
(def none map.empty)
(put (map.size none) (map.keys none) (map.has none "ann"))
```
```expect
ann bo 31
5 4
7 no cy
2 3
0 (List) false
```

```candy run
(import map ())
(sig ages (Map String Int))
(def ages (map.from (List (Tup "ann" 31) (Tup "bo" 4))))
(put (map.values ages) (map.at-or ages "bo" 0) (map.at-or ages "cy" 0))
(put (map (fn (n) (* n 2)) (map.values ages)))
```
```expect
(List 31 4) 4 0
(List 62 8)
```

<a id="library.files"></a>
## Files

A path is a `String`, relative to the directory the program runs in, with `/` between its
parts. `slurp` reads the path it is given, with no search; a file it can't read is a
panic ([[library.errors]]). A file `spit` can't write (its directory missing, say) stops
with Python's error, not a panic (*for now*: [[B160]]).

| Call | Type | Gives |
|---|---|---|
| `(slurp path)` | `(Fn (String) String)` | the file's text; one it can't read a panic |
| `(spit path s)` | `(Fn (String String) Unit)` | writes `s` to the file, replacing what was there |
| `(file-exists path)` | `(Fn (String) Bool)` | whether `path` is a file; `false` for a directory |
| `(make-dirs path)` | `(Fn (String) Unit)` | makes the directory, and those above it; nothing if it is there |
| `(path-stem path)` | `(Fn (String) String)` | the file's name without its extension |
| `(path-dir path)` | `(Fn (String) String)` | the directory part; `"."` for a bare name |
| `(path-join dir name)` | `(Fn (String String) String)` | `name` inside `dir` |
| `(path-resolve path)` | `(Fn (String) String)` | `path` made absolute, with `..` and links resolved |

```candy run
(sig dir String)
(def dir (path-join "output" "spec"))
(sig file String)
(def file (path-join dir "note.txt"))
(do (make-dirs dir) (make-dirs dir) (spit file "hi") (spit file "again"))
(put (slurp file) (file-exists file) (file-exists dir))
(put (path-stem "src/cdy/core.cdy") (path-dir "src/cdy/core.cdy") (path-dir "core.cdy"))
(put file (= (path-resolve "src/../src") (path-resolve "src")))
```
```expect
again true false
core src/cdy .
output/spec/note.txt true
```

<a id="library.math"></a>
## Math

`math` (since `stdlib`; before, `PI` and the trigonometric functions were `system`'s) is a
library module, a declaration module ([[programs.import]]): `PI` and the trigonometric
functions are built-ins, on `Double`s, an angle in radians; `abs`, `min` and `max` are
Candy, on any number or any comparable type. A program imports it by name, by convention
with no names unqualified, `(import math ())`, and writes `math.sin`.

| Call | Type | Gives |
|---|---|---|
| `math.PI` | `Double` | π, as near as a `Double` is |
| `(math.sin x)`, `(math.cos x)`, `(math.tan x)` | `(Fn (Double) Double)` | the sine, cosine and tangent of `x` |
| `(math.abs x)` | `(Fn (number) number)` | `x` without its sign |
| `(math.min a b)`, `(math.max a b)` | `(Fn (comparable comparable) comparable)` | the smaller, the larger (`a` if they are equal) |

```candy run
(import math ())
(put math.PI (math.sin 0.0) (math.cos 0.0) (math.tan 0.0))
(put (< (- 1.0 (math.sin (/ math.PI 2.0))) 1.0e-9))
(put (math.abs -3) (math.abs 2.5) (math.min 3 1) (math.max "a" "b"))
```
```expect
3.141592653589793 0.0 1.0 0.0
true
3 2.5 1 b
```

```candy errors
(put (sin 0.0)) => sin is declared by math, which this file doesn't import: (import math)
(import math ()) (put (math.abs "a")) => expected
```

<a id="library.format"></a>
## format

`(format "text {form} ...")` is a string with Candy forms in `{...}` holes, one form per
hole, each written as `put` writes it ([[library.show]]); `{{` and `}}` are literal braces. It is a hack from smz (*for
now*: [[B16]]). A hole is read from the string's text,
after its escapes, so a form in a hole writes a `"` as `\"`, can't use a char literal
(`00-syntax.md`), and can't hold a brace (so no `format` inside a hole).

```candy run
(import string ())
(sig n Int)
(def n 6)
(put (format "{n} times 7 is {(* n 7)}, in {{braces}}"))
(put (format "{(string.len \"four\")}"))
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
(import map ())
(deft Vec ((x Int) (y Int)))
(deft Shape (Circle ((r Double))) (Dot))
(deft (Tree a) (Leaf) (Node ((l (Tree a)) (v a) (r (Tree a)))))

(put 42 1500l 1b 3.14f 10.0 true nil)
(put 1.0e20 -1.5e-5 1.0e20f (* 1.0e300 1.0e300))
(put \a "text" (show \a) (show "say \"hi\""))
(put (List 1 2) (Tup 1 "a") (rest (List 1)) (map.from (List (Tup "k" 1))))
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

A program's type with the same name as a built-in type ([[programs.shadowing]]) is shown
as the program's (since `library-layers`):

```candy run
(deft Map ((x Int)))
(sig m Map)
(def m (Map 1))
(put (get m x) m)
```
```expect
1 (Map 1)
```

```candy errors
(put (fn (x) x)) => show: a function can't be shown
(deft F ((f (Fn (Int) Int)))) (put (F (fn (n) n))) => show: a function can't be shown, and F holds one
(deft F ((f (Fn (Int) Int)))) (deft S (A ((f F))) (B)) (put B) => show: a function can't be shown, and S holds one
(sig f (Fn (a) Unit)) (defn f (x) (put x)) => show: can't show a value of type a, a type variable
(put empty-list) => , a type variable
```

<a id="library.put"></a>
## put

`(put x ...)` writes its arguments' texts on one line, a space between them: a prelude
macro (`src/cdy/prelude_macros.cdy`), `(put a b)` being `(put-line (++ (text a) " " (text
b)))`, *lasting*. `(text x)` is `x` as `show` writes it, but a `String` or a `Char` as
its text ([[library.show]]); `put-line` writes one `String` and a newline. Macro code has
`put-line` and `text`, not `put` (it isn't expanded, *for now*: [[B52]]).

| Call | Type | Gives |
|---|---|---|
| `(put x ...)`, the prelude's macro | any number of arguments, of any type | writes their texts, a space between, and a newline; `nil` |
| `(put-line s)` | `(Fn (String) Unit)` | writes `s` and a newline to standard output |
| `(put-err s)` | `(Fn (String) Unit)` | writes `s` and a newline to standard error |
| `(text x)` | `(Fn (a) String)` | `x` as `put` writes it |
| `(show x)` | `(Fn (a) String)` | `x` as an expression that evaluates to it ([[library.show]]) |

```candy run
(put)
(put "a" \b 3 (List "c"))
(put-line (text 1.5))
(put (map text (List "d" "e")))
(put-err "standard error") ; not part of what the example writes
```
```expect

a b 3 (List "c")
1.5
(List "d" "e")
```

```candy errors
(put (if true 1 "a")) => if: the branches are Int and String
(put-line 1) => argument 1 of put-line: expected String, got Int
```

<a id="library.maybe"></a>
## Maybe

The prelude's `(deft (Maybe a) (Some ((v a))) (None))` is a value that may be missing
(*lasting*; [[checking.maybe]]). `(find keep xs)` is the first item `keep` is true of,
`(index-of x xs)` the index of the first item equal to `x`, each `None` when there is
none, and `(with-default fallback m)` is `m`'s value, or `fallback` for `None`. They are
prelude Candy, over the built-in `find-index`, which gives `-1` for none.

```candy run
(sig xs (List Int))
(def xs (List 3 1 4))
(put (find (fn (n) (> n 2)) xs) (find (fn (n) (> n 5)) xs))
(put (index-of 4 xs) (with-default -1 (index-of 9 xs)))
(put (find-index (fn (n) (= n 1)) xs) (find-index (fn (n) (= n 9)) xs))
```
```expect
(Some 3) None
(Some 2) -1
1 -1
```

<a id="library.errors"></a>
## Errors

**A panic is a bug,** *lasting*: `(fail msg)`, an index out of range
([[library.bounds]]), or a file `slurp` can't read (it reads the path it is given, with no
search). The program stops: it writes `candy: ` and the message to standard
error, and exits with 1, with or without `main` ([[programs.main]]). Candy can't catch a
panic, and has no exceptions (a narrow catch for tools is [[B139]]). `fail`'s result is
typed as anything, since it never returns, so it fits where any value does. The other
errors Python can raise (an integer divided by zero, a missing map key) aren't panics yet,
and stop with Python's traceback (*for now*: [[B160]]).

| Call | Type | Gives |
|---|---|---|
| `(fail msg)` | `(Fn (String) a)` | never returns: the program stops, writing `candy: msg` |
| `nil` | `Unit` | `Unit`'s one value ([[expr.unit]]) |

```candy panic
(sig half (Fn (Int) Int))
(defn half (n) (if (= (mod n 2) 0) (quot n 2) (fail (format "half: {n} is odd"))))
(put (half 4))
(put (half 3))
```
```expect-panic
candy: half: 3 is odd
```

```candy panic
(import string ())
(put (string.len (slurp "no/such/file.cdy")))
```
```expect-panic
candy: slurp: can't read no/such/file.cdy
```

**An expected failure is a value,** *lasting*: the prelude's `(deft (Result a e) (Ok ((v
a))) (Err ((err e))))`, either `(Ok v)`, with an `a`, or `(Err err)`, with an `e`, taken
apart with `match` ([[match.sum-types]]).

```candy run
(import string ())
(sig parse-number (Fn (String) (Result Int String)))
(defn parse-number (s)
  (if (string.is-decimal s) (Ok (string.to-int s)) (Err (format "not a number: {s}"))))
(sig describe (Fn ((Result Int String)) String))
(defn describe (r) (match r ((Ok v) (format "got {v}")) ((Err err) err)))
(put (parse-number "42") (parse-number "x"))
(put (describe (parse-number "42")) (describe (parse-number "x")))
```
```expect
(Ok 42) (Err "not a number: x")
got 42 not a number: x
```

<a id="library.test"></a>
## Tests

`test` (since `stdlib`) is a library module for tests written in Candy, with the macros
`deftest` and `check` in the macro file `test_macros`; they write the module's names
qualified, so a file using them imports it, by convention with no names unqualified:
`(import test ())`, `(import-macros test_macros)`. `(deftest name check+)` defines `name`,
a `test.Test` (a top-level `do` of its `sig` and its `def`, [[programs.top-do]]), whose
checks are made when it runs. `(check test)`, of a `Bool`, is a `test.Check`: `test.Pass`,
or `(test.Fail text pos)`, with the expression as the program writes it and where it is.
`test.run` runs each test once, writes each failed check (where, the test, the
expression) and a count, and gives 0 if every check passed, or else 1, for `main`'s exit
status ([[programs.main]]). A failed check doesn't stop the others; a panic stops the run,
as any panic does ([[library.errors]]). A program names its tests to `test.run`: no
registry, *for now* ([[B215]]), since a module can't collect its own definitions; and a
failed check's text doesn't write a string's escapes back (*for now*: [[B214]]).

| Call | Type | Gives |
|---|---|---|
| `(deftest name check+)` | a macro | defines `name`, a `test.Test` |
| `(check test)` | a macro | `test.Pass` if `test` is true, else a `test.Fail` |
| `(test.run tests)` | `(Fn ((List test.Test)) Int)` | 0 if every check passed, else 1 |
| `(test.failures name checks)` | `(Fn (String (List test.Check)) (List String))` | a line for each failed check |

```candy run
(import test ())
(import-macros test_macros)
(deftest adds (check (= (+ 1 2) 3)) (check (= (len (List 1 2)) 2)))
(deftest compares (check (< 1 2)) (check (= (+ 1 1) 3)))
(put (test.run (List adds compares)))
```
```expect
line 4, column 42: compares: (= (+ 1 1) 3)
tests: 2, checks: 4, failed: 1
1
```

```candy errors
(import-macros test_macros) (deftest t) => expected (deftest name check ...)
(import-macros test_macros) (deftest (t) (check true)) => expected (deftest name check ...)
```
