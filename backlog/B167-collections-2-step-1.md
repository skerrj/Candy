# B167: collections-2 step 1: map-acc

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections-2, 2026-11-10
where: `src/cdy/system.cdy`, `src/cdy_rt/`, `src/cdy/*.cdy`, `spec/60-library.md`
refs: [[B123]], [[B69]]

Step 1 of `doc/hl_rqmt/collections_2.md` (step 7 of `collections.md`, its first part). `map-acc`, `(Fn ((Fn (s a) (Tup s b)) s (List a)) (Tup s (List b)))`, a built-in with a primitive that doesn't copy, and its rule; the translator's loops that thread a state onto it, where each is one. No `reduce` (Question 2).

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-10, Claude: moved to branch `collections-2`, as the owner chose at Question 5's
  checkpoint; still `collections.md`'s step, to be renumbered in `collections-2`'s HLD,
  with [[B174]] and [[B173]] to be placed there.
- 2026-11-10, Claude: retitled for `collections_2.md` (its Question 3, as the owner chose): was
  "collections step 7: the list operations"; the rest of that step is steps 2 to 5.
- 2026-11-10, Claude: built (the HLD's step 1 *Done* note): `map-acc`, and 12 loops onto it;
  the build 1.02 s to 0.93 s. In review.
- 2026-11-11, the owner: ticked in review.
