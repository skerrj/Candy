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
| Parser | `src/py_cdy/parse_cdy.py` (parsec.py v4). Produces `Symbol`, `SList`, `Str` and one node per literal type (see below). No `'` shorthand. | Exists, with typed literals, string literals and `;` comments. |
| Symbol table | `table.py` and `table_defs.py` (**decided**, to be provided by the owner). | Not started. |
| Translator | Proposed: `core_cdy.py` (`analyse`), `lower_cdy.py` (`lower`), `emit_py.py`, all in `src/py_cdy/`. See "Layers" under option A. | Not started. |

## Surface syntax

From `src/cdy/candy-special.md`:

- **Comments (decided):** `;` starts a comment that runs to the end of the line. By
  convention `;` marks an inline comment, `;;` a standalone line comment and `;;;` a section
  header.
- **Literals (decided).** Each literal has its own type and its own AST node:

  | Literal | Type | AST node |
  |---|---|---|
  | `100`, `-7` | Int | `Int` |
  | `1500l` | Long | `Long` |
  | `3.14f` | Float | `Float` |
  | `10.0` | Double | `Double` |
  | `1b` | Byte | `Byte` |
  | `true`, `false` | Bool | `Bool` |
  | `\e` | Char | `Char` |
  | `"text"` | String | `Str` |

  These replace the parser's earlier `#t`/`#f`, and `true`/`false` are now literals, not
  symbols. A literal must end at a delimiter (whitespace, a paren, `;` or end of input), so
  `12x` and `1.5l` are errors, while `trueish` is a symbol.

  Parser choices not stated in the spec (**proposed**):
  - Suffixes are lowercase only (`1500L` is an error).
  - Float and Double need digits on both sides of the point (`1.` and `.5` are not numbers;
    `.5` is a symbol), and there are no exponents.
  - `3f` (Float suffix with no point) is an error.

  **Open:**
  - Byte's range, Int/Long sizes, overflow and Float precision. These matter once there is a
    second target; see `doc/hl_rqmt/multi_target.md`. The parser checks no ranges yet.
  - Named chars for characters that can't follow `\` directly, such as space and newline
    (Clojure uses `\space`, `\newline`, `\tab`). `\` followed by whitespace is
    currently an error.
- **No `'` shorthand (decided):** `'` is reserved and is a parse error for now. Write
  `(quote x)` instead. The shorthand will be added later as a Clojure-style reader macro.
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
| `let` | `(let ((name init)*) expr)` | Each binding is `(name init)` (**decided**), as in `(let ((x 1) (y 2)) (+ x y))`. Bindings are sequential, like Scheme's `let*`: each `init` sees the earlier names (**decided**). |
| `fn` | `(fn (args*) expr)` | Lambda. |
| `deft` | `(deft Name ((field Type)*))` | Defines a record (product) type (**proposed**), modelled on Carp's `deftype`. See "User-defined types" under Types. |
| `get`, `assoc` | `(get obj field)`, `(assoc obj field value ...)`, one or more field/value pairs | Generic field access for `deft` records (**decided**; the names are **proposed**). `assoc` returns a copy. |
| `quote` | `(quote form)` | Returns `form` unevaluated (**decided**). There is no `'` shorthand yet; it will come later as a Clojure-style reader macro. The runtime representation of quoted data is **open** (see option A). |
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

### User-defined types: `deft` (proposed)

Modelled on Carp's `deftype`. In Carp:

```clojure
(deftype Vector2 [x Int, y Int])          ; a product (record) type; commas are whitespace
(deftype (Pair a b) [first a, second b])  ; generic
(deftype Shape (Circle [Double]) (Rect [Double Double]))  ; a sum type
```

For a product type, Carp generates a constructor (`Vector2.init`), getters (`Vector2.x`),
setters (`Vector2.set-x`, and `Vector2.set-x!` to mutate), updaters (`Vector2.update-x`)
and helpers such as `str` and `copy`.

**Candy syntax.** Candy has no `[...]` and no commas, so fields are `(name Type)` pairs,
the same shape as `let`'s `(name init)` bindings:

```clojure
(deft Vector2 ((x Int) (y Int)))
```

