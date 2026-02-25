"""Helper utilities for rendering reports."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from mops.config import RouteConfig
from mops.logs import AggregatedReport


def format_markdown_report(
    report: AggregatedReport,
    window: str,
    route_cfg: Optional[RouteConfig],
    generated_at: Optional[datetime] = None,
) -> str:
    generated_at = generated_at or datetime.utcnow()
    lines: list[str] = []
    lines.append(f"# Usage report — last {window}")
    lines.append("")
    lines.append(f"Generated at **{generated_at.isoformat(timespec='seconds')}Z**")
    if route_cfg:
        lines.append(
            "Environment: `{env}` | Routes: {routes} | Guardrails: {guards}".format(
                env=route_cfg.environment,
                routes=len(route_cfg.routes),
                guards=len(route_cfg.guardrails),
            )
        )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        "- Total requests: **{reqs}**".format(reqs=report.total_requests)
    )
    lines.append(
        "- Total tokens: **{tokens}** ({prompt} prompt / {completion} completion)".format(
            tokens=report.total_tokens,
            prompt=report.total_prompt_tokens,
            completion=report.total_completion_tokens,
        )
    )
    lines.append("- Total cost: **${cost:.2f}**".format(cost=report.total_cost))
    lines.append("")
    lines.append("## Providers")
    lines.append("")
    lines.append(
        "| Provider | Model | Requests | Success | Errors | p95 latency (ms) | Cost (USD) |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for metric in sorted(report.metrics, key=lambda m: m.total_cost, reverse=True):
        lines.append(
            "| {provider} | {model} | {reqs} | {ok} | {err} | {lat:.0f} | {cost:.2f} |".format(
                provider=metric.provider,
                model=metric.model,
                reqs=metric.requests,
                ok=metric.success_count,
                err=metric.error_count,
                lat=metric.p95_latency_ms,
                cost=metric.total_cost,
            )
        )

    return "\n".join(lines)


def write_markdown_report(path: Path, content: str) -> None:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
