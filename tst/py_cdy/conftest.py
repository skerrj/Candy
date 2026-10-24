"""The translators the tests share, built once per session: T1 (the Candy translator, built
by the checked-in one) and T2 (T1's translation of the translator), for
``test_self_host.py`` and ``test_spec.py``."""

from pathlib import Path
from types import ModuleType

import pytest

from self_host import build_t1, build_with, load


@pytest.fixture(name="t1_path", scope="session")
def fixture_t1_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """T1, built once for the session."""
    return build_t1(tmp_path_factory.mktemp("t1"))


@pytest.fixture(name="t1", scope="session")
def fixture_t1(t1_path: Path) -> ModuleType:
    """T1, loaded."""
    return load(t1_path)


@pytest.fixture(name="t2", scope="session")
def fixture_t2(t1_path: Path, tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    """T2 (T1's translation of the translator) written to a file, and its source text."""
    path = build_with(t1_path, tmp_path_factory.mktemp("t2"))
    return path, path.read_text(encoding="utf-8")
