from pathlib import Path

from mops.evals import load_eval_config


def test_load_eval_config(tmp_path: Path) -> None:
    source = Path(__file__).parent.parent / "configs" / "evals.example.yaml"
    data = source.read_text()
    target = tmp_path / "evals.yaml"
    target.write_text(data)

    cfg = load_eval_config(target)

    assert len(cfg.suites) == 2
    assert cfg.suites[0].tests[0].metric == "rougeL"
