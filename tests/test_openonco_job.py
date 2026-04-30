"""Tests for the OpenOnco CI/landing integration job wiring."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

from tasktorrent.lint_chunk_spec import find_chunk_specs, lint_chunk_spec, main as lint_main


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_landing_builder():
    script = REPO_ROOT / "scripts" / "build_landing_data.py"
    spec = importlib.util.spec_from_file_location("build_landing_data", script)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _openonco_consumer() -> dict:
    cfg = yaml.safe_load((REPO_ROOT / "consumers.yaml").read_text(encoding="utf-8"))
    consumers = cfg["consumers"]
    matches = [consumer for consumer in consumers if consumer["name"] == "openonco"]
    assert len(matches) == 1
    return matches[0]


def test_openonco_lint_job_command_is_clean() -> None:
    chunks_dir = REPO_ROOT / "chunks" / "openonco"

    assert lint_main(["--all", str(chunks_dir), "--quiet"]) == 0

    specs = find_chunk_specs([chunks_dir])
    assert len(specs) >= 30
    assert all(spec.name.lower() not in {"readme.md", "index.md", "_example.md"} for spec in specs)
    assert all(lint_chunk_spec(spec).passed for spec in specs)


def test_openonco_consumer_points_to_local_chunk_shelf() -> None:
    consumer = _openonco_consumer()

    assert consumer["repo"] == "romeo111/OpenOnco"
    assert consumer["chunks_path"] == "chunks/openonco/"

    chunks_dir = REPO_ROOT / consumer["chunks_path"]
    specs = find_chunk_specs([chunks_dir])
    assert len(specs) >= 30


def test_openonco_landing_token_estimate_uses_chunk_specs() -> None:
    builder = _load_landing_builder()
    consumer = _openonco_consumer()

    stats = builder.ConsumerStats(
        name=consumer["name"],
        display_name=consumer["display_name"],
        repo=consumer["repo"],
    )

    estimate = builder.estimate_tokens_for_consumer(consumer, stats)

    assert estimate >= 3_000_000
    assert estimate % builder.TOKENS_PER_DROP == 0
