# B103: Triage the migrated items: priorities, and which leaks are kept

kind: task
state: done
priority: normal
found: tracking, 2026-10-25
fixed: triage
where: `backlog/`
refs: [[B90]]

The migration ([[B90]]) left every item `normal` (but [[B1]], `low`) and every leak `open`.
The owner sets the priorities, and decides over time which leaks are kept (a lasting rule
in the spec) and which items are dropped. Claude Code's proposal, as a start: `high` for
[[B3]] (silent wrong output) and [[B14]] (errors without a position); `low` for [[B57]]
(plainer Python), [[B60]] (three test directories) and [[B73]] (`master` vs `main`).

## Notes

- 2026-10-26, the owner: defects triaged: `high` [[B2]], [[B3]], [[B6]], [[B12]]; `low`
  [[B9]], [[B13]]; the rest `normal` ([[B14]] too, not `high` as proposed).
- 2026-10-26, the owner: leaks triaged: `high` [[B15]], [[B36]]; `low` [[B22]], [[B28]],
  [[B32]], [[B38]], [[B40]], [[B41]], [[B43]], [[B44]], [[B50]]; kept [[B24]], [[B33]] (the
  spec states them as lasting); the rest `normal` and open.
- 2026-10-26, the owner: tech debt triaged: `low` [[B55]], [[B57]], [[B58]], [[B60]],
  [[B64]], [[B67]], [[B70]], [[B71]], [[B74]], [[B76]], [[B79]]; dropped [[B73]], [[B77]],
  [[B78]]; the rest `normal`.
- 2026-10-26, the owner: tasks and ideas triaged: [[B81]] done; `low` [[B82]], [[B93]],
  [[B94]], [[B96]], [[B97]], [[B98]], [[B100]], [[B101]], [[B102]]; the rest `normal`.
- 2026-10-26, the owner: done; [[B82]]'s gist is [[B104]]. Kept and dropped are decided
  over time, as items come up.
