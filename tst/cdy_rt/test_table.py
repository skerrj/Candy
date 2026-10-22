"""Tests for the initial symbol table in ``cdy_rt.table``."""

from cdy_rt.table import (
    INITIAL_TABLE,
    RUNTIME_MODULE,
    get_py,
    is_op,
    is_special,
)


def test_lookups() -> None:
    assert is_special(INITIAL_TABLE, "defn")
    assert not is_special(INITIAL_TABLE, "+")
    assert is_op(INITIAL_TABLE, "slurp") and not is_op(INITIAL_TABLE, "nope")


def test_get_py() -> None:
    assert get_py(INITIAL_TABLE, "=") == "=="
    assert get_py(INITIAL_TABLE, "slurp") == f"{RUNTIME_MODULE}.slurp"
    assert get_py(INITIAL_TABLE, "empty-list") == "()"
    assert get_py(INITIAL_TABLE, "user-fn") == "user-fn"


def test_runtime_entries_exist() -> None:
    import importlib  # pylint: disable=import-outside-toplevel

    for entry in INITIAL_TABLE.values():
        if entry.kind == "call" and "." in entry.py:
            module, name = entry.py.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.py
