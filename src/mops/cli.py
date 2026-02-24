"""Entry point for the `mops` CLI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from mops.config import RouteConfig, load_route_config
from mops.logs import aggregate, parse_jsonl_logs, parse_window

app = typer.Typer(help="Model Ops Control Plane tooling")
console = Console()


def render_report(route_cfg: Optional[RouteConfig], log_path: Path, window: str) -> None:
    since = datetime.now(timezone.utc) - parse_window(window)
    entries = parse_jsonl_logs(log_path, since=since)
    if not entries:
        console.print(f"[yellow]No log entries found in {log_path} for window {window}[/yellow]")
        return

    report = aggregate(entries)

    table = Table(title=f"Usage report — last {window}")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Reqs", justify="right")
    table.add_column("p95 latency (ms)", justify="right")
    table.add_column("Cost (USD)", justify="right")
    table.add_column("Error rate", justify="right")

    for metric in sorted(report.metrics, key=lambda m: m.total_cost, reverse=True):
        table.add_row(
            metric.provider,
            metric.model,
            str(metric.requests),
            f"{metric.p95_latency_ms:.0f}",
            f"{metric.total_cost:.2f}",
            f"{metric.error_rate * 100:.1f}%",
        )

    console.print(table)
    console.print(f"[bold]Total cost:[/] ${report.total_cost:.2f} — [bold]requests:[/] {report.total_requests}")

    if route_cfg:
        console.print("\n[blue]Active environment:[/]", route_cfg.environment)
        console.print(f"Routes defined: {len(route_cfg.routes)} | Guardrails: {len(route_cfg.guardrails)}")


@app.command()
def report(
    log_dir: Path = typer.Option(Path("logs"), help="Directory containing *.jsonl usage logs"),
    route: Optional[Path] = typer.Option(None, help="Path to route.yaml (optional)"),
    window: str = typer.Option("24h", help="Time window, e.g. 24h or 30m"),
) -> None:
    """Aggregate cost/latency metrics for recent traffic."""

    route_cfg = load_route_config(route) if route else None
    render_report(route_cfg, log_dir, window)


@app.command()
def check(
    config: Path = typer.Option(Path("configs/route.example.yaml"), help="Route config to validate"),
) -> None:
    """Validate config files (placeholder for future eval execution)."""

    load_route_config(config)
    console.print(f"[green]Config {config} is valid.[/green]")


if __name__ == "__main__":  # pragma: no cover
    app()
