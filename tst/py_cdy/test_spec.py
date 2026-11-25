"""The executable spec: the examples in ``spec/*.md`` (``doc/hl_rqmt/executable_spec.md``).

A spec file's fenced blocks are its examples:

- ``candy run``, then ``expect``: the program's output must be the ``expect`` block;
- ``candy error``, then ``expect-error``: translating it must fail, with a message that
  contains the ``expect-error`` text;
- ``candy panic``, then ``expect-panic``: it must translate, and running it must fail,
  with the ``expect-panic`` text in what it writes to stderr;
- ``candy errors``: one error example per line, ``source => message``, after any setup
  lines ended by a ``---`` line (one per table), which go before each row's source and
  must translate on their own;
- any other fence (``candy`` alone, ``markdown``): an illustration, not run.

The fences are read by ``script/doc_links.py`` (three or more backticks, closed by as many
or more, so a block of four can show blocks without running them; indented ones lose their
indent), which also reads the spec's ids (``tst/py_cdy/test_doc_links.py``). Each example
is translated by T1 and run, one test each, named ``file:line``. Each file's ``run``
examples also pass ``mypy --strict`` together, in one mypy run, and T2 translates them as
T1 does. Each ``run`` and ``panic`` example also runs on T1's interpreter, in this
process (``interp.cdy``; ``doc/hl_rqmt/interpreter.md``), and must give the same output
or panic: the spec on two implementations. A file whose status line says
``status: draft`` has its examples marked as expected failures (a passing one is reported).

A backlog item's ``candy run`` and ``candy error`` blocks (``backlog/``, ``script/backlog.py``)
are its repro: what *should* happen, run the same way as a strict expected failure, so the
test fails once the defect is fixed, until the example moves into its spec file. (A repro
runs on the interpreter too, with the same mark: one of a Python-target defect would pass
there, and so fail, a difference to decide.)
"""

import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Literal, NamedTuple

import pytest
from mypy import api as mypy_api

from backlog import item_files
from cdy_rt.primitives import CandyFail
from doc_links import Block, blocks, status, tracked_docs
from self_host import candy, load, translate_with

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "spec"
# The index, which needs no status line (its examples show the block kinds).
INDEX = "README.md"


class SpecError(Exception):
    """A spec file whose blocks don't pair up."""


class Example(NamedTuple):
    """An example: a program, and its output (``run``) or part of its message (``error``,
    ``panic``); a ``setup`` (an error table's) has no expected text, and must translate."""

    kind: Literal["run", "error", "panic", "setup"]
    source: str
    expected: str
    line: int


# The blocks an expect block follows, and the kind of example they make.
PAIRS: dict[str, Literal["run", "error", "panic"]] = {
    "candy run": "run",
    "candy error": "error",
    "candy panic": "panic",
}


def examples(text: str, name: str) -> tuple[Example, ...]:
    """The examples of the spec file ``name``, whose text is ``text``."""
    found: tuple[Example, ...] = ()
    pending: Block | None = None
    for block in blocks(text):
        if pending is not None:
            kind = PAIRS[pending.info]
            want = "expect" if kind == "run" else f"expect-{kind}"
            if block.info != want:
                raise SpecError(f"{name}:{pending.line}: {pending.info} needs {want} after it")
            expected = block.text if kind == "run" else block.text.strip()
            found = (*found, Example(kind, pending.text, expected, pending.line))
            pending = None
        elif block.info in PAIRS:
            pending = block
        elif block.info in ("expect", "expect-error", "expect-panic"):
            raise SpecError(f"{name}:{block.line}: {block.info} with no example before it")
        elif block.info == "candy errors":
            found = (*found, *error_table(block, name))
    if pending is not None:
        raise SpecError(f"{name}:{pending.line}: {pending.info} at the end, with no expect")
    return found


def error_table(block: Block, name: str) -> tuple[Example, ...]:
    """The examples of a ``candy errors`` block, one per line that isn't blank, each after
    the block's setup (the lines before a ``---`` line, if it has one). The setup is an
    example of its own too, which must translate."""
    rows = block.text.splitlines()
    separators = [i for i, row in enumerate(rows) if row.strip() == "---"]
    if len(separators) > 1:
        line = block.line + separators[1] + 1
        raise SpecError(f"{name}:{line}: a second --- (a table has one setup)")
    first = separators[0] + 1 if separators else 0
    setup = "".join(f"{line}\n" for line in rows[: first - 1]) if separators else ""
    found: tuple[Example, ...] = (Example("setup", setup, "", block.line + 1),) if setup else ()
    for offset, row in enumerate(rows[first:], start=first + 1):
        if row.strip() == "":
            continue
        if " => " not in row:
            raise SpecError(f"{name}:{block.line + offset}: expected source => message")
        source, message = row.split(" => ", 1)
        example = Example("error", setup + source.strip(), message.strip(), block.line + offset)
        found = (*found, example)
    return found


