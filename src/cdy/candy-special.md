# candy special forms and other stuff
- these are informal descriptions 
- the special form grammar uses regular expression syntax: ? (optional), * (0 or more), and + (1 or more). 
- placeholders are denoted by a italics.
- the details and the reasons behind them are in `doc/hl_rqmt/iMVP_py_translator.md`, `doc/hl_rqmt/sum_types.md` and `doc/hl_rqmt/self_host_cleanup.md`
- the list of special forms and operators the translator knows is `src/cdy/special.cdy` (`doc/hl_rqmt/symbol_table.md`); this file describes them
## literals, comments
- in the spec: `spec/00-syntax.md` (forms, comments, literals, names, and the reader's errors)
## types
- type names are Capitalised, type variables are lowercase (`a`, `b`)
- `Int` `Long` `Byte` `Float` `Double` `Bool` `Char` `String` `Unit` `Any`
- `(Maybe a)` `(Fn (a b) r)` `(List a)` `(Tup a b)` `(Map k v)`
- a `deft` type, possibly generic: `Shape`, `(Tree a)`
- `Any` turns checking off: an escape hatch
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
### sig
- the type of a top-level `def` or `defn`
- top level only, required for every `def` and `defn`, anywhere before its definition, one per name
- in `src/cdy/system.cdy`, which the translator reads, a `sig` has no definition: it declares a built-in that the runtime provides, with its type; anywhere else that is an error
- a built-in's arity is its type's, so a built-in typed `Any` (`put`) takes any number of arguments
 > (sig *symbol* *type*)
### def
- not immutable... for now... 
- top level only; *init* is required
 > (def *symbol* *init*)
### defn
- define a function
- this will be replaced w/ a macro
- top level only; at least one arg; the body is exactly one form (use `do` for more)
- a function with no real input takes a `Unit` arg: `(defn run (_) ...)`, called as `(run nil)`
 > (defn *symbol* (*args*+) *expr*)
### deft
- define a type: a record (one field list) or a sum (one or more variants: `spec/30-match.md`)
- top level only
- the type name is also its constructor: `(Vector2 1 2)`
 > (deft *Name* ((*field* *type*)*))
### get
- the field of a record or variant; *field* is not evaluated
 > (get *expr* *field*)
### assoc
- a copy with fields replaced; *field* is not evaluated
 > (assoc *expr* *field* *value* ...)
- one or more *field* *value* pairs, written flat: `(assoc v x 3 y 4)`
### match
- in the spec: `spec/30-match.md` (sum types, `match`, and `tup` patterns)
### do
- multiple expressions sequentially and returns the value of the last expression
 > (do *expr**)
### if
- no *else* and a false *test* gives `nil`
 > (if *test* *then* *else*?)
### cond
- a macro, in the prelude's macros (`src/cdy/prelude_macros.cdy`), which every file gets without `import-macros`; it expands into nested `if`s
- its name can't be bound, like any macro's
- the `else` clause is optional; no match gives `nil`
 > (cond (*test* *expr*)+ (else *expr*)?)
### let
- a binding is (*symbol* *init*); bindings are sequential, like scheme's `let*`
- a binding can take a `tup` apart: ((*symbol*+) *init*), as `(match init ((tup *symbol*+) ...))` does
 > (let ( (*binding*)* ) *expr*)
### fn
- lambda
- same rules as `defn`: at least one arg, one body form
 > (fn (*args*+) *expr*)
### tup
- a fixed-size tuple, typed `(Tup a b)`; at least one item
- taken apart with a `tup` pattern in `match`, or in a `let` binding
 > (tup *expr*+)
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
