# TODOS

Done and earlier items are in `doc/archive/TODOS_self_host_cleanup.md`,
`doc/archive/TODOS_pre_self_host.md` and `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and its leak (now in `doc/archive/leaks_self_host_cleanup.md`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `src/cdy/candy-special.md`, "programs").

## macros

- [ ] Review `doc/hl_rqmt/macros.md` (draft HLD) and its open questions.
