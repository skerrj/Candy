# Leaks

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later. Each one is acceptable for bootstrapping. Each entry
says what leaks, and what a proper fix might be. Add to this list whenever a hack goes in.
Shortcuts that are too small to matter to Candy's design go in `doc/tech_debt.md` instead.

**Earlier leaks still apply.** The list for the iMVP Python translator (up to tag
`imvp-py-translator`) is in `doc/archive/leaks_imvp_py_translator.md`. Those entries stay in
effect until they are fixed. When one is fixed, mark it there (strike it through and say
where it was fixed) rather than copying it here. This file is for leaks added from branch
`pre-self-host` on.

## Hacked-in forms

(none yet)

## Types

- **Sum types are Python unions of `NamedTuple`s.** Two variants of different sums with
  the same fields compare equal (`==` is tuple equality), as records already do (see the
  archived list). A variant is also a tuple, so Python's tuple operations work on it.
- **`get` after `match` is checked by mypy, not Candy.** `(get s r)` on a `Shape` that
  might be a `Rect` translates; mypy rejects it in strict mode, but Candy itself doesn't.

## Python semantics showing through

(none yet)

## Translator shortcuts

- **Types and values share one namespace.** A sum type's name and its variants are all
  Python names, so a variant can't have its type's name (`(deft Box (Box ...))` is
  "defined more than once"), and no other top-level name can reuse a sum type's name.
  Candy keeps types and values apart in principle.
