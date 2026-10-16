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

### `tup` (from smz)

`(tup a b)` becomes the Python tuple `(a, b)`. A `let` binding can destructure it:
`(let (((x y) (f a b))) ...)`.

- **How:** `tup` is a special form that builds `ast.Tuple`. In `analyse`, a destructuring
  binding `((x y) e)` is rewritten into a fresh binding for `e` followed by `(x (at t 0))`
  and `(y (at t 1))`, so Core needs no pattern node. Its type is `(Tup A B)` in a `sig`.
- **Leaks:**
  - Tuples are Python tuples. A tuple and a `deft` record with the same items compare
    equal, because records are `NamedTuple`s too.
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

- **Missing values are `None`.** `(def x)`, an `if` with no else, and the value of `def`
  are all `None`. Candy will need a real unit/`Nil` type.
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
- **`in` works on both strings and lists**, as Python's `in` does.
- **`print` for `put` and `display`.** Output formatting is Python's, as for `format`.

## Translator shortcuts

- **Name mangling can collide.** `a-b` and `a_b` both become `a_b`. The translator reports
  an error when both appear in one scope, but doesn't rename.
- **A `let` can capture a global defined later in the file**, in the gap described in the
  iMVP doc's `let` scoping rule.
- **No source positions.** Errors can't name a line yet.
