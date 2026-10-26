# B4: `(def (x) 1)` says " needs a (sig  Type)", with no name

kind: defect
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[types.sig-def]]

A `def` whose name isn't a name gets the missing-`sig` message, with an empty name. With a
`sig` before it, `(sig x Int) (def (x) 1)` says "sig for x, but no def or defn of x"; a
`defn` with a list for its name does the same. From `doc/tech_debt.md`;
the audit's defect 3 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should say what a `def` looks like, as `(def)` does:

```candy error
(def (x) 1)
```
```expect-error
def: expected (def name init)
```
