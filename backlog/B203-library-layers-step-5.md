# B203: library-layers step 5: `slurp` without a search

kind: task
state: done
priority: normal
found: library-layers, 2026-11-15
fixed: library-layers, 2026-11-17
where: `src/cdy_rt/primitives.py`
refs: [[B54]], [[library.errors]]

Step 5 of `doc/hl_rqmt/library_layers.md`. `slurp` reads the path it is given; a missing file is a panic. `get_path`'s search goes.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
- 2026-11-17, Claude: built (the HLD's step 5, "Done"); [[B54]] to review. No `boot` tag:
  `bin` doesn't change.
- 2026-11-17, the owner: ticked in review.
