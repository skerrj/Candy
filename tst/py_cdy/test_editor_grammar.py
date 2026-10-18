"""The VS Code grammar (``editors/vscode-candy``) knows every special form in the table."""

import json
import re
from pathlib import Path

from cdy_rt.table import SPECIAL_FORMS

GRAMMAR = (
    Path(__file__).resolve().parents[2]
    / "editors"
    / "vscode-candy"
    / "syntaxes"
    / "candy.tmLanguage.json"
)


def test_grammar_has_every_special_form() -> None:
    repo = json.loads(GRAMMAR.read_text(encoding="utf-8"))["repository"]
    patterns = [p.get("match", "") for p in repo["head"]["patterns"]]
    patterns += [p["match"] for p in repo["definition"]["patterns"]]
    patterns.append(repo["format"]["begin"])
    named = {
        name
        for pattern in patterns
        for group in re.findall(r"\(\?<=\\\(\)\(([^)]*)\)", pattern)
        for name in group.split("|")
    }
    assert set(SPECIAL_FORMS) <= named, set(SPECIAL_FORMS) - named