`deft` declares a type, not a value, so field types written inline don't contradict the
rule that `def`, `defn` and `fn` take their types from signature statements.

**Field access is generic (decided).** Fields are reached through generic forms, not
through per-type names like Carp's `Vector2.x` or Scheme's `vector2-x`. The names `get` and
`assoc` are **proposed** (`assoc` is Clojure's name for "a copy with a field replaced"):

| Candy | Meaning | Python |
|---|---|---|
| `(deft Vector2 ((x Int) (y Int)))` | Defines the type | `class Vector2(NamedTuple):` with `x: int` and `y: int` |
| `(Vector2 1 2)` | Constructor: the type name itself, rather than Carp's `Vector2.init` | `Vector2(1, 2)` |
| `(get v x)` | The field `x` of `v` | `v.x` |
| `(assoc v x 3)` | A copy of `v` with `x` replaced (like Carp's `set-x`, not `set-x!`) | `v._replace(x=3)` |
| `(assoc v x 3 y 4)` | Several fields at once | `v._replace(x=3, y=4)` |

- **`get` and `assoc` are special forms.** The field name is a bare symbol and is not
  evaluated, the same way `def` treats its name. Their Core nodes are `Get(obj, field)`
  and `Assoc(obj, ((field, value), ...))`.
- **Why generic.** The translator doesn't need to know `v`'s type to write `v.x`, which
  matters while the iMVP has no type checker of its own. mypy still rejects a field that
  doesn't exist. Later, Candy's type checker resolves the field from `v`'s type, and
  backends that need the type (a C `struct`, for example) get it from there. `deft` adds
  no getter or setter names to the table, and the user's namespace stays small.
- **Later.** `get` could also cover maps, as Clojure's does, once Candy has them.

- **`NamedTuple` fits the repo's own style**: immutable, typed, and no decorators. mypy
  checks the field types, and it works for the self-hosted compiler's own AST nodes.
- **Table.** `deft` adds only the constructor to the table in `ctx`, as an ordinary
  `call` entry, the same way a `defn` adds its name. `get` and `assoc` go in
  `SPECIAL_FORMS`.
- **Type namespace.** `Vector2` also becomes a type name that signatures (and other
  `deft`s) can use. Field types are Candy type names, mapped to Python types like any
  other: `Int` becomes `int`, and a user type keeps its name. The generated module starts
  with `from __future__ import annotations`, so a type can refer to itself or to a type
  defined later in the file.
- **Core.** A `Deft(name, fields)` node, allowed only at top level, plus `Get` and
  `Assoc`.
- **Other targets.** A Candy record maps naturally to a C `struct`, a Java `record` or a
  JavaScript class, so `Deft` belongs in Core, not in the Python backend.

**Open (for `deft`):**

1. ~~**Accessor names.**~~ Generic (**decided**). Still open: the names `get` and
   `assoc`. Clojure-style alternatives are `(.x v)` or `(:x v)`; both already parse as
   symbols.
2. ~~**Mutation.**~~ **Skipped for the iMVP (decided).** Records stay immutable, and there
   is no `set-x!`. See `doc/hl_rqmt/mutation_optimization.md` (a placeholder HLD for
   mutation and optimizations).
3. **Generics.** Carp's `(deftype (Pair a b) ...)` would be `(deft (Pair a b) ((first a)
   (second b)))`. Python 3.12+ can express this as `class Pair[A, B](NamedTuple):`. This
   depends on how the signature spec writes type variables.
4. **Sum types.** These could be `(deft Shape (Circle ((r Double))) (Rect ((w Double) (h
   Double))))`. That can be told apart from a product type, because each variant starts
   with a symbol, while a product's field list starts with a list. Sum types need a `match`
   form to be useful, so they come after the iMVP. In Python they would be one `NamedTuple`
   per variant plus a type alias for their union.
5. **Compound field types**, such as a list of `Int`. These wait on the signature spec's
   compound types (open item 3 above).

## Symbol table: `table.py` and `table_defs.py`

**Decided:** operators and builtins (`+`, `*`, `=`, `print` and so on) are not hard-coded in
the translator.

- `table.py` is modelled on `~/dev/smz/smz-core/src/py_smz/table.py`. It maps Candy symbols
  to Python operators and helper definitions and becomes the **initial symbol table**.
- `table_defs.py` starts from `~/dev/smz/smz-core/src/py_smz/smztils.py`. It holds the
  Python runtime helpers that table entries point to.
- A Candy prelude may take this role over later.

**Runtime boundary (decided).** Generated Python code may depend only on `table.py` and
`table_defs.py`, not on the rest of `py_cdy` (parser, translator). The two modules import
only each other and the standard library, so they can be shipped or pinned on their own
alongside generated code.

**Layout (proposed, owner leaning towards it).** Move the two modules into their own
runtime package, `src/cdy_rt/` (the name is a placeholder), separate from the compiler in
`src/py_cdy/`. Generated code imports `cdy_rt.table_defs`, and only `cdy_rt` has to be on
the path, through an editable install of just `cdy_rt` or `PYTHONPATH=src`. The compiler
imports `cdy_rt.table`, and nothing in `cdy_rt` imports the compiler. Pinning a bootstrap
release then means tagging or copying only `cdy_rt/`. This replaces smz's copy scripts
(`cp_py_smz_out`, `update_py_deps`). The first drafts are in `src/py_cdy/` until the owner
has reviewed them; see `TODOS.md`.

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

- **A. Build Python's `ast` module (recommended).** Every Candy form can appear anywhere,
  and the translator rearranges the output so that it is valid Python. Detailed in the next
  section. The recommended version splits the work into layers (a Core AST and a small
  lowered IR, or "pseudo-AST", before Python's `ast`); see "Layers" below.
- **B. Copy smz's tail-position rendering.** It is cheaper and already proven to bootstrap,
  but it restricts where `if`, `let` and `do` may appear. See the comparison at the end of
  the next section.

Either way, the translator code follows the repo conventions: typed `NamedTuple` records,
pure functions and no decorators. See `doc/hl_rqmt/deps/parsec-py-DESIGN-COPY.md`.

## Option A in detail: `ast`-based translation

### The problem

In Candy every form is an expression and produces a value. In Python, many constructs are
statements: assignment, `def`, `if` with several steps per branch, and anything that needs
more than one line. An expression cannot contain a statement. So a Candy form such as
`(put (let ((m (* n 2))) (+ m 1)))` has no direct Python equivalent: the `let` needs an
assignment, but it sits inside a function-call argument.

### Layers: Core AST, lowered IR, Python (proposed)

Instead of going straight from `SExpr` to Python's `ast`, the translator has three steps.
Only the last one knows about Python.

```
SExpr ──analyse──▶ Core AST ──lower──▶ Lowered IR ──emit_py──▶ Python ast ──unparse──▶ .py
(parser)           every form an       statements vs.          the only Python-
                   expression;         expressions;            specific step
                   names resolved      temporaries, order
