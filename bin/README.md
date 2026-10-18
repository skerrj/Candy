# bin

Checked-in Candy translators, one directory per target (`bin/py/` for Python; later
targets get their own, see `doc/hl_rqmt/multi_target.md`).

- `py/cdy_translator.py`: the self-hosted translator, generated; don't edit it. It is T2,
  the Candy translator (`src/cdy/*.cdy`) translated by T1, its own build by the Python
  translator; T2 translates its own source into itself (the fixpoint, see
  `doc/hl_rqmt/self_hosting_primo.md`). Use it with
  `python src/py_cdy/main.py FILE.cdy --translator bin`. After changing `src/cdy/`, rebuild
  it with `python src/py_cdy/self_host.py`; `tst/py_cdy/test_self_host.py` fails while it
  is stale. It needs only the runtime `cdy_rt`: it has its own reader (stage 3), and it
  rebuilds itself (both tested).

T1 and T2 themselves are generated into `output/` (git-ignored).
