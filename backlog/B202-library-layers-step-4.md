# B202: library-layers step 4: the system, revisited

kind: task
state: review
priority: normal
found: library-layers, 2026-11-15
fixed: library-layers, 2026-11-16
where: `src/cdy/system.cdy`, `src/cdy_rt/spelling.py`, `src/cdy_rt/primitives.py`
refs: [[B32]], [[B49]], [[library.builtins]]

Step 4 of `doc/hl_rqmt/library_layers.md`. The 11 built-ins dropped, with their spellings and primitives: `re-search`, `re-findall`, `re-compile`, `is-coll`, `is-str` (Python's), and `is-alpha`, `is-neg-int`, `strip`, `is-empty-str`, `file-put-lines`, `SYS_ARGS` (unused). [[B32]] closed, [[B49]] narrowed to the macros. Staged.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
- 2026-11-16, Claude: built (the HLD's step 4, "Done"); generated code no longer imports
  `re`. Not staged after all: the chain reads the step's own library, which agrees with
  its runtime. [[B32]] fixed, [[B49]] narrowed.
- 2026-11-17, the owner: drop what else can go. Claude: `isspace-at`, `elem-index` and
  `is-digit` dropped, after step 6 (the HLD's step 6, "Then"), whose commit moved the
  reader and the prelude off the first two; the rest kept for `stdlib`.