FILES = sorted(SPEC_DIR.glob("*.md"))
ITEMS = list(item_files(ROOT))
TEXTS = {path: path.read_text(encoding="utf-8") for path in (*FILES, *ITEMS)}


def marks(path: Path) -> tuple[pytest.MarkDecorator, ...]:
    """A draft file's examples may fail; a backlog item's repro must."""
    if path in ITEMS:
        return (pytest.mark.xfail(reason=f"{path.name}: not fixed yet", strict=True),)
    return (pytest.mark.xfail(reason="draft"),) if status(TEXTS[path]) == "draft" else ()


def cases(kind: str) -> list[object]:
    """Each example of ``kind`` in the spec, as a test case named ``file:line``."""
    return [
        pytest.param(example, id=f"{path.name}:{example.line}", marks=marks(path))
        for path in (*FILES, *ITEMS)
        for example in examples(TEXTS[path], path.name)
        if example.kind == kind
    ]


def runs(path: Path) -> tuple[Example, ...]:
    """The ``run`` examples of the spec file at ``path``."""
    return tuple(e for e in examples(TEXTS[path], path.name) if e.kind == "run")


RUN_FILES = [pytest.param(p, id=p.name, marks=marks(p)) for p in FILES if runs(p)]


def run(source: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Write ``source`` to a file in ``tmp_path`` and run it from the repository root."""
    path = tmp_path / "example.py"
    path.write_text(source, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True, check=False, cwd=ROOT
    )


@pytest.mark.parametrize("example", cases("run"))
def test_run(example: Example, t1: ModuleType, tmp_path: Path) -> None:
    done = run(translate_with(t1, example.source), tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stdout == example.expected


@pytest.mark.parametrize("example", cases("error"))
def test_error(example: Example, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(example.expected)):
        translate_with(t1, example.source)


@pytest.mark.parametrize("example", cases("panic"))
def test_panic(example: Example, t1: ModuleType, tmp_path: Path) -> None:
    done = run(translate_with(t1, example.source), tmp_path)
    assert done.returncode != 0, done.stdout
    assert example.expected in done.stderr
    assert "Traceback" not in done.stderr, done.stderr


def interpret(t1: ModuleType, source: str) -> str:
    """Run ``source`` on T1's interpreter, in this process; what it panicked with, as a
    translated program writes it (``candy: msg``), or ``""``."""
    try:
        t1.interpret_text(source, ())
    except (CandyFail, IndexError) as err:
        return f"candy: {err}"
    return ""


@pytest.mark.parametrize("example", cases("run"))
def test_interpret(example: Example, t1: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    panic = interpret(t1, example.source)
    assert panic == ""
    assert capsys.readouterr().out == example.expected


@pytest.mark.parametrize("example", cases("panic"))
def test_interpret_panic(example: Example, t1: ModuleType) -> None:
    assert example.expected in interpret(t1, example.source)


@pytest.mark.parametrize("example", cases("setup"))
def test_setup(example: Example, t1: ModuleType) -> None:
    translate_with(t1, example.source)


@pytest.mark.parametrize("path", RUN_FILES)
def test_mypy_strict(path: Path, t1: ModuleType, tmp_path: Path) -> None:
    outs = [tmp_path / f"example_{example.line}.py" for example in runs(path)]
    for out, example in zip(outs, runs(path), strict=True):
        out.write_text(translate_with(t1, example.source), encoding="utf-8")
    stdout, _, code = mypy_api.run(["--strict", "--no-incremental", *map(str, outs)])
    assert code == 0, stdout


@pytest.mark.parametrize("path", RUN_FILES)
def test_t1_and_t2_agree(path: Path, t1: ModuleType, t2: tuple[Path, str]) -> None:
    t2_module = load(t2[0])
    for example in runs(path):
        assert translate_with(t2_module, example.source) == translate_with(t1, example.source)


def test_spec_files_have_a_status() -> None:
    missing = [p.name for p in FILES if p.name != INDEX and status(TEXTS[p]) == ""]
    assert not missing, f"no status: draft|stable|deprecated line in {missing}"


# --- the reader (spec_runner.cdy's; doc/hl_rqmt/test_runner.md, step 2) ---


def fields(values: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    """Records (the Candy reader's ``Block``s or ``Example``s) as plain tuples."""
    return [tuple(value) for value in values]


def test_readers_agree(t1: ModuleType) -> None:
    """The Candy reader reads every spec file and repro as this file's does (until step 4
    retires this one), and every doc's fences and status line as ``doc_links.py`` does."""
    for path in (*FILES, *ITEMS):
        found = candy(t1, "spec_runner.examples")(TEXTS[path], path.name)
        assert fields(found) == fields(examples(TEXTS[path], path.name)), path.name
    for name, text in tracked_docs(ROOT).items():
        assert fields(candy(t1, "spec_runner.blocks")(text)) == fields(blocks(text)), name
        assert candy(t1, "spec_runner.status")(text) == status(text), name


@pytest.mark.parametrize("reader", ["doc_links", "candy"])
def test_blocks_and_nested_fences(reader: str, t1: ModuleType) -> None:
    read = blocks if reader == "doc_links" else candy(t1, "spec_runner.blocks")
    text = "a\n```candy run\n(put 1)\n```\n````markdown\n```expect\n1\n```\n````\n"
    assert fields(read(text)) == [
        ("candy run", "(put 1)\n", 2),
        ("markdown", "```expect\n1\n```\n", 5),
    ]


@pytest.mark.parametrize("reader", ["doc_links", "candy"])
def test_indented_fences(reader: str, t1: ModuleType) -> None:
    read = blocks if reader == "doc_links" else candy(t1, "spec_runner.blocks")
    text = "- a rule:\n\n  ```candy run\n  (put 1)\n    (put 2)\n  ```\n"
    assert fields(read(text)) == [("candy run", "(put 1)\n  (put 2)\n", 3)]


def test_unclosed_fence_runs_to_the_end(t1: ModuleType) -> None:
    assert fields(candy(t1, "spec_runner.blocks")("```candy\nx\n")) == [("candy", "x\n", 1)]


def test_examples_pair_up(t1: ModuleType) -> None:
    text = (
        "```candy run\n(put 1)\n```\n```expect\n1\n```\n"
        "```candy error\n(put x)\n```\n```expect-error\nunknown name x\n```\n"
        "```candy errors\n(put y) => unknown name y\n\n(put ()) => empty form\n```\n"
        "```candy panic\n(put (at (List) 0))\n```\n```expect-panic\nIndexError\n```\n"
    )
    assert fields(candy(t1, "spec_runner.examples")(text, "t.md")) == [
        ("run", "(put 1)\n", "1\n", 1),
        ("error", "(put x)\n", "unknown name x", 7),
        ("error", "(put y)", "unknown name y", 14),
        ("error", "(put ())", "empty form", 16),
        ("panic", "(put (at (List) 0))\n", "IndexError", 18),
    ]


def test_error_table_setup(t1: ModuleType) -> None:
    text = "```candy errors\n(sig s Int)\n(def s 1)\n --- \n(put t) => unknown name t\n```\n"
    assert fields(candy(t1, "spec_runner.examples")(text, "t.md")) == [
        ("setup", "(sig s Int)\n(def s 1)\n", "", 2),
        ("error", "(sig s Int)\n(def s 1)\n(put t)", "unknown name t", 5),
    ]


def test_error_row_with_arrows(t1: ModuleType) -> None:
    text = "```candy errors\n(f) => a => b\n```\n"
    assert fields(candy(t1, "spec_runner.examples")(text, "t.md")) == [
        ("error", "(f)", "a => b", 2)
    ]


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("```candy run\n(put 1)\n```\n```candy\nx\n```\n", "t.md:1: candy run needs expect"),
        ("```expect\n1\n```\n", "t.md:1: expect with no example before it"),
        ("```candy error\n(put x)\n```\n", "t.md:1: candy error at the end"),
        (
            "```candy panic\n(put 1)\n```\n```expect\n1\n```\n",
            "t.md:1: candy panic needs expect-panic",
        ),
        ("```candy errors\n(put x)\n```\n", "t.md:2: expected source => message"),
        ("```candy errors\n(def a 1)\n---\n---\n```\n", "t.md:4: a second ---"),
    ],
    ids=[
        "no-expect",
        "orphan-expect",
        "unclosed-pair",
        "panic-no-expect",
        "bad-row",
        "second-separator",
    ],
)
def test_examples_that_dont_pair_up(text: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(message)):
        candy(t1, "spec_runner.examples")(text, "t.md")


