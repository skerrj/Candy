# B165: collections step 5: tuples

kind: task
state: done
priority: normal
found: collections, 2026-11-07
fixed: collections, 2026-11-09
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`, `src/cdy/special.cdy`, `src/cdy/*.cdy`, `spec/`
refs: [[B152]], [[B17]], [[B29]]

Step 5 of `doc/hl_rqmt/collections.md`. `tup`'s uses become `Tup` or `List`, as each means; `checking.tup-lists` goes; `at` on a tuple an error (taken apart by a pattern only, *lasting*); then `tup` goes, with `(special tup)`.

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
- 2026-11-09, Claude: takes [[B175]] along (spelling accessors, `and`/`or` by kind).
- 2026-11-09, Claude: built (`doc/hl_rqmt/collections.md`, step 5's *As built*): `tup`
  gone for `Tup` or `List`, the checker strict, `at` on a tuple an error, and a `Tup`
  pattern only on a tuple; [[B152]] and [[B175]] done, [[B17]] and [[B29]] narrowed.
- 2026-11-09, the owner: ticked in review.
