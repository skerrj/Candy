# B202: library-layers step 4: the system, revisited

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `src/cdy/system.cdy`, `src/cdy_rt/spelling.py`, `src/cdy_rt/primitives.py`
refs: [[B32]], [[B49]], [[library.builtins]]

Step 4 of `doc/hl_rqmt/library_layers.md`. The 11 built-ins dropped, with their spellings and primitives: `re-search`, `re-findall`, `re-compile`, `is-coll`, `is-str` (Python's), and `is-alpha`, `is-neg-int`, `strip`, `is-empty-str`, `file-put-lines`, `SYS_ARGS` (unused). [[B32]] closed, [[B49]] narrowed to the macros. Staged.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
