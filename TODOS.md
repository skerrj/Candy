# TODOS

- [x] Add pytest tests for `src/py_cdy/parse_cdy.py` under `tst/py_cdy/` (`tst/py_cdy/test_parse_cdy.py`; run `pytest` in the `py_cdy` conda env)
- [ ] **Review `src/cdy_rt/table.py` and `src/cdy_rt/table_defs.py`** (first draft from smz's `table.py` / `smztils.py`; not yet run, linted or type-checked). Points to check:
  - `rest` is not included (schmuz defined it in `parse.scm`); add it to `table_defs`?
  - `empty-list` still renders as a Python list `[]` (as in smz), not a tuple.
  - Behaviour changes from smz: `spit(path, text)` order, `is_str` is a type check (was a quoted-token check), `is_coll` accepts tuples, `slurp` raises `FileNotFoundError` and searches `*.cdy`.
  - Renames: `slice` → `slice_`, `in_it` → `in_`, `join_it` → `join`, `op-tab-*` → `table-*`.
  - Dropped: `true`/`false` and char constants (`LF`, `DQ`, `BS`, `ES`, ...) now that Candy has literals and escapes; `m_table_*` wrappers; `parse_string_help*` leftovers.
  - The self-hosted compiler must pass the table along (`table-add-fun` returns a new table).
- [x] Move `table.py` and `table_defs.py` to the runtime package `src/cdy_rt/`, with `RUNTIME_MODULE`/`TABLE_MODULE` set to `cdy_rt.table_defs`/`cdy_rt.table`.
- [x] Make `cdy_rt` importable: editable install of just `cdy_rt` in strict mode (`pip install -e . --config-settings editable_mode=strict`), with a `py.typed` marker so mypy and pyright use it.
- [x] Un-ignore `lib/` in `.gitignore`: `SEARCH_PATH` in `table.py` searches a `lib` directory for Candy files.
- [ ] After review: run ruff, pylint, mypy and pyright on them and add tests (in `tst/cdy_rt/`?).

## For owner review (from the design session after `36ca66e`)

- [ ] `sig` type names in `doc/hl_rqmt/iMVP_py_translator.md` ("Signature statement"): confirm `String`, `Unit` (value `nil`), `(Maybe a)`, `(List a)`, `(Fn (A B) R)`, `(Tup a b)`, `(Map k v)`.
- [ ] `(List a)`: Python `tuple[A, ...]` (lean, with `empty-list` → `()`) or `list[A]`?
- [ ] `Any` for nested `fn`s that become Python `def`s (iMVP doc, `sig` open item 2).
- [ ] `doc/leaks.md` (new): check the list of hacks and Python leaks, including `format`/`tup` as hacked in from smz.
- [ ] `src/cdy/candy-special.md`: Claude marked `### quote [SKIP]`; `sig`, `deft`, `get`/`assoc` are not in the spec yet. Add them?
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `def` inside a function, literal parser rules, strategy A/B and IR layering, error positions, `reader.py`.
