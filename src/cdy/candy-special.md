# candy special forms and other stuff
- these are informal descriptions 
- the special form grammar uses regular expression syntax: ? (optional), * (0 or more), and + (1 or more). 
- placeholders are denoted by a italics.
- the details and the reasons behind them are in `doc/hl_rqmt/iMVP_py_translator.md`, `doc/hl_rqmt/sum_types.md` and `doc/hl_rqmt/self_host_cleanup.md`
- the list of special forms and operators the translator knows is `src/cdy/special.cdy` (`doc/hl_rqmt/symbol_table.md`); this file describes them
## literals, comments
- in the spec: `spec/00-syntax.md` (forms, comments, literals, names, and the reader's errors)
## types
- in the spec: `spec/20-types.md`
## programs
- in the spec: `spec/10-programs.md` (top level, `main`, the prelude, `import`)
## special forms
### import
- in the spec: `spec/10-programs.md`
### import-macros
- top level only; *symbol*`.cdy` is found as for `import`, but it is a **macro file**: its `defmacro`s become macros of the importing file, and its other definitions are helpers, which run only while translating (the importing file's own `defmacro`s can call them; its program can't)
- a macro file can `import` ordinary files (their definitions are helpers too) and `import-macros` other macro files, whose macros expand in it; it doesn't pass those macros on
- each macro file is loaded once per importer; a cycle is an error
- only in the Candy translator
 > (import-macros *symbol*)
### sig, def, deft, get, assoc, tup
- in the spec: `spec/20-types.md` (records; sum types in `spec/30-match.md`)
- in `src/cdy/system.cdy`, which the translator reads, a `sig` has no definition: it declares a built-in that the runtime provides, with its type; anywhere else that is an error (goes to `spec/60-library.md`)
### match
- in the spec: `spec/30-match.md`
### defn, do, if, cond, let, fn
- in the spec: `spec/40-expressions.md`
### defmacro
- define a macro: Candy code that the translator runs on the *forms* of a call, before analysing it; the call is replaced by the form it returns (see `doc/hl_rqmt/macros.md`)
- top level only; every parameter is a `Form`, and no `sig` is needed
- scheme style: a bare *symbol* instead of the parameter list gets all the arguments as one `(List Form)`
- binding a macro's name (in `let`, `fn`, a pattern, `def` or `defn`) is an error
- calling a macro with the wrong number of arguments is an error at the call, and so is an error in the macro or in the code it returns
- a macro's body can use the built-ins, `Form` with its helpers (`form.cdy`), such as `sym-name`, `list-items`, `rest-of` and `gensym`, and the helpers of macro files (see `import-macros`); not the program's own definitions
- `(gensym "x")` returns a new symbol, `x__1`, which no program can write: the reader rejects `__` in a name
 > (defmacro *symbol* (*args**) *expr*)\
 > (defmacro *symbol* *args-symbol* *expr*)
### quo, quasi, unq, unq-sp
- quoting, for macros: only in macro code for now
- `quo` returns *form* unevaluated, as a `Form` (it replaces `quote`, reserved since the iMVP)
- `quasi` is like `quo`, but `unq` inside it puts in the value of *expr* (a `Form`), and `unq-sp` inside a list splices in the items of *expr* (a `(List Form)`)
- the `'` shorthand will be added later as a reader macro... ala clojure
 > (quo *form*)\
 > (quasi *form*)\
 > (unq *expr*)\
 > (unq-sp *expr*)
## weird stuff 
### format
- hacked in from smz: a string with Candy forms in `{...}` holes, one form per hole
- `{{` and `}}` are literal braces
 > (format "*text* {*form*} ...")
