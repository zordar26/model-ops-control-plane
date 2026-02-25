from pathlib import Path

from mops.logs import aggregate, parse_jsonl_logs


def test_aggregate_sample_logs(tmp_path: Path) -> None:
    sample = Path(__file__).parent.parent / "logs" / "sample_usage.jsonl"
    data = sample.read_text()
    target = tmp_path / "sample.jsonl"
    target.write_text(data)

    entries = parse_jsonl_logs(tmp_path)
    report = aggregate(entries)

    assert report.total_requests == 3
    assert report.total_prompt_tokens == 2600
    assert report.total_completion_tokens == 750
    assert len(report.metrics) == 2
    providers = {(m.provider, m.model): m for m in report.metrics}
    openrouter_metric = providers[("openrouter", "openrouter/anthropic/claude-3-sonnet")]
    assert openrouter_metric.requests == 2
    assert openrouter_metric.success_count == 2
    azure_metric = providers[("azure-openai", "gpt-4o-mini")]
    assert azure_metric.error_count == 1
