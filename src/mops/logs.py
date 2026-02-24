"""Log ingestion and aggregation utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

import json


@dataclass
class LogEntry:
    timestamp: datetime
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    cost_usd: float
    status: str


@dataclass
class AggregatedMetric:
    provider: str
    model: str
    requests: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_cost: float = 0.0
    p95_latency_ms: float = 0.0
    error_rate: float = 0.0
    _latencies: List[float] = field(default_factory=list, repr=False)
    _errors: int = 0

    def finalize(self) -> None:
        if self._latencies:
            sorted_lat = sorted(self._latencies)
            index = int(0.95 * (len(sorted_lat) - 1))
            self.p95_latency_ms = sorted_lat[index]
        if self.requests:
            self.error_rate = self._errors / self.requests


@dataclass
class AggregatedReport:
    metrics: List[AggregatedMetric]
    total_cost: float
    total_requests: int


def parse_jsonl_logs(log_dir: Path, since: datetime | None = None) -> List[LogEntry]:
    entries: List[LogEntry] = []
    for path in sorted(log_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                payload = json.loads(line)
                ts = datetime.fromisoformat(payload["timestamp"]).astimezone(timezone.utc)
                if since and ts < since:
                    continue
                entries.append(
                    LogEntry(
                        timestamp=ts,
                        provider=payload["provider"],
                        model=payload["model"],
                        prompt_tokens=int(payload.get("prompt_tokens", 0)),
                        completion_tokens=int(payload.get("completion_tokens", 0)),
                        latency_ms=float(payload.get("latency_ms", 0.0)),
                        cost_usd=float(payload.get("cost_usd", 0.0)),
                        status=payload.get("status", "ok"),
                    )
                )
    return entries


def aggregate(entries: Iterable[LogEntry]) -> AggregatedReport:
    metrics: Dict[tuple[str, str], AggregatedMetric] = {}
    total_cost = 0.0
    total_requests = 0

    for entry in entries:
        key = (entry.provider, entry.model)
        if key not in metrics:
            metrics[key] = AggregatedMetric(provider=entry.provider, model=entry.model)
        metric = metrics[key]
        metric.requests += 1
        metric.total_prompt_tokens += entry.prompt_tokens
        metric.total_completion_tokens += entry.completion_tokens
        metric.total_cost += entry.cost_usd
        metric._latencies.append(entry.latency_ms)
        if entry.status != "ok":
            metric._errors += 1
        total_cost += entry.cost_usd
        total_requests += 1

    for metric in metrics.values():
        metric.finalize()

    return AggregatedReport(metrics=list(metrics.values()), total_cost=total_cost, total_requests=total_requests)


def parse_window(window: str) -> timedelta:
    if window.endswith("h"):
        hours = float(window[:-1])
        return timedelta(hours=hours)
    if window.endswith("m"):
        minutes = float(window[:-1])
        return timedelta(minutes=minutes)
    raise ValueError("Unsupported window format. Use '24h' or '30m'.")
