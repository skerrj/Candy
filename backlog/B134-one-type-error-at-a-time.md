# B134: Translation stops at the first type error

kind: leak
state: open
priority: low
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/check.cdy`, `src/cdy/cdyc.cdy`
refs: [[checking.calls]], [[B15]]

`type-check` fails with the first type error it finds (`fail`, which raises), so a
program with several errors is fixed one translation at a time. The checker already
collects errors in `St`'s `errors` (`check-program` returns them), so reporting them all
is mostly a driver change: keep checking after an error (with `Any` for the failed node's
type, so one mistake doesn't cascade) and print every message. Split out of [[B15]].
