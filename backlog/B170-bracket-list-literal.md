# B170: Brackets for a list literal

kind: idea
state: open
priority: low
found: collections, 2026-11-07
fixed:
where: `src/cdy/read.cdy`
refs:

`[1 2 3]` as sugar for `(List 1 2 3)`, as Clojure's vector. Decided with the map's
literal and the reader macros (`'`), which may want the brackets for something else;
not in `collections` (`doc/hl_rqmt/collections.md`, Question 3, *for now*).

## Notes

- 2026-11-07, the owner: none now (Question 3).
