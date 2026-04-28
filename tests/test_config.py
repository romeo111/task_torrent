"""Tests for tasktorrent.config."""

from __future__ import annotations

from pathlib import Path

import pytest

from tasktorrent.config import (
    ConsumerConfigError,
    load_consumer_config,
    parse_consumer_config,
)


def test_parse_minimal_config() -> None:
    cfg = parse_consumer_config({"version": "v0.4", "consumer_name": "openonco"})
    assert cfg.version == "v0.4"
    assert cfg.consumer_name == "openonco"
    assert cfg.banned_sources == []
    assert cfg.active_cap.fixed == 10


def test_parse_full_config() -> None:
    raw = {
        "version": "v0.4",
        "consumer_name": "openonco",
        "banned_sources": ["SRC-ONCOKB", "SRC-SNOMED"],
        "active_cap": {
            "mode": "derived",
            "fixed": 8,
            "review_capacity_hours_per_week": 40,
            "avg_chunk_review_hours": 4,
        },
        "trust_tier_thresholds": {
            "T0_to_T1": {"merged_chunks": 5, "rejections_window_days": 60, "rejections_max": 1},
        },
        "trust_registry": {"honor": True, "min_consumer_count": 3},
        "volume_gates": {"bundle_size_mb": 3, "entity_count": 10000},
        "kb_root": "knowledge_base/hosted/content/",
    }
    cfg = parse_consumer_config(raw)
    assert cfg.banned_sources == ["SRC-ONCOKB", "SRC-SNOMED"]
    assert cfg.active_cap.mode == "derived"
    assert cfg.active_cap.resolve() == 10  # 40 / 4
    assert cfg.trust_tier_thresholds.merged_chunks == 5
    assert cfg.trust_registry.honor is True
    assert cfg.volume_gates.bundle_size_mb == 3
    assert cfg.kb_root == "knowledge_base/hosted/content/"


def test_active_cap_fixed_mode() -> None:
    cfg = parse_consumer_config(
        {"version": "v0.4", "consumer_name": "x", "active_cap": {"mode": "fixed", "fixed": 7}}
    )
    assert cfg.active_cap.resolve() == 7


def test_active_cap_int_shorthand() -> None:
    cfg = parse_consumer_config(
        {"version": "v0.4", "consumer_name": "x", "active_cap": 12}
    )
    assert cfg.active_cap.resolve() == 12


def test_missing_required_field() -> None:
    with pytest.raises(ConsumerConfigError):
        parse_consumer_config({"version": "v0.4"})  # no consumer_name
    with pytest.raises(ConsumerConfigError):
        parse_consumer_config({"consumer_name": "x"})  # no version


def test_load_from_disk(tmp_path: Path) -> None:
    (tmp_path / ".tasktorrent.yaml").write_text(
        "version: v0.4\nconsumer_name: testco\nbanned_sources: [SRC-X]\n",
        encoding="utf-8",
    )
    cfg = load_consumer_config(tmp_path)
    assert cfg.consumer_name == "testco"
    assert cfg.banned_sources == ["SRC-X"]


def test_load_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConsumerConfigError):
        load_consumer_config(tmp_path)


# --- Strict validation (per PR #19 owner review) ---

def test_invalid_active_cap_mode_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="active_cap.mode"):
        parse_consumer_config(
            {"version": "v0.4", "consumer_name": "x", "active_cap": {"mode": "bogus"}}
        )


def test_active_cap_derived_requires_both_inputs() -> None:
    with pytest.raises(ConsumerConfigError, match="derived"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "active_cap": {"mode": "derived", "review_capacity_hours_per_week": 40},
            }
        )


def test_active_cap_int_zero_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="positive"):
        parse_consumer_config(
            {"version": "v0.4", "consumer_name": "x", "active_cap": 0}
        )


def test_active_cap_negative_rejected() -> None:
    with pytest.raises(ConsumerConfigError):
        parse_consumer_config(
            {"version": "v0.4", "consumer_name": "x", "active_cap": -3}
        )


def test_active_cap_non_dict_non_int_rejected() -> None:
    with pytest.raises(ConsumerConfigError):
        parse_consumer_config(
            {"version": "v0.4", "consumer_name": "x", "active_cap": "ten"}
        )


def test_active_cap_fixed_zero_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="active_cap.fixed"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "active_cap": {"mode": "fixed", "fixed": 0},
            }
        )


def test_active_cap_avg_review_hours_negative_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="avg_chunk_review_hours"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "active_cap": {
                    "mode": "derived",
                    "review_capacity_hours_per_week": 40,
                    "avg_chunk_review_hours": -1,
                },
            }
        )


def test_trust_threshold_negative_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="merged_chunks"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "trust_tier_thresholds": {"T0_to_T1": {"merged_chunks": -1}},
            }
        )


def test_trust_window_zero_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="rejections_window_days"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "trust_tier_thresholds": {"T0_to_T1": {"rejections_window_days": 0}},
            }
        )


def test_volume_gate_zero_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="bundle_size_mb"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "volume_gates": {"bundle_size_mb": 0},
            }
        )


def test_volume_gate_negative_entity_count_rejected() -> None:
    with pytest.raises(ConsumerConfigError, match="entity_count"):
        parse_consumer_config(
            {
                "version": "v0.4",
                "consumer_name": "x",
                "volume_gates": {"entity_count": -100},
            }
        )
