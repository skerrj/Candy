# Self-hosting, first stage ("primo"): the translator in Candy, the parser borrowed

**Status: draft staging plan.** Nothing here is decided. Branch `pre-self-host`, after tag
`imvp-py-translator`. Related: `doc/hl_rqmt/sum_types.md` (a prerequisite) and
`doc/hl_rqmt/iMVP_py_translator.md` (the Python translator this stage builds on).

## The idea

Write the translator (`analyse` → `lower` → emit) in Candy first, and keep the Python
parser (`parse_cdy.py`, on parsec.py v4) for now. Port the parser to Candy last. This is a
"borrowed front end" bootstrap.

```
Candy text ─▶ parse_cdy (Python, parsec v4) ─▶ convert ─▶ translator written in Candy ─▶ Python text
            └──────── driver in py_cdy (glue) ────────┘   └─ compiled by the iMVP translator ─┘
```

## Why the parser comes last

- **It is what Candy is worst at today.** Parser combinators are closures and higher-order
  functions. Candy types nested `fn`s as `Any`, and `loop_tail_calls` skips functions that
  make closures.
- **It is what most needs to stay correct**, and the parsec version is already typed and
  tested.
- **The translator is mostly taking data apart and building new data.** Once sum types and
  `match` exist, that is what Candy will do well.

## Stages

0. ~~**Sum types and `match`**~~ (`doc/hl_rqmt/sum_types.md`), in the Python translator.
   **Done.** Without them, forms, Core nodes and IR nodes would all be `Any` in Candy.
1. **The translator in Candy, with the Python parser.**
   - Candy source under `src/cdy/` (for example `core.cdy`, `lower.cdy`, `emit.cdy`,
     `translate.cdy`), compiled by the iMVP translator into Python modules (T1) under
     `output/t1/` (git-ignored; rebuilt, not checked in).
   - The entry point is a Candy function such as `(sig translate (Fn ((List Form)) String))`.
   - The driver is a new mode of `src/py_cdy/main.py` (decided, for now). It reads the file,
     parses it with `parse_cdy`, converts the forms (see "The boundary"), calls T1's
     `translate`, and writes the result.
   - **Emit Python text, not Python `ast`,** as smz's `render.py` did. Building `ast`
     objects from Candy would need a table entry for every `ast` constructor. This applies
     only to the Candy translator; the Python translator keeps strategy A.
2. **The fixpoint.** T1 translates the Candy translator's own source, giving T2. Then T1 and
   T2 must produce the same output for the translator's source and for every
   `tst/cdy/*.cdy` program. This becomes a test, as it was for smz. Two comparisons are
   possible, and both are done (open question 4, decided):
   - **What they produce: byte-identical**. T1 and T2 run the same Candy code,
     the same `emit`, compiled two ways, so on the same input they must print exactly the
     same text. Formatting can't differ here, and any difference is a real bug.
   - **The files T1 and T2 themselves: equal up to formatting** (the owner's vote). T1 was
     written by the Python translator (`ast.unparse`) and T2 by the Candy translator's own
     text emitter, so their layout differs even when they mean the same thing. Compare
     them by parsing both with Python's `ast` and comparing `ast.dump`, which ignores
     layout, comments and parentheses.
3. **The parser in Candy.** It replaces `parse_cdy` and the conversion step. It needs a
   closure story (typed nested `fn`s, or a hand-written recursive-descent reader in the
   style of `tst/cdy/read_sexpr.cdy`, which needs no closures), more of the runtime, and
   perhaps better recursion (mutual recursion and non-tail recursion still use the Python
   stack). After this, Candy is self-hosting on Python.

## Stage 1 in slices (as planned)

The Candy translator's source may use everything the Python translator supports (`let`,
`cond`, `match`, `deft`, `format`, `tup`, ...). What the Candy translator itself supports
grows slice by slice, until it can translate its own source (stage 2).

- **1a: the pipeline and a small subset** (**done**). `Form` (`src/cdy/form.cdy`), the driver mode,
  the conversion, and a translator with all three layers that handles literals, symbols
  (locals, globals, built-ins of every table kind), calls, `if`, `cond`, `do`, `sig`,
  `def`, `defn` and `put`. Tests: small programs in `tst/cdy/t1/`, each translated by T1,
  run, compared with its `.out` and checked with `mypy --strict`.
  - As built: `src/cdy/form.cdy`, `core.cdy`, `lower.cdy`, `emit.cdy` (about 600 lines of
    Candy); `src/py_cdy/self_host.py` builds T1 into `output/t1/cdy_translator.py`,
    converts forms and calls `translate`; `main.py FILE.cdy --translator t1`.
    `tst/py_cdy/test_self_host.py` also runs `mypy --strict` on T1 itself, which
    type-checks the Candy translator's own code. Both translators print the same output
    for `tst/cdy/t1/basics.cdy`.
- **1b:** `let` (with destructuring), `fn`, `tup`, `format`, `get`/`assoc`.
- **1c:** `deft` records and sums, `match`.
- **1d:** self tail calls as loops, local renaming as in the Python translator, and the
  remaining checks. Then the T1 source is in the supported subset: stage 2.