```

Proposed modules: `core_cdy.py` (nodes and `analyse`), `lower_cdy.py` (IR nodes and
`lower`), `emit_py.py`.

**1. Core AST (`analyse`): target-independent.** It turns the generic `SList`s into one
node per special form and checks their shape, so `(def)` and a `let` binding that isn't
`(name init)` are rejected here, with Candy-level error messages. It also:

- expands `cond` into nested `If`s, as the future macro will;
- desugars `let` into nested applied `Fn`s, as in Scheme (**decided**; see the `let`
  note below);
- resolves every symbol to a local binding, a global or a table entry;
- gives every binding a unique id. An inner `x` and an outer `x` become `Local("x", 7)` and
  `Local("x", 3)`, so shadowing is settled once, here, instead of again in every backend;
- attaches signatures. Later, Candy's own type checker runs on this stage and fills in
  the types.

| Node | Fields |
|---|---|
| `Lit` | `value` (`int`, `float`, `bool`, `str` or `None`), `ctype` (`"Int"`, `"Char"`, ...) |
| `Local` | `name`, `id` |
| `Global` | `name` |
| `Prim` | `name`: a table entry such as `+` or `slurp` |
| `Call` | `fn`, `args` |
| `If` | `test`, `then`, `other` |
| `Do` | `body` |
| `Fn` | `params` (`Local`s), `body` |
| `Def` | `name` (`Global`), `init` |
| `Defn` | `name` (`Global`), `params`, `body` |
| `Quote` | `form` (the `SExpr`, as is) |

**2. Lowered IR (`lower`): the pseudo-AST.** This does the "statements first, then an
expression" work described in the rest of this section, but builds a small IR of its own
instead of Python `ast` nodes. The IR has:

- statements: `Assign`, `ExprStmt`, `Return`, `IfStmt`, `FuncDef`;
- expressions: `Const`, `Ref`, `CallE`, `BinOp`, `Compare`, `BoolOp`, `Not`, `CondExpr`,
  `LambdaE`.

Modes, temporaries, evaluation order and an `if` in value position are handled here. These
problems are shared by every statement-based target (C, Java, JavaScript, Go, ...), not
just Python. Names are still binding ids, not Python spellings.

Targets differ in what their expressions can hold. Python has `a if t else b` and lambdas
whose body is a single expression. C has `?:` but no closures, and Go has neither. So
`lower` takes a `Caps` record saying what the target allows, and falls back to statements
where it can't. The iMVP defines Python's `Caps` only. See `doc/hl_rqmt/multi_target.md`
for the other targets.

**3. Python backend (`emit_py`).** Mostly one IR node to one `ast` node. It also:

- picks Python spellings: name mangling (below), keyword clashes, and renaming a binding
  only if another binding with the same spelling is already used in the same Python
  function (the `let` scoping rule below, applied by binding id);
- maps each `Prim` through `table.py`: `+` becomes `ast.Add`, and `slurp` becomes
  `table_defs.slurp`;
- maps Candy types to Python annotations.

`ast.unparse` then writes the text, and gets operator precedence and parentheses right.

**Why the extra layers pay off in the iMVP.**

- **Core** separates "is this valid Candy?" from "how is it written in Python?". It gives
  clear errors and can be unit-tested without producing any Python. The type checker needs
  it anyway.
- **The IR** costs about a dozen small NamedTuples and a short emitter. In return, the
  hard part (modes, temporaries, evaluation order) is tested on plain data, and a second
  target reuses it.
- **Bootstrapping.** The self-hosted translator, written in Candy, compiles to Python that
  may depend only on `table.py` and `table_defs.py`. Building Python `ast` nodes from Candy
  would need table entries for dozens of `ast` constructors. With an IR of its own, the
  Candy version keeps steps 1 and 2 as plain data and replaces only `emit_py`, with a
  small text printer. That printer indents with `get-indent`, as smz does, and puts
  parentheses around every compound subexpression. The Python-hosted iMVP can still use
  `ast`, because it is convenient and `compile()` checks its output.

**Costs and risks.** There is one more layer to keep in step. An IR designed with only one
target in sight may need reshaping when a second arrives, so keep it minimal: add a node
only when a form needs it.

**Fallback.** If three steps feel like too much for the iMVP, merge steps 2 and 3, so that
`lower` builds Python `ast` directly as described below, but keep Core. Splitting them
later is mechanical as long as Core exists.

The rest of this section describes the lowering in terms of the Python it produces. With
the layers above, `lower` builds the IR equivalents and `emit_py` turns them into Python.

### Core shape

Each form translates to a pair: the statements that must run first, and an expression for
the form's value.

```python
class Lowered(NamedTuple):
    stmts: tuple[Stmt, ...]  # run these first, in order
    expr: Expr               # then this is the form's value
