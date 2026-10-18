# Candy sum types and `match` (HLD, draft)

**Status: draft.** Nothing here is decided. This is the first design step of the
pre-self-hosting phase (branch `pre-self-host`, after tag `imvp-py-translator`). It builds
on `deft` (still **proposed**) in `doc/hl_rqmt/iMVP_py_translator.md` ("User-defined types:
`deft`", open item 4) and on the `sig` decisions there.

## Why now

Self-hosting means writing Candy code that handles Candy code. The first program that
does, `tst/cdy/read_sexpr.cdy`, has to type every form as `Any`, because a form is one of
several things: a symbol, a number, a string or a list. It tells them apart with Python's
runtime types. That is a leak (see `doc/archive/leaks_imvp_py_translator.md`, "Forms are
`Any`"). A Candy `analyse` would make it far worse: Core alone has about a dozen node
kinds, and the lowered IR has more.

In the Python translator these are unions of `NamedTuple`s (`SExpr`, `Expr`, `IrExpr`,
`Stmt`), taken apart with `match`. Candy needs the same two things:

1. a way to **declare** a type with several variants (a sum type, or tagged union);
2. a way to **take one apart**: test which variant a value is and bind its fields
   (`match`).

The alternative is to keep `Any` and add runtime predicates (`is-str`, `is-coll`, ...), as
smz did. That is cheaper, but it gives up static typing exactly where the self-hosted
translator needs it most. See open question 1.

## Declaring: `deft` with variants (proposed)

This extends the `deft` proposal (open item 4 in the iMVP doc) and follows Carp's
`deftype`, where a sum type lists its variants:

```clojure
; Carp
(deftype Shape (Circle [Double]) (Rect [Double Double]))
```

```clojure
; Candy (proposed)
(deft Shape
  (Circle ((r Double)))
  (Rect ((w Double) (h Double))))

(deft (Tree a)
  (Leaf)
  (Node ((left (Tree a)) (val a) (right (Tree a)))))

(deft Form
  (Sym ((name String)))
  (Num ((val Int)))
  (Text ((val String)))
  (Lst ((items (List Form)))))
```

- **Product or sum.** A product type has one list of fields, which starts with a list
  `((x Int) ...)`. A sum type has one or more variants, each starting with a symbol
  (`(Circle ...)`). So the two can be told apart from the form alone. A one-variant sum
  `(deft Box (Box ((v Int))))` is allowed, but a product is the usual way to write it.
- **Variant fields are named**, unlike Carp's positional `[Double]`. That keeps them like
  `deft` records, so `get` and `assoc` work on a variant too.
- **Recursive and generic.** A variant can refer to its own type (`(List Form)`,
  `(Tree a)`), and type variables work as they do for a generic `deft`.
- **Nullary variants** (`(Leaf)`) have no fields. See open question 3 for how they are
  built.

**Names.** Each variant is a constructor in the table, like a record's constructor:
`(Circle 1.0)`, `(Node l 3 r)`. The variant names share the module's global namespace with
everything else. Types are separate, so the type `Shape` and the variants `Circle` and
`Rect` are all defined.

## Taking apart: `match` (proposed)

```clojure
(sig area (Fn (Shape) Double))
(defn area (s)
  (match s
    ((Circle r) (* 3.14159 r r))
    ((Rect w h) (* w h))))

(sig count-syms (Fn (Form) Int))
(defn count-syms (f)
  (match f
    ((Sym _) 1)
    ((Lst items) (sum-syms items 0))
    (else 0)))
```

- **Clauses** are `(pattern expr)`, like `cond`'s `(test expr)`. A pattern is
  `(Variant name ...)`: it matches that variant and binds its fields by position, in the
  order of the `deft`. `_` ignores a field. The optional last clause `(else expr)` matches
  anything.
- **Flat patterns only** for a start: no nested patterns, literals or guards. Those can come
  later, along with tuple patterns, which would replace the `let`-only destructuring of
  `tup` (a stopgap in the archived leaks list).
- **Exhaustiveness.** Without `else`, every variant must have a clause. Candy's front end
  can check this, because it knows the variants from the `deft`. Then the result type
  never needs to be `(Maybe A)`. See open question 4.
- **Scope.** Each clause's names are locals, like `let` bindings, with new ids in Core.

## Through the translator layers

- **Core (`analyse`).** A new `Match(subject, clauses, default)` node, where each clause
  holds the variant name, the field locals and the body. Unlike `let`, there is no other
  form for it to desugar into: an `if` chain would need a "which variant" test and field
  access, so Core would need those as primitives anyway. `match` is also something a
  target can do well natively (Python `match`, Rust `match`, a C `switch` on a tag), so
  keeping it whole is better for `doc/hl_rqmt/multi_target.md`.
- **Top level.** `Deft` gains a variants form. The type and its variants are known in the
  `top_names` pre-pass, like other `deft`s.
- **Lowered IR (`lower`).** A `MatchStmt(subject, cases, default)` statement, with each
  case's body lowered in the current mode (`value` through a temporary, `tail` or
  `effect`). It needs no `Caps` flag at first. A target without a `match` statement can get
  an `IfStmt` chain from the backend.
- **Python (`emit_py`).** Each variant is a `NamedTuple` class, as a record is now. The sum
  type is a PEP 695 alias of their union, and mypy accepts it being recursive:

  ```python
  class Circle(NamedTuple):
      r: float

  class Rect(NamedTuple):
      w: float
      h: float

  type Shape = Circle | Rect

  def area(s: Shape) -> float:
      match s:
          case Circle(r):
              return 3.14159 * r * r
          case Rect(w, h):
              return w * h
  ```

  A positional class pattern works because `NamedTuple` sets `__match_args__`. mypy checks
  exhaustiveness: a missing case leaves a path with no return, which strict mode reports.
  In effect or value mode, an `assert_never` in a `case _:` would make it explicit.
- **Tail calls.** `loop_tail_calls` has to look inside `MatchStmt` cases, as it does
  `IfStmt` branches.

## What it would change

- `tst/cdy/read_sexpr.cdy` could return `(List Form)` instead of `Any`, and drop the
  runtime-type checks.
- `(Maybe a)` could become an ordinary sum type, `(deft (Maybe a) (Nothing) (Just ((val
  a))))`, instead of Python's `A | None`. But `nil`, `None` and `(Maybe A)` are tied
  together across the iMVP decisions, so that is open question 5, not part of this step.

## Open questions

1. **Sum types now, or `Any` plus predicates** (as smz) until the translator is
   self-hosted? Recommendation: sum types now, since the self-hosted translator is mostly
   code that takes sums apart.
2. **Syntax.** Variants inside `deft`, as above, or a separate form (`defsum`, `defenum`)?
   One form follows Carp. A separate form is easier to read and to give errors for.
3. **Nullary variants.** `defn` and `fn` need at least one argument, so is `Leaf` a value
   (`Leaf`, a singleton) or a constructor called with `nil` (`(Leaf nil)`)? A value is
   simpler, and in Python it would be an instance, `Leaf()`.
4. **Non-exhaustive `match` without `else`.** An error (proposed), or a `nil` result like
   `cond`?
5. **`Maybe`.** Keep it as `A | None` (as decided for the iMVP), or make it a real sum type
   once `match` exists?
6. **Field access.** Should `get` work on a sum-typed value only after `match` has narrowed
   it (as mypy requires), or also on a field that every variant has?
7. **Variant namespace.** Global names, as proposed, or qualified by the type
   (`Shape.Circle`), as in Carp and Rust?
