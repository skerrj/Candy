"""The executable spec: the examples in ``spec/*.md`` (``doc/hl_rqmt/executable_spec.md``),
checked by the spec's runner, which is Candy (``src/cdy/spec_runner.cdy``;
``doc/hl_rqmt/test_runner.md``), and here for the Python target.

A spec file's fenced blocks are its examples (``spec/README.md``; ``spec_runner.cdy``):

- ``candy run``, then ``expect``: the program's output must be the ``expect`` block;
- ``candy error``, then ``expect-error``: translating it must fail, with a message that
  contains the ``expect-error`` text;
- ``candy panic``, then ``expect-panic``: it must translate, and running it must fail,
  with the ``expect-panic`` text in what it writes to stderr;
- ``candy errors``: one error example per line, ``source => message``, after any setup
  lines ended by a ``---`` line (one per table), which go before each row's source and
  must translate on their own;
- any other fence (``candy`` alone, ``markdown``): an illustration, not run.

Each file is tested whole, by T1, its failures the message, each at its ``file:line``:

- ``test_candy``: the Candy runner's checks, in this process: ``run`` and ``panic``
  examples on the interpreter, ``error`` and ``setup`` examples through the translator
  (``cdy_translator.py --spec FILE.md`` runs the same checks without pytest);
- ``test_python``: each ``run`` and ``panic`` example translated and run as a Python
  program, with the same output, or panic, as the interpreter's: the spec on two
  implementations;
- ``test_mypy_strict``: the ``run`` examples pass ``mypy --strict`` together, in one run;
- ``test_t1_and_t2_agree``: T2 translates them as T1 does.

The examples come from the Candy reader (``spec_runner.examples``). Which files have
examples is decided before T1 is built, so by ``script/doc_links.py``'s reading of the
fences, the same rules. A file whose status line says ``status: draft`` is marked as an
expected failure (a passing one is reported).

A backlog item's ``candy run`` and ``candy error`` blocks (``backlog/``, ``script/backlog.py``)
are its repro: what *should* happen, checked the same way as a strict expected failure, so
the test fails once the defect is fixed, until the example moves into its spec file. (A
repro runs on the interpreter too, with the same mark: one of a Python-target defect would
pass there, and so fail, a difference to decide.)
"""

import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from mypy import api as mypy_api

from backlog import item_files
from cdy_rt.primitives import CandyFail
from doc_links import blocks, status
from self_host import candy, load, translate_with

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "spec"
# The index, which needs no status line (its examples show the block kinds).
INDEX = "README.md"
# The blocks that start an example.
STARTS = ("candy run", "candy error", "candy errors", "candy panic")

FILES = sorted(SPEC_DIR.glob("*.md"))
ITEMS = list(item_files(ROOT))
TEXTS = {path: path.read_text(encoding="utf-8") for path in (*FILES, *ITEMS)}


def has(path: Path, infos: tuple[str, ...]) -> bool:
    """Whether the file at ``path`` has a block of one of the kinds ``infos``."""
    return any(block.info in infos for block in blocks(TEXTS[path]))


def marks(path: Path) -> tuple[pytest.MarkDecorator, ...]:
    """A draft file's examples may fail; a backlog item's repro must."""
    if path in ITEMS:
        return (pytest.mark.xfail(reason=f"{path.name}: not fixed yet", strict=True),)
    return (pytest.mark.xfail(reason="draft"),) if status(TEXTS[path]) == "draft" else ()


def params(paths: list[Path]) -> list[object]:
    """``paths`` as test cases, named by the file, with their marks."""
    return [pytest.param(p, id=p.name, marks=marks(p)) for p in paths]


# The spec files, and the backlog items with a repro.
ALL_FILES = params([p for p in (*FILES, *ITEMS) if p in FILES or has(p, STARTS)])
# Those with an example to run as a Python program, and those with one that runs.
RUNNING = params([p for p in (*FILES, *ITEMS) if has(p, ("candy run", "candy panic"))])
RUN_FILES = params([p for p in FILES if has(p, ("candy run",))])


def examples(t1: ModuleType, path: Path, kinds: tuple[str, ...]) -> list[Any]:
    """The examples of ``kinds`` in the file at ``path``, read by the Candy reader."""
    found = candy(t1, "spec_runner.examples")(TEXTS[path], path.name)
    return [example for example in found if example.kind in kinds]


@pytest.mark.parametrize("path", ALL_FILES)
def test_candy(path: Path, t1: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """The file's examples, checked by the Candy runner (``spec_runner.cdy``): on the
    interpreter, and through the translator, in this process."""
    _, failures = candy(t1, "spec_runner.check-file")(candy(t1, "SPEC_RUNNER"), str(path))
    capsys.readouterr()  # what an example wrote to stderr
    assert not failures, "\n".join(failures)


def run(source: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Write ``source`` to a file in ``tmp_path`` and run it from the repository root."""
    path = tmp_path / "example.py"
    path.write_text(source, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True, check=False, cwd=ROOT
    )


def python_failure(example: Any, t1: ModuleType, tmp_path: Path) -> str:
    """What is wrong with the ``run`` or ``panic`` example, translated by T1 and run as a
    Python program: ``""`` if nothing is."""
    done = run(translate_with(t1, example.source), tmp_path)
    if "Traceback" in done.stderr:
        return f"a traceback:\n{done.stderr}"
    if example.kind == "run" and done.returncode != 0:
        return f"its status was {done.returncode}:\n{done.stderr}"
    if example.kind == "run" and done.stdout != example.expected:
        return f"its output was:\n{done.stdout}expected:\n{example.expected}"
    if example.kind == "panic" and done.returncode == 0:
        return f"it didn't panic; expected: {example.expected}"
    if example.kind == "panic" and example.expected not in done.stderr:
        return f"it panicked with: {done.stderr}expected: {example.expected}"
    return ""


@pytest.mark.parametrize("path", RUNNING)
def test_python(path: Path, t1: ModuleType, tmp_path: Path) -> None:
    """The file's ``run`` and ``panic`` examples on the Python target, each a process."""
    failures = [
        f"{path.name}:{example.line}: {example.kind}: {failure}"
        for example in examples(t1, path, ("run", "panic"))
        if (failure := python_failure(example, t1, tmp_path))
    ]
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("path", RUN_FILES)
def test_mypy_strict(path: Path, t1: ModuleType, tmp_path: Path) -> None:
    runs = examples(t1, path, ("run",))
    outs = [tmp_path / f"example_{example.line}.py" for example in runs]
    for out, example in zip(outs, runs, strict=True):
        out.write_text(translate_with(t1, example.source), encoding="utf-8")
    stdout, _, code = mypy_api.run(["--strict", "--no-incremental", *map(str, outs)])
    assert code == 0, stdout


@pytest.mark.parametrize("path", RUN_FILES)
def test_t1_and_t2_agree(path: Path, t1: ModuleType, t2: tuple[Path, str]) -> None:
    t2_module = load(t2[0])
    for example in examples(t1, path, ("run",)):
        assert translate_with(t2_module, example.source) == translate_with(t1, example.source)


def test_spec_files_have_a_status() -> None:
    missing = [p.name for p in FILES if p.name != INDEX and status(TEXTS[p]) == ""]
    assert not missing, f"no status: draft|stable|deprecated line in {missing}"


# --- the reader (spec_runner.cdy's; doc/hl_rqmt/test_runner.md, step 2) ---


def fields(values: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    """Records (the Candy reader's ``Block``s or ``Example``s) as plain tuples."""
    return [tuple(value) for value in values]


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
