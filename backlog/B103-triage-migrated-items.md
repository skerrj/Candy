# B103: Triage the migrated items: priorities, and which leaks are kept

kind: task
state: open
priority: normal
found: tracking, 2026-10-25
fixed:
where: `backlog/`
refs: [[B90]]

The migration ([[B90]]) left every item `normal` (but [[B1]], `low`) and every leak `open`.
The owner sets the priorities, and decides over time which leaks are kept (a lasting rule
in the spec) and which items are dropped. Claude Code's proposal, as a start: `high` for
[[B3]] (silent wrong output) and [[B14]] (errors without a position); `low` for [[B57]]
(plainer Python), [[B60]] (three test directories) and [[B73]] (`master` vs `main`).
