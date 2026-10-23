"""Runtime helpers that translated Candy code calls (``table.py`` entries point here).

Started from schmuz's ``src/py_smz/smztils.py``. Differences from schmuz:

- No ``bop_table`` copy or renamed imports: ``SEARCH_PATH`` comes straight from ``table``.
- Names that clash with Python built-ins or keywords get a trailing ``_``: ``slice_``,
  ``in_``. ``join_it`` is now ``join``.
- ``spit`` takes ``(path, text)`` and writes a string, like Clojure's ``spit``.
  ``file_put_lines`` takes ``(path, lines)``. (schmuz had them in opposite orders.)
- ``slurp`` raises ``FileNotFoundError`` instead of calling ``exit()``, and looks for
  ``.cdy`` files.
- ``is_coll`` accepts tuples as well as lists.
- ``is_str`` is a plain type check. schmuz's version tested for a ``"``-quoted token.
- Added ``is_empty_str`` (schmuz's table referred to it, but smztils never defined it).
- Dropped the ``m_table_*`` functions (the self-hosted compiler calls ``table``'s functions
  directly), the ``parse_string_help*`` leftovers (schmuz's own ``parse.scm`` defined the
  one it used) and commented-out experiments.
"""

import functools
import itertools
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any, NoReturn, cast

from cdy_rt.table import SEARCH_PATH

# --- collections ---


def at[T](coll: Sequence[T], i: int) -> T:
    """The item at index ``i``."""
    return coll[i]


def slice_[T](coll: Sequence[T], i: int, j: int) -> Sequence[T]:
    """Items ``i`` up to (not including) ``j``."""
    return coll[i:j]


def join(coll: Sequence[str], delim: str) -> str:
    """The strings in ``coll`` joined with ``delim``."""
    return delim.join(coll)


def is_coll(expr: object) -> bool:
    """Whether ``expr`` is a list or tuple."""
    return isinstance(expr, (list, tuple))


def list_map[A, B](f: Callable[[A], B], xs: Sequence[A]) -> tuple[B, ...]:
    """``f`` of each item of ``xs``. A built-in, not Candy, for speed: Candy adds to a list
    by copying it (doc/hl_rqmt/system_prelude.md, step 5)."""
    return tuple(map(f, xs))


def list_filter[A](keep: Callable[[A], bool], xs: Sequence[A]) -> tuple[A, ...]:
    """The items of ``xs`` for which ``keep`` is true (a built-in for speed, as ``list_map``)."""
    return tuple(x for x in xs if keep(x))


def list_fold[A, B](f: Callable[[B, A], B], acc: B, xs: Sequence[A]) -> B:
    """``f`` applied to ``acc`` and each item of ``xs`` in turn (a built-in for speed)."""
    return functools.reduce(f, xs, acc)


def to_list[T](val: T) -> tuple[T, ...]:
    """A one-item list holding ``val`` (a Candy ``List`` is a Python tuple)."""
    return (val,)


def map_get[K, V](m: Mapping[K, V], key: K) -> V:
    """The value for ``key``, which must be in ``m``."""
    return m[key]


def map_has[K, V](m: Mapping[K, V], key: K) -> bool:
    """Whether ``key`` is in ``m``."""
    return key in m


def map_set[K, V](m: Mapping[K, V], key: K, val: V) -> Mapping[K, V]:
    """A new map: ``m`` with ``key`` set to ``val``."""
    return {**m, key: val}


def map_keys[K, V](m: Mapping[K, V]) -> tuple[K, ...]:
    """The keys of ``m``, in the order they were first set."""
    return tuple(m)


def in_(item: object, coll: Sequence[object]) -> bool:
    """Whether ``item`` is in ``coll`` (a string is a sequence too)."""
    return item in coll


# --- strings ---


def is_str(expr: object) -> bool:
    """Whether ``expr`` is a string."""
    return isinstance(expr, str)


def is_empty_str(text: str) -> bool:
    """Whether ``text`` is the empty string."""
    return text == ""


def is_digit(text: str) -> bool:
    """Whether ``text`` is all digits (and not empty)."""
    return text.isdigit()


def is_alpha(text: str) -> bool:
    """Whether ``text`` is all letters (and not empty)."""
    return text.isalpha()


def is_neg_int(text: str, pos: int) -> bool:
    """Whether ``text`` has a ``-`` followed by a digit at ``pos``."""
    return text[pos : pos + 1] == "-" and text[pos + 1 : pos + 2].isdigit()


def isspace(text: str) -> bool:
    """Whether ``text`` is all whitespace (and not empty)."""
    return text.isspace()


def isspace_at(text: str, pos: int) -> bool:
    """Whether the character at ``pos`` is whitespace."""
    return text[pos].isspace()


def to_int(text: str) -> int:
    """``text`` parsed as an integer."""
    return int(text)


def to_float(text: str) -> float:
    """``text`` parsed as a floating-point number."""
    return float(text)


def is_decimal(text: str) -> bool:
    """Whether ``text`` is all decimal digits (and not empty), as a regex's ``\\d`` matches."""
    return text.isdecimal()


def hex_char(text: str) -> str:
    """The character whose code is ``text`` in hexadecimal: ``hex_char("41")`` is ``"A"``."""
    return chr(int(text, 16))


def strip(text: str, chars: str) -> str:
    """``text`` without leading or trailing characters from ``chars``."""
    return text.strip(chars)


def replace(text: str, old: str, new: str) -> str:
    """``text`` with the first ``old`` replaced by ``new``."""
    return text.replace(old, new, 1)


# --- files ---


