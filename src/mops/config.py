"""Configuration models for the Model Ops control plane."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class Guardrail(BaseModel):
    name: str
    type: str = Field(description="ENUM: pii_scan | jailbreak_scan | custom")
    threshold: Optional[float] = None


class ProviderRoute(BaseModel):
    name: str
    provider: str
    model: str
    weight: float = 1.0
    max_latency_ms: Optional[int] = None
    cost_cap_usd: Optional[float] = None
    fallbacks: List[str] = Field(default_factory=list)


class RouteConfig(BaseModel):
    version: str = "1"
    environment: str = "dev"
    comment: Optional[str] = None
    routes: List[ProviderRoute]
    guardrails: List[Guardrail] = Field(default_factory=list)


def load_route_config(path: Path) -> RouteConfig:
    """Load and validate a route config YAML file."""

    expanded = path.expanduser().resolve()
    if not expanded.exists():
        raise FileNotFoundError(f"Route config not found: {expanded}")

    with expanded.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    return RouteConfig.model_validate(data)
