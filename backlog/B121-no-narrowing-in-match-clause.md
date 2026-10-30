# B121: Inside a `match` clause, the subject isn't narrowed to its variant

kind: leak
state: open
priority: low
found: type-checker, 2026-10-29
fixed:
where: `src/cdy/check.cdy`
refs: [[checking.records]], [[match.sum-types]], [[B20]]

`get` on a sum names a field every variant has ([[checking.records]], *lasting*), and
inside a clause the subject is still the sum: in `(match s ((A _) (get s x)) (else 0))`,
`(get s x)` is `get: S has no field x`, though `s` is known there to be an `A`. The
clause's names read the variant's fields (`((A x) x)`), so nothing is lost but the
spelling. Fix: in a clause whose subject is a local, check its body with the local typed
as the variant (variants would need types of their own in the checker, not in the
language). [[B20]] is the same narrowing for `Maybe`, after `(= m nil)`.
