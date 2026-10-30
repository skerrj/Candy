*Archived 2026-10-29, from a Claude Code session on branch `type-checker`, during step 3
(the checker on; `doc/hl_rqmt/type_checker.md`).* A side conversation, the owner's
questions on `get` on a sum type (Question 8, answered A: a variant's constructor gives
the sum, and `get` on a sum names a field every variant has, with one type). The turns are
verbatim. What came of it, in the same step: the message for a field every variant has
with different types, and `checking.records`' rows for it, for a field-less variant, for
`get` inside a clause and for a generic sum; [[B119]] (a variant written as a type),
[[B120]] (`get` before a type is known, which the earlier turns call B119), [[B121]] (no narrowing
in a clause); [[B18]]'s text.

# `get` on a sum type

*Chat archive, 2026-10-29*

## Owner

> i'm still reading the above, so forgive me if it's in there, is there a leak for any cases todo with the get type stuff?

## Claude Code

Partly. Three cases come out of the `get` work, and only one has a proper item:

1. **`get` on a value whose type isn't known yet** gives the error "get: the type of p isn't known here (name)". It's *for now* (`[[checking.order]]`, Question 4), but its only record is a bullet in B15's narrowed text and the link from the spec rule. It has no item of its own. Since it's a shortcut a user can hit, CLAUDE.md's rule says it should be a `leak` item. The survey found it never fires on the translator or the tests, so I'd make it `low`.

2. **`get` on a value typed `Any`** isn't checked at all. B18 covers this, and B30's closing note points to it. But B18's text still says only that *mypy* checks nothing that passes through `Any`. Now that Candy's checker exists, the text should say Candy's checker skips it too. That's a small edit.

3. **`get` on a sum needs a field that every variant has.** This was your answer A to Question 8, recorded as *lasting*, so it isn't a leak and has no item. The alternative, variants as their own types (which needs variance), was tried in the survey and dropped. If you'd like that kept as a possibility for later, it could go in as an `idea`. Otherwise the HLD's Question 8 is the only record of it.

My suggestion:
- add **B119** as a `low` leak for case 1, with B15's bullet pointing to it;
- fix B18's text for case 2;
- leave case 3 as it is.

Both changes would go into the step 3 commit. Should I make them?

## Owner