```

`Stmt` and `Expr` are the lowered IR's node types (or `ast.stmt` and `ast.expr` if steps 2
and 3 are merged).

The `let` example above becomes `stmts = (m = n * 2,)` and `expr = print(m + 1)`. Whoever
uses the result (a function body, an enclosing `do`, the module) emits the statements
first and then uses the expression.

Translation is a pure function. Everything it needs is passed in and returned explicitly:

```python
class Ctx(NamedTuple):
    table: Table               # initial symbol table (table.py) plus user definitions so far
    sigs: Signatures           # signature statements seen so far, by name
    env: Env                   # Candy name -> Python name for the current scope
    fn_locals: frozenset[str]  # Python names already bound in the current Python function
    counter: int               # for fresh generated names

def lower(form: SExpr, mode: Mode, ctx: Ctx) -> tuple[Lowered, Ctx]: ...
```

With the layers above, `lower` takes a Core node instead of an `SExpr`, and `env` and
`fn_locals` are not needed in it: `analyse` resolves names to binding ids, and `emit_py`
tracks which spellings each Python function uses.

A new `Ctx` comes back because translating can add definitions and use up fresh names.

### Modes: avoiding temporaries

A naive version would store every intermediate value in a temporary variable. Instead, each
form is translated in one of three modes, depending on what the surrounding code needs:

| Mode | Used for | Effect |
|---|---|---|
| `value` | Function arguments, `let` initialisers, `if` tests | Produces an expression. Statements only when unavoidable. |
| `tail` | The last form of a function body | Produces `return <expr>`, so an `if` can return from each branch with no temporary. |
| `effect` | Top-level forms, all but the last form of a `do` | The value is thrown away. An expression is emitted as a plain statement (a call), and a pure value is dropped. |

With these modes, typical code comes out looking like smz's hand-shaped output. Temporaries
appear only where Candy really nests a statement inside an expression.

Generated names use a reserved prefix, `_cdy_` (`_cdy_t1`, `_cdy_fn2`, ...), that mangled
user names can never produce.

### Rules for each form

**Literals.** Every literal becomes `ast.Constant`. A missing value is `Constant(None)`.
For now the iMVP uses the simplest mapping to Python types (**decided**):

| Candy | Python |
|---|---|
| `Int`, `Long`, `Byte` | `int` |
| `Float`, `Double` | `float` |
| `Bool` | `bool` |
| `Char`, `String` | `str` (a `Char` is one character long) |

As a result, mypy can't tell an `Int` from a `Long`, or a `Char` from a `String`. That is
intended: Python won't be the only target, so these distinctions belong to Candy's front end
and type checker, not to the Python backend. That is also why `typing.NewType` was rejected.
See `doc/hl_rqmt/multi_target.md`.

**Symbols.** A symbol is looked up first in `ctx.env` (local names), then in the table.

- Table entries for values become their Python name. For example, `PI` becomes `math.pi`.
  Dotted names are built with `ast.parse(name, mode="eval").body`, which gives an
  `Attribute` chain.
- An unknown symbol is treated as a global name for now (mangled). That allows forward
  references between top-level `defn`s, which Python resolves at call time.

**Calls: `(f a b)`.** Each argument is translated in `value` mode, and the result is the
call `f(a, b)`. One subtlety is **evaluation order**. If a later argument has statements,
those statements would run before the earlier arguments are evaluated. So when any argument
has statements, every earlier argument that is not a constant or a plain name is first
stored in a temporary:

```python
# (f (g n) (let ((x 1)) x))
_cdy_t1 = g(n)
x = 1
f(_cdy_t1, x)
```

**Operators.** Table entries say what kind of operator a symbol is:

- Arithmetic (`+ - * /`) becomes `ast.BinOp`. With more than two arguments it folds from the
  left: `(+ a b c)` gives `a + b + c`.
- Comparisons (`= < <= ...`) become `ast.Compare`. With more than two arguments they chain:
  `(< a b c)` gives `a < b < c`, which matches what Lisp means.
- `and` and `or` become `ast.BoolOp`. These short-circuit, so if a later argument has
  statements, they can't simply be moved in front. In that case the form is rewritten as
  `if`s.
- `not` becomes `ast.UnaryOp`.
- Everything else becomes a call to the entry's Python name.

**`def`.** `(def x init)` becomes the statements of `init`, then `x = <init expr>`. With a
signature it becomes an annotated assignment, `x: int = ...`. The form's value is `None`.
`(def x)` becomes `x = None`.

**`defn`.** `(defn name (args*) body)` becomes an `ast.FunctionDef`:

- Its body is `body` translated in `tail` mode.
- The function's own name is added to `ctx.env` and the table before the body is
  translated, so recursion works.
- With a signature, the arguments and the return value get annotations.
- The form's value is `None`.

**`do`.** `(do e1 ... en)` translates `e1` to `e(n-1)` in `effect` mode, then `en` in the
current mode. `(do)` is `None`.

**`if`.**
- If neither branch needs statements, the result is a conditional expression,
  `then if test else other`, in any mode.
- Otherwise, in `tail` mode, it becomes an `if` statement with a `return` in each branch.
- In `effect` mode it becomes an `if` statement whose branches just run.
- In `value` mode each branch assigns a temporary, and the temporary is the result:

```python
# (put (if (< n 0) (do (log "neg") "neg") "ok"))
if n < 0:
    log('neg')
    _cdy_t1 = 'neg'
