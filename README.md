# Candy

Candy (`.cdy`) is an early-stage, experimental, statically typed language with an
S-expression syntax. It translates to Python, and its translator is written in Candy: the
checked-in translator (`bin/py/cdy_translator.py`) builds itself.

```
(sig greet (Fn (String) String))
(defn greet (name) (format "hello, {name}"))

(put (greet "candy"))
```

## Setup

You need **Python 3.14**. In a fresh environment (a `venv`, conda, ...):

```
pip install -e . --config-settings editable_mode=strict   # the runtime, cdy_rt (editable)
pip install mypy pyright ruff pylint pytest              # checks and tests
```

The runtime package `cdy_rt` (`src/cdy_rt/`) is the only thing generated Python imports.
It is installed editable in strict mode, so edits show up at once; after adding or removing a
module in it, run the `pip install -e .` line again.

To run the bootstrap chain (below) you also need **parsec.py v4**, a typed, functional
rewrite of sighingnow/parsec.py (not the PyPI release, 3.x): only the chain's first step
uses it, where the original Python translator parses. *It isn't published yet*, so for now
the chain's first step runs only where that rewrite is installed (`doc/tech_debt.md`).

## Using it

```
python src/py_cdy/main.py FILE.cdy --run    # translate to output/FILE.py, then run it
python src/py_cdy/main.py FILE.cdy          # translate only
python bin/py/cdy_translator.py FILE.cdy [OUT.py]   # the translator on its own
```

A program that defines `main`, typed `(Fn ((List String)) Int)`, runs it with its
command-line arguments and exits with its result. Errors say `file:line:col: message`.

The language is described informally in `src/cdy/candy-special.md`, and in the design docs in
`doc/hl_rqmt/`; test programs in `tst/cdy/` (`NAME.cdy`, with its output in `NAME.out`) show
it in use. `editors/vscode-candy/` highlights `.cdy` files in VS Code.

## Working on the translator

The translator is `src/cdy/cdyc.cdy` and the files it imports. After changing it, rebuild
the checked-in copy, which must reproduce itself and pass `mypy --strict`
(`bin/README.md`):

```
python src/py_cdy/self_host.py
```

Checks and tests:

```
pytest                                   # all tests (tst/)
pytest -m bootstrap                      # the bootstrap chain too (about a minute)
mypy src/py_cdy src/cdy_rt tst script
pyright src tst script
ruff check src tst script && ruff format src tst script
pylint src/py_cdy src/cdy_rt tst script
```

## Bootstrapping

Candy was first translated by a translator written in Python, which built the first Candy
translator at tag `self-host-py`. Every translator since was built by the one before. The
chain is checked from that Python translator to today's, each step byte for byte:

```
python script/bootstrap.py --from-scratch   # the whole chain
python script/bootstrap.py --list           # its steps, the boot/NN tags
```

See `doc/hl_rqmt/bootstrap.md`.

## Repository

- `src/cdy/`: the translator, in Candy, with the library it reads (`special.cdy`,
  `system.cdy`, `prelude.cdy`, `form.cdy`, `prelude_macros.cdy`);
- `src/cdy_rt/`: the runtime generated Python imports;
- `src/py_cdy/`: the Python driver (`main.py`, `self_host.py`);
- `bin/`: the checked-in translators, one directory per target;
- `script/bootstrap.py`: the bootstrap chain;
- `tst/`: tests and test programs;
- `doc/`: design docs (`hl_rqmt/`), the process (`process.md`), leaks, tech debt and ideas.
