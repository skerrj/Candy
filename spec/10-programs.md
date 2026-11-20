# Programs

status: stable, since: imvp-py-translator

What a program is: its top-level forms, `main`, the prelude every file gets, `import`
(since `modules`), and qualified and private names (since `namespaces`). A program of
several files can't be an example here (each example is one file), so the examples of
`import` are the programs in `tst/cdy/cdyc/` (`imports`, `modules`, `qualified`,
`import_list`, `private`, `library_module`); macro files and `import-macros` are in `50-macros.md`.

```candy
(import name)
(import name (name*))
(private name+)
(sig main (Fn ((List String)) Int))
(defn main (args) expr)
```

<a id="programs.top-level"></a>
## Top level

A program runs its top-level forms in order. The definitions (`sig`, `def`, `defn`,
`deft`, `defmacro`), the imports and `private` are allowed only at top level. A `def` is a
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

<a id="programs.top-do"></a>
**A top-level `do`** (since `stdlib`) is its forms, spliced into the top level, so they
may be definitions: a macro expands to one form, and this is how one defines several
things (`deftest`, [[library.test]]). A `do` in an expression still can't hold one. A
`defmacro`, `import` or `import-macros` can't be in it, since those are read before
macros are expanded.

```candy run
(defmacro defsquare (name n)
  (quasi (do (sig (unq name) Int) (def (unq name) (* (unq n) (unq n))))))
(defsquare nine 3)
(do (put "a") (sig x Int) (def x (+ nine 1)))
(put x)
```
```expect
a
10
```

```candy errors
(do (defmacro m (a) a)) => defmacro can't be in a top-level do: it is read before macros are expanded
(do (import x)) => import can't be in a top-level do: it is read before macros are expanded
(do (import-macros x)) => import-macros can't be in a top-level do: it is read before macros are expanded
```

<a id="programs.namespace"></a>
**One namespace** (since `namespaces`): a module's types, values and variants share one
namespace, *lasting*, so a type can't share its name with a value or a variant; a record's
name is both its type and its constructor.

```candy run
(deft P ((x Int)))
(sig p P)
(def p (P 3))
(put (get p x))
```
```expect
3
```

```candy errors
(deft Box ((n Int))) (sig Box Int) (def Box 1) => defined more than once: Box
(deft T (A)) (deft A ((n Int))) => defined more than once: A
(deft S (S) (B)) => defined more than once: S
```

<a id="programs.sees"></a>
**What every file sees**, unqualified and with no import, *lasting*: the special forms,
the operators and the other built-ins (`system.cdy`), and the prelude's names
([[programs.prelude]]). The built-ins are `system.name` too (since `library-layers`):
every file imports `system`, `system.cdy`, implicitly, but only qualified, so a built-in
unqualified is the last a name can mean ([[programs.shadowing]]); a library of modules is
`stdlib`'s ([[B108]]). The prelude's are `prelude.name` too. Its
macros are its own: the file's `defmacro`s, those it loads with `import-macros`
([[macros.import-macros]]), and the prelude's (`cond`, `put`); `import` doesn't pass a
module's macros on, and a macro has no qualified name.

```candy run
(put (len (List 1 2)) (with-default 0 (Some 2)) (prelude.with-default 0 None))
(sig n system.Int)
(def n (system.len (List 1 2 3)))
(put n (system.+ n 1))
```
```expect
2 2 0
3 4
```

<a id="programs.shadowing"></a>
**Shadowing**: a name means, from the innermost, a local; the file's own top-level
definition; an unqualified import's; a built-in or the prelude's, *lasting*. So a file's
definition of a built-in's name (`(defn len ...)`) is its own, in that file only, and a
local shadows everything ([[expr.let]]). A qualified name is never shadowed. A macro's
expansion sees what its use sees, the file's own definitions too, so a file's own `text`
is the one `put` calls (*for now*: [[B46]]). The translator's five built-ins
(`py-spellings`, `load-macros`, `call-macro`, `module-dir`, `fresh-name`) are only a
file's that imports `translator` ([[programs.import]]); macro code imports it
implicitly ([[macros.macro-code]]).