else:
    _cdy_t1 = 'ok'
print(_cdy_t1)
```

**`cond`.** Expand it to nested `if`s before translating, as smz does and as the future
macro will. A missing `else` leaves a final `None`.

**`let`.** `(let ((a e1) (b e2)) body)` becomes `a = e1` then `b = e2` (each with its own
statements first), followed by `body` in the current mode, with `a` and `b` added to
`ctx.env`.

- **Scoping (the catch).** Python variables belong to a whole function, not to a block. A
  `let` translated to plain assignments therefore leaks its names past the end of the
  `let`, and it can overwrite a name of the same spelling in the enclosing code. Worse, if
  a function assigns `x` anywhere, every `x` in that function refers to the local one, even
  a reference meant for a global `x`.
- **Rule.** A `let` binding keeps its own name unless that name is already bound: in
  `ctx.env` (an enclosing parameter, `let` or global) or in `ctx.fn_locals` (already used
  in this Python function). If it is, the binding is renamed to a fresh `_cdy_` name, and
  `ctx.env` maps the Candy name to it. Most code keeps readable names, and shadowing still
  works.
- **Known gap.** A global defined *later* in the file can still be captured by mistake. If
  that bites, switch to always renaming `let` bindings.
- **`let` is defined as an applied lambda, as in Scheme (decided).** Core has no `Let`
  node, and `lower` turns the applied lambda back into the assignments described here. See
  the note below.
- **Sequential bindings (decided).** Each `init` can see the names bound before it in the
  same `let`, like Scheme's `let*` and like smz. This maps directly onto Python assignments
  in order.

**Note: `let` as an applied lambda, as in Scheme.** In Scheme, `let` is sugar for calling
a lambda straight away:

```scheme
(let ((a e1) (b e2)) body)    ≡  ((lambda (a b) body) e1 e2)
(let* ((a e1) (b e2)) body)   ≡  ((lambda (a) ((lambda (b) body) e2)) e1)
```

Candy's `let` is sequential, so it is the nested `let*` form. There are two ways to use
this.

1. **Translate every `let` this way.** In Python, an expression-only body gives
   `(lambda a: (lambda b: body)(e2))(e1)`. A body that needs statements gives a nested
   `def _cdy_fnN(a): ...` followed by a call.
   - *For:* scoping is exact, because a Python function is a real scope. There is no
     renaming, no `fn_locals`, and no capturing a later global by mistake. When the inits
     and the body are expressions, a `let` in value position needs no statements at all.
   - *Against:* the output is hard to read. Every `let` costs a function call and a stack
     frame, and deep nesting adds up against Python's recursion limit. mypy gets little
     from an unannotated lambda, so typed `let`s would need `def`s with annotations. A
     `def` inside the `let` body would bind a local of the lambda, not of the enclosing
     function.
   - **Rejected for the iMVP** as the general translation: assignments read better and
     run faster.
2. **Define `let` this way in Core, and undo it in `lower`.** `analyse` desugars
   `Let(binds, body)` into nested `Call(Fn((a,), ...), (e1,))`, so Core no longer needs a
   `Let` node. `lower` then recognises an immediately applied `Fn` (a beta-redex, which
   Scheme compilers also turn back into plain bindings) and emits assignments, using the
   binding ids for scoping. This keeps Core smaller and makes `let`'s meaning exactly
   `fn`'s, which suits a later `let` macro. The cost is that `lower` must spot the
   pattern. Otherwise every `let` would come out as the slow form above. **Decided.**

Either way, a fallback is available. If a binding can't safely become an assignment (for
example, a future case the renaming rule gets wrong), `lower` can emit that one `let` as an
applied lambda.

**`fn`.**
- If the body needs no statements, it becomes `ast.Lambda`.
- Otherwise it becomes a nested `def _cdy_fnN(...)`, which is added to the statements, and
  the result is the name `_cdy_fnN`.
- Python lambdas can't carry type annotations, so once signatures apply to `fn`, a typed
  `fn` always becomes a `def`.

**`quote`.** `(quote form)` is a special form (**decided**). It needs no parser support,
because it is an ordinary list. The `'` shorthand is not in the iMVP: `'` is reserved, and
a later reader macro will expand `'x` into `(quote x)`, as in Clojure.

