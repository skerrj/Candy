# B57: The translator's Python is plainer than it could be

kind: tech-debt
state: open
priority: normal
found: bootstrap, 2026-10-20
fixed:
where: `src/cdy/emit.cdy`
refs:

Than the Python translator's was (at tag `self-host-py`): every operator is
parenthesised; `if` in tail position stays an `if` statement; a nested scope's locals
avoid every outer name, so it renames more than it must; `format` is a `str()`
concatenation, not an f-string. None of these change what a program does. From `doc/tech_debt.md`.
