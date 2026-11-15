# B190: namespaces step 3: the name list, and `import`'s shape declared

kind: task
state: done
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-13
where: `src/cdy/core.cdy`, `src/cdy/special.cdy`, `spec/10-programs.md`
refs: [[B47]]

Step 3 of `doc/hl_rqmt/namespaces.md`. `(import m (a b))`; the import's record; `(special import (ModName (Opt (List Name))))`, the syntax categories `import` needs, the check and its error written from the shape; staged (`old-library`) or two boot steps.

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-13, Claude: built (the HLD's step 3 *Done* note): `(import m (a b))`, an
  unlisted name reached as m.name, and `import`'s shape declared in `special.cdy` and
  checked by `syntax.cdy` (new). Staged `old-library`. In review.
- 2026-11-13, Claude: its commit (`b98b523`) left one ruff finding in
  `test_self_host.py` (ISC004, a wrapped message not in parentheses: `ruff check` wasn't
  rerun after the wrap); fixed in step 4's commit.
- 2026-11-14, the owner: ticked in review.
