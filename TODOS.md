# TODOS

Done and earlier items are in `doc/archive/TODOS_pre_self_host.md` and
`doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [x] `src/cdy/candy-special.md`: added `sig`, `deft` (records and sums), `match`, `get` and `assoc` (done on `self-host-cleanup`).
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).

## self-host-cleanup

- [x] Review `doc/hl_rqmt/self_host_cleanup.md`: accepted (inclusion first, Python translator frozen, top file `cdyc.cdy`).
- [x] `import` step A (inclusion) in the Candy translator; `src/cdy/cdyc.cdy`; `bin/py/` rebuilds itself.
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and the new leak in `doc/leaks.md`.
- [x] `and`/`or` short-circuit in the Candy translator (`tst/cdy/short_circuit.cdy`).
- [x] Review the spec update (`src/cdy/candy-special.md`): approved; `tup` moved out of "weird stuff".
- [x] A driver in Candy: `main` in `cdyc.cdy` (`python bin/py/cdy_translator.py FILE.cdy [OUT.py]`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `src/cdy/candy-special.md`, "programs").
- [ ] Read `doc/hl_rqmt/macros.md` (placeholder): macros proposed as the next branch after this one, once errors carry positions.
- [x] Parse and `import` errors name their file (`lib/b.cdy: parse error at ...`).
- [x] Positions on forms: errors say `file:line:col: msg`.
- [x] Recursion limit: not needed (removed from `self_host.py`); `translate-text` errors now have positions too.
- [x] Long `cond`s: `elif` chains in the Candy translator (`test_long_cond`).
