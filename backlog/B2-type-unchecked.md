# B2: A type's name and number of arguments aren't checked

kind: defect
state: open
priority: high
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy` (`analyse-type`), `src/cdy/emit.cdy` (`emit-tcon`), `src/cdy/system.cdy`
refs: [[types.table]], [[B53]], [[B99]]

Nothing lists the types that exist, or how many arguments each takes (its arity, as a type
constructor), so `analyse` reads any `(Name arg ...)` as a type:

| Written | What happens |
|---|---|
| `(List)` | `emit-tcon` fails with Python's `IndexError`, not a Candy error |
| `(Maybe Int Int)` | the second argument is dropped silently: `int \| None` |
| `(Int String)` | the argument is dropped silently: `int` |
| `(Shape Int)`, `Shape` not generic | translates; only mypy rejects it |
| `Foo`, defined nowhere | translates and runs: Python never evaluates `x: Foo` |

Found writing the spec (`doc/hl_rqmt/executable_spec.md`, step 3); the audit's defect 2
(`doc/hl_rqmt/tracking.md`); the unknown name found in triage ([[B103]]). A type from a
module the file doesn't import ([[B53]]) is the same check across modules.

Proposed fix (its own small HLD when picked up, as `doc/hl_rqmt/symbol_table.md` was for
the built-in functions): declare the built-in types in `system.cdy` as bodiless `deft`s,
as the built-in functions are bodiless `sig`s, with their type parameters giving their
arity: `(deft Int)`, `(deft (List a))`, `(deft (Map k v))`. `analyse` checks every type
against them and the program's own `deft`s: the name exists, and the number of arguments
matches. `Fn` keeps its own form; `Tup` takes any number, so it stays special until
variadic types ([[B99]]). The Python spellings (`int`, `tuple[a, ...]`) move from
`emit-tcon` into `spelling.py`, next to the functions'.

## Repro

The translator should fail, naming the type:

```candy error
(sig x (List))
(def x 1)
```
```expect-error
List
```

```candy error
(sig x Foo)
(def x 1)
```
```expect-error
Foo
```

## Notes

- 2026-10-25, the owner: the repro's message (`List`) is a placeholder; whoever fixes this
  writes the real one, and tightens the `expect-error` when the example moves into the
  spec.
- 2026-10-26, the owner: in triage ([[B103]]), `high`; widened from `(List)`'s crash to
  every type's name and arity, with the proposed fix (built-in types declared in
  `system.cdy`).
