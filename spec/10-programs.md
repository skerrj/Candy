# Programs

status: stable, since: imvp-py-translator

What a program is: its top-level forms, `main`, the prelude every file gets, and `import`
(since `modules`). A program of several files can't be an example here (each example is
one file), so the examples of `import` are the programs in `tst/cdy/cdyc/` (`imports`,
`modules`); macro files and `import-macros` are in `src/cdy/candy-special.md` until they
move to `50-macros.md`.

```candy
(import name)
(sig main (Fn ((List String)) Int))
(defn main (args) expr)
```

## Top level

A program runs its top-level forms in order. The definitions (`sig`, `def`, `defn`,
`deft`, `defmacro`) and the imports are allowed only at top level.

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
```

## main (since `self-host-cleanup`)

A program that defines `main`, typed `(Fn ((List String)) Int)`, runs it after its
top-level forms, with the command-line arguments (without the program's name), and exits
with its result. `main` runs only when the program is run, not when it is imported (as
the translator's own `main`, its driver, isn't when the tests load it). A `fail` in
`main` prints `candy: ` and the message to standard error, and exits with 1
(`test_self_host.py`'s `test_bin_driver`).

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

## The prelude (since `system-prelude`)

Every file imports the prelude (`src/cdy/prelude.cdy`) without saying so: what is built
on the built-ins (declared in `src/cdy/system.cdy`), `rest` and `map-update` so far.
Macro code doesn't get it (`doc/archive/leaks_library.md`). A file's own definition of a
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
