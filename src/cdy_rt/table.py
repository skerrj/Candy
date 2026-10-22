"""The initial Candy symbol table: what each built-in Candy symbol translates to in Python.

Modelled on schmuz's ``src/py_smz/table.py`` (``OP_TABLE``). Differences from schmuz:

- Entries are typed ``TableEntry`` records instead of dicts, and ``kind`` says how the
  translator renders the symbol (operator, call, value, special form).
- The table is immutable, and holds only the built-ins: a program's own names are in the
  translator's scope (``doc/hl_rqmt/symbol_table.md``).
- No arity: a built-in's arity comes from its type in ``src/cdy/system.cdy``. Calls render
  every argument (schmuz rendered only ``arity`` of them, defaulting to 1).
- Generated code refers to helpers through ``RUNTIME_MODULE`` and ``TABLE_MODULE``, so
  changing where they live is a one-line change here.
- Candy literals (``true``/``false``, chars, string escapes) replace schmuz's ``true``,
  ``false``, ``LF``, ``DQ``, ``BS``, ``ES``, ... symbols.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Literal, NamedTuple

# Modules the generated code imports, by name. ``RUNTIME_MODULE`` holds the helper functions
# (``table_defs.py``); ``TABLE_MODULE`` is this module, which the translator needs for
# ``initial-table`` and ``PY_IMPORTS``.
RUNTIME_MODULE = "cdy_rt.table_defs"
TABLE_MODULE = "cdy_rt.table"
IMPORTS: tuple[str, ...] = ("math", "re", TABLE_MODULE, RUNTIME_MODULE)

# Where ``slurp`` looks for a Candy file that isn't found at the given path.
SEARCH_PATH: tuple[str, ...] = ("src", "tst", "lib")

# How the translator renders a symbol:
#   special  - a special form, translated by its own rule (``py`` is unused)
#   binop    - arithmetic, ``a + b``; folds left with more than two arguments
#   compare  - comparison, ``a < b``; chains with more than two arguments
#   boolop   - ``and`` / ``or``; short-circuits
#   unary    - prefix operator, ``not a``
#   call     - a function call, ``py(args...)``
#   value    - a Python expression, used as is (``math.pi``, ``None``)
#   index    - indexing, ``coll[i]`` (``py`` is the runtime helper, for use as a value)
#   slice    - slicing, ``coll[i:j]``, so a ``String`` slice stays a ``str`` (likewise)
Kind = Literal["special", "binop", "compare", "boolop", "unary", "call", "value", "index", "slice"]


class TableEntry(NamedTuple):
    """What one Candy symbol translates to."""

    py: str
    kind: Kind


Table = Mapping[str, TableEntry]


def special() -> TableEntry:
    """An entry for a special form."""
    return TableEntry("", "special")


def call(py: str) -> TableEntry:
    """An entry for a function call to the Python name ``py``."""
    return TableEntry(py, "call")


def runtime(name: str) -> TableEntry:
    """An entry for a call to a helper in ``table_defs.py``."""
    return call(f"{RUNTIME_MODULE}.{name}")


def value(py: str) -> TableEntry:
    """An entry for a Python expression used as a value."""
    return TableEntry(py, "value")


SPECIAL_FORMS: Table = {
    "import": special(),
    "import-macros": special(),
    "def": special(),
    "defn": special(),
    "do": special(),
    "if": special(),
    "let": special(),
    "fn": special(),
    # Macros (doc/hl_rqmt/macros.md): quote, quasiquote, unquote, unquote-splicing.
    "quo": special(),
    "quasi": special(),
    "unq": special(),
    "unq-sp": special(),
    "defmacro": special(),
    "format": special(),
    "tup": special(),
    "sig": special(),
    "deft": special(),
    "get": special(),
    "assoc": special(),
    "match": special(),
}

MATH: Table = {
    "PI": value("math.pi"),
    "sin": call("math.sin"),
    "cos": call("math.cos"),
    "tan": call("math.tan"),
    "+": TableEntry("+", "binop"),
    "-": TableEntry("-", "binop"),
    "*": TableEntry("*", "binop"),
    "/": TableEntry("/", "binop"),
    "quot": TableEntry("//", "binop"),  # integer division, rounding down
}

BOOL: Table = {
    "=": TableEntry("==", "compare"),
    "!=": TableEntry("!=", "compare"),
    "<": TableEntry("<", "compare"),
    ">": TableEntry(">", "compare"),
    "<=": TableEntry("<=", "compare"),
    ">=": TableEntry(">=", "compare"),
    "and": TableEntry("and", "boolop"),
    "or": TableEntry("or", "boolop"),
    "not": TableEntry("not", "unary"),
    "nil": value("None"),
}

IO: Table = {
    "print": call("print"),
    "display": call("print"),
    "put": call("print"),
    "put-err": runtime("put_err"),
    "file-put-lines": runtime("file_put_lines"),
    "slurp": runtime("slurp"),
    "spit": runtime("spit"),
    "file-exists": runtime("file_exists"),
    "make-dirs": runtime("make_dirs"),
    "path-stem": runtime("path_stem"),
    "path-dir": runtime("path_dir"),
    "path-join": runtime("path_join"),
    "path-resolve": runtime("path_resolve"),
}

RE: Table = {
    "re-search": call("re.search"),
    "re-findall": call("re.findall"),
    "re-compile": call("re.compile"),
}

COLLECTION: Table = {
    "len": call("len"),
    "empty-list": value("()"),
    # Rendered as ``coll[i]``, which mypy types precisely (``t[0]`` of a ``tuple[str, int]``
    # is a ``str``); ``table_defs.at`` would type it as the join of the element types.
    "at": TableEntry(f"{RUNTIME_MODULE}.at", "index"),
    "slice": TableEntry(f"{RUNTIME_MODULE}.slice_", "slice"),
    "join": runtime("join"),
    "is-coll": runtime("is_coll"),
    "to-list": runtime("to_list"),
    # Writable in Candy (the prelude), but built in for speed: Candy adds to a list by
    # copying it, so its own map would take quadratic time.
    "map": runtime("list_map"),
    "filter": runtime("list_filter"),
    "fold": runtime("list_fold"),
    # Maps: ``map-set`` returns a new map.
    "empty-map": value("{}"),
    "map-get": runtime("map_get"),
    "map-has": runtime("map_has"),
    "map-set": runtime("map_set"),
    "map-keys": runtime("map_keys"),
}

STRING: Table = {
    "is-empty-str": runtime("is_empty_str"),
    "to-int": runtime("to_int"),
    "to-float": runtime("to_float"),
    "is-decimal": runtime("is_decimal"),
    "hex-char": runtime("hex_char"),
    "is-str": runtime("is_str"),
    "is-digit": runtime("is_digit"),
    "is-alpha": runtime("is_alpha"),
    "is-neg-int": runtime("is_neg_int"),
    "strip": runtime("strip"),
    "replace": runtime("replace"),
    "isspace-at": runtime("isspace_at"),
    "isspace": runtime("isspace"),
    "in": runtime("in_"),
}

# For the translator: this table, which it reads as Candy data (each entry a pair, its text
# and kind; doc/hl_rqmt/symbol_table.md). schmuz read its table through ``op-tab-*``
# functions.
META_TABLE: Table = {
    "initial-table": value(f"{TABLE_MODULE}.INITIAL_TABLE"),
}

PY_RENDER: Table = {
    "get-indent": runtime("get_indent"),
    "py-mangle": runtime("py_mangle"),
    "py-repr": runtime("py_repr"),
}

# Macros (doc/hl_rqmt/macros.md): the translator loads a translated macro program and calls
# its macros; ``fresh-name`` is behind ``gensym`` (form.cdy).
MACRO: Table = {
    "load-macros": runtime("load_macros"),
    "call-macro": runtime("call_macro"),
    "module-dir": runtime("module_dir"),
    "fresh-name": runtime("fresh_name"),
}

INFRA: Table = {
    "PY_IMPORTS": value(f"{TABLE_MODULE}.IMPORTS"),
    "SYS_ARGS": value(f"{RUNTIME_MODULE}.get_args()"),
    "fail": runtime("fail"),
}

INITIAL_TABLE: Table = MappingProxyType(
    {
        **SPECIAL_FORMS,
        **MATH,
        **BOOL,
        **IO,
        **RE,
        **COLLECTION,
        **STRING,
        **META_TABLE,
        **PY_RENDER,
        **MACRO,
        **INFRA,
    }
)
