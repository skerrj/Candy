# Leaks

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later. Each one is acceptable for bootstrapping. Each entry
says what leaks, and what a proper fix might be. Add to this list whenever a hack goes in.
Shortcuts that are too small to matter to Candy's design go in `doc/tech_debt.md` instead.

**Earlier leaks still apply.** They are archived by branch:

- `doc/archive/leaks_imvp_py_translator.md`: the iMVP Python translator (up to tag
  `imvp-py-translator`);
- `doc/archive/leaks_pre_self_host.md`: self-hosting (up to tag `self-host-py`).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `self-host-cleanup` on.

## Hacked-in forms

- **`import` is inclusion, not modules** (step A of `doc/hl_rqmt/self_host_cleanup.md`,
  `src/cdy/include.cdy`). `(import name)` pastes `name.cdy`'s forms into the program, once
  per file, so there are no namespaces: every top-level name is global across all the
  files, two files can't define the same name, and a file sees names from files it
  doesn't import (whatever else the program includes). The name is a path relative to the
  importing file, without `.cdy` (`(import lib/util)`). Only the Candy translator has it.
  `import-as` and `import-from` are still unsupported. Fix: modules (step B).
