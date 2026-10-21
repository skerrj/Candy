"""Tests for the initial symbol table in ``cdy_rt.table``."""

from cdy_rt.table import (
    INITIAL_TABLE,
    RUNTIME_MODULE,
    TableEntry,
    add_fun,
    get_py,
    is_bin_op,
    is_op,
    is_special,
)


def test_lookups() -> None:
    assert is_special(INITIAL_TABLE, "defn")
    assert not is_special(INITIAL_TABLE, "+")
    assert is_bin_op(INITIAL_TABLE, "+") and is_bin_op(INITIAL_TABLE, "<")
    assert is_bin_op(INITIAL_TABLE, "and")
    assert not is_bin_op(INITIAL_TABLE, "not")
    assert is_op(INITIAL_TABLE, "slurp") and not is_op(INITIAL_TABLE, "nope")


def test_get_py() -> None:
    assert get_py(INITIAL_TABLE, "=") == "=="
    assert get_py(INITIAL_TABLE, "slurp") == f"{RUNTIME_MODULE}.slurp"
    assert get_py(INITIAL_TABLE, "empty-list") == "()"
    assert get_py(INITIAL_TABLE, "user-fn") == "user-fn"


def test_add_fun_returns_new_table() -> None:
    table = add_fun(INITIAL_TABLE, "sq", "sq")
    assert table["sq"] == TableEntry("sq", "call")
    assert "sq" not in INITIAL_TABLE


def test_runtime_entries_exist() -> None:
    import importlib  # pylint: disable=import-outside-toplevel

    for entry in INITIAL_TABLE.values():
        if entry.kind == "call" and "." in entry.py:
            module, name = entry.py.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.py
