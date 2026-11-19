# Brainstorm

Random thoughts about Candy's design, a scratchpad for quick notes: not decided, not
planned. Add one whenever it comes up. Once one is written up (a second sentence, or
something links to it) it moves into the backlog as an `idea` (`backlog/`), or as a
`feature` once the owner agrees to it, and leaves this file (`doc/hl_rqmt/tracking.md`,
question 3).

- **vscode syntax extension**: `(defn line (level text) (+ (get-indent level) text "\n"))`: get-indent is the same color as args... should be similar to `+`
- **rewrite parsec-v4 in Candy**: ref *publish parsec*
- **type checker**: *lean4*?
  - fork and start rewriting with lean4? 
- **rust host**: *pulled from dump*
- **dump** (i.e. needs expansion): IO, interpreter, reader improvements, repl, jit
- **Joy like recursive macros**: optimized target implementations
- **Curry**: could this be a macro?
- **cndy specifice macros**: any boiler plate patterns worth a macro
- **metadata on names** (Clojure's `^:tag`, a map on a symbol): tag `system.cdy`'s
  translator-only built-ins instead of a `translator.cdy`? Kept the module: what a file
  sees is its imports' to say, and `(import translator)` shows the use. Metadata could
  carry what cuts across that: docs, `deprecated`, `pure`, which targets have a built-in
  (`doc/hl_rqmt/multi_target.md`); `private` too ([[programs.private]])?
- **does the prelude need to exist?** (for `stdlib`'s HLD): once `list`, `string` and
  `map` are modules, the prelude may be little more than `Maybe` and `Result`. Keep it
  apart from `system` either way: `system` is declarations only (a declaration module,
  each target providing it), the prelude ordinary Candy, the same on every target.
- **is `system` only the language?** (`stdlib`'s HLD, Question 8, tabled 2026-11-18):
  Candy's code is `Form`s, not its lists, so the Lisp reason to put lists in the core
  doesn't hold; the `List` type stays (rest parameters, `++`), but its operations could
  be an implicitly imported `list` declaration module, `system` the language alone.
  Decide at `io` ([[B95]]) or a second target.
