"""The backlog (``backlog/``, ``script/backlog.py``; ``doc/hl_rqmt/tracking.md``, step 2).

Every item is well formed (its file name, title and fields; a done item says where it was
fixed; a closed item has no repro left), no two share a number, and the index,
``backlog/README.md``, is what ``python script/backlog.py`` writes. The repros run with the
spec (``tst/py_cdy/test_spec.py``).
"""

import re
from pathlib import Path

import pytest

from backlog import INDEX, BacklogError, Item, index, item, items, rule_files

ROOT = Path(__file__).resolve().parents[2]


def test_items_are_well_formed() -> None:
    assert items(ROOT)


def test_index_is_current() -> None:
    want = index(items(ROOT), rule_files(ROOT))
    assert (ROOT / INDEX).read_text(encoding="utf-8") == want, "run python script/backlog.py"


# --- the format itself ---

FIELDS = (
    "kind: defect\nstate: open\npriority: normal\nfound: tracking, 2026-10-25\nfixed:\n"
    "where: `src/cdy/emit.cdy`\nrefs: [[types.names]], [[B1]]\n"
)
GOOD = f"# B3: a thing\n\n{FIELDS}\nWhat it is.\n"


def test_an_item() -> None:
    assert item("backlog/B3-a-thing.md", GOOD) == Item(
        "B3",
        3,
        "backlog/B3-a-thing.md",
        "a thing",
        "defect",
        "open",
        "normal",
        "tracking, 2026-10-25",
        "",
        "`src/cdy/emit.cdy`",
        ("types.names", "B1"),
    )


REPRO = "```candy error\n(put x)\n```\n```expect-error\nunknown\n```\n"


@pytest.mark.parametrize(
    ("path", "text", "message"),
    [
        ("backlog/b3-thing.md", GOOD, "B<n>-<slug>.md"),
        ("backlog/B3_thing.md", GOOD, "B<n>-<slug>.md"),
        ("backlog/B4-a-thing.md", GOOD, "the first line is # B4: <title>"),
        ("backlog/B3-a-thing.md", "# B3: a thing\n" + FIELDS, "then the fields"),
        ("backlog/B3-a-thing.md", GOOD.replace("kind: defect", "kind: bug"), "kind is bug"),
        ("backlog/B3-a-thing.md", GOOD.replace("state: open", "state: blocked"), "state is"),
        ("backlog/B3-a-thing.md", GOOD.replace("priority: normal", "priority: p1"), "priority"),
        ("backlog/B3-a-thing.md", GOOD.replace("found: tracking, 2026-10-25", "found:"), "found"),
        ("backlog/B3-a-thing.md", GOOD.replace("kind:", "sort:"), ":3: expected kind"),
        ("backlog/B3-a-thing.md", GOOD.replace("state: open", "state: done"), "where it was"),
        (
            "backlog/B3-a-thing.md",
            GOOD.replace("state: open", "state: dropped") + REPRO,
            "a closed item has a repro left",
        ),
        ("backlog/B3-a-thing.md", GOOD.replace(", [[B1]]", ", B1"), "refs are links only"),
    ],
    ids=[
        "lowercase-name",
        "bad-name",
        "title-number",
        "no-blank",
        "kind",
        "state",
        "priority",
        "empty-found",
        "field-order",
        "done-unfixed",
        "closed-repro",
        "refs",
    ],
)
def test_items_that_arent(path: str, text: str, message: str) -> None:
    with pytest.raises(BacklogError, match=re.escape(message)):
        item(path, text)


def test_the_index() -> None:
    first = item(
        "backlog/B1-first.md", GOOD.replace("B3", "B1").replace("priority: normal", "priority: low")
    )
    second = item("backlog/B3-a-thing.md", GOOD)
    done = item(
        "backlog/B2-done.md",
        GOOD.replace("B3", "B2")
        .replace("state: open", "state: done")
        .replace("fixed:", "fixed: x"),
    )
    text = index((first, done, second), {"types.names": "spec/20-types.md"})
    assert "The next item is B4." in text
    open_rows = text.split("## Open")[1].split("## By rule")[0]
    assert open_rows.index("[B3]") < open_rows.index("[B1]")
    assert "[B2]" not in open_rows and "[B2](B2-done.md)" in text.split("## Closed")[1]
    assert "- [types.names](../spec/20-types.md#types.names): [B3](B3-a-thing.md)" in text


def test_two_items_with_one_number(tmp_path: Path) -> None:
    (tmp_path / "backlog").mkdir()
    for name in ("B3-a-thing.md", "B3-other.md"):
        (tmp_path / "backlog" / name).write_text(GOOD, encoding="utf-8")
    with pytest.raises(BacklogError, match="two items numbered B3"):
        items(tmp_path)