```candy run
(sig len (Fn (String) Int))
(defn len (s) 99)
(sig rest Int)
(def rest 5)
(put (len "ab") rest (prelude.rest (List 1 2)) (let ((rest 0)) rest))
```
```expect
99 5 (List 2) 0
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
the translator's own `main`, its driver, isn't when the tests load it). A panic in
`main`, as anywhere, prints `candy: ` and the message to standard error, and exits with 1
([[library.errors]]; `test_self_host.py`'s `test_bin_driver`). Only the top file's `main` is the program's: a `main` in a
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
on the built-ins (declared in `src/cdy/system.cdy`): `rest`, `map-update`, `Maybe`
with `find`, `index-of` and `with-default` ([[library.maybe]]), and `Result`
([[library.errors]]).
Macro code doesn't get it ([[B52]]). A file's own definition of a
prelude or built-in name wins over it; a module the file imports that defines one clashes
with it, as any two imports do ([[programs.import]]). Its names are also `prelude.name`
([[programs.qualified]]).

```candy run
(put (len (rest (List 1 2 3))))
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

`(import name)` imports the module `name.cdy`, found in the importing file's directory,
or else in the library's, next to the translator (since `library-layers`): a **library
module**. A file of the program wins over a library module of the same name, *lasting*,
so a new library module can't break a program. Two of the library's files aren't
modules, `special` and `prelude_macros`: the translator reads them itself. A
**declaration module** is a library module that declares built-ins, which the target
defines, each with a bodiless `sig` (since `library-layers`): `translator`, which declares
those only the translator needs, seen only by a file that imports it. The declaration
modules are those the target provides built-ins for, and each built-in is its module's,
`translator.fresh-name`, as a program's names are (since `stdlib`), so two declaration
modules may each declare a name. Its other forms, the `sig`s of names it defines and its
definitions, are ordinary Candy, which may use its built-ins; its importers see both
(since `stdlib`). A declaration module is
always the library's, *lasting*: a program's file of that name isn't imported in its
place, so a program can't replace a target's declarations. `name` may be
a relative path (`lib/util`). Every name the module defines at top level (`def`, `defn`,
and `deft` with its variants) becomes visible, unqualified, and as `m.name` too
([[programs.qualified]]); the names it imports don't.

`(import name (a b))` (since `namespaces`) makes only the names it lists unqualified; the
module's other names are reached as `m.name` ("b: the import of m doesn't list it: write
m.b"), and `(import name ())` makes none unqualified. Each listed name must be one the
module defines ("import: m doesn't define c"), listed once. The two forms are `import`'s
shape, declared in `special.cdy` as `(special import (ModName (Opt (List Name))))`, a
module path and, optionally, a list of names; a form that doesn't fit it is an error
written from it, `expected (import ModName [(Name*)])`. The example with a name list is
`tst/cdy/cdyc/import_list.cdy`, and with a library module
`tst/cdy/cdyc/library_module.cdy`.

- Two imports that define the same name are an error only where the name is used
  unqualified ("x is defined by a and b: write a.x or b.x"); the file's own definition of a
  name wins over both.
- Importing a module twice is fine; an import cycle is an error, and so are two modules
  with the same file name (`util` and `lib/util`).
- In a macro file, `import` pastes the file in (inclusion), as its helpers, so it lists no
  names.

