# The Candy spec

The language, rule by rule, each rule with examples that run: `tst/py_cdy/test_spec.py`
translates every example with the translator and checks what it does
(`doc/hl_rqmt/executable_spec.md`). A rule here is what Candy *is*; the HLDs in
`doc/hl_rqmt/` record how it got there.

## The files

One file per feature, a few hundred lines at most (split one that grows past that). The
numbers are a reading order, roughly bottom-up, but there can be order issues: a file's
examples use features a later file specifies (`00-syntax.md` uses `defn`, `if` and
`format`), and some point ahead (`10-programs.md` to `50-macros.md`). The tests don't care
(each example runs on its own), but a reader may.

| File | What it covers |
|---|---|
| `00-syntax.md` | forms, comments, literals, names: what the reader accepts and rejects |
| `10-programs.md` | the top level, `main`, the prelude, `import` |
| `20-types.md` | the types, `sig`, `def`, records (`deft`, `get`, `assoc`), `tup` |
| `30-match.md` | patterns and match: sum types (`deft` with variants), `match`, `tup` patterns |
| `40-expressions.md` | names and calls, the operators, `do`, `if`, `cond`, `let`, `fn`, `defn`, `Unit` |
| `50-macros.md` | `defmacro`, quoting, `gensym`, macro files (`import-macros`), `cond` as a macro |
| `60-library.md` | the built-ins, the prelude, and `format` |

## Writing a spec file

A spec file starts with a title and a status line:

````markdown
# Sum types and match

status: stable, since: sum-types
````

- **status** is `draft` (written with the feature's HLD, before its code: its examples may
  fail), `stable` (its examples must pass) or `deprecated` (they still pass until the
  feature goes; the file says what replaces it);
- **since** is the feature branch that brought it, by its tag (Candy has no versions).

In each section, the rule comes first, in prose, so it reads on its own; then its examples.
Every rule that is meant to stay has at least one example; edge cases go in a `candy
errors` table, or stay in `tst/`. A rule that holds only *for now* says so, and points at
its leak (`doc/leaks.md` and `doc/archive/leaks_*.md`).

**Output is numbers and text** (*for now*): an example prints numbers, and strings it
builds with `format`, never a raw list, `Bool`, `nil` or record, since those print the way
Python prints them (`doc/archive/leaks_imvp_py_translator.md`, "How each value is shown
is Python's `str()`"; `doc/hl_rqmt/executable_spec.md`, question 12).

## The blocks

A fenced block's info string says what it is. Each example is a whole program, in a file
of its own, with the prelude and the prelude macros as every program has them.

- **`candy run`**, followed by **`expect`**: the program runs, and its output must be the
  `expect` block, exactly:

  ```candy run
  (put (+ 1 2))
  (put (format "{(* 6 7)} is the answer"))
  ```
  ```expect
  3
  42 is the answer
  ```

- **`candy error`**, followed by **`expect-error`**: translating the program must fail,
  and the message must contain the `expect-error` text. The position before it
  (`line 2, column 1: `) is usually left out, and given only for a rule about where an
  error points (as in `50-macros.md`):

  ```candy error
  (put nope)
  ```
  ```expect-error
  unknown name nope
  ```

- **`candy errors`**: a table of error examples, one per line, `source => message`, for a
  rule's edge cases. Lines before a `---` line (one per table) are the table's setup,
  which goes before each row; the setup must translate on its own, so a row can only fail
  on its own source:

  ```candy errors
  (put ()) => empty form
  (put (+ 1)) => needs at least 2 arguments
  ```
  ```candy errors
  (sig n Int)
  (def n 1)
  ---
  (def n 2) => defined more than once: n
  (put (len n n)) => takes 1 argument(s), got 2
  ```

- **any other block** (`candy` alone, `markdown`): an illustration, not run. A block of
  four backticks can show these blocks without running them, as "Writing a spec file"
  does.

A failing example is reported as `file:line`, the line of its opening fence (or of its row
in a `candy errors` table).
