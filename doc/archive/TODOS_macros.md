# TODOS (macros, archived)

**Archived** at tag `macros`. Open items were carried over to `TODOS.md`. Earlier ones are in `doc/archive/TODOS_self_host_cleanup.md`, `doc/archive/TODOS_pre_self_host.md` and `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and its leak (now in `doc/archive/leaks_self_host_cleanup.md`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `src/cdy/candy-special.md`, "programs").

## macros

- [x] Review `doc/hl_rqmt/macros.md`: accepted (proposals on 1, 3–6; reader rejects `__`; `cond` first).
- [x] Macros step 1: `quo`, `quasi`, `unq`, `unq-sp`, `defmacro` as special forms (spec, table, grammar).
- [x] Macros step 2: `quo` and `quasi` build `Form` values (`tst/cdy/cdyc/quoting.cdy`).
- [x] Macros step 3: `defmacro` and expansion (`src/cdy/expand.cdy`), `gensym`, `__` rejected by the reader.
- [x] Macros step 4: `import-macros`, helpers in macro files.
- [x] Macros step 5: `cond` as a macro in `src/cdy/prelude_macros.cdy` (out of `core.cdy` and the table).
- [x] Review step 5 as built (accepted): the prelude's macros (name, place, implicit import) and the A/B bootstrap.
- [x] Review steps 3 and 4 as built, accepted (`doc/hl_rqmt/macros.md`, the steps' "Done" notes and "How `load-macros` runs macro code"): `form.cdy` kept next to the translator, expansion skipping binding positions, and the three new leaks in `doc/leaks.md`.
- [ ] Add the up, down, down*, meta-template side conversation to `doc/brainstorm.md` (owner to supply the gist).
