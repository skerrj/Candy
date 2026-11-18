# B54: `slurp` searches `src/`, `tst/` and `lib/` when a path is missing

kind: leak
state: done
priority: normal
found: macros, 2026-10-18
fixed: library-layers, 2026-11-17
where: `src/cdy_rt/primitives.py`
refs: [[library.builtins]], [[library.errors]]

From smz's `get_path`, relative to the current directory: it can hide a wrong path (it
found `form.cdy` for a translator that had none next to it, until `expand.cdy` checked
with `file-exists` first). In `doc/tech_debt.md` until now, but a Candy user sees it (the
audit, `doc/hl_rqmt/tracking.md`).

## Notes

- 2026-11-17, Claude: fixed (library-layers step 5, [[B203]]): `slurp` reads the path it
  is given, and one it can't read is a panic, "slurp: can't read path"
  (`library.errors`).
- 2026-11-17, the owner: ticked in review.
