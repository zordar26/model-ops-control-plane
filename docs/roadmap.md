# Roadmap

## Milestone 0 — Seed the control plane (Week 1)
- [ ] Repository scaffolding, devcontainer, and lint/test harness
- [ ] CLI skeleton (`mops`) with config loader + command routing
- [ ] Define `route.yaml` schema covering:
  - Providers (openrouter, together, azure, self_hosted)
  - Traffic weights, latency budgets, fallback chains
  - Pre/post-processing hooks (prompt filters, PII scrubbers)
- [ ] Write golden evaluation spec (`evals/*.yaml`) for regression tests

## Milestone 1 — Visibility & telemetry (Weeks 2-3)
- [ ] Log ingestor that accepts JSONL traces (requests + responses)
- [ ] Cost + latency calculators per provider/model
- [ ] Exporters for CSV and OpenMetrics (Prometheus/Grafana)
- [ ] CLI command `mops report --window 24h` that prints spend, p95 latency, error spikes

## Milestone 2 — Governance flows (Weeks 3-4)
- [ ] Policy engine that declares required eval suites per environment
- [ ] "Safe deploy" command: run evals, surface regressions, require approval
- [ ] Artifact store for prompt bundles + agent graphs with semantic diffing
- [ ] Slack/Teams webhooks for approval + alert handoffs

## Milestone 3 — Managed rollouts (Weeks 4-6)
- [ ] Progressive rollout support (percentage-based/segment-based)
- [ ] Automated rollback on quality or cost regressions
- [ ] CRUD API so other tools (e.g., internal portals) can manage routes
- [ ] Terraform provider / Pulumi component for GitOps integration

## Stretch — Marketplace integrations
- [ ] Native OpenRouter + Together connectors (streaming, cost hints)
- [ ] Support for custom inference gateways (vLLM, LM Studio, Ollama)
- [ ] Partner dashboard (multi-tenant view for consultancies running fleets)

---

**Operating principles**
1. Every change is evaluated before production.
2. Costs are visible in near real-time.
3. Guardrails are declarative and enforced automatically.

Contributions start with a short spec in `docs/rfcs/` (to be created).