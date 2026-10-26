# B54: `slurp` searches `src/`, `tst/` and `lib/` when a path is missing

kind: leak
state: open
priority: normal
found: macros, 2026-10-18
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[library.builtins]]

From smz's `get_path`, relative to the current directory: it can hide a wrong path (it
found `form.cdy` for a translator that had none next to it, until `expand.cdy` checked
with `file-exists` first). In `doc/tech_debt.md` until now, but a Candy user sees it (the
audit, `doc/hl_rqmt/tracking.md`).
