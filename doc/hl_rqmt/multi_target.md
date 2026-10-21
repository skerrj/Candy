# Candy targets beyond Python (placeholder)

**Status: placeholder.** Python is the only target for the iMVP (see
`doc/hl_rqmt/iMVP_py_translator.md`). Other targets will come later, perhaps the JVM, C or
WASM; none has been chosen. This document collects what the iMVP decisions mean for those
targets, so that they aren't designed out by accident.

## Principles

1. **Type distinctions belong to Candy's front end, not to a backend.** The difference
   between `Int`, `Long` and `Byte`, or between `Char` and `String`, lives in the parser's
   typed AST (each literal type already has its own node) and later in Candy's own type
   checker. Every backend reads it from there.
   - For that reason the Python backend does **not** use `typing.NewType` to keep Candy
     types apart. NewType would only change how mypy checks the generated Python, and other
     targets would get nothing from it.
   - NewType is also awkward in Python itself. Arithmetic drops the wrapper: for two `Long`
     values `a` and `b`, mypy types `a + b` as plain `int`. Typed code would then need casts
     everywhere, or wrapper classes with overloaded operators.
2. **The translator keeps target-independent stages.** The pipeline is:
   - parser → `SExpr`
   - `analyse` → Core AST (typed, once Candy's type checker exists)
   - `lower` → lowered IR, the "pseudo-AST" (statements vs. expressions)
   - one backend per target, which emits that target's code

   The iMVP's Python backend (`emit_py`) is the first such backend. A new target adds its
   own backend and reuses everything before it. See "Stages and targets" below and
   "Layers" in the iMVP doc.
3. **Each target maps the Candy types for itself.** For the iMVP's Python mapping (`Int`,
   `Long` and `Byte` to `int`, and so on), see the iMVP doc.

## Stages and targets

What each stage does, and how much of it a new target can reuse:

| Stage | What it settles | Reused by |
|---|---|---|
| Core AST (`analyse`) | Valid Candy; special forms; `cond` expanded; names resolved to unique binding ids; signatures and (later) types | Every target |
| Core → Core passes (none in the iMVP) | Closure conversion or lambda lifting, for targets without closures | C, WASM |
| Lowered IR (`lower`) | Statements vs. expressions; temporaries; evaluation order; an `if` in value position | Statement-based targets: Python, JavaScript, Java source, C, Go |
| Backend (`emit_<target>`) | Spellings (mangling, keywords); built-ins through the target's table; type mapping; output text or AST | One target |

Expression-based targets (WASM, where blocks yield values; another Lisp) don't need the
statement/expression split. They can lower from Core directly, or use a different IR.

### Target capabilities (`Caps`)

`lower` is shared by the statement-based targets, so it takes a `Caps` record saying what
the target's expressions can do. Where a target can't do something, `lower` falls back to
statements and temporaries.

| Capability | Python | JavaScript | Java | C | Go |
|---|---|---|---|---|---|
| Conditional expression | `a if t else b` | `t ? a : b` | `t ? a : b` | `t ? a : b` | no |
| Anonymous function | lambda, body one expression | closure, any body | lambda (captures effectively final) | none | closure, any body |
| Chained comparison (`a < b < c`) | yes | no | no | no | no |

The iMVP's `Caps` has only `cond_expr` and `lambda_expr` (see `src/py_cdy/lower_cdy.py`);
the other rows become flags when a target needs them.

Some differences are not `lower`'s problem:

- No closures (C): a Core → Core pass first, then `lower`.
- `(< a b c)` on targets without chained comparisons: `a < b and b < c`, with `b` stored in
  a temporary if it isn't a plain name or a constant.
- Integer sizes and memory management: the backend, the runtime and the open questions
  below.

### The symbol table across targets

The iMVP's `TableEntry` already separates the two halves. Its `kind` (`binop`, `compare`,
`call`, ...) and `arity` describe the Candy built-in and hold for any target. Only `py` is
Python-specific. When a second target arrives, split `table.py` into:

- a target-neutral table of built-ins: name, kind, arity and (later) Candy signature;
- one mapping per target, from built-in name to that target's name or operator. Each
  target also gets its own runtime, the equivalent of `table_defs.py`.

Core refers to built-ins by Candy name (`Prim("+")`), so it never sees a target's names.

Later, the target-neutral half becomes Candy code. `system.cdy` (and the files it imports)
declares each built-in with a bodiless `sig`, the way Carp's `register` does, and
`prelude.cdy` defines more on top of it.

*Started on branch `system-prelude`* (`doc/hl_rqmt/system_prelude.md`):
- `src/cdy/system.cdy` holds the Candy type of every built-in but the special forms and
  operators, which gives the Candy translator their arities;
- `table.py` is the Python mapping: each built-in's Python name and kind (its `arity`
  field went once the Python translator left `master`: `doc/hl_rqmt/bootstrap.md`, step 3);
- the operators are still described by the table alone, since a `Fn` type can't say "two
  or more arguments";
- `src/cdy/prelude.cdy` is ordinary Candy, so it is the same for every target.

The open questions below are still open: there is one `system.cdy`, for Python.

### Open: abstracting `system.cdy` while allowing specifics

`system.cdy` has to do two things that pull against each other:

- **Abstract.** Portable Candy code (the prelude, the self-hosted compiler, user programs)
  should see one set of built-ins with one set of types, whatever the target.
