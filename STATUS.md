# STATUS — 2026-02-26

## Current state
- Repo `model-ops-control-plane` live on GitHub (main branch clean as of `c7b26d5`).
- Branch `feat/telemetry-ci` adds telemetry/report upgrades, eval config validation, Markdown export, and CI workflow (pending review/merge).
- CLI now supports Markdown export and richer metrics; `mops check` validates route + eval configs.
- GitHub Actions pipeline (`ci.yaml`) runs lint + pytest on push/PR.

## Next steps
1. Review and merge `feat/telemetry-ci` into `main` once approved.
2. Start GitHub Pages microsite + lightweight UI scaffold (per roadmap).
3. Extend eval command to actually run suites (currently validation-only).
4. Layer on additional telemetry sources (streaming logs, provider APIs) once base is merged.

## Notes
- Virtualenv `.venv` already set up locally; reinstall with `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- `reports/` directory gets auto-created when using `--output` flag.
- See `docs/rfcs/0001-mvp.md` for updated requirements (Markdown export added).
