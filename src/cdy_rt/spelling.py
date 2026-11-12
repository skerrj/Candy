"""The Python spellings of Candy's built-ins: what each translates to in Python. What a
built-in is (special form, operator, or function or value with a type) is declared in
Candy, in ``src/cdy/special.cdy`` and ``src/cdy/system.cdy``, which the translator checks
against these spellings both ways (``doc/hl_rqmt/symbol_table.md``).

Modelled on schmuz's ``src/py_smz/table.py`` (``OP_TABLE``). Differences from schmuz:

- Entries are typed ``Spelling`` records instead of dicts, and ``kind`` says how the
  translator renders the symbol (operator, call, value). Special forms have no entry.
- The spellings are immutable, and cover only the built-ins: a program's own names are in the
  translator's scope (``doc/hl_rqmt/symbol_table.md``).
- No arity: a built-in's arity comes from its type in ``src/cdy/system.cdy``. Calls render
  every argument (schmuz rendered only ``arity`` of them, defaulting to 1).
- Generated code refers to primitives through ``PRIMITIVES_MODULE`` and ``SPELLING_MODULE``,
  so changing where they live is a one-line change here.
- Candy literals (``true``/``false``, chars, string escapes) replace schmuz's ``true``,
  ``false``, ``LF``, ``DQ``, ``BS``, ``ES``, ... symbols.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Literal, NamedTuple

# Modules the generated code refers to, by name (emit.cdy's PY_IMPORTS lists the imports).
# ``PRIMITIVES_MODULE`` holds the primitives (``primitives.py``); ``SPELLING_MODULE`` is
# this module, which the translator needs for ``py-spellings``.
PRIMITIVES_MODULE = "cdy_rt.primitives"
SPELLING_MODULE = "cdy_rt.spelling"

# How the translator renders a symbol:
#   binop    - arithmetic, ``a + b``; folds left with more than two arguments
#   compare  - comparison, ``a < b``; chains with more than two arguments
#   boolop   - ``and`` / ``or``; short-circuits
#   unary    - prefix operator, ``not a``
#   call     - a function call, ``py(args...)``
#   value    - a Python expression, used as is (``math.pi``, ``None``)
#   index    - indexing: ``coll[i]`` for a literal index that can't be negative (Python's
#              IndexError covers the high side), else ``py``, the runtime helper, which
#              checks the bounds (spec/60-library.md, library.bounds)
#   type     - a built-in type, ``tuple[{}, ...]``: its arguments, joined, replace ``{}``
Kind = Literal["binop", "compare", "boolop", "unary", "call", "value", "index", "type"]


class Spelling(NamedTuple):
    """What one Candy symbol translates to: an operator's ``value`` is the Python function
    it is as a value (``(fold + 0 xs)``; spec/40-expressions.md, expr.operator-values), or
    ``""`` if it can't be one."""

    py: str
    kind: Kind
    value: str = ""


Spellings = Mapping[str, Spelling]


def call(py: str) -> Spelling:
    """An entry for a function call to the Python name ``py``."""
    return Spelling(py, "call")


def primitive(name: str) -> Spelling:
    """An entry for a call to a primitive in ``primitives.py``."""
    return call(f"{PRIMITIVES_MODULE}.{name}")


def value(py: str) -> Spelling:
    """An entry for a Python expression used as a value."""
    return Spelling(py, "value")


def operator(py: str, kind: Kind, name: str = "") -> Spelling:
    """An operator's entry: ``py`` infix (or prefix), and as a value the primitive
    ``name`` in ``primitives.py`` (none if ``name`` is empty)."""
    return Spelling(py, kind, f"{PRIMITIVES_MODULE}.{name}" if name else "")


def type_(py: str) -> Spelling:
    """An entry for a built-in type, its arguments in place of ``{}``."""
    return Spelling(py, "type")


# The built-in types (system.cdy's bodiless defts). ``_cdy_Any`` and ``_cdy_Mapping`` are
# what every generated file imports ``Any`` and ``Mapping`` as.
TYPES: Spellings = {
    "Int": type_("int"),
    "Long": type_("int"),
    "Byte": type_("int"),
    "Float": type_("float"),
    "Double": type_("float"),
    "Bool": type_("bool"),
    "Char": type_("str"),
    "String": type_("str"),
    "Unit": type_("None"),
    "Any": type_("_cdy_Any"),
    "List": type_("tuple[{}, ...]"),
    "Map": type_("_cdy_Mapping[{}]"),
}

MATH: Spellings = {
    "PI": value("math.pi"),
    "sin": call("math.sin"),
    "cos": call("math.cos"),
    "tan": call("math.tan"),
    "+": operator("+", "binop", "add"),
    "++": operator("+", "binop", "append"),  # strings or lists (tuples)
    "-": operator("-", "binop", "sub"),
    "*": operator("*", "binop", "mul"),
    "/": operator("/", "binop", "div"),
    "quot": operator("//", "binop", "quot"),  # integer division, rounding down
    "mod": operator("%", "binop", "mod"),  # its remainder, with the divisor's sign
}

