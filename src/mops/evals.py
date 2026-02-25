"""Evaluation config models."""

from __future__ import annotations

from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, Field


class EvalTest(BaseModel):
    name: str
    dataset: str = Field(description="Path or identifier for the evaluation dataset")
    metric: str = Field(description="Name of the metric, e.g., rougeL, accuracy")
    threshold: float = Field(description="Minimum acceptable score before deploy")


class EvalSuite(BaseModel):
    name: str
    tests: List[EvalTest]
    owner: str


class EvalConfig(BaseModel):
    suites: List[EvalSuite]


def load_eval_config(path: Path) -> EvalConfig:
    expanded = path.expanduser().resolve()
    if not expanded.exists():
        raise FileNotFoundError(f"Eval config not found: {expanded}")

    with expanded.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    return EvalConfig.model_validate(data)
