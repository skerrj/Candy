# parsec.py v4 — design notes

Context for continuing the rewrite of [sighingnow/parsec.py](https://github.com/sighingnow/parsec.py)
(forked from upstream master at `e451411`). Work lives on branch `functional-rewrite`,
one commit: *"Rewrite as typed, purely functional Parsec-style combinators (v4)"*.

## Requirements (from the owner)

1. **No Python decorators anywhere** — library internals *and* the user-facing API,
   examples and docs. This includes `@dataclass`, `@property`, `@staticmethod`,
   `@overload`, `@wraps`, and the old `@generate`.
2. **As pure a functional style as possible.** Tail recursion is fine. Correctness and
   readability first; optimization explicitly deferred.
3. **Typed output based on the grammar** — interpreted as *statically typed
   combinators* (option 1): `Parser[T]` is generic, rules produce user-defined typed
   AST nodes, and mypy/pyright verify it. (Rejected option 2: deriving types from a
   declarative EBNF grammar — that's a parser generator, much bigger scope.)
4. **Compatibility with 3.x is not required.** Lean into the library's Haskell
   (Parsec) heritage.

## Settled decisions

| Topic | Decision | Why |
|---|---|---|
| Naming | Haskell **camelCase** (`sepBy`, `many1`, `chainl1`, `notFollowedBy`, `optionMaybe`, `manyTill`, `lookAhead`) | One-to-one with Parsec docs. Keyword clashes get a trailing underscore: `try_`, `open_`. |
| Stack safety | **Trampoline** (`_trampoline.py`: `Done` / `Suspend` / `FlatMap` + one `run` loop with an immutable cons-list continuation stack) | Python has no TCO; recursive `many` would hit the ~1000-frame limit. The loop is the only imperative code in the library. |
| Choice semantics | **Parsec consumed/empty model.** `p \| q` tries `q` only if `p` failed *without consuming*; `try_(p)` enables backtracking | Faithful to Parsec; precise errors; backtracking cost explicit. |
| Errors | `ParseError(offset, unexpected, expected: frozenset, messages)`, merged Parsec-style (known beats unknown, later offset wins, same offset unions). Line/column computed lazily at formatting | Messages like `line 1, column 4: unexpected 'x'; expected ',', digit or end of input`. |
| Records | `typing.NamedTuple` for all immutable data; `Parser` is a plain class with `__slots__` | `@dataclass` is a decorator. `Parser` isn't a NamedTuple so `p + q` can't silently concatenate tuples. |
| Recursive rules | `lazy(lambda: ...)` (memoized via `functools.cache(build)`, called as a function) and `fix(lambda self: ...)` | Replaces `@generate`. |
| Generators | `generate` removed entirely | Generators are stateful; no decorator form allowed anyway. |
| Sequencing | `liftA2` … `liftA5`, plus homogeneous `sequence([...])` | No `@overload`, so a variadic typed `seq` isn't expressible. |
| Operators | `\|` = `<\|>`, `>>` = `*>`, `<<` = `<*`; methods `.map`, `.bind`, `.label` | No operator for `>>=`: Python chains `a >= f >= g` as comparisons. |
| Repetition results | Immutable `tuple[T, ...]`; `manyChars`/`many1Chars` join to `str` | Purity. |
| Empty-loop guard | `many`/`many1` on a parser that succeeds without consuming raises `EmptyLoopError` | Parsec calls `error` in the same case. |
| `string` / `regex` | **Atomic** — fail without consuming on partial match (Megaparsec behaviour, deviates from Parsec) | `string("let") \| string("lex")` works without `try_`. *Owner hasn't confirmed — see open items.* |
| Nullary parsers | Values, not functions: `digit`, `letter`, `spaces`, `eof` | Haskell style. |
| Running | `runParser(p, text) -> Success(value, offset) \| Failure(error, text)` (pure); `parse(p, text)` requires full input and raises `ParseFailure` | Pure core, convenient wrapper. |
| Python | 3.10+ (uses `match` in examples) | |

## Code layout

```
src/parsec/
  _trampoline.py   Done/Suspend/FlatMap, flat_map, run (the only loop)
  core.py          State, SourcePos, ParseError, Ok/Err replies, Parser[T];
                   pure, fail, empty, bind, fmap, ap, liftA2/3, then, skip, alt;
                   try_, label, lookAhead, notFollowedBy, lazy, fix;
                   satisfy, eof; runParser, parse, Success/Failure/ParseFailure
  combinators.py   liftA4/5, sequence, voidP, choice, option, optionMaybe, optional,
                   between, many, many1, skipMany(1), count, manyTill, sepBy(1),
                   endBy(1), sepEndBy(1), chainl(1), chainr(1), EmptyLoopError
  char.py          char, oneOf, noneOf, anyChar, digit, hexDigit, letter, alphaNum,
                   upper, lower, space, spaces, tab, newline, crlf, endOfLine, eof,
                   string, regex, manyChars, many1Chars
  py.typed
examples/          calculator.py, json_parser.py, sexpr.py (typed ASTs + pure evaluators)
tests/             test_core.py, test_combinators.py, test_examples.py (unittest, 56 tests)
                   typecheck_api.py (assert_type checks; run by mypy, not executed)
```

Run: `PYTHONPATH=src python -m unittest discover -s tests` and `mypy` (strict config in
`pyproject.toml`). Both pass; pyright also clean. pytest wasn't installable in the build
environment, hence unittest.

## Open items

1. **`many` performance** — appends with `acc + (x,)`, so O(n²): ~2.4 s for 20,000
   characters. Deferred per requirement 2. Likely fix: accumulate a cons list and
   reverse once at the end.
2. **Atomic `string`** — keep the Megaparsec behaviour, or match Parsec exactly
   (consume on partial match, require `try_`)?
3. **Earlier optimization ideas (all deferred):** flatten sequencing chains, build error
   expectations lazily, avoid `Suspend` on primitive parsers.
4. **Not yet done:** pushing the branch to the owner's GitHub fork / opening a PR;
   fuller Sphinx docs (only `docs/index.rst` with automodule stubs exists).
