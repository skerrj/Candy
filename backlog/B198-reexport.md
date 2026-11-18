# B198: Re-export, so a program can see only the prelude

kind: idea
state: dropped
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
- 2026-11-17, the owner: dropped; it would make what a program sees more confusing, not
  clearer. Claude: what it was for is had already. `system.cdy` is target-neutral (Candy
  types only; a target's spellings and runtime are its own), and what differs by target
  goes to a target extension (`py`), a declaration module imported by name, so `system`
  is the one interface itself. Re-export would make a name's origin indirect (`len` the
  prelude's, or `system`'s through it), add a layer to shadowing and qualified names,
  and to errors. Elm, cited above, has no re-export either, as far as recalled: it
  imports a fixed list of modules implicitly, as Candy does. A wrapped built-in (an
  `at` giving a `Maybe`) is an ordinary function, with its own name; re-export in
  general, for a program's own modules, would be an item of its own, if one needs it.
