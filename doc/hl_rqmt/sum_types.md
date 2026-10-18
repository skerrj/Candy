# Candy sum types and `match` (HLD)

**Status: decided and implemented** (stage 0 of `doc/hl_rqmt/self_hosting_primo.md`).
All seven open questions are answered (see the end). Tests: `tst/cdy/sums.cdy` (golden),
and `test_core_cdy.py`/`test_lower_cdy.py`. This is the first design step of the
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

## Declaring: `deft` with variants (decided)

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

## Taking apart: `match` (decided)

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

- **Core (`analyse`).** A new `Match(subject, clauses, default)` node, where each
  `Clause` holds the variant name, the `(field, Local)` pairs it binds (`_` is left out)
  and the body. Unlike `let`, there is no other
  form for it to desugar into: an `if` chain would need a "which variant" test and field
  access, so Core would need those as primitives anyway. `match` is also something a
  target can do well natively (Python `match`, Rust `match`, a C `switch` on a tag), so
  keeping it whole is better for `doc/hl_rqmt/multi_target.md`.
- **Top level.** A sum is its own node, `DeftSum(name, tvars, variants)`, next to `Deft`
  for records. The `top_names` pre-pass finds the type and its variants (with their field
  names, as `VariantInfo`), so `match` and calls can check them before the `deft` is
  analysed. Variant names are values, the sum's name is only a type, and all of them share
  one namespace with other top-level names (a variant can't take its type's name).
- **Lowered IR (`lower`).** A `MatchStmt(subject, cases, default)` statement, with each
  case's body lowered in the current mode (`value` through a temporary, `tail` or
  `effect`), and `SumDef` for the type. The subject is always simple. It needs no `Caps`
  flag: each backend writes `MatchStmt` its own way (Python: an `isinstance` chain).
- **Python (`emit_py`).** Each variant is a `NamedTuple` class, as a record is now; a
  variant is generic only in the type variables its fields use, and one with no fields
  gets `pass`. The sum type is a PEP 695 alias of their union, which may be recursive. A
  variant with no fields is built with no arguments, `Leaf()`.

  **`match` is not emitted as Python's `match`** (as built). mypy (2.4) loses a generic
  variant's type arguments in a class pattern: in `case Node(l, v, r):` on a
  `Tree[int]`, `v` is `Any`, and strict mode rejects the result. It keeps them when
  `isinstance` narrows, so `match` becomes an `isinstance` chain that binds each named
  field by attribute (`_` binds nothing):

  ```python
  class Leaf(NamedTuple):
      pass

  class Node[a](NamedTuple):
      left: Tree[a]
      val: a
      right: Tree[a]

  type Tree[a] = Leaf | Node[a]

  def size(t: Tree[int]) -> int:
      if isinstance(t, Leaf):
          return 0
      elif isinstance(t, Node):
          l = t.left
          r = t.right
          return 1 + size(l) + size(r)
  ```

  The subject is tested more than once, so `lower` stores a subject that isn't simple in
  a temporary first. `analyse` checks exhaustiveness, and mypy sees that the chain covers
  the union, so a function that returns from every case needs no fallback `return`.
  pyright handles class patterns fine, so a later Python backend could switch back.
- **Tail calls.** `loop_tail_calls` looks inside `MatchStmt` cases, as it does
  `IfStmt` branches.

## What it changes

- `tst/cdy/read_sexpr.cdy` could return `(List Form)` instead of `Any`, and drop the
  runtime-type checks.
- `(Maybe a)` could become an ordinary sum type, `(deft (Maybe a) (Nothing) (Just ((val
  a))))`, instead of Python's `A | None`. But `nil`, `None` and `(Maybe A)` are tied
  together across the iMVP decisions, so that is open question 5, not part of this step.

## Open questions

1. ~~**Sum types now, or `Any` plus predicates** (as smz) until the translator is
   self-hosted?~~ **Sum types now** (decided as a consequence of choice A in
   `doc/hl_rqmt/self_hosting_primo.md`: forms at the boundary are `deft` variants).
2. ~~**Syntax.**~~ Variants inside `deft` (**decided**), following Carp.
3. ~~**Nullary variants.**~~ A value, `Leaf` (**decided**); `(Leaf)` is an error. The
   pattern is `(Leaf)`. In Python it is `Leaf()`.
4. ~~**Non-exhaustive `match` without `else`.**~~ An error (**decided**): without `else`,
   every variant needs a clause.
5. ~~**`Maybe`.**~~ Stays `A | None` for now (**decided**); revisit after self-hosting.
6. ~~**Field access.**~~ `get` on a sum-typed value only after `match` has narrowed it
   (**decided**). Candy doesn't check this yet; mypy does.
7. ~~**Variant namespace.**~~ Global names (**decided**), no `Shape.Circle`.
