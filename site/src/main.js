import sampleReport from "./data/sample-report.json";

const PILLARS = [
  {
    title: "Routing & orchestration",
    body:
      "Plug in OpenRouter, Anthropic, Azure, or self-hosted models. Define weights, priorities, and failovers as declarative infrastructure.",
  },
  {
    title: "Evaluation & quality gates",
    body:
      "Attach golden datasets, human review hooks, and policy scans so every prompt or agent update ships with evidence.",
  },
  {
    title: "Observability & spend",
    body:
      "Track cost, latency, and error spikes per provider/agent. Trigger alerts when budgets or SLAs drift.",
  },
  {
    title: "Governance & rollout",
    body:
      "Promote configs from dev → prod with approvals, audit history, and instant rollback when metrics regress.",
  },
];

const ROADMAP = [
  "GitHub Pages microsite + telemetry snapshot",
  "Live eval execution + guardrail hooks",
  "Dashboards & Grafana export",
  "Progressive rollout + rollback automation",
];

async function loadTelemetry() {
  try {
    const resp = await fetch("./sample-report.json", { cache: "no-store" });
    if (resp.ok) {
      return resp.json();
    }
  } catch (error) {
    console.warn("Falling back to bundled sample report", error);
  }
  return sampleReport;
}

function renderProvidersTable(providers) {
  return `
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Provider</th>
            <th>Model</th>
            <th>Requests</th>
            <th>Success</th>
            <th>Errors</th>
            <th>p95 latency</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          ${providers
            .map(
              (row) => `
                <tr>
                  <td>${row.provider}</td>
                  <td>${row.model}</td>
                  <td>${row.requests}</td>
                  <td>${row.success}</td>
                  <td>${row.errors}</td>
                  <td>${row.p95LatencyMs} ms</td>
                  <td>$${row.cost.toFixed(2)}</td>
                </tr>
              `
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderPillars() {
  return `
    <div class="pillar-grid">
      ${PILLARS.map(
        (pillar) => `
          <article class="pillar-card">
            <h3>${pillar.title}</h3>
            <p>${pillar.body}</p>
          </article>
        `
      ).join("")}
    </div>
  `;
}

function renderRoadmap() {
  return `
    <ol class="roadmap-list">
      ${ROADMAP.map((item) => `<li>${item}</li>`).join("")}
    </ol>
  `;
}

function formatSummary(summary) {
  return `
    <ul>
      <li><strong>${summary.requests}</strong> requests</li>
      <li><strong>${summary.tokens}</strong> tokens (${summary.promptTokens} prompt / ${summary.completionTokens} completion)</li>
      <li><strong>$${summary.cost.toFixed(2)}</strong> total cost</li>
    </ul>
  `;
}

async function bootstrap() {
  const app = document.getElementById("app");
  const telemetry = await loadTelemetry();

  app.innerHTML = `
    <header>
      <p class="eyebrow">Telemetry + governance for multi-model teams</p>
      <h1 class="hero-title">Model Ops Control Plane</h1>
      <p class="hero-subtitle">
        Replace brittle scripts with one opinionated workflow for routing, evals, observability, and rollout approvals.
      </p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="https://github.com/zordar26/model-ops-control-plane" target="_blank" rel="noreferrer">
          View repository
        </a>
        <a class="btn btn-secondary" href="https://zordar26.github.io/model-ops-control-plane" target="_blank" rel="noreferrer">
          Live demo
        </a>
      </div>
    </header>

    <section>
      <h2>Product pillars</h2>
      ${renderPillars()}
    </section>

    <section>
      <h2>Roadmap snapshot</h2>
      ${renderRoadmap()}
    </section>

    <section>
      <h2>Latest telemetry snapshot</h2>
      <p class="generated-time">Generated at ${new Date(telemetry.generatedAt).toLocaleString()}</p>
      ${formatSummary(telemetry.summary)}
      ${renderProvidersTable(telemetry.providers)}
    </section>
  `;
}

bootstrap();
