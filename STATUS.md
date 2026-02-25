# STATUS — 2026-02-26

## Current state
- Repo `model-ops-control-plane` live on GitHub (main branch clean).
- MVP scaffold merged: CLI (`mops`), sample config/logs, RFC, tests.
- Roadmap includes GitHub Pages + lightweight UI deliverable.
- Outstanding work (in progress but not committed):
  1. Telemetry/report upgrades (`mops report`): token counts, success/error breakdown, provider ranking, Markdown export.
  2. Eval config stub (`configs/evals.example.yaml`) plus `mops check` extensions.
  3. CI workflow (lint + pytest) via GitHub Actions.

## Next steps for whoever picks this up
1. Create/continue branch (e.g., `feat/telemetry-reports`).
2. Implement the telemetry/report enhancements and add regression tests.
3. Introduce eval config sample + validations wired into `mops check`.
4. Add `.github/workflows/ci.yaml` running `pip install -r requirements.txt`, `ruff`, and `pytest`.
5. Update README/RFC with new features + CI badge, then open PR / merge.

## Notes
- Virtualenv `.venv` already set up locally; reinstall with `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Use `logs/sample_usage.jsonl` for quick report testing; expand with more cases as needed.
- Remember to update memory files after major actions, and log independent decisions per SOUL.md guidance.
