# Macros

status: stable, since: macros

`defmacro`, quoting (`quo`, `quasi`, `unq`, `unq-sp`), `gensym`, macro files and
`import-macros`, and `cond`, the prelude's macro (`doc/hl_rqmt/macros.md`).

```candy
(defmacro name (param*) expr)
(defmacro name params expr)
(quo form)
(quasi form)
(unq expr)
(unq-sp expr)
(import-macros name)
```

<a id="macros.defmacro"></a>
## defmacro

A macro is Candy code that the translator runs on the *forms* of a call, before analysing
it; the call is replaced by the form the macro returns, which is then analysed (and
expanded again) in its place. `defmacro` is top level only; every parameter is a `Form`
(`src/cdy/form.cdy`), and no `sig` is needed. With a bare name instead of the parameter
list (Scheme style), the macro gets all the arguments as one `(List Form)`.

```candy run
(defmacro unless (test body) (quasi (if (unq test) nil (unq body))))
(defmacro add-all xs (quasi (+ 0 (unq-sp xs))))
(defmacro answer () (quo (+ 40 2)))

(unless (> 1 2) (put "unless: yes"))
(put (add-all 1 2 3 4) (answer))
```
```expect
unless: yes
10 42
```

<a id="macros.macro-code"></a>
A macro's body is **macro code**: it can use the built-ins, the prelude (`rest`, `Maybe`,
`find`; since `host-macros`), `Form` with its helpers (`form.cdy`: `sym-name`,
`list-items`, `gensym`, and the variants, such as `Sym` and `Txt`), the helpers of the
macro files it imports, and the translator's built-ins, since it imports `translator`
implicitly (`gensym` calls `fresh-name`; [[programs.import]]); not the program's own
definitions. It sees what a program sees, then, but runs while translating: it is run
on the interpreter, so what it prints, or puts in a message, is what `show` and `text`
write ([[library.show]]).

```candy run
(import string ())
(defmacro name-of (s) (Txt (sym-name s) NOWHERE))
(defmacro swap (call) (let ((items (list-items call))) (Lst (reverse items) NOWHERE)))
(defmacro first-name args
  (with-default (Txt "none" NOWHERE) (find (fn (f) (!= (sym-name f) "")) (rest args))))

(put (name-of hello))
(put (swap ("abc" string.len)))
(sig b Int)
(def b 4)
(put (first-name 1 2 "x" 4))
(put (first-name 1 2 "x" b))
```
```expect
hello
3
none
4
```

<a id="macros.checked"></a>
**Macro code is type-checked** (since `host-macros`), as a program is, before any macro
runs: a macro is a function from its arguments, a `(List Form)`, to a `Form`, and every
expression of its code is checked, whether or not the macro is called, the error at the
macro's code. In a template, an `(unq e)`'s `e` must be a `Form`, and an `(unq-sp e)`'s a
`(List Form)`. What a form contains isn't checked there (a template's `if` with no
`then`, say): the expansion is checked as the program's code, at the call
([[macros.errors-at-call]]; *for now*: [[B232]]).

```candy errors
(defmacro m (a) 5) => line 1, column 17: defmacro m: expected Form, got Int
(defmacro m (a) (list-items "x")) => line 1, column 29: argument 1 of list-items: expected Form, got String
(defmacro m (a) (quasi (+ (unq 1) 2))) => line 1, column 24: List: an item: expected Form, got Int
(defmacro m (a) (quasi (f (unq-sp a)))) => line 1, column 35: argument 2 of ++: expected (List Form), got Form
```

<a id="macros.binding"></a>
A macro's name can't be bound or defined (a value, a function, a type or a variant), and
a macro is defined once; a special form can't be a macro. A macro is its file's own
([[programs.sees]]).

```candy errors
(defmacro m) => defmacro: expected (defmacro name (params) body) or (defmacro name args body)
(defmacro m (1) a) => defmacro: a parameter must be a name
(defmacro if (a) a) => defmacro: if is a special form
(defmacro m (a) a) (defmacro m (a) a) => defmacro: m is defined twice
(sig h Int) (def h 1) (defmacro m (a) (do h a)) (m 1) => unknown name h
(defmacro m (a) a) (sig f (Fn (Int) Int)) (defn f (m) m) => m is a macro, so it can't be bound
(defmacro m (a) a) (put (let ((m 1)) m)) => m is a macro, so it can't be bound
(defmacro m (a) a) (put ((fn (m) 1) 2)) => m is a macro, so it can't be bound
(defmacro m (a) a) (deft S (Mm ((x Int)))) (put (match (Mm 1) ((Mm m) m))) => m is a macro, so it can't be bound
(defmacro m (a) a) (sig m Int) (def m 1) => m is a macro, so it can't be defined
(defmacro M (a) a) (deft S (M ((x Int)))) => M is a macro, so it can't be defined
(defmacro T (a) a) (deft T ((x Int))) => T is a macro, so it can't be defined
(defmacro m (a) a) (deft (m a) ((x a))) => m is a macro, so it can't be defined
```

<a id="macros.errors-at-call"></a>
**Errors point at the call:** a wrong number of arguments, a `fail` in the macro, a
panic in it (an index out of range, with the built-in's message: macro code runs on the
interpreter, since `host-macros`), an error the host raises while it runs, and an error
in the form it returns are all reported at the call (so these rows give the position):

