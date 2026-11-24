# B230: host-macros step 6: `load-macros` dropped

kind: task
state: open
priority: normal
found: host-macros, 2026-11-22
fixed:
where: `src/cdy/translator.cdy`, `src/cdy_rt/spelling.py`, `src/cdy_rt/primitives.py`, `script/bootstrap.py`
refs: 

Step 6 of `doc/hl_rqmt/host_macros.md`. `load-macros` taken out of `translator.cdy`, `spelling.py` and `primitives.py` ([[B41]], [[B70]]), with a built-in that restarts `gensym`'s count in its place (step 1 restarts it by a `load-macros` of no Python), staged `old-runtime`; `macros.md`'s account of `exec` marked history; [[B49]] narrowed to `module-dir`.

## Notes

- 2026-11-22, Claude: filed on the HLD's acceptance (the owner, 2026-11-22).
