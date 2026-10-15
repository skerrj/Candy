# TODOS

- [x] Add pytest tests for `src/py_cdy/parse_cdy.py` under `tst/py_cdy/` (`tst/py_cdy/test_parse_cdy.py`; run `pytest` in the `py_cdy` conda env)
- [ ] **Review `src/py_cdy/table.py` and `src/py_cdy/table_defs.py`** (first draft from smz's `table.py` / `smztils.py`; not yet run, linted or type-checked). Points to check:
  - `rest` is not included (schmuz defined it in `parse.scm`); add it to `table_defs`?
  - `empty-list` still renders as a Python list `[]` (as in smz), not a tuple.
  - Behaviour changes from smz: `spit(path, text)` order, `is_str` is a type check (was a quoted-token check), `is_coll` accepts tuples, `slurp` raises `FileNotFoundError` and searches `*.cdy`.
  - Renames: `slice` → `slice_`, `in_it` → `in_`, `join_it` → `join`, `op-tab-*` → `table-*`.
  - Dropped: `true`/`false` and char constants (`LF`, `DQ`, `BS`, `ES`, ...) now that Candy has literals and escapes; `m_table_*` wrappers; `parse_string_help*` leftovers.
  - The self-hosted compiler must pass the table along (`table-add-fun` returns a new table).
- [ ] After review: move `table.py` and `table_defs.py` to their own runtime package (leaning towards `src/cdy_rt/`), set `RUNTIME_MODULE`/`TABLE_MODULE` to match, and decide how generated code finds it (editable install of just `cdy_rt`, or `PYTHONPATH=src`).
- [ ] After review: run ruff, pylint, mypy and pyright on them and add tests in `tst/py_cdy/`.
