# Programs

status: stable, since: imvp-py-translator

What a program is: its top-level forms, `main`, the prelude every file gets, and `import`
(since `modules`). A program of several files can't be an example here (each example is
one file), so the examples of `import` are the programs in `tst/cdy/cdyc/` (`imports`,
`modules`); macro files and `import-macros` are in `50-macros.md`.

```candy
(import name)
(sig main (Fn ((List String)) Int))
(defn main (args) expr)
```

<a id="programs.top-level"></a>
## Top level

A program runs its top-level forms in order. The definitions (`sig`, `def`, `defn`,
`deft`, `defmacro`) and the imports are allowed only at top level. A `def` is a
constant (*lasting*): it is defined once and no form changes it; a mutable cell, if one
comes, will be a form of its own.

```candy run
(put "first")
(sig x Int)
(def x 2)
(put (* x 21))
```
```expect
first
42
```

```candy errors
(put (do (sig x Int))) => sig is only allowed at top level
(put (do (def x 1))) => def is only allowed at top level
(put (do (defn f (x) x))) => defn is only allowed at top level
(put (do (deft T (A)))) => deft is only allowed at top level
(put (do (defmacro m (a) a))) => defmacro is only allowed at top level
(put (do (import x))) => import is only allowed at top level
(sig x Int) (def x 1) (def x 2) => defined more than once: x
```

<a id="programs.def-order"></a>
**Definition order:** a `def`'s initial value and a top-level expression run when the
program starts, so each top-level name they use must be defined before them: a value
(`def`), a function (`defn`), or a record's or variant's constructor (`deft`). So must
each name used by the body of a function they use, and by the functions that body uses,
and so on: those bodies run then too. A `fn` written in them counts as called. Otherwise
it is an error when translated, *lasting* (a `def` that uses itself, or a cycle, too).
The body of a function that nothing runs at the start can use any top-level name,
before or after it, so functions can call each other in any order.

```candy run
(sig even (Fn (Int) Bool))
(defn even (n) (if (= n 0) true (odd (- n 1))))
(sig odd (Fn (Int) Bool))
(defn odd (n) (if (= n 0) false (even (- n 1))))
(sig base Int)
(def base 10)
(sig scaled (Fn (Int) Int))
(defn scaled (n) (* n base))
(sig x Int)
(def x (scaled 4))
(put x (even x))
```
```expect
40 true
```

So mutual recursion is in any order, and so is a reference inside another function's
body: `total` below uses `offset`, defined after it, and is only called after both. Types
are in any order too, since a type is only read by the translator (in Python, an
annotation, which isn't run): a `sig` or a field can name a `deft` that comes later, and
two `deft`s can name each other. So are macros: a `defmacro` can come after its uses,
since a file's macros are all compiled before any is expanded.

```candy run
(sig total (Fn (Int) Int))
(defn total (n) (+ n offset))
(sig offset Int)
(def offset 5)

(sig wrap (Fn (Int) Box))
(defn wrap (n) (Box (Item n)))
(deft Box ((item Item)))
(deft Item ((n Int)))

(deft Tree (Leaf) (Node ((kids Forest))))
(deft Forest (Empty) (More ((first Tree) (others Forest))))
(sig f Forest)
(def f (More (Node Empty) Empty))

(put (total 1) (wrap 2) f (twice 3))
(defmacro twice (x) (quasi (* 2 (unq x))))
```
```expect
6 (Box (Item 2)) (More (Node Empty) Empty) 6
```

```candy errors
(sig x Int) (def x y) (sig y Int) (def y 1) => y is used before its def
(put y) (sig y Int) (def y 1) => y is used before its def
(sig x Int) (def x (+ x 1)) => x is used before its def
(sig x Int) (def x (g 1)) (sig g (Fn (Int) Int)) (defn g (n) n) => g is used before its defn
(sig x S) (def x (A 1)) (deft S (A ((v Int))) (B)) => A is used before its deft
(sig f (Fn (Int) Int)) (defn f (n) (+ n y)) (sig x Int) (def x (f 1)) (sig y Int) (def y 1) => y is used before its def, through f
(sig f (Fn (Int) Int)) (defn f (n) (h n)) (sig h (Fn (Int) Int)) (defn h (n) y) (sig x Int) (def x (f 1)) (sig y Int) (def y 1) => line 1, column 101: y is used before its def, through f
(sig k (Fn (Int) Int)) (def k (fn (n) (+ n y))) (sig y Int) (def y 1) => y is used before its def
```

<a id="programs.main"></a>
## main (since `self-host-cleanup`)

A program that defines `main`, typed `(Fn ((List String)) Int)`, runs it after its
top-level forms, with the command-line arguments (without the program's name), and exits
with its result. `main` runs only when the program is run, not when it is imported (as
the translator's own `main`, its driver, isn't when the tests load it). A `fail` in
`main` prints `candy: ` and the message to standard error, and exits with 1
(`test_self_host.py`'s `test_bin_driver`). Only the top file's `main` is the program's: a `main` in a
module it imports is an ordinary function (`tst/cdy/cdyc/modules.cdy`, whose `lib/tags`
defines one).

```candy run
(sig main (Fn ((List String)) Int))
(defn main (args) (do (put (format "main: {(len args)} argument(s)")) 0))

(put "top level first")
```
```expect
top level first
main: 0 argument(s)
```

```candy errors
(sig main Int) (def main 1) => main must be a defn
(sig main (Fn (Int) Int)) (defn main (n) n) => main must be typed
```

<a id="programs.prelude"></a>
## The prelude (since `system-prelude`)

Every file imports the prelude (`src/cdy/prelude.cdy`) without saying so: what is built
on the built-ins (declared in `src/cdy/system.cdy`): `rest`, `map-update`, and `Maybe`
with `find`, `index-of` and `with-default` ([[library.maybe]]).
Macro code doesn't get it ([[B52]]). A file's own definition of a
prelude or built-in name wins over it; a module the file imports that defines one is a
clash, as between any two imports.

```candy run
(put (len (rest (tup 1 2 3))))
```
```expect
2
```

```candy run
(sig rest Int)
(def rest 7)
(sig map Int)
(def map 8)
(put rest map)
```
```expect
7 8
```

<a id="programs.import"></a>
## import (since `modules`)

`(import name)` imports the module `name.cdy`, found in the importing file's directory;
`name` may be a relative path (`lib/util`). Every name the module defines at top level
(`def`, `defn`, and `deft` with its variants) becomes visible, unqualified; the names it
imports don't (*for now*: `doc/hl_rqmt/modules.md`, with `import-as` and `import-from`
later).

- Two imports that define the same name are an error; the file's own definition of a name
  wins over an import's.
- Importing a module twice is fine; an import cycle is an error, and so are two modules
  with the same file name (`util` and `lib/util`).
- In a macro file, `import` pastes the file in (inclusion), as its helpers.

```candy errors
(import) => expected (import name)
(import "x") => expected (import name)
(import a b) => expected (import name)
(import nope) => can't find nope.cdy in .
```

The errors that need more than one file (clashes, cycles, two modules of one name, a name
used from a module that isn't imported) are `test_self_host.py`'s `test_module_errors`.
