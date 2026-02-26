# STATUS — 2026-02-26

## Current state
- Repo `model-ops-control-plane` live on GitHub (`main@12b102f`).
- CLI: telemetry upgrades + eval validation + CI ✅
- Public site: branch `feat/ui-pages` adds Vite-based landing page, telemetry snapshot, and Pages deploy workflow (awaiting merge / first deploy).

## Completed this round
1. `site/` scaffolded with Vite (`npm install`, `npm run build`).
2. Landing page mirrors product pillars + roadmap + telemetry table backed by `src/data/sample-report.json`.
3. `.github/workflows/pages.yml` builds and deploys the site via GitHub Pages.
4. README now links to the live demo; STATUS updated.

## Next steps
- Merge `feat/ui-pages`, ensure Pages deploy succeeds, and verify public URL.
- Replace sample telemetry JSON with automated export from `mops report` (cron or workflow artifact).
- Begin wiring eval execution + guardrails as the next CLI milestone.

## Notes
- Run the site locally with `cd site && npm install && npm run dev`.
- GitHub Pages workflow expects repository Pages settings to use `GitHub Actions`. After first successful run, the URL will resolve at `https://zordar26.github.io/model-ops-control-plane/`.
