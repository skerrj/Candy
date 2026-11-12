# B172: `=` and `!=` aren't values

kind: leak
state: dropped
priority: low
found: collections step 3, 2026-11-09
fixed:
where: `src/cdy_rt/spelling.py`, `src/cdy/check.cdy` (`infer-compare`)
refs: [[expr.operator-values]], [[expr.equality]], [[B163]], [[B173]]

Every operator but `=` and `!=` is a value, its function of two arguments
([[expr.operator-values]]): `(fold = true xs)` fails with `the operator = can't be used
as a value, for now; wrap it in a fn`. A function can't be compared ([[expr.equality]]),
which a call's checker sees (`infer-compare`, on the arguments' type), but as a value `=`
is an `(Fn (a a) Bool)`, and nothing would keep `a` off a function type.

Fix: a constraint the checker can carry (an `equatable` variable, every type but a
function's, with the check `has-fn` does), or interfaces ([[B34]]); then a value for each
in `spelling.py` and `primitives.py`.

## Notes

- 2026-11-09, Claude: found building step 3 of `collections`; not a value *for now*,
  rather than a hole in `expr.equality`.
- 2026-11-09, the owner: dropped (option A): `=` and `!=` are values after all. Not being
  one closed nothing: a generic function's `=` compares functions already ([[B173]]), so
  as values they are no worse.
- 2026-11-11, Claude: `infer-compare` is gone (`collections-2` step 7, [[B173]]): `=` as a
  value is an `(Fn (equatable equatable) Bool)`, which keeps it off functions.
