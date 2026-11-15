# B198: Re-export, so a program can see only the prelude

kind: idea
state: open
priority: low
found: library-layers (HLD), 2026-11-15
fixed:
where: `src/cdy/core.cdy`, `src/cdy/prelude.cdy`
refs: [[programs.sees]], [[programs.import]], [[B97]]

`library.md`'s "What a program sees", B: a program sees only the prelude, which imports
the system and re-exports what programs need, as they are or wrapped, as OCaml's
`Stdlib` and Elm's core do. The prelude's names would then be the one interface for every
target, each target's system free to differ underneath ([[B97]]). It needs re-export, a
module passing on names it imports, which modules haven't: today a module's imports are
its own (`programs.import`).

## Notes

- 2026-11-15, the owner: `library_layers.md` Question 6, both the system and the prelude
  imported implicitly, *for now*; re-export when the standard library shows it is needed.
  Claude: filed.
