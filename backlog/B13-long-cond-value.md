# B13: A `cond` of about 200 clauses, used as a value, doesn't compile

kind: defect
state: open
priority: normal
found: self-host-cleanup, 2026-10-18
fixed:
where: `src/cdy/emit.cdy`
refs: [[macros.cond]], [[expr.conditionals]]

Used as a value, with simple arms, a `cond` becomes nested conditional expressions
(`a if t else (b if ...)`), and Python allows 200 nested parentheses. Written as
statements (in a tail, or with arms that need statements) a `cond` of any length is fine:
an `if`/`elif` chain. Fix: lift a long one into statements. The repro would be 200 lines,
so it is described. From `doc/tech_debt.md`; the audit's defect 12 (`doc/hl_rqmt/tracking.md`).