**Open: how quoted data looks at runtime.** The proposal is that `form` becomes a Python
constant expression:
- A number, string or boolean becomes itself.
- A symbol becomes a string: `(quote foo)` gives `'foo'`.
- A list becomes a tuple, recursively: `(quote (a 1 "b"))` gives `('a', 1, 'b')`.

This is roughly what smz's self-hosted compiler worked with. The drawback is that a quoted
symbol and a string look the same at runtime. Macros written in Candy will need to tell
them apart, so a small `Symbol` type in `table_defs` may be needed instead.

**`def` inside a function.** **Open.** In the proposal it binds a local, like a `let`
without a body. Assigning a global from inside a function would need a Python `global`
statement.

### Name mangling

Candy symbols such as `a-b`, `empty?` and `set!` are not valid Python identifiers. The
proposed mapping is deterministic and easy to read:

- `-` becomes `_`.
- `?` becomes `_p`.
- `!` becomes `_x`.
- Any other character that isn't allowed becomes `_uXXXX` (its hex code point).
- A name that clashes with a Python keyword, or with a name `table_defs` exports, gets a
  trailing `_` (for example `if_`).

`a-b` and `a_b` both become `a_b`. Rather than making the scheme more complicated, the
translator reports an error if two different Candy names in the same scope mangle to the
same Python name.

