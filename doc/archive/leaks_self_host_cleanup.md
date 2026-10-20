# Leaks (self-host-cleanup, archived)

**Archived** at tag `self-host-cleanup`. These entries still apply until they are fixed; when one is fixed, strike it through here and say where. New leaks go in `doc/leaks.md`. Earlier lists are `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`.

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later, added on branch `self-host-cleanup`.

## Hacked-in forms

- **`import` is inclusion, not modules** (step A of `doc/hl_rqmt/self_host_cleanup.md`,
  `src/cdy/include.cdy`). `(import name)` pastes `name.cdy`'s forms into the program, once
  per file, so there are no namespaces: every top-level name is global across all the
  files, two files can't define the same name, and a file sees names from files it
  doesn't import (whatever else the program includes). The name is a path relative to the
  importing file, without `.cdy` (`(import lib/util)`). Only the Candy translator has it.
  `import-as` and `import-from` are still unsupported. Fix: modules (step B).
