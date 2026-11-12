# B181: collections-2 step 6: to-list gone

kind: task
state: review
priority: normal
found: collections-2, 2026-11-10
fixed: collections-2, 2026-11-11
where: `src/cdy/system.cdy`, `src/cdy_rt/spelling.py`, `src/cdy/*.cdy`, `spec/`
refs: [[B174]]

Step 6 of `doc/hl_rqmt/collections_2.md`. The `to-list`s left become `(List x)` by script, then `to-list` goes from `system.cdy` and `spelling.py`: two boot steps, since the step before still calls it (Question 1).

## Notes

- 2026-11-10, Claude: filed on the HLD's acceptance (the owner, 2026-11-10).
- 2026-11-11, Claude: the first boot step built (the HLD's step 6 note): the 108
  `to-list` calls left are `(List x)`; found [[B185]], worked around. The declaration's
  removal is the second boot step, after this one is committed.
- 2026-11-11, Claude: the second boot step built: `to-list` gone from `system.cdy`,
  `spelling.py` and `primitives.py`; the spec says `(List x)` is the one way. In review.
