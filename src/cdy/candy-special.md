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
- in the spec: `spec/50-macros.md`
### sig, def, deft, get, assoc, tup
- in the spec: `spec/20-types.md` (records; sum types in `spec/30-match.md`)
- `system.cdy`'s bodiless `sig`s: `spec/60-library.md`
### match
- in the spec: `spec/30-match.md`
### defn, do, if, cond, let, fn
- in the spec: `spec/40-expressions.md`
### defmacro, quo, quasi, unq, unq-sp
- in the spec: `spec/50-macros.md`
### format
- in the spec: `spec/60-library.md` (with the built-ins and the prelude)
