# Types, definitions and records

status: stable, since: imvp-py-translator

The type names, `sig` and `def`, records (`deft` with one field list) with `get` and
`assoc`, and tuples. Functions (`defn`, `fn`) are in `40-expressions.md`, and sum types
in `30-match.md`.

```candy
(sig name Type)
(def name init)
(deft Name ((field Type)*))
(deft (Name tvar+) ((field Type)*))
(get expr field)
(assoc expr field value (field value)*)
(tup expr+)
```

## Types

| Type | Values |
|---|---|
| `Int`, `Long`, `Byte` | whole numbers |
| `Float`, `Double` | floating-point numbers |
| `Bool` | `true`, `false` |
| `Char`, `String` | a character, text |
| `Unit` | `nil` only |
| `(List a)` | a list of `a`s, of any length |
| `(Tup a b ...)` | a fixed-size tuple: an `a`, then a `b`, ... |
| `(Map k v)` | a map from `k`s to `v`s |
| `(Maybe a)` | an `a`, or `nil` |
| `(Fn (a b ...) r)` | a function from an `a`, a `b`, ... to an `r` |
| `Name`, `(Name a ...)` | a `deft` type, possibly generic |
| `Any` | anything: an escape hatch, which turns checking off |

Type names are Capitalised; lowercase names in a type are type variables (`a`, `b`), so a
function can be generic:

```candy run
(sig id (Fn (a) a))
(defn id (v) v)
(put (id 3) (id "three"))
```
```expect
3 three
```

**Types are checked by mypy, not by the translator** (*for now*: Candy has no type checker
yet, `doc/archive/leaks_imvp_py_translator.md`). The translator turns each type into a
Python annotation, and `mypy --strict` checks the translation: the spec runner checks
every `candy run` example that way. So a type error, an unknown type name, or a value
used as a function, translates, and only mypy or the run rejects it. The translator
checks a type's shape where it needs it (a function type for `defn`, below).

## sig and def

`(sig name Type)` gives a top-level name its type. Every top-level `def` and `defn` needs
one, anywhere before its definition, one per name. `(def name init)` defines a value; the
initial value is required. Both are top level only (`10-programs.md`), and a name is
defined once. No form changes a `def`'s value yet (whether one will is open:
`doc/hl_rqmt/mutation_optimization.md`).

A top-level function can call one defined after it, but a value is only there once its
`def` has run (forms run in order), so using it earlier fails at run time with Python's
`NameError` (*for now*: `doc/leaks.md`).

```candy run
(sig double (Fn (Int) Int))
(sig quad (Fn (Int) Int))
(defn quad (n) (double (double n)))
(defn double (n) (* n 2))

(sig x Int)
(def x (quad 3))
(put x)
```
```expect
12
```

```candy errors
(def x 1) => x needs a (sig x Type)
(sig x) => sig: expected (sig name Type)
(sig 1 Int) => sig: expected (sig name Type)
(sig y Int) => sig for y, but no def or defn of y in this file
(sig x Int) (def x 1) (sig x Int) => sig for x comes after its definition
(sig x Int) (sig x Int) (def x 1) => more than one sig
(sig x Int) (def x 1) (def x 2) => defined more than once: x
(sig x Int) (def x) => the initial value is required
(sig x (Fn Int)) (def x 1) => bad function type: expected (Fn (Arg+) Ret)
(sig f Int) (defn f (x) x) => its sig must be a function type with one type per argument
(sig f (Fn (Int) Int)) (defn f (x y) x) => one type per argument
```

## Records

A record is a `deft` with one field list: each field a name and its type. The type's
name is also its constructor, taking the fields in order. `get` reads a field, and
`assoc` makes a copy with fields replaced, written as flat `field value` pairs; neither
evaluates the field's name. A record is immutable (*for now*:
`doc/hl_rqmt/mutation_optimization.md`). A record can be generic.

```candy run
(deft Vec ((x Int) (y Int)))

(sig v Vec)
(def v (Vec 1 2))
(sig w Vec)
(def w (assoc v x 3 y 4))
(put (get v x) (get v y))
(put (get w x) (get w y))

(deft (Box a) ((item a)))
(put (get (Box "boxed") item))
```
```expect
1 2
3 4
boxed
```

```candy errors
(deft V) => deft: expected (deft Name ((field Type)+))
(deft V ((x))) => deft: field must be (name Type)
(deft V ((x Int))) (deft V ((y Int))) => defined more than once: V
(put (get 1)) => expected (get obj field)
(put (assoc 1 x)) => expected (assoc obj field value
(put (assoc 1 x 2 y)) => expected (assoc obj field value
```

The translator doesn't check a record constructor's arguments, or the fields `get` and
`assoc` name (*for now*: `doc/leaks.md`): a wrong number of arguments, or a field the
record doesn't have, fails only in mypy or at run time, with Python's error.

## Tuples

`(tup expr+)` makes a fixed-size tuple of at least one item, typed `(Tup a b ...)`. `at`
reads an item by its position, from 0, and `len` is its size. A tuple is taken apart with
a `tup` pattern, in `match` or a `let` binding (`30-match.md`).

```candy run
(sig p (Tup Int String Int))
(def p (tup 1 "two" 3))
(put (at p 1) (len p))
```
```expect
two 3
```

```candy errors
(put (tup)) => at least one item
```
