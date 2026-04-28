"""TaskTorrent consumer-side config — `.tasktorrent.yaml` schema + loader.

Each consumer repo (OpenOnco, future social-good projects) declares its
TaskTorrent integration parameters in `.tasktorrent.yaml` at the repo root.
This file is the contract between task_torrent rules and the consumer's
custom policies (banned sources, active cap, trust thresholds, etc.).

Usage:
  from tasktorrent.config import load_consumer_config
  cfg = load_consumer_config(Path("/path/to/consumer/repo"))
  print(cfg.version, cfg.banned_sources)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


CONFIG_FILENAME = ".tasktorrent.yaml"


@dataclass
class TrustTierThresholds:
    merged_chunks: int = 3
    rejections_window_days: int = 90
    rejections_max: int = 0


@dataclass
class TrustRegistry:
    honor: bool = False
    min_consumer_count: int = 2


@dataclass
class ActiveCap:
    mode: str = "fixed"  # "fixed" | "derived"
    fixed: int = 10
    review_capacity_hours_per_week: int | None = None
    avg_chunk_review_hours: float | None = None

    def resolve(self) -> int:
        if self.mode == "fixed":
            return self.fixed
        if (
            self.review_capacity_hours_per_week is not None
            and self.avg_chunk_review_hours
            and self.avg_chunk_review_hours > 0
        ):
            return max(
                1,
                int(self.review_capacity_hours_per_week / self.avg_chunk_review_hours),
            )
        return self.fixed


@dataclass
class VolumeGates:
    bundle_size_mb: float | None = None
    entity_count: int | None = None


@dataclass
class ConsumerConfig:
    version: str
    consumer_name: str
    banned_sources: list[str] = field(default_factory=list)
    active_cap: ActiveCap = field(default_factory=ActiveCap)
    trust_tier_thresholds: TrustTierThresholds = field(default_factory=TrustTierThresholds)
    trust_registry: TrustRegistry = field(default_factory=TrustRegistry)
    volume_gates: VolumeGates = field(default_factory=VolumeGates)
    kb_root: str | None = None
    contributions_root: str = "contributions/"
    chunks_root: str = "chunks/"


class ConsumerConfigError(ValueError):
    pass


def load_consumer_config(repo_root: Path) -> ConsumerConfig:
    """Load and validate `.tasktorrent.yaml` from a consumer repo."""
    cfg_path = Path(repo_root) / CONFIG_FILENAME
    if not cfg_path.is_file():
        raise ConsumerConfigError(
            f"no {CONFIG_FILENAME} at {repo_root}; run `tasktorrent init` to scaffold one"
        )

    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ConsumerConfigError(f"{cfg_path} did not parse to a mapping")

    return parse_consumer_config(raw)


def parse_consumer_config(raw: dict) -> ConsumerConfig:
    for required in ("version", "consumer_name"):
        if required not in raw:
            raise ConsumerConfigError(f"missing required field `{required}`")

    ac_raw = raw.get("active_cap", {}) or {}
    if isinstance(ac_raw, int):
        active_cap = ActiveCap(mode="fixed", fixed=ac_raw)
    else:
        active_cap = ActiveCap(
            mode=ac_raw.get("mode", "fixed"),
            fixed=int(ac_raw.get("fixed", 10)),
            review_capacity_hours_per_week=ac_raw.get("review_capacity_hours_per_week"),
            avg_chunk_review_hours=ac_raw.get("avg_chunk_review_hours"),
        )

    tt_raw = raw.get("trust_tier_thresholds", {}) or {}
    t0_to_t1 = tt_raw.get("T0_to_T1", {}) or {}
    trust_thresholds = TrustTierThresholds(
        merged_chunks=int(t0_to_t1.get("merged_chunks", 3)),
        rejections_window_days=int(t0_to_t1.get("rejections_window_days", 90)),
        rejections_max=int(t0_to_t1.get("rejections_max", 0)),
    )

    tr_raw = raw.get("trust_registry", {}) or {}
    trust_registry = TrustRegistry(
        honor=bool(tr_raw.get("honor", False)),
        min_consumer_count=int(tr_raw.get("min_consumer_count", 2)),
    )

    vg_raw = raw.get("volume_gates", {}) or {}
    volume_gates = VolumeGates(
        bundle_size_mb=vg_raw.get("bundle_size_mb"),
        entity_count=vg_raw.get("entity_count"),
    )

    return ConsumerConfig(
        version=str(raw["version"]),
        consumer_name=str(raw["consumer_name"]),
        banned_sources=list(raw.get("banned_sources", [])),
        active_cap=active_cap,
        trust_tier_thresholds=trust_thresholds,
        trust_registry=trust_registry,
        volume_gates=volume_gates,
        kb_root=raw.get("kb_root"),
        contributions_root=raw.get("contributions_root", "contributions/"),
        chunks_root=raw.get("chunks_root", "chunks/"),
    )
