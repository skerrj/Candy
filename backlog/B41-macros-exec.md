# B41: Macros run with Python's `exec`

kind: leak
state: open
priority: low
found: macros, 2026-10-18
fixed:
where: `src/cdy_rt/primitives.py` (`load_macros`), `src/cdy/expand.cdy`
refs: [[macros.defmacro]], [[macros.macro-code]]

The translator translates a program's macro code into Python and executes it in its own
module namespace (`doc/hl_rqmt/macros.md`, "How `load-macros` runs macro code"), so
Candy's macros depend on the translator running on Python, and on Python module
namespaces. Fix: with modules, the macro program could import the translator's `form`
module instead of copying it; a translator on another host needs another way to run macro
code (or an interpreter). From `doc/archive/leaks_macros.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): matters once there is a second target.
