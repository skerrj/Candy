"""Tests for the bootstrap chain (``script/bootstrap.py``, ``doc/hl_rqmt/bootstrap.md``)."""

import subprocess
import sys

import pytest

import bootstrap


def test_steps_start_at_self_host_py() -> None:
    steps = bootstrap.found_steps()
    assert steps[0].label == bootstrap.FIRST
    assert len(steps) > 1


def test_staging_names_steps() -> None:
    found = {step.commit for step in bootstrap.found_steps()}
    assert set(bootstrap.STAGING) <= found
    for staging in bootstrap.STAGING.values():
        assert staging.split()[0] in ("joined", "old-runtime")


def test_tags_cover_the_steps() -> None:
    tagged = bootstrap.tagged_steps()
    if not tagged:
        pytest.skip("no boot/NN tags yet")
    found = bootstrap.found_steps()
    assert [step.label for step in tagged] == [f"boot/{n:02}" for n in range(len(tagged))]
    assert [step.commit for step in tagged] == [step.commit for step in found[: len(tagged)]]
    # Only the newest step may be untagged (it is tagged after it is committed).
    assert len(found) - len(tagged) <= 1
    for step in tagged:
        staging = " ".join(bootstrap.staging_of(step))
        assert staging == bootstrap.STAGING.get(step.commit, "")


@pytest.mark.bootstrap
def test_every_step_rebuilds_its_bin() -> None:
    done = subprocess.run(
        (sys.executable, str(bootstrap.ROOT / "script" / "bootstrap.py"), "--check"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
