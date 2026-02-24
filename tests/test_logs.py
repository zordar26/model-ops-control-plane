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
    assert len(report.metrics) == 2
    providers = {(m.provider, m.model): m for m in report.metrics}
    assert providers[("openrouter", "openrouter/anthropic/claude-3-sonnet")].requests == 2
    assert providers[("azure-openai", "gpt-4o-mini")]._errors == 1
