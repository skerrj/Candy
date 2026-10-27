# Name checks (HLD)

**Status: accepted (2026-10-26), with the proposed answers to its questions; branch
`name-checks`.** For a branch `name-checks`, after tag
`triage`. From the triage ([[B103]]): three of its `high` defects, [[B3]], [[B12]] and
[[B2]], are names the translator doesn't check.

## Where things stand

- **Python names can collide.** `py-mangle` (`src/cdy/emit.cdy`) turns `-` into `_`, so
  the top-level names `a-b` and `a_b` are both `a_b`, and the second definition silently
  replaces the first ([[B3]]). A module's names get its stem as a prefix (`util__greet`,
  in `cdyc.cdy`), which is also what the top module's `util--greet` mangles to; the reader
  rejects `__` in a name, but not `--` ([[B12]]). Locals are safe: a function's locals are
  renamed apart (`(let ((a-b 1) (a_b 2)) ...)` works).
- **Types aren't checked.** Nothing lists the types that exist or how many arguments each
  takes, so `analyse` reads any `(Name arg ...)` as a type ([[B2]]): `(List)` crashes
  `emit-tcon` with Python's `IndexError`, `(Maybe Int Int)` and `(Int String)` drop their
  extra arguments silently, `(Shape Int)` for a non-generic `Shape` is left to mypy, and
  `(sig x Foo)` with no `Foo` anywhere translates and runs. The built-in types are known
  only to `emit-tcon`'s `cond`, which spells each one in Python.

## Goals

- Two Candy names that would be one Python name are an error, at top level and across
  modules.
- Every type a program writes names a type that exists, with the right number of
  arguments; the built-in types are declared in Candy, as the built-in functions are.
- Each defect's repro passes and moves into its spec file.

**Not goals:** a type checker ([[B15]]); a type from a module the file doesn't import
([[B53]]), though step 2's check is where it would go; record fields that mangle alike,
which go with [[B5]] and [[B6]]; variadic types for `Tup` ([[B99]]).

## Proposal

### Python-name clashes ([[B3]], [[B12]])

Where top-level names become Python names (`add-globals` in `emit.cdy`, which already
keeps the Python names `taken`), a Python name already taken by a *different* Candy name
is an error: `a-b and a_b are one name in Python (a_b)`. The module prefix is applied
before the check, so the top module's `util--greet` against `util`'s `greet` is the same
error. Nothing about mangling changes, so `bin`'s output doesn't either.

### Built-in types ([[B2]])

`system.cdy` declares the built-in types as bodiless `deft`s, as it declares the built-in
functions as bodiless `sig`s; a type's parameters give its arity:

```candy
(deft Int) (deft Long) (deft Byte) (deft Float) (deft Double) (deft Bool) (deft Char)
(deft String) (deft Unit) (deft Any)
(deft (Maybe a))
(deft (List a))
(deft (Map k v))
```

`read-builtins` (`core.cdy`) reads them into the builtins, and `analyse-type` checks each
type it reads against them and the program's own `deft`s: the name exists (`unknown type
Foo`), and the number of arguments matches (`List takes 1 type argument, got 0`). `Fn`
keeps its own form, `(Fn (args) ret)`; `Tup` takes any number, so it stays special until
variadic types ([[B99]]). The Python spellings (`int`, `tuple[a, ...]`, `_cdy_Mapping[k,
v]`) move from `emit-tcon` into `spelling.py`, next to the functions', checked against
`system.cdy` both ways as the functions are.

## Pros and cons

- **Pro:** three silent wrong outputs become errors; the built-in types are data, in one
  place, as the functions have been since `symbol-table`.
- **Pro:** rejecting a clash changes no generated name, so step 1 leaves `bin`'s output as
  it is.
- **Con:** a bodiless `deft` is a new form in `system.cdy`, which the old `bin` (reading
  its own `bin/py/system.cdy`) doesn't know: step 2 needs two rebuilds (see "Bootstrap").
- **Why now:** they are the backlog's small `high` items, and step 2 is the groundwork for
  any type checking Candy does itself ([[B15]]).

## Bootstrap

Step 1 is one rebuild. Step 2 first teaches the translator to read bodiless `deft`s in
`system.cdy` and the type spellings in `spelling.py`, with the old declarations still
working (one rebuild, `boot/NN`); then `system.cdy` (and `bin/py/system.cdy`) gets the
`deft`s and `emit-tcon` its spellings from `spelling.py` (a second rebuild, `boot/NN`).

## Steps

1. **Python-name clashes:** the check in `add-globals`, with the module prefix applied
   first; [[B3]] and [[B12]]'s repros pass and move into the spec (`[[syntax.names]]`); a
   two-file case as a test program in `tst/cdy/cdyc/`.

   *Done.* As built:
   - **`add-globals`** (`emit.cdy`): a Python name already taken by another top-level name
     fails, naming both as written, a module's own name as `greet (in util)`
     (`candy-name`; a name can't hold `__`, so the first one ends the prefix):
     `greet (in util) and util--greet are one name in Python (util__greet)`. The names
     reach `emit` already prefixed by `analyse`, so one check covers both items. It also
     catches a reserved name's trailing `_`: `print_` and `print` clash.
   - **The spec:** `[[syntax.python-names]]` (in `spec/00-syntax.md`, *lasting*), with
     two error rows and a `candy run` showing locals renamed apart. [[B3]]'s repro was
     text, so the rows replace it.
   - **Tests:** the two-file case is a `test_module_errors` row (an error needs no test
     program).
   - **Bootstrap:** one rebuild; `bin` gains the check (129 changed lines), and translates
     itself unchanged otherwise.
2. **Built-in types:** bodiless `deft`s in `system.cdy`, read with the built-ins;
   `analyse-type` checks names and arity; the spellings in `spelling.py`; [[B2]]'s repros
   pass and move into `spec/20-types.md` (`[[types.table]]`), with the other cases of its
   table as error rows.

   *Done, in two commits (see "Bootstrap").* As built, the first (`boot/35`):
   - **`core.cdy`:** a `Builtin` variant `BType` (its arity); `read-sigs` reads a
     bodiless `(deft Name)` or `(deft (Name a ...))` in `system.cdy` (`read-type`), which
     needs a `type` entry in `spelling.py`; a built-in type isn't a value (`resolve`).
   - **`emit.cdy`:** `emit-tcon` spells a type with a `type` entry from it, `{}` standing
     for the arguments, and falls back on its own `cond` for the rest.
   - Nothing is declared yet, so the output is the same.
3. **Docs:** CLAUDE.md ("The built-ins"), `symbol_table.md`'s pointer, the spec.

## Questions (answered: the proposals, 2026-10-26)

1. **A clash: reject, or mangle so names can't collide?** Mangling injectively (`-` to
   `_d_`, say) would change nearly every name in `bin` and make the Python harder to read.
   **Proposed: reject** (*lasting*: a Candy name that mangles like another is an error).
2. **[[B12]]: the clash check, or also ban `--` in names?** The check alone catches it,
   and whatever a later mangling might cause. **Proposed: the check alone.**
3. **Where the clash check goes:** in `emit` (`add-globals`, where the Python names are
   made) or in `analyse`? `emit`'s errors have no position ([[B14]]), so the message names
   both Candy names instead. **Proposed: `emit`, for now**, until `analyse` knows the
   Python names.
4. **The built-in types: bodiless `deft`s in `system.cdy`?** Or a new form
   (`(type (List a))`), or in `special.cdy`. **Proposed: bodiless `deft`s in `system.cdy`**:
   no new form, and the same shape as a program's own generic `deft`.
