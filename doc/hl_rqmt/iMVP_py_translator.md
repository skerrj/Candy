# iMVP Candy → Python translator

High-level requirements and design notes for the initial MVP (iMVP) translator, on branch
`py-py-translator`. This summarises the discussion that followed `src/cdy/candy-special.md`.
Items are marked **decided** (agreed by the owner), **proposed** (suggested and not yet
agreed) or **open** (needs an answer).

## Purpose

- The iMVP is an **MVP path to bootstrapping Candy**. A translator written in Python turns
  Candy source into Python source. Once Candy is expressive enough, the translator gets
  rewritten in Candy and compiled with this one, so that Candy becomes self-hosting.
- Favour the simplest thing that works over completeness or performance. Parts are expected
  to be replaced. For example, `defn` and `cond` will become macros.
- Candy is a **strongly and statically typed** language (**decided**). The iMVP has to leave
  room for that, even if the iMVP itself does not check types yet.

## Pipeline

```
.cdy file ──reader.py──▶ text ──parse_cdy.py──▶ SExpr AST ──translator──▶ Python source
                                                               ▲
                                              table.py / table_defs.py
                                         (initial symbol table + runtime helpers)
```

| Stage | Module | Status |
|---|---|---|
| Reader | `reader.py`. For the iMVP it just slurps a whole Candy file into a string (**decided**). | Not started. Owner to say whether they provide it or Claude writes it. |
| Parser | `src/py_cdy/parse_cdy.py` (parsec.py v4). Produces `Symbol`, `Number`, `Str`, `Bool` and `SList`, and `'x` becomes `(quote x)`. | Exists, with string literals and `;` comments. |
| Symbol table | `table.py` and `table_defs.py` (**decided**, to be provided by the owner). | Not started. |
| Translator | Proposed: `src/py_cdy/translate_cdy.py`. | Not started. |

## Surface syntax

From `src/cdy/candy-special.md`:

- **Comments (decided):** `;` starts a comment that runs to the end of the line. By
  convention `;` marks an inline comment, `;;` a standalone line comment and `;;;` a section
  header.
- **Grammar notation:** the spec writes special-form grammar with regex operators `?`, `*`
  and `+`, and italics mark placeholders.

Parser work needed before the translator is useful (both done):

1. **Comments: done.** `lexeme` now skips `ignore` (whitespace and `;` comments, ported from
   `doc/hl_rqmt/src/ignore_parse.py`) instead of `spaces`, and `;` ends a number or symbol
   token. Tests are in `tst/py_cdy/test_parse_cdy.py`.
2. **String literals: done.** Parsed into `Str`, with tests in `tst/py_cdy/test_parse_cdy.py`. Self-hosting needs them
   (`slurp`, `format`, string comparisons in macros). smz got its strings from the
   `edn_format` library. smz's `parse_string_help_4` in `smztils.py` handles the escapes
   `\n \t \r \" \\`. The parser uses the `atom_parse.py` grammar below instead.

**Reference: `doc/hl_rqmt/src/atom_parse.py`.** This is an old parser from before schmuz,
written against an early (v3-style) parsec.py. Its string-literal grammar can be reused. It
has JSON-style escapes (`\\ \/ \" \b \f \n \r \t \uXXXX`) and runs of plain characters with
no escapes. It has to be ported to v4:

- `@generate` and `@lexeme` become combinators.
- `.parsecmap` becomes `.map`, and `.result(x)` becomes `>> pure(x)`.
- The `^` try-choice becomes `try_(p) | q`.

The file also suggests other features the spec hasn't decided:

- `[ ]` and `{ }` brackets as well as parentheses.
- Floats and exponents in numbers.
- `true`/`false` for booleans. smz also uses these, while `parse_cdy.py` uses `#t`/`#f`.

Its `ignore` parser (whitespace and `;` comments) is in `doc/hl_rqmt/src/ignore_parse.py`.

## Special forms

