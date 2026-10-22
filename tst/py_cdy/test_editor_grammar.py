"""The VS Code grammar (``editors/vscode-candy``) knows every special form in special.cdy."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECIAL = ROOT / "src" / "cdy" / "special.cdy"
GRAMMAR = ROOT / "editors" / "vscode-candy" / "syntaxes" / "candy.tmLanguage.json"


def test_grammar_has_every_special_form() -> None:
    repo = json.loads(GRAMMAR.read_text(encoding="utf-8"))["repository"]
    rules = [*repo["head"]["patterns"], *repo["definition"]["patterns"], repo["format"]]
    patterns = [rule.get("match", rule.get("begin", "")) for rule in rules]
    named = {
        name
        for pattern in patterns
        for group in re.findall(r"\(\?<=\\\(\)\(([^)]*)\)", pattern)
        for name in group.split("|")
    }
    special = set(
        re.findall(r"^\(special (\S+)\)", SPECIAL.read_text(encoding="utf-8"), re.MULTILINE)
    )
    assert special, SPECIAL
    assert special <= named, special - named
