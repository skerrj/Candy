# B95: An I/O refactor

kind: idea
state: open
priority: normal
found: executable-spec, 2026-10-23
fixed:
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[library.builtins]], [[B36]], [[B48]]

The owner (2026-10-23): "I/O is total crap at the moment"; expect a big one. `print`,
`display` and `put` are all Python's `print`, typed `Any`, showing values with Python's
`str()` ([[B36]], [[B48]]), and the file and path built-ins are
thin wrappers. A built-in that shows a value in Candy's syntax belongs to it
(`doc/hl_rqmt/executable_spec.md`, question 12). From `doc/brainstorm.md`.
