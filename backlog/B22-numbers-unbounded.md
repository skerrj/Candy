# B22: Overflow isn't checked, and a `Float` is 64 bits on Python

kind: leak
state: open
priority: low
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`, `doc/hl_rqmt/multi_target.md`
refs: [[syntax.numbers]], [[expr.arithmetic]]

The number types have sizes ([[syntax.numbers]]: `Byte` 8 bits unsigned, `Int` 32,
`Long` 64, `Float` 32, `Double` 64), and a literal out of its range is an error, but on
Python arithmetic that overflows isn't checked (`(* 2147483647 2)` is `4294967294`, an
`Int`), and a `Float` is a 64-bit `float` like a `Double`. Fix (`porting-surface`): a
rule, trap (Swift) or wrap (Java), with each target's way to keep it; on Python, check
each operation (slow) or keep this leak, and round a `Float` with `struct`. Only literals
are checked, so a number made when the program runs can be out of range (`(to-int
"99999999999")` is an `Int`); and a `Float` literal isn't rounded to 32 bits.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): matters once there is a second target.
- 2026-11-01, the owner: in the semantics HLD (Question 5) the sizes are decided, *lasting*:
  `Byte` 8 bits unsigned, `Int` 32, `Long` 64, `Float` 32, `Double` 64; `semantics`
  checks literal ranges (`300b` an error). Overflow is left undecided, with a note to
  `porting-surface`: the potential fix is to choose trap (Swift) or wrap (Java) as
  Candy's rule and, on Python, check each operation or keep this leak; `Float` stays 64
  bits on Python likewise. At `semantics`' step 6 this item's text is reworded to what
  remains (overflow unchecked, `Float` 64-bit on Python).
- 2026-11-06, Claude: reworded in `semantics-2` step 1, which checks literal ranges: what
  remains is overflow and `Float`'s size. The title and text were:

  ```text
  # B22: `Int`, `Long` and `Byte` are unbounded; `Float` is 64-bit

  All three integer types are Python `int`s, and `Float` is a 64-bit `float` like `Double`,
  with no range checks (`300b` is accepted). A second target will have sizes. From `doc/archive/leaks_imvp_py_translator.md`
  ("Numbers").
  ```