**Decisions for the Candy translator** (proposed with slice 1a and built that way;
simplest first):

- **No `import` yet, so the driver concatenates files.** The translator is several files
  under `src/cdy/`, listed in order in `main.py`. They are joined into one program, which
  works because top-level names may be used before their definition. This is a stopgap
  (a leak) until `import` exists.
- **IR expressions reuse Core's `Expr` sum.** The Python translator has separate IR
  expressions (`CallE`, `CondE`, ...). Here `lower` produces statements (`Stmt`) whose
  expressions are Core `Expr`s, plus a `Temp` variant; an `If` left inside an expression
  is a conditional expression. One sum instead of two keeps the Candy code smaller.
- **Emit text with full parentheses** around every operator, instead of working out
  precedence. The output is valid and typed, just not pretty.
- **Python-specific helpers live in the runtime** (`cdy_rt`), as smz's did: `py-mangle`
  (Candy names to Python names, with the reserved-name list) and `py-repr` (Python
  literals). They are part of the Python backend, so the target-independent layers don't
  use them.
- **Errors:** a new `fail` built-in raises `CandyFail` (Candy has no exceptions); the
  driver reports it like a `CandyError`.
- **Maps:** new built-ins `empty-map`, `map-get`, `map-has`, `map-set` (`map-set` returns
  a new map). The table itself is an opaque value typed `Any` (a leak), read with the
  `table-*` built-ins plus a new `table-get-kind`.
- **No `Maybe` in the translator's own types.** mypy narrows `x is None`, but Candy's
  `(= x nil)` is `x == None`, which mypy doesn't narrow, so optional values are sums
  (`(deft Annot (NoAnnot) (HasAnnot ((t CType))))`).

## The boundary

There is one boundary, right after the parser, and the driver owns it.

- **The rule still holds.** Generated code depends only on `cdy_rt`. The compiled
  translator never imports `parse_cdy` or `parsec`; the driver imports both and hands the
  translator plain data.
- **Converting forms.** `parse_cdy` yields its own `NamedTuple`s (`Symbol`, `SList`, `Str`,
  `Int`, `Long`, ...). The Candy translator needs a type for them. Of the two choices, **A is
  decided** (open question 1):
  - **A. `deft` variants.** Candy declares `(deft Form (Sym ...) (Lst ...) (Int ...) ...)`,
    and the driver converts each `parse_cdy` node into the matching generated class. This
    keeps the translator statically typed. **(Decided.)**
  - **B. `Any` plus runtime predicates** (`sym?`, `list?`, ...), as in smz. This is cheaper
    and needs no sum types, but it gives up static typing exactly where the translator
    needs it most.
- **Don't port one stage at a time.** For example, a Candy `analyse` feeding Python's
  `lower` would need Candy's Core node classes and `core_cdy`'s to be the same. They aren't,
  so every boundary between a Candy stage and a Python stage would need its own conversion.
  One boundary, after the parser, is far simpler.

## What the Candy translator needs from Candy

These come up in stage 1 and go into the leaks list, or get fixed, as they appear:

- sum types and `match` (stage 0);
- `Map` operations for the symbol table and the scope (the runtime has a table today; Candy
  would need it typed);
- counter threading, as the Python code does (`n` for ids and temporaries), since mutation
  is skipped;
- string building for the emitted text: `join`, `format`, escaping string literals;
- mutual recursion between the translator's functions, which uses the Python stack (fine at
  the depth of a syntax tree).

## Open questions

1. ~~**Forms at the boundary:** A (`deft` variants plus conversion) or B (`Any` plus
   predicates)?~~ **A (decided).** This makes sum types (stage 0) a hard prerequisite, so
   the sum-types draft's open question 1 ("sum types now, or `Any` plus predicates") is
   effectively answered too: sum types now.
2. ~~**Where the Candy translator lives**~~ (**decided**, the easiest option): the Candy
   source goes in `src/cdy/`, next to `candy-special.md`. T1 and T2 are generated into
   `output/` (for example `output/t1/` and `output/t2/`), which is git-ignored, and rebuilt
   whenever they are needed. `bin/` is no longer git-ignored (decided): once the
   translator reaches the fixpoint, a checked-in copy goes in `bin/py/`, as smz had, so
   Candy can be rebuilt without the Python translator. Other targets get their own
   `bin/<target>/` later (`doc/hl_rqmt/multi_target.md`).
3. ~~**Driver**~~ (**decided, for now**): a mode of `src/py_cdy/main.py`, not a separate
   script. The flag name is still to choose (for example `--translator t1`, where the
   default is the Python translator).
4. ~~**Fixpoint scope**~~ (**decided**): both checks in stage
   2. The files T1 and T2 are compared up to formatting (`ast.dump`), as the owner voted,
   because they come from two different emitters. Their output is compared byte for byte,
   because it comes from the same emitter, so this costs nothing and catches more. (In the
   usual three-stage bootstrap, T3 = T2(source) would also be byte-identical to T2.)
