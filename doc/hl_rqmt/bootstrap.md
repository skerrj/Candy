# Bootstrap: the frozen Python translator off `master`, checked through the history (HLD)

**Status: proposal (draft); option B decided** (the history, not a separate repo; see
"Repo or history"), **and the `boot/NN` tags** ("Tags and history"). Written on branch `system-prelude`; proposed as its own branch after
that one is merged, before or alongside the library branch (`doc/hl_rqmt/library.md`),
whose table work it makes simpler.

## Where things stand

- **The Python translator is frozen** at tag `self-host-py` (`src/py_cdy/`: `parse_cdy`,
  `core_cdy`, `lower_cdy`, `emit_py`, `translate_cdy`). It can't build today's
  `src/cdy/`; the checked-in `bin/py/cdy_translator.py` builds each new translator.
- **It still runs here,** and keeps code in step with it:
  - its own tests (`test_parse_cdy.py`, `test_core_cdy.py`, `test_lower_cdy.py`,
    `test_emit_py.py`), and the golden tests in `test_cdy_programs.py`, which translate
    `tst/cdy/` with it;
  - `main.py` translates with it unless given `--translator bin` or `t1`;
  - `self_host.py` uses `parse_cdy` to check that the Candy reader (`read.cdy`) reads
    what `parse_cdy` reads (`to_form`, `parse_forms`);
  - it reads the live `table.py`, so `table.py` keeps `arity` for it alone
    (`doc/hl_rqmt/system_prelude.md`, step 2 dropped; `doc/tech_debt.md`).
- **It is the only way to build Candy from scratch,** from a language that isn't Candy.
  Today that bootstrap is only implicit in the history: each commit's `bin` was built by
  the one before. Since `self-host-py`, 16 of 37 commits changed `bin/`, so the chain has 17 steps.

## Goals

1. **`master` holds only Candy and its runtime:** `src/cdy/`, `src/cdy_rt/`, `bin/`, and
   the Python driver pieces (`self_host.py`, `main.py`, `reader.py`).
2. **The bootstrap is explicit and checked:** a script builds Candy from the Python
   translator at `self-host-py` to today's `bin`, through the history, and says whether
   every step reproduces what was checked in.
3. **The runtime is free to change:** `table.py` loses `arity`, and nothing frozen reads
   it.

Not goals: a bootstrap from anything but Python; making old commits build faster; a
separate repo (for now).

## Proposal

### Repo or history (decided: the history)

The chain needs this repo's history either way (the Candy source of every step is here),
so a separate repo would only hold the starting point and the script. So:
- the Python translator is removed from `master` and stays at tag `self-host-py`;
- `script/bootstrap.py` (`script/` is an empty placeholder today) walks the chain;
- each step is a `boot/NN` tag (below), which records what the step needs.

If a standalone bootstrap is wanted later, `src/py_cdy` at the tag can be split out into
its own repo (`git subtree split`), named `candy-bootstrap`.

### Tags and history (decided)

The chain is anchored on tags, not on branches: a tag keeps its commit reachable even if a
branch is rewritten, so the chain survives a rewrite.
1. **One annotated tag per step, `boot/NN`:** `boot/00` is `self-host-py`, and `boot/01`
   on are the later commits that changed `bin/`, in order (16 today). The tag's message
   records the step's Python version and any staging it needs, for example:

   ```
   boot/05: python 3.14
   staging: none
   ```

   So there is no separate list file, and a commit needn't name itself: it is tagged after
   it is made. `boot/` can't clash with a branch name (`macros` and `modules` are both a
   branch and a tag). The script reads the chain with `git tag -l 'boot/*'`.
2. **Tagging new steps:** a commit that changes `bin/` gets the next `boot/NN` when it is
   committed (with gawc).
3. **Before any history rewrite** (only when the owner asks for one): tag the old tip
   `archive/<branch>-<YYYY-MM-DD>` and push the tag first. The `boot/` tags keep the old
   chain alive either way; rewritten commits that change `bin/` get new `boot/` tags only
   if the chain is moved onto them, decided then.
4. **Never delete** `boot/*` or `archive/*` tags, locally or on `origin`.
5. **Pushing** uses full refs, as for everything else: `git push origin
   refs/tags/boot/NN:refs/tags/boot/NN`.

### The chain

The steps are `self-host-py` and then every commit after it that changed `bin/`. Each step
**reuses that commit's own `self_host.py`**, which by construction worked with the `bin`
before it:
- **at `self-host-py`**, `build_bin` builds T1 with the Python translator, and T1 builds
  the `bin`;
