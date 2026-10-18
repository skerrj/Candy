# Candy for VS Code

Syntax highlighting for Candy (`.cdy`): a declarative extension (no code, no build step).

## Install

Link this directory into VS Code's extensions, then run "Developer: Reload Window":

```
ln -sfn "$PWD/editors/vscode-candy" ~/.vscode/extensions/candy-local.candy-0.1.0
```

`code --list-extensions` then shows `candy-local.candy`. Because it is a link, edits to the
grammar show up on the next reload. To remove it, delete the link.

## What it highlights

`syntaxes/candy.tmLanguage.json` is a TextMate grammar. Its structure (comments, strings,
nested lists, the name after a defining form) follows the Scheme grammar in
`sjhuangx.vscode-scheme`; its literal and symbol rules follow VS Code's built-in Clojure
grammar, changed to match `src/py_cdy/parse_cdy.py` and `src/cdy/read.cdy`:

- `;` comments; strings and their escapes (`\n`, `\uXXXX`; others are marked invalid);
- literals that end at a delimiter: `100`, `1500l`, `1b`, `10.0`, `3.14f`, `\e`, `true`,
  `false`, `nil` (so `12x` is marked invalid);
- the special forms in head position (`tst/py_cdy/test_editor_grammar.py` checks the list
  against `SPECIAL_FORMS` in `src/cdy_rt/table.py`), `else`, and the operators;
- the name defined by `defn`, `def`, `sig` and `deft`;
- capitalised names as types and variants (`Shape`, `Circle`, `Fn`, `List`), and
  all-caps names (`HEADER`) as constants;
- the holes in `format` strings as Candy code (`{(+ 1 2)}`), with `{{`/`}}` as escapes
  and the hole's escaped strings (`\"s\"`) as strings;
- `'` (reserved) and a stray `)` as invalid.

## Not yet

- Parameter lists (`(defn f (x y) ...)`, `fn`) and `let` bindings aren't told apart from
  calls: their first name is coloured as a function.
- A `format` inside a hole isn't recognised.
- No snippets, no Markdown code-block support (the docs use ```` ```clojure ```` fences).
