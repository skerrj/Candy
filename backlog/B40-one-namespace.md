# B40: Types and values share one namespace

kind: leak
state: open
priority: low
found: pre-self-host, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[match.namespace]]

A sum type's name and its variants are all Python names, so a variant can't have its
type's name (`(deft Box (Box ...))` is "defined more than once"), and no other top-level
name can reuse a type's name. Candy keeps types and values apart in principle. From
`doc/archive/leaks_pre_self_host.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an easy workaround, or rare.
