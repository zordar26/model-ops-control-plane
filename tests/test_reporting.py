from datetime import datetime
from pathlib import Path

from mops.config import load_route_config
from mops.logs import AggregatedMetric, AggregatedReport
from mops.reporting import format_markdown_report


def test_markdown_export():
    route_cfg = load_route_config(Path(__file__).parent.parent / "configs" / "route.example.yaml")
    metric = AggregatedMetric(
        provider="openrouter",
        model="anthropic/claude",
        requests=2,
        total_prompt_tokens=100,
        total_completion_tokens=40,
        total_cost=1.23,
        p95_latency_ms=1800,
        error_count=0,
        success_count=2,
    )
    report = AggregatedReport(
        metrics=[metric],
        total_cost=1.23,
        total_requests=2,
        total_prompt_tokens=100,
        total_completion_tokens=40,
    )

    md = format_markdown_report(report, "24h", route_cfg, generated_at=datetime(2026, 2, 26))
    assert "Total requests: **2**" in md
    assert "anthropic/claude" in md
    assert "Environment: `dev`" in md
