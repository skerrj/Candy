# Syntax

status: stable, since: imvp-py-translator

How text becomes forms: lists, names and literals, and comments. The reader
(`src/cdy/read.cdy`) is the authority *for now* (`doc/hl_rqmt/executable_spec.md`,
question 6: a grammar file comes when a second reader needs one); this file says what it
accepts, and every error it gives.

```candy
form    = list | literal | name
list    = "(" form* ")"
literal = int | long | byte | double | float | bool | char | string
```

<a id="syntax.forms"></a>
## Forms

A program is a sequence of forms. A list is forms between parentheses, separated by
whitespace; a name or a literal runs up to the next delimiter. Line breaks are whitespace,
so a form can span lines. `()` reads, but isn't code: it is an empty form.

```candy run
(put
  (+ 1
     2))
(put (* 2 (+ 3 4)))
```
```expect
3
14
```

```candy errors
(put (+ 1 2) => ( is never closed
(put 1)) => unexpected )
) => unexpected )
(put ()) => empty form
```

<a id="syntax.comments"></a>
## Comments

`;` starts a comment, to the end of the line. By convention, `;` is a comment beside code,
`;;` one on a line of its own, and `;;;` a section's header; the reader treats them all
alike.

```candy run
;;; A section.
;; A comment on its own line.
(put 1) ; and one beside code
(put 2);no space needed
```
```expect
1
2
```

<a id="syntax.literals"></a>
## Literals

| Literal | Type | Written |
|---|---|---|
| `100`, `-7` | `Int` | digits, after an optional `-` |
| `1500l` | `Long` | an `Int`, then `l` |
| `1b` | `Byte` | an `Int`, then `b` |
| `10.0`, `-0.5` | `Double` | digits, `.`, digits |
| `3.14f` | `Float` | a `Double`, then `f` |
| `true`, `false` | `Bool` | |
| `\e` | `Char` | `\` and one character that isn't whitespace |
| `"text\n"` | `String` | between `"`s, with escapes |

A literal must end at a delimiter: whitespace, a parenthesis, `;`, or the end of the text.
`nil` (the `Unit` value) is a name, not a literal.

```candy run
(put 100 -7 1500l 1b)
(put 10.0 -0.5 3.14f)
(put (if true 1 0) (if false 1 0))
```
```expect
100 -7 1500 1
10.0 -0.5 3.14
1 0
```

<a id="syntax.numbers"></a>
A number has digits on both sides of its `.`, and its suffix comes last; anything else
that starts with a digit is an error. A word that starts with `.` or `-` and isn't a
number is a name (`.5`, `-x`):

```candy errors
(put 12x) => unexpected 1
(put 1.5l) => unexpected 1
(put 1.) => unexpected 1
(put .5) => unknown name .5
```

<a id="syntax.chars"></a>
A char is `\` and exactly one character, which may be a delimiter's (`\(` is the char
`(`), then a delimiter:

```candy run
(put \e)
(put \( \; \))
```
```expect
e
( ; )
```

```candy errors
(put \ab) => a char is \ and one character, then a delimiter
(put \ x) => a char is \ and one character, then a delimiter
(put \) => ( is never closed
```

<a id="syntax.strings"></a>
A string's escapes are `\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, and `\u` with four
hex digits. A string can span lines.

```candy run
(put "say \"hi\"")
(put "a\tb")
(put "café \\ \/")
(put "two
lines")
```
```expect
say "hi"
a	b
café \ /
two
lines
```

```candy errors
(put "abc) => string is never closed
(put "\q") => bad escape sequence
(put "\u00g1") => bad escape sequence
```

<a id="syntax.names"></a>
## Names

A name is any word that isn't a literal and doesn't start with a digit, `'`, `#`, `"` or
`\`. It runs up to a delimiter, or a `'`, `"` or `\`. So names can hold punctuation that
other languages reserve: `set-x!`, `empty?`, `->`, `a.b`, `a#b`.

```candy run
(sig empty? (Fn (Int) Int))
(defn empty? (n) (if (= n 0) 1 0))
(sig ->str (Fn (Int) String))
(defn ->str (n) (format "<{n}>"))
(put (empty? 0) (->str 5))
```
```expect
1 <5>
```

<a id="syntax.reserved"></a>
`'` is reserved for a quote shorthand (a reader macro, later), and a name can't start
with `#`. A name can't contain `__`: only `gensym` makes such names, for macros, so they
can't clash with a program's.

```candy errors
(put 'a) => unexpected '
(put a'b) => unexpected '
(put #a) => unexpected #
(put b__c) => a name can't contain __ (only gensym makes such names)
```
