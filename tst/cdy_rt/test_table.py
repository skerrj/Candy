"""Tests for the initial symbol table in ``cdy_rt.table``: each built-in's Python spelling."""

from cdy_rt.table import INITIAL_TABLE, RUNTIME_MODULE, TableEntry


def test_spellings() -> None:
    assert INITIAL_TABLE["="] == TableEntry("==", "compare")
    assert INITIAL_TABLE["slurp"] == TableEntry(f"{RUNTIME_MODULE}.slurp", "call")
    assert INITIAL_TABLE["empty-list"] == TableEntry("()", "value")
    assert "user-fn" not in INITIAL_TABLE


def test_runtime_entries_exist() -> None:
    import importlib  # pylint: disable=import-outside-toplevel

    for entry in INITIAL_TABLE.values():
        if entry.kind == "call" and "." in entry.py:
            module, name = entry.py.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.py