# --- the checks (spec_runner.cdy's; doc/hl_rqmt/test_runner.md, step 3) ---

# One example of each kind that passes, then one of each that fails.
CHECKED = (
    "```candy run\n(put 1)\n```\n```expect\n1\n```\n"
    '```candy panic\n(fail "stop")\n```\n```expect-panic\ncandy: stop\n```\n'
    "```candy errors\n(sig s Int)\n(def s 1)\n---\n(put t) => unknown name t\n```\n"
    "```candy run\n(put 2)\n```\n```expect\n1\n```\n"
    '```candy run\n(fail "no")\n```\n```expect\n\n```\n'
    "```candy panic\n(put 1)\n```\n```expect-panic\nstop\n```\n"
    '```candy panic\n(fail "go")\n```\n```expect-panic\nstop\n```\n'
    "```candy error\n(put 1)\n```\n```expect-error\nunknown\n```\n"
    "```candy error\n(put y)\n```\n```expect-error\nunknown name x\n```\n"
    "```candy errors\n(put\n---\n(put u) => unknown name u\n```\n"
)


# The spec files, and the backlog items with a repro.
ALL_FILES = [
    pytest.param(p, id=p.name, marks=marks(p))
    for p in (*FILES, *ITEMS)
    if p in FILES or examples(TEXTS[p], p.name)
]


