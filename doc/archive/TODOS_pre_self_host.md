# TODOS (pre-self-host, archived)

**Archived** at tag `self-host-py`. Open items were carried over to `TODOS.md`. Earlier ones are in `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over from the iMVP (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` (was `doc/leaks.md`): check the list of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `src/cdy/candy-special.md`: Claude marked `### quote [SKIP]`; `sig`, `deft`, `get`/`assoc` are not in the spec yet. Add them?
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.

## pre-self-host

- [x] `doc/hl_rqmt/sum_types.md`: all seven questions decided (variants in `deft`; nullary variants are values; exhaustive `match`; `Maybe` stays `A | None`; `get` after `match`; global variant names), and implemented (stage 0).
- [ ] `src/cdy/candy-special.md`: add `deft` (records and sums) and `match` to the spec, with `sig`, `get` and `assoc` (see the carried-over item above).
- [x] Fixpoint (stage 2, reached in slice 1d): the `ast.dump` comparison of the files T1 and T2 is dropped (decided). The checks: T2 passes `mypy --strict`, T3 = T2 byte for byte, and T1 and T2 agree on every test program.
- [x] Checked-in translator `bin/py/cdy_translator.py` (= T2; rebuild with `python src/py_cdy/self_host.py`, a test catches it going stale; `main.py --translator bin`).
- [x] Stage 3: the reader in Candy (`src/cdy/read.cdy`), the same forms as `parse_cdy` on every file and edge case; the checked-in translator rebuilds itself and runs without the Python translator. See "Stage 3 as built" in `doc/hl_rqmt/self_hosting_primo.md`.
- [ ] Next (owner to choose): retire the Python translator as the way to build (a driver that rebuilds `bin/py/` from itself), `import` instead of joining files, or the next language features.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (draft staging plan): the translator in Candy with the Python parser borrowed, the T1 = T2 fixpoint, then the parser in Candy. Forms at the boundary: A, `deft` variants plus conversion (decided). Decided: Candy source in `src/cdy/`, T1/T2 generated into git-ignored `output/`. Driver: a `main.py` mode, for now (decided). Fixpoint (decided): T3 = T2 and T1/T2 output byte for byte (the `ast.dump` file comparison was dropped).
