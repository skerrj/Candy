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

(none yet)

## Python semantics showing through

(none yet)

## Translator shortcuts

(none yet)
