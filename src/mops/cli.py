"""Entry point for the `mops` CLI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from mops.config import load_route_config
from mops.evals import load_eval_config
from mops.logs import aggregate, parse_jsonl_logs, parse_window
from mops.reporting import format_markdown_report, write_markdown_report

app = typer.Typer(help="Model Ops Control Plane tooling")
console = Console()


def _collect_report(log_path: Path, window: str):
    since = datetime.now(timezone.utc) - parse_window(window)
    entries = parse_jsonl_logs(log_path, since=since)
    if not entries:
        console.print(f"[yellow]No log entries found in {log_path} for window {window}[/yellow]")
        return None
    return aggregate(entries)


def _render_table(report, window: str) -> None:
    table = Table(title=f"Usage report — last {window}")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Reqs", justify="right")
    table.add_column("Success", justify="right")
    table.add_column("Errors", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("p95 latency (ms)", justify="right")
    table.add_column("Cost (USD)", justify="right")

    for metric in sorted(report.metrics, key=lambda m: m.total_cost, reverse=True):
        table.add_row(
            metric.provider,
            metric.model,
            str(metric.requests),
            str(metric.success_count),
            str(metric.error_count),
            str(metric.total_tokens),
            f"{metric.p95_latency_ms:.0f}",
            f"{metric.total_cost:.2f}",
        )

    console.print(table)
    totals_template = (
        "[bold]Total cost:[/] ${cost:.2f} — [bold]requests:[/] {reqs} — "
        "[bold]tokens:[/] {tokens}"
    )
    console.print(
        totals_template.format(
            cost=report.total_cost,
            reqs=report.total_requests,
            tokens=report.total_tokens,
        )
    )


@app.command()
def report(
    log_dir: Path = typer.Option(Path("logs"), help="Directory containing *.jsonl usage logs"),
    route: Optional[Path] = typer.Option(None, help="Path to route.yaml (optional)"),
    window: str = typer.Option("24h", help="Time window, e.g. 24h or 30m"),
    output: Optional[Path] = typer.Option(None, help="Optional path to write a Markdown report"),
) -> None:
    """Aggregate cost/latency metrics for recent traffic."""

    route_cfg = load_route_config(route) if route else None
    report_data = _collect_report(log_dir, window)
    if not report_data:
        return

    _render_table(report_data, window)

    if route_cfg:
        console.print("\n[blue]Active environment:[/]", route_cfg.environment)
        console.print(
            "Routes defined: {routes} | Guardrails: {guards}".format(
                routes=len(route_cfg.routes),
                guards=len(route_cfg.guardrails),
            )
        )

    if output:
        markdown = format_markdown_report(report_data, window, route_cfg)
        write_markdown_report(output, markdown)
        console.print(f"[green]Markdown report written to {output}[/green]")


@app.command()
def check(
    route: Path = typer.Option(Path("configs/route.example.yaml"), help="Route config to validate"),
    evals: Optional[Path] = typer.Option(None, help="Eval config to validate"),
) -> None:
    """Validate config + eval definitions."""

    route_cfg = load_route_config(route)
    console.print(
        "[green]Route config valid:[/] {env} ({routes} routes, {guards} guardrails)".format(
            env=route_cfg.environment,
            routes=len(route_cfg.routes),
            guards=len(route_cfg.guardrails),
        )
    )

    if evals:
        eval_cfg = load_eval_config(evals)
        total_tests = sum(len(suite.tests) for suite in eval_cfg.suites)
        console.print(
            "[green]Eval config valid:[/] {suites} suites / {tests} tests".format(
                suites=len(eval_cfg.suites),
                tests=total_tests,
            )
        )
    else:
        console.print("[yellow]No eval config provided; skipping eval validation.[/yellow]")


if __name__ == "__main__":  # pragma: no cover
    app()
