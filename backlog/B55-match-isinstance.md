# B55: `match` is an `isinstance` chain, not Python's `match`

kind: tech-debt
state: open
priority: normal
found: pre-self-host, 2026-10-17
fixed:
where: `src/cdy/emit.cdy` (`emit-match`)
refs: [[match.match]]

mypy (2.4) loses a generic variant's type arguments in a class pattern (`case Node(l, v,
r):` makes `v` `Any`). pyright handles class patterns; switch back if mypy catches up.
From `doc/tech_debt.md`.
