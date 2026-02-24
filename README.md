# Model Ops Control Plane

A control plane for AI platform teams who operate multiple LLMs, agents, and inference providers. The goal is to replace brittle scripts and spreadsheets with a unified system for routing, evaluation, governance, and cost management.

## Why it exists

Teams are stitching together OpenRouter/Together, self-hosted LLMs, and bespoke agents. They lack:

- Version control for prompts and agent graphs
- Automated regression/evaluation signals before shipping changes
- Centralized cost, latency, and error visibility across providers
- Guardrails for privacy, compliance, and rollout approvals

## Product pillars

1. **Routing & orchestration** – plug in OpenRouter, Anthropic, Azure, local models, or custom agents. Express priority lists, failovers, and traffic shifting rules declaratively.
2. **Evaluation & quality gates** – attach golden datasets, human review tasks, and policy/PII scans that must pass before deploys.
3. **Observability & spend** – per-agent dashboards for cost, latency, error spikes, with anomaly alerts and budget caps.
4. **Governance & rollout** – approval workflows, environment promotion (dev → staging → prod), and instant rollback with full audit history.

## Initial focus

- Command-line prototype that ingests request/response logs and produces spend + latency snapshots
- YAML spec for defining model routes and evaluation steps
- CI workflow that runs offline eval suites whenever prompts or routes change

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mops report --log-dir logs --window 24h  # uses sample data
```

(CLI currently supports `report` + `check`; more subcommands coming next.)

## Roadmap snapshot

- [ ] Define the spec for `route.yaml` (models, weights, fallbacks)
- [ ] Build log ingestor + cost tracker (OpenRouter + Anthropic to start)
- [ ] Ship guardrail hooks (PII scrub, jailbreak classifier)
- [ ] Publish reference dashboards + Grafana export
- [ ] Launch GitHub Pages microsite + lightweight web UI for telemetry/approvals

See `docs/roadmap.md` and `docs/rfcs/0001-mvp.md` for more detail.