@pytest.mark.parametrize("path", ALL_FILES)
def test_candy(path: Path, t1: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """The spec file's examples, checked by the Candy runner (``spec_runner.cdy``): on the
    interpreter, and through the translator, in this process. Its failures, each at its
    ``file:line``, are the message."""
    _, failures = candy(t1, "spec_runner.check-file")(candy(t1, "SPEC_RUNNER"), str(path))
    capsys.readouterr()  # what an example wrote to stderr
    assert not failures, "\n".join(failures)


def test_checks(t1: ModuleType) -> None:
    count, failures = candy(t1, "spec_runner.check-text")(candy(t1, "SPEC_RUNNER"), CHECKED, "t.md")
    assert count == 12
    assert failures == (
        "t.md:19: run: its output was:\n    2\n    expected:\n    1\n    ",
        "t.md:25: run: it panicked: candy: no",
        "t.md:31: panic: it didn't panic; expected: stop",
        "t.md:37: panic: it panicked with: candy: go\n    expected: stop",
        "t.md:43: error: it translated; expected: unknown",
        (
            "t.md:49: error: its error was: line 1, column 6: unknown name y\n"
            "    expected: unknown name x"
        ),
        (
            "t.md:56: setup: the setup doesn't translate: line 1, column 1: parse error: "
            "( is never closed"
        ),
        (
            "t.md:58: error: its error was: line 1, column 1: parse error: ( is never closed\n"
            "    expected: unknown name u"
        ),
    )


def test_checks_report_a_file_that_doesnt_pair_up(t1: ModuleType) -> None:
    check = candy(t1, "spec_runner.check-text")
    assert check(candy(t1, "SPEC_RUNNER"), "```expect\n1\n```\n", "t.md") == (
        0,
        ("t.md:1: expect with no example before it",),
    )


def test_spec_flag(t1_path: Path, tmp_path: Path) -> None:
    """``--spec``, on T1, as a process: each failure, a count, and the status."""
    good = tmp_path / "good.md"
    good.write_text("```candy run\n(put 1)\n```\n```expect\n1\n```\n", encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text("```candy error\n(put 1)\n```\n```expect-error\nx\n```\n", encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(t1_path), "--spec", str(good), str(bad)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 1
    assert done.stdout == (
        "bad.md:1: error: it translated; expected: x\nspec: 2 files, 2 examples, 1 failed\n"
    )


def test_status(t1: ModuleType) -> None:
    read = candy(t1, "spec_runner.status")
    assert read("# Match\n\nstatus: draft, since: sum-types\n") == "draft"
    assert read("# Match\n\nstatus: stable\n") == "stable"
    assert read("# Match\n\nStatus is stable.\n") == ""
    assert read("status: stable, since:\nstatus: draft\n") == "draft"
    assert read("status: stablest\n") == ""
