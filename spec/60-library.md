# The library

status: stable, since: system-prelude

The built-ins (`src/cdy/system.cdy`), the prelude (`src/cdy/prelude.cdy`) and `format`
(`doc/hl_rqmt/system_prelude.md`, `doc/hl_rqmt/library.md`). The operators are in
`40-expressions.md`.

Lists, tuples, strings and maps are the host's, so their operations are built-ins, which
the runtime provides (`src/cdy_rt/primitives.py`); the prelude holds what is built on
them. The examples print lists and `Bool`s through small helpers, since a list or a `Bool`
prints the way Python prints it (*for now*: `spec/README.md`).

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

`fail` stops the program with a message (Candy has no exceptions yet); in `main` it
prints `candy: ` and the message (`10-programs.md`). Five built-ins are only for the
translator: `py-spellings`, `load-macros`, `call-macro`, `module-dir` and `fresh-name`.

<a id="library.lists"></a>
## Lists

A list is typed `(List a)`; `tup` and `range` make one, and `empty-list` is the empty
one. The functions take the list last. `map`, `filter` and `fold` are built in for
speed, since Candy adds to a list by copying it. `find` and `index-of` give a `(Maybe a)`:
`nil` when nothing is found, which `with-default` replaces.

```candy run
(sig show (Fn ((List Int)) String))
(defn show (xs) (+ "[" (join (map (fn (n) (format "{n}")) xs) " ") "]"))
(sig yes (Fn (Bool) String))
(defn yes (b) (if b "yes" "no"))

(sig nums (List Int))
(def nums (range 1 6))

(put (show nums) (show (range 3 3)))
(put (show (map (fn (n) (* n n)) nums)) (show (filter (fn (n) (> n 2)) nums)))
(put (fold (fn (acc n) (+ acc n)) 0 nums))
(put (yes (any (fn (n) (> n 4)) nums)) (yes (any (fn (n) (> n 5)) nums)) (yes (any (fn (n) true) empty-list)))
(put (yes (all (fn (n) (> n 0)) nums)) (yes (all (fn (n) (> n 1)) nums)) (yes (all (fn (n) false) empty-list)))
(put (with-default 0 (find (fn (n) (> n 2)) nums)) (with-default 0 (find (fn (n) (> n 9)) nums)))
(put (show (reverse nums)) (show (reverse empty-list)))
(put (show (take 2 nums)) (show (take 9 nums)) (show (take -1 nums)))
(put (show (drop 2 nums)) (show (drop 9 nums)))
(put (show (concat (tup (tup 1 2) empty-list (tup 3)))))
(put (with-default -1 (index-of 3 nums)) (with-default -1 (index-of 9 nums)))
(put (yes (contains 3 nums)) (yes (contains 9 nums)))
```
```expect
[1 2 3 4 5] []
[1 4 9 16 25] [3 4 5]
15
yes no no
yes no yes
3 0
[5 4 3 2 1] []
[1 2] [1 2 3 4 5] []
[3 4 5] []
[1 2 3]
2 -1
yes no
```

<a id="library.zip"></a>
`zip` pairs two lists' items into tuples, up to the shorter one's length:

```candy run
(sig pairs (List (Tup Int String)))
(def pairs (zip (range 1 6) (tup "a" "b" "c")))
(put (len pairs) (join (map (fn (p) (format "{(at p 0)}{(at p 1)}")) pairs) " "))
```
```expect
3 1a 2b 3c
```

<a id="library.rest"></a>
The prelude's `rest` is all of a list but its first item:

```candy run
(put (len (rest (tup 1 2 3))) (len (rest (tup "only"))))
```
```expect
2 0
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
(def ages (map-from (tup (tup "ann" 30) (tup "bo" 4) (tup "ann" 31))))

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
hole, each shown as text; `{{` and `}}` are literal braces. It is a hack from smz (*for
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
