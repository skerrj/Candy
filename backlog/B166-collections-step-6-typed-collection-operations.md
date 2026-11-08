# B166: collections step 6: typed collection operations

kind: task
state: open
priority: normal
found: collections, 2026-11-07
fixed:
where: `src/cdy/system.cdy`, `src/cdy/prelude.cdy`, `src/cdy/*.cdy`, `spec/`
refs: [[B34]], [[B18]], [[B48]]

Step 6 of `doc/hl_rqmt/collections.md`. Lists', strings' and maps' own operations, per collection *for now* until interfaces (Question 2): `len`, `at`, `slice`, `contains` on lists; `str-len`, `char-at`, `substring`, `str-contains` on strings (Question 6); `map-size`; `in` gone; `put` a prelude macro over `text` (Question 4). Two boot steps. The checkpoint follows (Question 5).

## Notes

- 2026-11-07, Claude: filed on the HLD's acceptance (the owner, 2026-11-07).