- **Allow specifics.** Specifics come at two levels:
  - **Between targets.** Python, C and the JVM offer different built-ins, and the same
    built-in may need a different type or behaviour on each (integer sizes, how strings
    and chars are stored, file I/O).
  - **Within one target.** One target can still differ by platform (Linux, macOS,
    Windows: paths, line endings), by runtime or version (CPython vs. PyPy, Python 3.14 vs.
    later), or by optional libraries (`re` is in the standard library, a GUI toolkit is not).

None of this is designed yet. Questions to answer:

1. **Layout.** One shared `system.cdy` plus per-target files that add or override
   (`system/py.cdy`, `system/c.cdy`), with platform files beneath them
   (`system/py/windows.cdy`)? Or one `system.cdy` per target, with the shared part in a
   file they all import?
2. **Selection.** How does the compiler choose the files: by the target and platform it is
   compiling for, by explicit imports, or by conditional forms inside one file? Examples
   from other languages: Clojure's reader conditionals (`#?(:clj ... :cljs ...)`), Rust's
   `#[cfg(...)]`, Zig's compile-time `builtin.target`, Go's `_linux.go` file suffixes.
3. **Overrides.** May a target-specific `sig` replace a shared one, or only add new names?
   If it replaces one, must the type stay the same, so portable code still type-checks on
   every target?
4. **Portability checks.** How does portable code find out it used a target-only built-in?
   An error unless the code says it is target-specific, or a warning?
5. **Interfaces.** Abstract interfaces such as `Collection` (see the iMVP doc) are one way
   to keep the shared surface small: `system.cdy` declares the interface, and each target
   supplies its own implementation.
6. **Relation to `Caps`.** `Caps` describes what a target's *code* can express (for
   `lower`). This is about what its *runtime library* provides. The two may end up in one
   target description.

### Modules and output units

A **Candy module** (a file, `doc/hl_rqmt/modules.md`) is a namespace: what it defines,
imports and exports. The front end settles that, the same way for every target. An
**output unit** is what a backend writes, and each target has its own natural one:

| Target | Natural output unit |
|---|---|
| Python | one `.py` per module, as a package (or one file for the program, as now) |
| JavaScript | one ES module per file (`import {greet} from "./util.js"`) |
| C | a `.c` and `.h` per module, or one file for the whole program |
| JVM | a class per module |
| WASM, native (LLVM) | object files linked together, or one module for the program |

So whether a backend writes one unit per module or one for the whole program is a choice
for each target, not a property of the language. For that, modules have to reach the
backend:

- **References carry their module.** A `Global` (and a definition, and a type name) holds
  the module and the name, not a prefixed string: `(Global "util" "greet")`. The modules
  MVP flattens it to `util__greet` in `analyse`, which only suits a one-unit backend.
- **Each module's definitions stay grouped**, with its imports, through `lower`.
- **The backend spells references:** flat and prefixed (`util__greet`), qualified
  (`util.greet`), or with an import and a bare name.

Separate compilation and caching then come per target. Macros are separate from all of
this: they run on the translator's **host**, so caching compiled macro files is about the
host's modules, whatever the target (`doc/hl_rqmt/macros.md`, "Terms: host and target").

### Is the pseudo-AST worth it?

- **The Core AST is needed in any case.** The type checker, error messages and every
  backend depend on it.
- **The lowered IR** is worth keeping as its own layer if a second statement-based target
  is likely. It is also worth keeping for bootstrapping: the self-hosted Candy translator
  can keep it as plain data and print Python text from it, without Python's `ast` module.
  (Generated code may depend only on `table.py` and `table_defs.py`.)
- **The risk** is designing the IR around Python alone. To limit it, keep Python-isms out
  of the IR nodes themselves and in `Caps` and `emit_py`: the IR has a `CondExpr` node,
  but a `Caps` flag says whether a target may use it.

## Open language-level questions

Python can't show these differences, so the iMVP can ignore them. A target with
fixed-size numbers can't.

- **Integer sizes and overflow.** Python's `int` has no size limit. On fixed-size targets,
  what are the sizes of `Byte`, `Int` and `Long`? Is overflow an error, a wrap-around, or
  undefined? What is `Byte`'s range: `-128..127` or `0..255`?
- **Float precision.** Python's `float` is 64-bit, so `Float` and `Double` behave the same
  there. Elsewhere `Float` is normally 32-bit.
- **Literal range checks.** Should the parser or type checker reject literals that don't
  fit their type, such as `300b`? The iMVP parser checks no ranges.
- **Char.** Is a `Char` a Unicode code point, a UTF-16 unit, or a byte?

## To be written

- The candidate targets and which comes first.
- The exact lowered IR node set, and whether types live on IR nodes or only on Core.
- How each target provides its runtime: the equivalent of `table.py` / `table_defs.py`.

## Checked-in translators: `bin/<target>/`

`bin/` was git-ignored to leave room for per-target build outputs. It is tracked again from
branch `pre-self-host`, so that a self-hosted translator can be checked in as `bin/py/`
(see `doc/hl_rqmt/self_hosting_primo.md`). It is: `bin/py/cdy_translator.py`. Open: how other targets' outputs fit next to it
(checked-in bootstrap translators in `bin/<target>/`, with throwaway build output under
`output/<target>/`?).