| Form | Grammar | Semantics |
|---|---|---|
| `import` | `(import sym)`, `(import-as sym as-sym)`, `(import-from sym from-sym+)` | **Skipped** until after the initial bootstrap. |
| `def` | `(def sym init?)` | Binds `sym`. The spec says it is not immutable, for now. `(def x)` binds `None`, and a `def` form evaluates to `None` (**decided**). `(def)` and a bare `def` are errors (**decided**). |
| `defn` | `(defn sym (args*) expr)` | Defines a function with a single body expression (use `do` for several). It will become a macro. |
| `do` | `(do expr*)` | Evaluates its expressions in order and returns the last value. |
| `if` | `(if test then else?)` | If `else` is missing and `test` is false, the result is `None` (**decided**). |
| `cond` | `(cond (test expr)+ (else expr)?)` | The `else` clause is **optional for now** (**decided**). If no test matches, the result is `None`. It will become a macro. smz expands it to nested `if`s. |
| `let` | `(let ((name init)*) expr)` | Each binding is `(name init)` (**decided**), as in `(let ((x 1) (y 2)) (+ x y))`. |
| `fn` | `(fn (args*) expr)` | Lambda. |
| `format` | Not specified yet (**open**). | In smz, `(format "x: {x} sum: {(f1 x y)}")` becomes a Python f-string whose `{...}` holes contain s-expressions. |
| `tup` | Not specified yet (**open**). | In smz, `(tup a b)` builds a tuple, and `let` can destructure one: `((x y) (mp a b))`. |

## Types

- **Decided:** types are declared in a separate **signature statement**, not inline in
  `def`, `defn` or `fn`. The special-form syntax above therefore stays as it is.
- **Proposed iMVP approach:** the translator attaches each signature to its definition and
  emits Python annotations. For example, a signature for `sq` plus `(defn sq (x) ...)`
  becomes `def sq(x: int) -> int:`. mypy/pyright in strict mode then check the generated
  Python. This gives real static checking straight away, and the self-hosted compiler is
  typed from its first line. Candy's own type checker can replace mypy later without
  changing the syntax.
- **Rejected for the iMVP:**
  - An untyped iMVP with types added later. The self-hosted compiler would need
    retrofitting, and the grammar would change under existing code.
  - A full Candy type checker inside the iMVP. That is too much for a bootstrap.
- **Open (for the signature spec):**
  1. The syntax: its keyword and how function types are written.
  2. Base type names (Candy's own, such as `Int` and `Str`, or Python's), and how they map
     to Python types, possibly through `table.py`.
  3. Compound types: lists, tuples (for `tup`) and function types.
  4. Scope: only top-level `def`/`defn`, or also `let` bindings and `fn`.
  5. Whether a signature is required, or whether an unsigned definition falls back to `Any`
     during bootstrapping.

## Symbol table: `table.py` and `table_defs.py`

**Decided:** operators and builtins (`+`, `*`, `=`, `print` and so on) are not hard-coded in
the translator.

- `table.py` is modelled on `~/dev/smz/smz-core/src/py_smz/table.py`. It maps Candy symbols
  to Python operators and helper definitions and becomes the **initial symbol table**.
- `table_defs.py` starts from `~/dev/smz/smz-core/src/py_smz/smztils.py`. It holds the
  Python runtime helpers that table entries point to.
- A Candy prelude may take this role over later.

How smz's table works:

- It is a set of dicts grouped by area: special forms, math, bool, IO, regex, collections,
  strings, table helpers and infra. These are merged into one `OP_TABLE`.
- Each entry is `{'built-in': <python name>, 'bin_op': bool, 'arity': n}`.
- An `IMPORTS` list gives the import lines to emit at the top of the generated file.
- Helper functions (`is_special_p`, `bin_op_p`, `get_sym_name`, ...) look things up in the
  table, and `add_fun` registers each user `defn` as it is translated.

How smz's `smztils.py` is organised:

- **Runtime helpers called by generated code:** `at`, `slice`, `join_it`, `in_it`,
  `to_int`, the `is_*` predicates, `strip`, `replace`, `slurp`/`spit`/`file_put_lines` and
  `get_args`.
- **`m_table_*` functions:** these let the self-hosted compiler query and extend the op
  table, which is how compiled schmuz code could see the table. Candy will need the same.
- **Generated-code utilities:** `get_indent` and `get_py_imports`.
- **Leftovers:** commented-out experiments and four versions of `parse_string_help`.