def find_path(name: str, search_path: Sequence[str]) -> Path | None:
    """The first ``.cdy`` file under ``search_path`` whose stem matches ``name``.

    Files under a ``tmp`` directory (below the search root) are skipped.
    """
    stem = Path(name).stem
    matches = (
        path
        for root in search_path
        for path in Path(root).rglob("*.cdy")
        if path.stem == stem and "tmp" not in path.relative_to(root).parts
    )
    return next(matches, None)


def get_path(name: str, search_path: Sequence[str]) -> Path:
    """``name`` if it exists, otherwise the matching file under ``search_path``."""
    given = Path(name)
    found = given if given.exists() else find_path(name, search_path)
    if found is None:
        raise FileNotFoundError(f"can't find {name} (searched {', '.join(search_path)})")
    return found


def slurp(name: str) -> str:
    """The whole text of a Candy file, found as ``get_path`` describes."""
    return get_path(name, SEARCH_PATH).read_text(encoding="utf-8")


def put_err(text: str) -> None:
    """Print ``text`` on standard error."""
    print(text, file=sys.stderr)


def spit(path: str, text: str) -> None:
    """Write ``text`` to ``path``, replacing its contents."""
    Path(path).write_text(text, encoding="utf-8")


def file_put_lines(path: str, lines: Sequence[str]) -> None:
    """Write ``lines`` to ``path`` as they are (they carry their own newlines)."""
    Path(path).write_text("".join(lines), encoding="utf-8")


def file_exists(path: str) -> bool:
    """Whether ``path`` is a file (``slurp`` would otherwise search for it)."""
    return Path(path).is_file()


def make_dirs(path: str) -> None:
    """Create the directory ``path``, and any missing parents, unless it exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def path_stem(path: str) -> str:
    """The file name in ``path`` without its extension: ``src/x/prog.cdy`` -> ``prog``."""
    return Path(path).stem


def path_dir(path: str) -> str:
    """The directory part of ``path``."""
    return str(Path(path).parent)


def path_join(directory: str, name: str) -> str:
    """``name`` inside ``directory``."""
    return str(Path(directory) / name)


def path_resolve(path: str) -> str:
    """``path`` made absolute, with symbolic links and ``..`` resolved."""
    return str(Path(path).resolve())


# --- infra ---


class CandyFail(Exception):
    """Raised by ``fail``: a Candy program (such as the self-hosted translator) gave up."""


def fail(msg: str) -> NoReturn:
    """Stop with the error ``msg`` (Candy has no exceptions yet)."""
    raise CandyFail(msg)


def get_args() -> tuple[str, ...]:
    """The command-line arguments, without the program name."""
    return tuple(sys.argv[1:])


def run_main(main: Callable[[tuple[str, ...]], int]) -> NoReturn:
    """Run a Candy program's ``main`` with the command-line arguments and exit with its
    result. A ``fail``, or a file that can't be read, prints ``candy: <error>`` and exits
    with 1."""
    try:
        status = main(get_args())
    except (CandyFail, OSError) as err:
        print(f"candy: {err}", file=sys.stderr)
        status = 1
    sys.exit(status)


# --- macros (doc/hl_rqmt/macros.md) ---

# Counts the names fresh_name makes; load_macros restarts it, so a program's translation
# doesn't depend on what was translated before it.
_FRESH = [itertools.count(1)]


def fresh_name(prefix: str) -> str:
    """A new name, ``prefix__N``, for a macro to introduce. The reader rejects ``__`` in a
    name, so no program can spell it."""
    return f"{prefix}__{next(_FRESH[0])}"


def module_dir(fn: Callable[..., object]) -> str:
    """The directory of the Python module that defines the function ``fn``."""
    return str(Path(module_globals(fn)["__file__"]).parent)


def module_globals(fn: Callable[..., object]) -> dict[str, Any]:
    """The namespace of the module that defines the function ``fn``. (Generated code types
    a Candy function as a ``Callable``, which has no ``__globals__``.)"""
    return cast(dict[str, Any], getattr(fn, "__globals__"))  # noqa: B009


def load_macros(
    python: str, home: Callable[..., object], keep: Mapping[str, object]
) -> Mapping[str, Any]:
    """Run ``python``, a translated macro program, in a copy of the namespace of the module
    that defines the function ``home`` (the translator), and return its macros: the functions
    named ``macro__...``. The Candy names in ``keep`` (``form.cdy``'s) are then set back to
    the translator's, so the macros build the translator's own ``Form``s, not those of the
    macro program's copy of ``form.cdy`` (``home`` is one of ``form.cdy``'s functions).
    See "How load-macros runs macro code" in ``doc/hl_rqmt/macros.md``."""
    home_ns = module_globals(home)
    namespace = dict(home_ns)
    exec(compile(python, "<macros>", "exec"), namespace)  # noqa: S102  # pylint: disable=exec-used
    # In a translator built with modules, form.cdy's names have its prefix (``form__Sym``),
    # which ``home``'s own Python name shows; a translator built before modules has none.
    # ``keep``'s names are Python names (the translator mangles them).
    head, sep, _ = home.__name__.rpartition("__")
    for name in keep:
        namespace[name] = home_ns[head + sep + name]
    _FRESH[0] = itertools.count(1)
    return {name: val for name, val in namespace.items() if name.startswith("macro__")}


def call_macro(macro: Any, args: Sequence[Any], where: str) -> Any:
    """``macro`` called on the forms ``args``. An error in it, a ``fail`` or a bug, starts
    with ``where`` (the call's position and the macro's name)."""
    try:
        return macro(args)
    except CandyFail as err:
        raise CandyFail(f"{where}{err}") from err
    except Exception as err:  # pylint: disable=broad-exception-caught
        raise CandyFail(f"{where}{type(err).__name__}: {err}") from err