BOOL: Spellings = {
    "=": operator("==", "compare", "eq"),
    "!=": operator("!=", "compare", "ne"),
    "<": operator("<", "compare", "lt"),
    ">": operator(">", "compare", "gt"),
    "<=": operator("<=", "compare", "le"),
    ">=": operator(">=", "compare", "ge"),
    "and": operator("and", "boolop", "and_"),
    "or": operator("or", "boolop", "or_"),
    "not": operator("not", "unary", "not_"),
    "nil": value("None"),
}

IO: Spellings = {
    "put-line": call("print"),
    # ``emit`` writes ``text`` and ``show`` by the argument's static type; as a value (or
    # for a translator that doesn't), ``text`` goes by the Python value.
    "text": primitive("text_any"),
    "show": primitive("show"),
    "put-err": primitive("put_err"),
    "file-put-lines": primitive("file_put_lines"),
    "slurp": primitive("slurp"),
    "spit": primitive("spit"),
    "file-exists": primitive("file_exists"),
    "make-dirs": primitive("make_dirs"),
    "path-stem": primitive("path_stem"),
    "path-dir": primitive("path_dir"),
    "path-join": primitive("path_join"),
    "path-resolve": primitive("path_resolve"),
}

RE: Spellings = {
    "re-search": call("re.search"),
    "re-findall": call("re.findall"),
    "re-compile": call("re.compile"),
}

COLLECTION: Spellings = {
    "len": call("len"),
    "empty-list": value("()"),
    # Rendered as ``coll[i]``, which mypy types precisely (``t[0]`` of a ``tuple[str, int]``
    # is a ``str``); ``primitives.at`` would type it as the join of the element types.
    "at": Spelling(f"{PRIMITIVES_MODULE}.at", "index"),
    "slice": primitive("slice_"),
    "join": primitive("join"),
    "is-coll": primitive("is_coll"),
    # Writable in Candy (the prelude), but built in for speed: Candy adds to a list by
    # copying it, so its own map would take quadratic time.
    "map": primitive("list_map"),
    "filter": primitive("list_filter"),
    "fold": primitive("list_fold"),
    "map-acc": primitive("list_map_acc"),
    # Maps: ``map-set`` returns a new map.
    "empty-map": value("{}"),
    "map-get": primitive("map_get"),
    "map-has": primitive("map_has"),
    "map-set": primitive("map_set"),
    "map-keys": primitive("map_keys"),
    "map-from": primitive("map_from"),
    "map-size": call("len"),
    # The library (doc/hl_rqmt/library.md): a list is the host's tuple, so its operations
    # are built-ins.
    "any": primitive("list_any"),
    "all": primitive("list_all"),
    "find-index": primitive("list_find_index"),
    "reverse": primitive("list_reverse"),
    "range": primitive("list_range"),
    "take": primitive("list_take"),
    "drop": primitive("list_drop"),
    "concat": primitive("list_concat"),
    "zip": primitive("list_zip"),
    "elem-index": primitive("list_elem_index"),
    "contains": primitive("list_contains"),
}

STRING: Spellings = {
    "str-len": call("len"),
    "char-at": Spelling(f"{PRIMITIVES_MODULE}.char_at", "index"),
    "substring": primitive("substring"),
    "str-contains": primitive("str_contains"),
    "is-empty-str": primitive("is_empty_str"),
    "to-int": primitive("to_int"),
    "to-float": primitive("to_float"),
    "is-decimal": primitive("is_decimal"),
    "hex-char": primitive("hex_char"),
    "starts-with": primitive("starts_with"),
    "ends-with": primitive("ends_with"),
    "split": primitive("split"),
    "repeat": primitive("repeat"),
    "char-code": call("ord"),
    "is-str": primitive("is_str"),
    "is-digit": primitive("is_digit"),
    "is-alpha": primitive("is_alpha"),
    "is-neg-int": primitive("is_neg_int"),
    "strip": primitive("strip"),
    "replace": primitive("replace"),
    "isspace-at": primitive("isspace_at"),
    "isspace": primitive("isspace"),
}

# For the translator: these spellings, which it reads as Candy data (each entry a pair, its
# text and kind; doc/hl_rqmt/symbol_table.md). schmuz read its table through ``op-tab-*``
# functions.
TRANSLATOR: Spellings = {
    "py-spellings": value(f"{SPELLING_MODULE}.SPELLINGS"),
}

# Macros (doc/hl_rqmt/macros.md): the translator loads a translated macro program and calls
# its macros; ``fresh-name`` is behind ``gensym`` (form.cdy).
MACRO: Spellings = {
    "load-macros": primitive("load_macros"),
    "call-macro": primitive("call_macro"),
    "module-dir": primitive("module_dir"),
    "fresh-name": primitive("fresh_name"),
}

INFRA: Spellings = {
    "SYS_ARGS": value(f"{PRIMITIVES_MODULE}.get_args()"),
    "fail": primitive("fail"),
}

SPELLINGS: Spellings = MappingProxyType(
    {
        **TYPES,
        **MATH,
        **BOOL,
        **IO,
        **RE,
        **COLLECTION,
        **STRING,
        **TRANSLATOR,
        **MACRO,
        **INFRA,
    }
)
