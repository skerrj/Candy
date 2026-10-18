# Leaks

Places where the iMVP lets Python show through Candy, or takes a shortcut that Candy's
design will need to fix later. Each one is acceptable for bootstrapping. Each entry says
what leaks, and what a proper fix might be. Add to this list whenever a hack goes in.

**Type checking in the iMVP.** `sig` statements are part of the iMVP. They become Python
annotations, and mypy (strict) checks the generated code. Candy has no type checker of its
own yet. So the type-related leaks below are the ones mypy can't see, because Python's types
are looser than Candy's (`Char` and `String` are both `str`, for example).

See `doc/hl_rqmt/iMVP_py_translator.md` for the iMVP itself, and
`doc/hl_rqmt/multi_target.md` for why these matter once there is a second target.

## Hacked-in forms

### `format` (from smz)

`(format "x: {x} sum: {(+ x y)}")` becomes the f-string `f'x: {x} sum: {x + y}'`.

- **How:** the translator finds each `{...}` hole in the string literal, parses the text
  inside it as one Candy form, translates that form, and builds a Python f-string (in
  option A, `ast.JoinedStr`). It accepts exactly one string literal.
- **Leaks:**
  - The string is scanned for holes with a regex after parsing, so a hole is not real
    syntax. A `}` inside a string inside a hole ends the hole early, and errors in a hole
    can't point to a position.
  - How each value is shown is Python's `str()`. A `Bool` prints as `True`, a `deft` record
    prints as `Vector2(x=1, y=2)`, and `None` prints as `None`.
  - Literal braces are written `{{` and `}}`, as in Python. (smz used `{LCB}` and `{RCB}`
    symbols.)
- **Later:** parse format strings properly (holes as part of the grammar, or a reader
  macro), and give Candy its own `str`/show for each type.

### `tup` destructuring (from smz)

`(tup a b)` becomes the Python tuple `(a, b)`. Building a tuple is not a hack; the
stopgap is destructuring. A `let` binding can destructure a tuple:
`(let (((x y) (f a b))) ...)`.

- **How:** `tup` is a special form that builds `ast.Tuple`. In `analyse`, a destructuring
  binding `((x y) e)` is rewritten into a fresh binding for `e` followed by `(x (at t 0))`
  and `(y (at t 1))`, so Core needs no pattern node. Its type is `(Tup A B)` in a `sig`.
- **Leaks:**
  - Tuples are Python tuples, and so are `List`s and `deft` records (`NamedTuple`s). A
    `Tup`, a `List` and a record with the same items compare equal. mypy also accepts a
    `(Tup Int Int)` (`tuple[int, int]`) where a `(List Int)` (`tuple[int, ...]`) is
    expected.
  - Destructuring works only in `let`, not in `defn` or `fn` parameters. The translator
    doesn't check its arity. mypy catches a wrong arity when a `sig` gives the tuple's type;
    otherwise it fails at runtime with an `IndexError`.
- **Later:** real tuple types in Candy's type checker, and patterns (probably with
  `match`) instead of the `let` special case.

## Types

- **`Any`.** `sig` is required, and `Any` is the escape hatch for a type that can't be
  written yet: `(sig f (Fn (Any Any) Any))`. It becomes Python's `Any`, so mypy checks
  nothing that passes through it. Every use is a leak. Grep for `Any` in `.cdy` files to
  find them.
- **Nested functions get `Any`.** `sig` covers only top-level definitions. A `fn` that has
  to become a nested Python `def` gets `Any` annotations, so that mypy in strict mode
  accepts it, until Candy infers types.
- **`(Maybe A)` is `A | None`.** Properly it is a sum type that has to be unwrapped (with
  `match`). In the iMVP, mypy's narrowing (`if x is not None`) is all there is, and `nil`
  tests use Python truthiness.

## Python semantics showing through

- **Missing values are `None`.** An `if` with no else, a `cond` with no match, and the
  value of a `def` form are all `None`. Candy will need a real unit/`Nil` type.
- **Numbers.** `Int`, `Long` and `Byte` are all unbounded Python `int`s, and `Float` is
  64-bit like `Double`. There are no range checks (`300b` is accepted). See
  `doc/hl_rqmt/multi_target.md`.
- **`/` on integers.** `(/ 7 2)` is `3.5`, because `/` is Python's true division. A
  strongly typed Candy will want `Int / Int` to stay an `Int`, or a separate operator.
- **`if` tests use Python truthiness.** `0`, `""` and an empty list are false. Candy is
  strongly typed, so a test should have to be a `Bool`. mypy accepts any type in a test,
  so nothing enforces that until Candy has its own type checker.
- **`and` and `or` return an operand, not a `Bool`.** `(or x 5)` can be `5`.
- **`=` is Python `==`.** Equality is structural, and `1 == 1.0` is true, across types.
- **`Char` is a one-character `str`.** Nothing stops a `Char` and a `String` being mixed.
- **Records are `NamedTuple`s.** Two different `deft` types with the same field values
  compare equal, and a record also behaves as a tuple (indexing, iterating, unpacking).
- **`get` works on any Python object with that attribute**, not just `deft` records. mypy
  catches a missing field when a `sig` gives the object's type; Candy itself doesn't
  check.
- **`empty-list` is a mutable Python list**, while everything else is immutable.
- **Regexes are Python's.** `re-search`, `re-findall` and `re-compile` use Python's
  syntax and return Python match objects.
- **No unary minus.** `-` is a `binop` in `table.py`, and binops need two or more
  arguments, so `(- x)` is an error: write `(- 0 x)`. A negative literal (`-5`) is fine.
- **`in` works on both strings and lists**, as Python's `in` does.
- **No `Collection` interface yet.** Candy's collection operations are meant to work on an
  abstract `Collection`. In the iMVP they work on whatever Python accepts: the
  `table_defs` helpers take any `Sequence`, and `len` is Python's `len`, so strings,
  tuples and lists all pass. Candy has no way to declare the interface itself yet.
- **`print` for `put` and `display`.** Output formatting is Python's, as for `format`.

## Translator shortcuts

- **Name mangling can collide.** `a-b` and `a_b` both become `a_b`. The translator reports
  an error when both appear in one scope, but doesn't rename.
- **Operators can't be values yet.** `(put +)` or passing `<` to a function is an error;
  wrap it: `(fn (a b) (< a b))`.
- **Record fields can't start with `_`** (or `-`, which mangles to `_`), because
  `NamedTuple` forbids it.
- **Using a `Unit` value.** `(put (put 1))` translates, but the Python uses the result of a
  `None`-returning call, which mypy rejects. Candy's own type checker should reject it
  first.
- **Every runtime module is imported**, whether the program uses it or not.
- **The destructuring temporary is named `_tup`**, a plain local; it is renamed like any
  other local if the name is taken.
- **No source positions** (skipped for the iMVP). Translation errors can't name a line
  yet; only parse errors have a line and column.