```candy errors
(defmacro m (a) a)
---
(m 1 2) => line 2, column 1: m: expected 1 argument(s), got 2
(defmacro bad () (quo (if))) (put 1) (bad) => line 2, column 38: if: expected (if test then else?)
(defmacro f (a) (fail "no")) (f 1) => line 2, column 30: f: no
(defmacro f (a) (at (list-items a) 5)) (f x) => line 2, column 40: f: at: index out of range: 5, for length 0
```

<a id="macros.quoting"></a>
## Quoting

Quoting is only for macro code (*for now*). `(quo form)` is `form` unevaluated, as a
`Form`. `(quasi form)` is the same, except that inside it `(unq expr)` puts in the value
of `expr` (a `Form`), and `(unq-sp expr)`, inside a list, splices in the items of `expr`
(a `(List Form)`). `quote` is not a name (`quo` replaces it), and the `'` shorthand is
reserved for later, as a reader macro (`00-syntax.md`).

```candy run
(defmacro twice-call (f x) (quasi ((unq f) ((unq f) (unq x)))))
(defmacro call-with fs (quasi (+ (unq-sp fs))))

(sig inc (Fn (Int) Int))
(defn inc (n) (+ n 1))
(put (twice-call inc 5) (call-with 1 2 3))
```
```expect
7 6
```

```candy errors
(put (quo x)) => quo: only in macro code
(put (quasi x)) => quasi: only in macro code
(put (unq x)) => unq: only inside quasi
(put (quote x)) => unknown name quote
(defmacro m () (quo (quo x))) (m) => quo: only in macro code
(defmacro m () (quo)) => quo: expected (quo form)
(defmacro m () (quo a b)) => quo: expected (quo form)
(defmacro m () (quasi (f (unq)))) => unq: expected (unq expr)
(defmacro m () (unq-sp x)) => unq-sp: only inside quasi
(defmacro m () (quasi (unq-sp x))) => unq-sp: only inside a list in quasi
(defmacro m () (quasi (f (quasi x)))) => quasi: a quasi inside a quasi isn't supported yet
(defmacro m () (quasi (f (unq nope)))) => unknown name nope
```

<a id="macros.hygiene"></a>
**Built-ins in a template:** a symbol in a `quasi` template that names a built-in value
every file sees (an operator too) or a prelude value, as the macro's own module sees
it, is written qualified, `system.text` or `prelude.rest`, so the expansion means the
same wherever it is used: a file's own `text` doesn't change `put` (since
`host-macros`; [[programs.shadowing]]). A name the macro's module defines or imports,
a special form's, a macro's, a type's and a variant's stay as written, so an expansion
that calls a macro file's helper needs it where it is used (*for now*: [[B46]]); and a
template that binds a built-in's name binds a qualified name, an error: `gensym` is
the way.

```candy run
(defmacro size (e) (quasi (len (unq e))))

(sig len (Fn (String) Int))
(defn len (s) 99)
(sig text (Fn (Int) String))
(defn text (n) "mine")
(put (size (List 1 2)) (len "ab") (text 1))
```
```expect
2 99 mine
```

```candy errors
(defmacro m () (quasi (let ((len 1)) len))) (put (m)) => system.len: a name can't hold a ., which qualifies a name with its module (m.name)
```

<a id="macros.gensym"></a>
## gensym

`(gensym "x")` returns a new symbol, such as `x__1`, which no program can write, since
the reader rejects `__` in a name (`00-syntax.md`). So a name a macro introduces can't
capture the program's:

```candy run
(defmacro twice (e)
  (let ((x (gensym "x")))
    (quasi (let (((unq x) (unq e))) (+ (unq x) (unq x))))))

(sig x Int)
(def x 5)
(put (twice (+ x 1)))
```
```expect
12
```

<a id="macros.import-macros"></a>
## Macro files: import-macros

`(import-macros name)`, top level only, finds `name.cdy` as `import` does
(`10-programs.md`), but reads it as a **macro file**, a module of macro code (since
`host-macros`): its `defmacro`s become macros of the importing file, and its other
definitions are helpers, which run only while translating (the importing file's own
`defmacro`s can call them, unqualified; its program can't).

- A macro file's `import`s are a module's ([[programs.import]]): a name list, qualified
  names (`h.wrap`) and private names as for any module. The modules it imports are macro
  code too, since they run only while translating: they can quote, and see `Form`.
- A macro file can `import-macros` other macro files, whose macros expand in it and whose
  helpers it can call; it doesn't pass those macros on.
- Each macro file is loaded once per translation, however many files import it (since
  `host-macros`); a cycle is an error.

The examples need a second file, so they are `tst/cdy/cdyc/macro_files.cdy` and
`test_self_host.py`'s `test_macro_file_errors`, `test_macro_file_is_a_module` and
`test_macro_file_loads_once`.

```candy errors
(import-macros) => import-macros: expected (import-macros name)
(import-macros nope) => import-macros: can't find nope.cdy in . or the library
(put (import-macros m)) => import-macros is only allowed at top level
```

<a id="macros.cond"></a>
## cond

`cond` (`40-expressions.md`) is a macro, from the prelude's macros
(`src/cdy/prelude_macros.cdy`), which every file gets without `import-macros`. Like any
macro's, its name can't be bound or defined.

```candy errors
(put (cond ((= 1 1) 2) 3)) => cond: clause must be (test expr)
(sig cond Int) (def cond 1) => cond is a macro, so it can't be defined
(put (let ((cond 1)) cond)) => cond is a macro, so it can't be bound
```
