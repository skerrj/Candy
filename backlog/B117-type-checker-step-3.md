# B117: type-checker step 3: the checker on

kind: task
state: done
priority: normal
found: type-checker, 2026-10-28
fixed: type-checker
where: `doc/hl_rqmt/type_checker.md`
refs: [[B15]], [[B25]], [[B10]], [[B30]], [[B17]]

Step 3 of `doc/hl_rqmt/type_checker.md`. The checker's errors fail translation, with positions; `spec/25-checking.md`'s rows pass, and the stable files' rules change; [[B25]], [[B10]] and [[B30]] closed (or narrowed), [[B15]] narrowed to what is left.

## Notes

- 2026-10-29, the owner: ticked in review; an error in a leaf is reported at its parent, [[B122]].
