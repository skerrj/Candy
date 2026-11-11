# B174: `to-list` duplicates `(List x)`

kind: tech-debt
state: open
priority: low
found: collections step 4, 2026-11-09
fixed:
where: `src/cdy/system.cdy`, `src/cdy/*.cdy`
refs: [[types.constructors]], [[library.builtins]], [[B69]], [[B167]], [[B165]]

`(to-list x)`, a built-in typed `(Fn (a) (List a))`, makes a one-item list, which `(List
x)` does too since `semantics` ([[types.constructors]]). The translator has 152, 88 of
them `(++ acc (to-list x))` (adding to a list by copying it, [[B69]]), which `map-acc` and
`reduce` take away (`collections` step 7, [[B167]]); the spec has 6.

Fix: the rest become `(List x)`, mechanically (with step 5's `tup` rewrite, [[B165]], or
step 7's), then `to-list` goes from `system.cdy` and `spelling.py`.

## Notes

- 2026-11-09, the owner: noticed it in step 4's review; for later. Claude: filed, where it
  goes decided at the checkpoint after step 6.
- 2026-11-10, Claude: comes along to `collections-2`, its step 6 ([[B181]]), as the owner chose (`collections_2.md`, Question 1).