- **at every later step**, `build_bin` builds T1 with the checked-in `bin`, T1 builds T2,
  and T2 replaces the `bin`.

So the script, for each step C:
1. checks C out into a scratch worktree (`git worktree add`, under `tmp/bootstrap/`);
2. replaces C's `bin` with the previous step's output (not at `self-host-py`);
3. copies C's library files (`self_host.LIBRARY` at C: `form.cdy`, `system.cdy`, ...)
   next to that translator, the staging most rebuilds needed (`system-prelude` step 5);
4. applies any other staging C's `boot/NN` tag lists;
5. runs C's `python src/py_cdy/self_host.py`, with `PYTHONPATH` putting C's `src/` first
   so that C's `cdy_rt` is the runtime, not the installed one;
6. compares the `bin` it wrote with C's checked-in `bin`, byte for byte, and keeps it for
   the next step.

### Testing it

- **The check is by induction, so steps are independent.** If each step C reproduces C's
  checked-in `bin` from its parent step's checked-in `bin`, then the whole chain from
  the Python translator reproduces today's `bin`. So the script can check:
  - **one step** (`bootstrap.py --step C`), using the parent step's checked-in `bin`;
  - **all steps** from their checked-in parents (`--check`), in any order or in parallel;
  - **the true chain** (`--from-scratch`), feeding each output into the next: the slow,
    final proof, run when it matters (before a merge into `master`).
- **In the test suite:**
  - an opt-in pytest (a `bootstrap` marker, skipped unless asked for) that runs
    `--check`; a few minutes, too slow for every run;
  - a fast test, run always: every commit that changed `bin/` since `self-host-py` is a
    step: it has a `boot/` tag, numbered in order (the newest commit is exempt until it
    is tagged), so the tags can't drift silently.
- **The current step.** Until it is tagged, the newest step is checked by what already
  runs: `test_self_host.py` checks that `bin` is T2. The script's
  `--step HEAD` adds the stronger check (the parent's `bin` builds today's `bin`)
  before a commit that changes `bin`.
- **What can make a step differ** besides a bug, so the script records them:
  - **the Python version:** `py-mangle` avoids the names in `dir(builtins)`, so a new
    built-in in a later Python changes mangling, and the output. each `boot/NN` tag records
    the Python version each step was built with (3.14 today), and the script warns on a
    mismatch;
  - **mypy's version:** it only checks, so it changes pass or fail, not the output;
  - **parsec v4:** only the `self-host-py` step uses it (a pinned commit of
    `functional-rewrite`).
- **Finding the chain** is the first run: `--check` over all steps, then a staging entry
  in the `boot/NN` tag of each step that fails until staged by hand (macros step 5 may be
  one).

### `master`, after the move

- **Removed:** `parse_cdy`, `core_cdy`, `lower_cdy`, `emit_py`, `translate_cdy` and their
  tests.
- **`test_cdy_programs.py`:** translates `tst/cdy/` with `bin` (as `test_self_host.py`
  already does with T1 and T2), still checked with `mypy --strict`.
- **`main.py`:** translates with `bin` by default; `--translator` keeps `t1`.
- **`self_host.py`:** the reader check against `parse_cdy` goes. The Candy reader is
  checked by its own tests (`tst/cdy/`, the error tests in `test_self_host.py`); the
  agreement test was for porting the reader, which is done.
- **`table.py`:** drops `arity` (the dropped step 2), and the tech debt entry goes.
- **Docs:** CLAUDE.md, `bin/README.md` and the iMVP doc point at the bootstrap;
  `doc/leaks.md` and the archives keep the Python translator's leaks as history.

## Steps (sketch)

1. **The script and the chain:** `script/bootstrap.py` (`--step`, `--check`,
   `--from-scratch`); run `--check`, stage the steps that need it, tag `boot/00` to
   `boot/16` (pushed), then `--from-scratch` passes. Tests: the fast list check and the opt-in `--check`.
2. **Remove the Python translator** from `master`: the files, their tests and the
   `main.py` default; `test_cdy_programs.py` on `bin`.
3. **`table.py` without `arity`.**
4. **Docs.**

Step 1 comes first and runs while the Python translator is still on `master`, so the
chain is proven before anything is removed.

## Questions (open)

1. **The reader agreement check:** drop it (proposed), or keep it as part of the
   `self-host-py` step?
2. **When `--from-scratch` runs:** before each merge into `master` (proposed), or only
   by hand?
3. **Order:** before the library branch (proposed, so its table work needn't keep
   `arity`), or with it?
