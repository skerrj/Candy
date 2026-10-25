# Sum types and match

status: stable, since: self-host-py

A sum type lists its variants; `match` takes a value of it apart. Tuples are taken apart
with `match` too (since `self-host-cleanup`). Records (`deft` with one field list), `get`
and `assoc` are in `src/cdy/candy-special.md` until they move to `20-types.md`.

```candy
(deft Name (Variant ((field Type)*)?)+)
(deft (Name tvar+) (Variant ((field Type)*)?)+)
(match expr ((Variant name*) expr)+ (else expr)?)
(match expr ((tup name+) expr))
```

## Declaring a sum type

`deft` with one or more variants, each a Capitalised name and, unless it has none, its
fields. Each variant is also its constructor, taking the fields in order; a variant with
no fields is a value, not a call. `deft` is top level only.

```candy run
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))) (Dot))

(sig area (Fn (Shape) Int))
(defn area (s) (match s ((Circle r) (* 3 r r)) ((Rect w h) (* w h)) ((Dot) 0)))

(put (area (Circle 2)))
(put (area (Rect 2 5)))
(put (area Dot))
```
```expect
12
10
0
```

A variant's fields are named, as a record's are, so `get` reads one:

```candy run
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))))
(put (get (Rect 4 5) h))
```
```expect
5
```

A sum can be generic and recursive:

```candy run
(deft (Tree a) (Leaf) (Node ((left (Tree a)) (val a) (right (Tree a)))))

(sig size (Fn ((Tree Int)) Int))
(defn size (t) (match t ((Leaf) 0) ((Node l _ r) (+ 1 (size l) (size r)))))

(put (size (Node (Node Leaf 1 Leaf) 2 (Node Leaf 3 Leaf))))
```
```expect
3
```

Types and values share one namespace *for now* (so a type and a variant can't both be
named `Box`), and variant names must be Capitalised:

```candy errors
(deft Box (Box ((v Int)))) => defined more than once: Box
(deft S2 (A) (b)) => variant names are Capitalised
(deft S2 (A ())) => variant must be
```

Constructors take exactly their fields:

```candy errors
(deft Shape (Rect ((w Int) (h Int))) (Dot)) (put (Rect 1)) => takes 2 field
(deft Shape (Rect ((w Int) (h Int))) (Dot)) (put (Dot)) => it is a value
```

## Taking it apart: match

A clause is `(pattern expr)`. A pattern `(Variant name ...)` matches that variant and binds
its fields by position, in the order of the `deft`; `_` skips one. The names are new
locals, scoped to the clause, and shadow outer ones. `match` is an expression: its value is
the chosen clause's.

```candy run
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))))

(sig width (Fn (Shape) Int))
(defn width (s) (match s ((Circle r) (* 2 r)) ((Rect w _) w)))

(sig w Int)
(def w 100)
(put (+ (width (Circle 3)) (width (Rect 4 9))))
(put w)
```
```expect
10
100
```

**Exhaustive:** without `else`, every variant needs a clause, and each variant gets at most
one. The optional last clause `(else expr)` matches whatever is left.

```candy run
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))) (Dot))

(sig kind (Fn (Shape) String))
(defn kind (s) (match s ((Circle _) "round") (else "not round")))

(put (kind (Circle 1)))
(put (kind Dot))
```
```expect
round
not round
```

```candy error
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))) (Dot))
(put (match (Circle 1) ((Circle r) r)))
```
```expect-error
match on Shape: no clause for Rect, Dot (or add else)
```

The clauses, case by case:

```candy errors
(deft Shape (Circle ((r Int))) (Rect ((w Int) (h Int))) (Dot))
(sig s Shape)
(def s Dot)
---
(put (match s ((Circle r) r) ((Circle r) r) (else 1))) => more than one clause for Circle
(put (match s ((Circle) 1) (else 2))) => pattern needs that many names
(put (match s ((Rect a a) a) (else 2))) => must be different
(put (match s (else 1))) => after a pattern
(put (match s (else 1) ((Dot) 2))) => must be the last clause
(put (match s ((Nope x) x))) => not a variant
(put (match s (x 1))) => pattern must be
(put (match s)) => expected (match
(deft B (T) (F)) (put (match s ((Dot) 1) ((T) 2) (else 3))) => mix variants of Shape and B
```

Patterns are flat *for now*: a pattern names a variant and its fields' names, with no
nested patterns, literals or guards (`doc/hl_rqmt/sum_types.md`).

## Taking a tuple apart

A `tup` pattern binds a tuple's items by position (`_` skips one). A tuple has one shape,
so its clause is the only one, with no `else`. It works wherever an expression goes, and
in a `let` binding as `((a b) init)`.

```candy run
(sig divmod (Fn (Int Int) (Tup Int Int)))
(defn divmod (a b) (tup (quot a b) (- a (* b (quot a b)))))

(put (match (divmod 17 5) ((tup q r) (format "q={q} r={r}"))))
(put (+ 1 (match (divmod 17 5) ((tup q _) q))))
(put (match (tup "a" 2 "c") ((tup _ _ last) last)))
```
```expect
q=3 r=2
4
c
```

Nested, the inner names shadow the outer ones:

```candy run
(sig swap-diff (Fn ((Tup Int Int)) Int))
(defn swap-diff (p) (match p ((tup a b) (match (tup b a) ((tup a b) (- a b))))))
(put (swap-diff (tup 10 3)))
```
```expect
-7
```

```candy errors
(put (match (tup 1 2) ((tup a b) a) (else 0))) => must be the only clause
(put (match (tup 1 2) ((tup a b) a) ((tup c d) c))) => must be the only clause
(deft Shape (Circle ((r Int))) (Dot)) (put (match (Circle 1) ((Circle r) r) ((tup a b) a))) => must be the only clause
(put (match (tup 1 2) ((tup) 1))) => needs at least one name
(put (match (tup 1 2) ((tup a a) a))) => must be different
(put (match (tup 1 2) ((tup a (b)) a))) => match name must be a name
```
