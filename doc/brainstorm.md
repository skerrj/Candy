# Brainstorm

Random thoughts about Candy's design, a scratchpad for quick notes: not decided, not
planned. Add one whenever it comes up. Once one is written up (a second sentence, or
something links to it) it moves into the backlog as an `idea` (`backlog/`), or as a
`feature` once the owner agrees to it, and leaves this file (`doc/hl_rqmt/tracking.md`,
question 3).

- **variadic args, interfaces, and generics**: *break this up*
- **vscode syntax extension**: `(defn line (level text) (+ (get-indent level) text "\n"))`: get-indent is the same color as args... should be similar to `+`
- **rewrite parsec-v4 in Candy**: ref *publish parsec*
- **type checker**: *lean4*?
  - fork and start rewriting with lean4? 
- **rust host**: *pulled from dump*
- **up, down, down-splice, meta-template**: (`up`, `dwn`, `dwn*`, `mt`); replacements for quote, unquote, quasiquote, and quasi-splice (low pri)
- **dump** (i.e. needs expansion): IO, interpreter, reader improvements, repl, jit
- **Map, reduce, fold, etc**: optimized target implementations
- **Joy like recursive macros**: optimized target implementations
- **Curry**: could this be a macro?
- **Generics**: not sure where we are at... so just a note/question
- **cndy specifice macros**: any boiler plate patterns worth a macro
