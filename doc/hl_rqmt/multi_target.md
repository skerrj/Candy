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