> ya, the question was about the get on a sum type: so, if you do a get on a valid field of a type (that's part of a sum type), but it's on a field that's not in every type of the sum type, the type checker fails and what else happens, does it let thru to lower and we cross our fingers?

## Claude Code

No. The checker runs after analysis and before `lower`, and its first error stops translation, so nothing reaches `lower` or `emit` and no Python is written. I tried it with the rebuilt `bin`:

```
(deft S (A ((x Int))) (B ((y Int))))
(put (get (A 1) x))
```
```
candy: a.cdy:2:6: get: S has no field x
```

It exits with status 1 and no output file. That's the rule from your answer A to Question 8: `(A 1)` has type `S`, and `x` isn't a field of every `S`. To read `x`, take the value apart with `match`.

The case that does still get through is a value typed `Any`, which the checker doesn't check at all:

```
(deft S (A ((x Int))) (B ((y Int))))
(sig s Any)
(def s (B 2))
(put (get s x))
```

This translates, and fails when it runs, with Python's `AttributeError: 'B' object has no attribute 'x'`. mypy doesn't catch it either, because the type is `Any` in Python too. That's B18, whose text still mentions only mypy (the fix I suggested). A value gets typed `Any` by writing it in a `sig`, or by using a built-in that returns `Any`, such as `at` on a list.

The two fixes I suggested still stand: B119 for the "isn't known here" error, and the B18 text. Should I make them?

## Owner

> i guess the question is: there's a chance that a valid get on a sum type is going to fail? currently...

## Claude Code

Yes, in one direction. The checker turns away some `get`s that would have worked when run. It never accepts a `get` on a sum that then fails when run, unless the value is typed `Any`.

**What it accepts is safe.** It accepts `get` on a sum only when every variant has that field with the same type. Then whichever variant the value turns out to be, the field is there.

**What it rejects that would have worked.** All of these stop translation; none reaches Python. I ran each with the rebuilt `bin`:

1. **The variant is obvious from the code:** `(get (A 1) x)` gives `get: S has no field x`. This is the rule you chose, *lasting*. The way to write it is `match`.

2. **Inside the clause that matched it:**
   ```
   (defn f (s) (match s ((A _) (get s x)) (else 0)))
   ```
   This also gives `get: S has no field x`. The checker doesn't narrow, so `s` is still an `S` inside the `(A _)` clause. You can write `((A x) x)` and use the bound name instead. Still, this cuts against the reason recorded for A ("unknown until matched"): here it *has* been matched. I think this one deserves an item: narrowing the subject inside its clause, an `idea` or a `leak` for you to choose. B20 covers narrowing only for `Maybe` (after `(= m nil)`), not for sums.

3. **A shared field with different types:**
   ```
   (deft S (A ((id Int) (x Int))) (B ((id String))))
   (put (get (A 1 2) id))
   ```
   This gives `get: S has no field id`. Rejecting it is right, but the message is wrong: every variant *has* `id`, just not with one type. It should say something like `get: field id of S has different types in its variants`. That's a small fix in `sum-field` and `field-type` in `check.cdy`, plus a spec row, and it belongs in step 3.

Counting what's pending now:
- the message fix (case 3), in step 3;
- an item for narrowing inside a clause (case 2);
- B119 for the "isn't known here" error;
- the B18 text.

Should I do all four?

## Owner

> have another question: the error is on the get (which has to be inside a match...) why isn't the error on the `deft`?

## Claude Code

Because the `deft` isn't wrong. Variants of one sum having different fields is the normal case: `Circle` has `r`, `Rect` has `w` and `h`. What's wrong is the `get`, which assumes a field that only some of the values have, so that's where the error points.

One correction to the question: `get` doesn't have to be inside a `match`. Outside one, `get` works on any field every variant has, which is what the new example in `30-match.md` shows (`(get (Rect "a" 4 5) id)`). Inside a clause, you'd normally use the names the pattern binds; `get` on the subject there fails only because the checker doesn't narrow (case 2 above).

For case 3, the same field name with different types in different variants, the error could go on the `deft`: "variants of S give `id` different types". But the translator itself does this. In Core's `Expr`, `Do` has `(body (List Expr))` and `Lambda` has `(body Expr)`. A rule on the `deft` would reject the translator's own types, and every program that reuses a field name the way records reuse `name`. So it's left legal, and only a `get` across those variants is an error, since no one type fits there.

If you'd prefer the stricter rule, it's a real choice. It would rename fields in `core.cdy` and probably elsewhere, and I'd suggest a backlog item for it rather than doing it in this branch.

The four pending changes are unchanged: the case 3 message fix, an item for narrowing inside a clause, B119, and the B18 text.

## Owner

> so what's are the test cases for `Shape`... in all tests?

## Claude Code

`Shape` appears in four test programs and the spec's examples. It's always a sum with a few variants, and almost every test of it uses `match`. The `get`-on-a-sum rule is tested twice in all of that.

**Test programs (`tst/cdy/`):**

| File | `Shape` | What it tests |
|---|---|---|
| `sums.cdy` | `Circle r`, `Rect w h`, all `Double` | `area` and `describe` by `match`, and a generic tree. Line 67 was `(get (Rect 4.0 5.0) h)`; it now reads `h` inside `match` |
| `t1/sums_1c.cdy` | the same | `area` and `describe` by `match` (T1's copy) |
| `cdyc/lib/shapes.cdy`, used by `cdyc/modules.cdy` | `Circle r`, `Square s` | a sum defined in an imported module, and `match` on it there |

**The spec:**

| Where | What it tests |
|---|---|
| `30-match.md:25` (`[[match.sum-types]]`) | declaring a sum, `match` on it with `Dot`, a variant with no fields |
| `30-match.md:46` | **`get` on a sum:** `id` is in both variants and is read with `get`, while `h` is read inside `match`. This is new in step 3 |
| `30-match.md:81–82` | constructor errors: too few fields, `(Dot)` called |
| `30-match.md:94–159` | `match` clauses, `else`, exhaustiveness ("no clause for Rect, Dot"), mixing two sums' variants |
| `30-match.md:201` | a `tup` pattern mixed with variant patterns |
| `20-types.md:60` | `(Shape Int)` when `Shape` isn't generic |
| `25-checking.md:212` (`[[checking.match]]`) | `Circle` and `Sq` in `match`, the clauses' one type |

The second `get`-on-a-sum test isn't on `Shape`. It's the new row in `[[checking.records]]`: `(deft S (A ((x Int))) (B ((y Int)))) (put (get (A 1) x)) => get: S has no field x`.

**What no test covers for `get` on a sum:**
- **Case 3:** a field in every variant but with different types (and the misleading message);
- **Case 2:** `get` on the subject inside its own clause, since there's no narrowing;
- **A field-less variant:** with a variant like `Dot`, no field is shared, so any `get` on the sum fails;
- **A generic sum:** a shared field whose type is a type variable, such as `(deft (T a) (L ((v a))) (N ((v a))))`. I believe the checker handles it, but nothing tests it.

I'd add rows to `[[checking.records]]` for case 3 (with the message fix), case 2 and the generic sum, as part of the four pending changes. Should I go ahead?

## Owner

> i need help on this, "The second get-on-a-sum test isn't on Shape. It's the new row in [[checking.records]]: (deft S (A ((x Int))) (B ((y Int)))) (put (get (A 1) x)) => get: S has no field x.": how can you access `A`, which is part of a sum type, directly (i.e without a match or some sort of reference to `S`?

## Claude Code

A variant's name is a constructor: a global function, unqualified like every top-level name. Any code can call it without a `match` and without naming `S`. Haskell and ML work the same way: you write `Just 1` without mentioning `Maybe`. So `(A 1)` is just a call that builds a value. What that call does *not* give you is an `A` type.

- **The value's type is `S`, not `A`.** This is question 8's answer A: the constructor's type is `(Fn (Int) S)`. After `(A 1)`, the checker only knows "some `S`" and has forgotten which variant built it. So `(get (A 1) x)` gets the sum rule: `x` isn't in `B`, so the `get` is rejected. That row tests exactly this. You're right that you can't reach `A`'s fields through `A` itself, and that's the rule. The row only shows that building the value with `A` doesn't get around it.
- **`A` isn't a type name.** A sum's variants are constructors only; `S` is the only type. I checked with `bin` (the step-3 build):
  - `(sig a S) (def a (A 1))` translates, and the Python is `a: S = A(1)` with `type S = A | B`.
  - `(sig a A)` is rejected.

So the only way to read a field that isn't in every variant is `match`, where the clause binds the field to a name: `((A x) x)`.

**Something new this turned up:** the error for `(sig a A)` is wrong.

```
candy: bad.cdy:2:1: A is not defined here; bad defines it, but this file doesn't import bad
```

It's a one-file program, so `bad` is the file itself. The message comes from the type-name check's "defined in another module" path, which mistakes a variant for a type defined elsewhere. It should say something like "A is a variant of S, not a type." This is a `defect` and not part of step 3. I'd add it as B119 and move the "isn't known here" leak to B120, alongside the other pending changes.

Shall I go ahead with those, plus the test rows from before?

