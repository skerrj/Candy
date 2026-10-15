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
2. **The translator keeps a target-independent stage.** The pipeline is:
   - parser
   - typed Candy AST
   - (later) a typed intermediate representation
   - a lowering step for each target

   The iMVP's Python lowering (option A, `lower()` in the iMVP doc) is the first such
   step. A new target adds its own lowering and reuses everything before it.
3. **Each target maps the Candy types for itself.** For the iMVP's Python mapping (`Int`,
   `Long` and `Byte` to `int`, and so on), see the iMVP doc.

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
- How the typed intermediate representation is defined.
- How each target provides its runtime: the equivalent of `table.py` / `table_defs.py`.
