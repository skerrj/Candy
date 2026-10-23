"""Tests for ``cdy_rt.spelling``: each built-in's Python spelling."""

from cdy_rt.spelling import PRIMITIVES_MODULE, SPELLINGS, Spelling


def test_spellings() -> None:
    assert SPELLINGS["="] == Spelling("==", "compare")
    assert SPELLINGS["slurp"] == Spelling(f"{PRIMITIVES_MODULE}.slurp", "call")
    assert SPELLINGS["empty-list"] == Spelling("()", "value")
    assert "user-fn" not in SPELLINGS


def test_runtime_entries_exist() -> None:
    import importlib  # pylint: disable=import-outside-toplevel

    for entry in SPELLINGS.values():
        if entry.kind == "call" and "." in entry.py:
            module, name = entry.py.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.py
