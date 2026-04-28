"""Tests for tasktorrent.init scaffold."""

from __future__ import annotations

from pathlib import Path

import pytest

from tasktorrent.init import init


def test_init_creates_expected_files(tmp_path: Path) -> None:
    results = init("openonco", tmp_path)

    assert (tmp_path / ".tasktorrent.yaml").exists()
    assert (tmp_path / "TASKTORRENT_ONBOARDING.md").exists()
    assert (tmp_path / "contributions" / ".gitkeep").exists()
    chunk_files = list((tmp_path / "chunks").glob("example-chunk-*.md"))
    assert len(chunk_files) == 1

    assert all(status == "created" for status in results.values())


def test_init_consumer_name_substituted(tmp_path: Path) -> None:
    init("foobar", tmp_path)
    cfg = (tmp_path / ".tasktorrent.yaml").read_text(encoding="utf-8")
    assert "consumer_name: foobar" in cfg
    assert "{{CONSUMER_NAME}}" not in cfg


def test_init_idempotent_skips_existing(tmp_path: Path) -> None:
    init("openonco", tmp_path)
    results = init("openonco", tmp_path)
    assert all(status == "skipped" for status in results.values())


def test_init_force_overwrites(tmp_path: Path) -> None:
    init("openonco", tmp_path)
    results = init("openonco", tmp_path, force=True)
    # All except .gitkeep (which is an empty file always treated as overwrite)
    assert any(status == "overwritten" for status in results.values())


def test_init_rejects_nonexistent_root() -> None:
    with pytest.raises(FileNotFoundError):
        init("openonco", Path("/definitely/does/not/exist/zzz"))


def test_init_rejects_bad_consumer_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        init("Bad Name", tmp_path)
    with pytest.raises(ValueError):
        init("UPPERCASE", tmp_path)
    with pytest.raises(ValueError):
        init("", tmp_path)


def test_init_example_chunk_passes_lint(tmp_path: Path) -> None:
    """The scaffold's example chunk must itself pass the linter."""
    from tasktorrent.lint_chunk_spec import lint_chunk_spec

    init("openonco", tmp_path)
    chunk_path = next((tmp_path / "chunks").glob("example-chunk-*.md"))
    result = lint_chunk_spec(chunk_path)
    assert result.passed, f"scaffold example chunk failed lint: {[f.message for f in result.errors]}"
