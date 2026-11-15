# B203: library-layers step 5: `slurp` without a search

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[B54]], [[library.errors]]

Step 5 of `doc/hl_rqmt/library_layers.md`. `slurp` reads the path it is given; a missing file is a panic. `get_path`'s search goes.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
