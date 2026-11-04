# B121: Inside a `match` clause, the subject isn't narrowed to its variant

kind: leak
state: done
priority: low
found: type-checker, 2026-10-29
fixed: semantics
where: `src/cdy/check.cdy`
refs: [[checking.records]], [[match.sum-types]], [[B20]]

`get` on a sum names a field every variant has ([[checking.records]], *lasting*), and
inside a clause the subject is still the sum: in `(match s ((A _) (get s x)) (else 0))`,
`(get s x)` is `get: S has no field x`, though `s` is known there to be an `A`. The
clause's names read the variant's fields (`((A x) x)`), so nothing is lost but the
spelling. Fix: in a clause whose subject is a local, check its body with the local typed
as the variant (variants would need types of their own in the checker, not in the
language). [[B20]] is the same narrowing for `Maybe`, after `(= m nil)`.

## Notes

- 2026-11-03, Claude: fixed in semantics step 5 ([[B144]]): in a clause whose subject is a local, the
  checker narrows the local to the clause's variant (`narrow`, by a map in its `Ctx`: no
  variant types, the sum's arguments kept), for `get` and `assoc`; `emit` reads them on
  the match's temporary, which Python's `isinstance` has narrowed, with a cast for a
  generic variant's field of a type-variable type (mypy narrows `T[int]` to `N[Any]`).
  The spec's new rule is [[checking.narrowing]]. [[checking.records]] said, before:

  ```text
  its variants, not known until it is matched, [[match.sum-types]]). Inside a `match`
  clause the subject is still the sum, so `get` on it there follows the same rule (*for
  now*: the checker doesn't narrow the subject to the clause's variant, [[B121]]); the
  clause's names read the variant's fields.
  ```

  with the error, now [[checking.narrowing]]'s run example:

  ```text
  (deft S (A ((x Int))) (B ((y Int)))) (sig f (Fn (S) Int)) (defn f (s) (match s ((A _) (get s x)) (else 0))) => get: S has no field x
  ```

  and `spec/30-match.md`'s [[match.sum-types]] (now: by the clause's names or, if the
  subject is a local, by `get` on it):

  ```text
  one type ([[checking.records]]); any other field is read in its variant's clause of a
  `match`:
  ```