### Hooks for signatures and the table

- **Signatures.** Signature statements are collected into `ctx.sigs` as they are read. When
  `def`/`defn` is translated, it looks up its name there and attaches annotations. A Candy
  type maps to a Python type through the table, for example `Int` to `int`. Without a
  signature, nothing is annotated (or `Any`, depending on open item 5 under Types).
- **Table.** A `TableEntry` NamedTuple says whether a symbol is a binary operator, a
  comparison, a boolean operator, a unary operator, a call or a value. It also gives the
  entry's Python name, its type (once signatures exist) and which module it needs imported.
  A user `defn` adds an entry to the copy of the table carried in `ctx`, rather than
  changing a global table.

### Output and checking

1. The module body is: imports collected from the table entries used, then the translated
   top-level forms (in `effect` mode).
2. `ast.fix_missing_locations`, then `ast.unparse`, then write `output/<name>.py`.
3. `compile()` the result as a quick check that it is valid Python, then run mypy (strict)
   and execute it. The generated code imports helpers from `table_defs`, so `src/py_cdy`
   has to be on `PYTHONPATH` when it runs.

**Error positions (open).** The parser's AST nodes don't record where they came from, so a
translation error can't name a line yet. Adding source offsets to `SExpr` nodes would fix
that.

### Worked comparison with smz (option B)

Candy:

```clojure
(defn f2 (n m)
  (let ((x (+ n 1))
        (y (+ m 3)))
    (if (< x y) x y)))

(defn show (n)
  (put (let ((m (* n 2))) (+ m 1))))
```

Option A:

```python
def f2(n, m):
    x = n + 1
    y = m + 3
    return x if x < y else y

def show(n):
    m = n * 2
    return print(m + 1)
```

smz's approach handles `f2` fine, because the `let` and the `if` are both in tail
position. It breaks on `show`. smz renders the `let` as text containing assignments and a
`return`, and then pastes that text inside `print(...)`, which is a Python syntax error. In
option A, the `let`'s assignment goes to the statements and only `m + 1` stays inside the
call.

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
4. Pick translation strategy A or B (and, for A, whether to keep the lowered IR as its own
   layer or merge it with the Python step), and answer the open items in the option A
   section (`def` inside a function, the runtime representation of `quote`). Then build the translator core for `def`, `defn`, `do`,
   `if`, `cond`, `let` and `fn`, with tests.
5. Wire up reader → parser → translator → `output/`, run mypy on the generated Python, and
   run a first Candy program end to end.
