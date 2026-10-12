# candy special forms and other stuff
- these are informal descriptions 
- the special form grammar uses regular expression syntax: ? (optional), * (0 or more), and + (1 or more). 
- placeholders are denoted by a italics.
## comments
- `;` are comments
- `;` — Used for inline comments next to code.
- `;;` — Used for standalone line comments.
- `;;;` — Used for section headers or block descriptions 
## special forms
### import [SKIP]
- will add after initial bootstrap
 > (import *symbol*)\
 > (import-as *symbol* *as-symbol*)\
 > (import-from *symbol* *from-symbols*+) 
### def
- not immutable... for now... 
 > (def *symbol* *init*?)
### defn
- define a function
- this will be replaced w/ a macro
 > (defn *symbol* (*args**) *expr*)
### do
- multiple expressions sequentially and returns the value of the last expression
 > (do *expr**)
### if
 > (if *test* *then* *else*?)
### cond
- this will be replaced w/ a macro
 > (cond (*test* *expr*)+ (else *expr*))
### let
 > (let ( (*binding*)* ) *expr*)
### fn
- lambda
 > (fn (*args**) *expr*)
## weird stuff 
### format
### tup