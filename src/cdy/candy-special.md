# candy special forms and other stuff
- these are informal descriptions 
- the special form grammar uses regular expression syntax: ? (optional), * (0 or more), and + (1 or more). 
- placeholders are denoted by a italics.
- the details and the reasons behind them are in `doc/hl_rqmt/iMVP_py_translator.md`, `doc/hl_rqmt/sum_types.md` and `doc/hl_rqmt/self_host_cleanup.md`
## literals
```
100        ;; Int
1500l      ;; Long
3.14f      ;; Float
10.0       ;; Double
1b         ;; Byte
true|false ;; Bool
\e         ;; Char
"text\n"   ;; String (escapes: \" \\ \/ \b \f \n \r \t \uXXXX)
```
- `nil` (the `Unit` value) is a built-in name, not a literal
- a literal must end at a delimiter: whitespace, a paren, `;` or the end
- `'` is reserved (for the quote shorthand)
## comments
- `;` are comments
- `;` — Used for inline comments next to code.
- `;;` — Used for standalone line comments.
- `;;;` — Used for section headers or block descriptions 
## types
- type names are Capitalised, type variables are lowercase (`a`, `b`)
- `Int` `Long` `Byte` `Float` `Double` `Bool` `Char` `String` `Unit` `Any`
- `(Maybe a)` `(Fn (a b) r)` `(List a)` `(Tup a b)` `(Map k v)`
- a `deft` type, possibly generic: `Shape`, `(Tree a)`
- `Any` turns checking off: an escape hatch
## programs
- a program runs its top-level forms in order
- if it defines `main`, typed `(Fn ((List String)) Int)`, `main` then runs with the command-line arguments, and the program exits with its result
- `main` runs only when the program itself is run: not when it's imported, as the translator's own `main` (its driver) isn't when tests load it
- a `fail` in `main` prints `candy: ` and the message, and exits with 1
## special forms
### import
- top level only
- imports the module *symbol*`.cdy`, found in the importing file's directory; *symbol* may be a relative path (`lib/util`)
- every name the module defines at top level (`def`, `defn`, `deft` with its variants) becomes visible here, unqualified; names the module imports don't
- two imports that define the same name are an error; the file's own definition of a name wins over an import's
- importing a module twice is fine; an import cycle is an error, and so are two imported modules with the same file name (`util` and `lib/util`)
- in a macro file, `import` still pastes the file in (inclusion), as the macro file's helpers
- only in the Candy translator (the Python translator is frozen)
 > (import *symbol*)
### import-macros
- top level only; *symbol*`.cdy` is found as for `import`, but it is a **macro file**: its `defmacro`s become macros of the importing file, and its other definitions are helpers, which run only while translating (the importing file's own `defmacro`s can call them; its program can't)
- a macro file can `import` ordinary files (their definitions are helpers too) and `import-macros` other macro files, whose macros expand in it; it doesn't pass those macros on
- each macro file is loaded once per importer; a cycle is an error
- only in the Candy translator
 > (import-macros *symbol*)
#### import-as, import-from [SKIP]
- will come with modules (step B)
 > (import-as *symbol* *as-symbol*)\
 > (import-from *symbol* *from-symbols*+) 
### sig
- the type of a top-level `def` or `defn`
- top level only, required for every `def` and `defn`, anywhere before its definition, one per name
- later: a `sig` with no definition in `system.cdy` declares a runtime built-in
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
- define a type: a record (one field list) or a sum (one or more variants)
- top level only
- the type name, and each variant name, is also its constructor: `(Vector2 1 2)`, `(Circle 1.0)`
- a variant with no fields is a value: `Leaf`, not `(Leaf)`
- variant names are Capitalised; types and values share one namespace for now
 > (deft *Name* ((*field* *type*)*))\
 > (deft *Name* (*Variant* ((*field* *type*)*)?)+)\
 > (deft (*Name* *tvar*+) ...)
### get
- the field of a record or variant; *field* is not evaluated
 > (get *expr* *field*)
### assoc
- a copy with fields replaced; *field* is not evaluated
 > (assoc *expr* *field* *value* ...)
- one or more *field* *value* pairs, written flat: `(assoc v x 3 y 4)`
### match
- take a sum value apart; a pattern binds the variant's fields by position, `_` skips one
- exhaustive: without `else`, every variant needs a clause; one clause per variant
- flat patterns only (no nesting, literals or guards)
- a `tup` pattern takes a tuple apart: it is the only clause (a tuple has one shape), with no `else`; `_` skips an item
 > (match *expr* ((*Variant* *names**) *expr*)+ (else *expr*)?)\
 > (match *expr* ((tup *names*+) *expr*))
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