```candy errors
(import) => import: expected (import ModName [(Name*)])
(import "x") => expected (import ModName [(Name*)])
(import a b) => expected (import ModName [(Name*)])
(import a (b) c) => expected (import ModName [(Name*)])
(import a (1)) => expected (import ModName [(Name*)])
(import nope) => can't find nope.cdy in . or the library
(import nope (a)) => can't find nope.cdy in . or the library
(import special) => import: special is the translator's, not a module
(import prelude_macros) => import: prelude_macros is the translator's, not a module
(import translator (nope)) => import: translator doesn't define nope
(import system) => import: every file imports system, implicitly
(put (fresh-name "x")) => fresh-name is declared by translator, which this file doesn't import: (import translator)
```

The errors that need more than one file (clashes, cycles, two modules of one name, a name
used from a module that isn't imported, a name list's) are `test_self_host.py`'s `test_module_errors`.

<a id="programs.qualified"></a>
## Qualified names (since `namespaces`)

`m.name` is the name `name` that the module imported as `m` defines, *lasting*. `m` is the
module's file stem (`lib/util` is `util`), and the prelude's is `prelude`. It reaches
anything a module defines: a value or a function, a type (`(sig p shapes.Pt)`), a
constructor (`(shapes.Circle 1.0)`), and a variant in a pattern. It is never shadowed (a
local can't hold a `.`, [[syntax.names]], and a file's own `rest` leaves `prelude.rest`
the prelude's). It reaches the module's own names, not those it imports; a built-in is
`system.name` ([[programs.sees]]), but not a special form (`if`) nor a declaration
module's built-in, which is its own module's (`translator.fresh-name`). A `/` is no qualifier:
`lib/util` is an import's path, and a name can't hold one ([[syntax.names]]). The example
with two modules is `tst/cdy/cdyc/qualified.cdy`.

```candy run
(sig m (prelude.Maybe Int))
(def m (prelude.Some 4))
(put (match m ((prelude.Some v) v) ((None) 0)) (prelude.rest (List 1 2 3)) (/ 6.0 2.0))
```
```expect
4 (List 2 3) 3.0
```

```candy errors
(put prelude.nope) => prelude.nope: prelude doesn't define nope
(sig x prelude.Nope) (def x 1) => prelude.Nope: prelude doesn't define Nope
(put nope.x) => nope.x: this file doesn't import a module nope
(put a.b.c) => a.b.c: a qualified name is m.name, one . between a module (its file name, without its path) and a name
(put .x) => .x: a qualified name is m.name
(put prelude.Maybe) => prelude.Maybe is a type, not a value
(put system.Int) => system.Int is a type, not a value
(sig x system.len) (def x 1) => system.len is a value, not a type
(put system.if) => system.if: system doesn't define if
(sig x (Maybe Int)) (def x None) (put (match x ((prelude.Some v) v) ((Some w) w) ((None) 0))) => match: more than one clause for Some
```

<a id="programs.private"></a>
## Private names (since `namespaces`)

`(private a b)`, at top level, keeps the names it lists in their module: a module that
imports it can't use them, unqualified ("a is private to m") or qualified ("m.a: a is
private to m"), nor list them (`(import m (a))`: "import: a is private to m"). Everything
else a module defines stays visible, *lasting*. A private name may be any name the file
defines but a variant: a private type's variants are private with it, and a variant
alone is an error. A private name of one import gives way to another import's name, with
no clash. In its own module a private name is an ordinary name, and a public function can
take or give a value of a private type, which the importer can hold but not name or take
apart. The example with two modules is `tst/cdy/cdyc/private.cdy`.

```candy run
(private twice Box)
(deft Box ((n Int)))
(sig twice (Fn (Int) Int))
(defn twice (n) (* 2 n))
(put (twice 3) (get (Box 4) n))
```
```expect
6 4
```

```candy errors
(private x) => private: x isn't defined in this file
(sig x Int) (def x 1) (private x x) => private: x is listed twice
(deft S (A) (B)) (private A) => private: A is a variant, private only with its type: (private S)
(private "x") => private: expected (private name ...)
(sig f (Fn (Int) Int)) (defn f (n) (do (private n) n)) => private is only allowed at top level
```