**Proposed changes when porting** (to fit this repo's conventions):

1. **No global mutation.** `add_fun` and `m_table_add_fun` change a global dict. Instead,
   make the table an immutable initial value that each `def`/`defn` extends and passes
   along.
2. **Render every argument.** smz renders only `arity` arguments, and `get_sym_arity`
   defaults to 1, so extra arguments are silently dropped. Check arity separately if it is
   wanted.
3. **Typed entries.** Use one `NamedTuple` per entry instead of a dict. That fits mypy
   strict and the no-decorator rule, and leaves room for a type field once signatures exist.
4. **Operators beyond two arguments.** smz's `bin_op` handles exactly two arguments.
   Either fold `(+ a b c)` or make two arguments an explicit rule.
5. **Quirks to check before copying:**
   - `is_coll` tests for `list` while `m_table_is_bin_op` ignores the `bin_op` value. These
     may be things the self-hosted compiler relied on.
   - `slice` shadows Python's built-in.
   - `spit(lines, fn)` and `file_put_lines(fn, lines)` take their arguments in opposite
     orders.
6. **Imports.** smz's `smztils` imports a copied `bop_table`, which is why it needed the
   `cp_py_smz_out` and `update_py_deps` copy scripts. Candy could avoid that by having the
   generated code import `table_defs` from one fixed location.

## Reference prototype: smz-core ("schmuz")

`~/dev/smz/smz-core` is a rough, **untyped** prototype of this same approach, and it is
**already self-hosting**. Use it as a reference, not as a style guide, because it is
imperative and untyped.

How it bootstrapped:

1. `src/py_smz/` (Python) reads `.scm` files with `edn_format`. `render.py` then builds
   Python source text using `table.py`.
2. `py_smz` compiled `src/smz/main.scm` (with modules `parse`, `macros`, `render`,
   `render_help` and `infra`, about 650 lines) into `bin/py/smz.py`.
3. The generated `smz.py` then compiles schmuz itself (`smz_py src/smz/main.scm
   bin/py/smz.py`). It was tagged `v0.0.1`. Notes are in `doc/init_bootstrap_from_py.md`
   and `doc/with_modules_bootstrap.md`.

How smz copes with "everything is an expression": it emits Python **statements** and relies
on `let` and `if` only appearing in **tail position** inside a `def`. `let` becomes
assignments followed by `return`, and `if` becomes `if ...: return ... else: return ...`.
This is simple and worked well enough to self-host, but an `if` or `let` in any other
position produces broken Python.

## Translation strategy (proposed, not decided)

Choose one:

- **A. Build Python's `ast` module (recommended).** Translate each form into a list of
  setup statements plus a final expression.
  - A `do` becomes statements followed by its last expression.
  - A `fn` whose body needs statements becomes a generated nested `def`.
  - An `if` with statement-like branches becomes a Python `if` that assigns a temporary
    variable.
  - Output comes from `ast.unparse` (readable source) or `compile` (to run it).
  - This works in any position.
- **B. Copy smz's tail-position rendering.** It is cheaper and already proven to bootstrap,
  but it restricts where `if`, `let` and `do` may appear.

Either way:

- Candy symbols that are not valid Python identifiers (`a-b`, `empty?`) need consistent
  renaming.
- The translator code follows the repo conventions: typed `NamedTuple` records, pure
  functions and no decorators. See `doc/hl_rqmt/deps/parsec-py-DESIGN-COPY.md`.

## Tooling and conventions

- **Environment:** run everything in the `py_cdy` conda environment:
  `source ~/dev/activate-conda && conda activate py_cdy`. It provides Python 3.14, and
  parsec.py v4 loads from `~/dev/exp/parsec.py/src`.
- **Checks:** `pyproject.toml` sets line length 100 for ruff and pylint and turns on
  `mypy --strict`. mypy, pyright, ruff, pylint and pytest are installed.
- **Tests:** pytest tests go in `tst/py_cdy/`, and Candy-language tests in `tst/cdy/`.
  Adding pytest tests is in `TODOS.md`.

## Next steps

1. ~~Parser: add `;` comments and string literals, with pytest tests.~~ Done.
2. Owner: provide `table.py` and `table_defs.py`, and say whether to provide `reader.py` or
   have Claude write it.
3. Owner: write the signature statement spec, and the `format` and `tup` specs.
4. Pick translation strategy A or B. Then build the translator core for `def`, `defn`, `do`,
   `if`, `cond`, `let` and `fn`, with tests.
5. Wire up reader → parser → translator → `output/`, run mypy on the generated Python, and
   run a first Candy program end to end.
