// TaskTorrent landing — fetches metrics.json + chunks.json, renders KPIs +
// per-consumer breakdown + claimable-chunks table + paste-and-go prompt.
//
// Pure vanilla JS, no build step. metrics.json + chunks.json are written
// to landing/ by scripts/build_landing_data.py (cron + dispatch).

const PROMPT_TEMPLATE = `You are a TaskTorrent contributor agent. Your goal is to do one chunk of structured AI work and submit it as a PR for {{PROJECT_DISPLAY}}.

1. Read https://github.com/{{REPO}}/blob/master/docs/contributing/CONTRIBUTOR_QUICKSTART.md (full workflow).
2. Run scripts/tasktorrent/bootstrap_contributor.sh — it tells you the next available chunk.
3. Read the chunk spec at the printed URL. Confirm you can complete it within the Drop estimate. If not, exit.
4. Run scripts/tasktorrent/auto_claim.sh <chunk-id> --issue <#> --method <method>.
5. Do the work on branch tasktorrent/<chunk-id>, only under contributions/<chunk-id>/. Every sidecar's _contribution_meta.yaml must declare ai_tool + ai_model.
6. Run python -m scripts.tasktorrent.validate_contributions <chunk-id> until it passes.
7. Run scripts/tasktorrent/auto_pr.sh <chunk-id> --issue <#> to open the PR.
8. STOP after PR is opened. Do not push to master, do not create chunks, do not delete branches.`;

const GENERIC_PROMPT = PROMPT_TEMPLATE
  .replace("{{PROJECT_DISPLAY}}", "the project below")
  .replace("{{REPO}}", "<owner>/<consumer-repo>");

let metricsCache = null;
let chunksCache = null;

// ---------- Number formatting ----------

function fmtCount(n) {
  if (n == null) return "—";
  return n.toLocaleString("en-US");
}

function fmtTokens(n) {
  if (n == null || n === 0) return "0";
  if (n >= 1e9) return (n / 1e9).toFixed(1) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(1) + "k";
  return String(n);
}

function fmtRelative(iso) {
  if (!iso) return "never";
  const t = new Date(iso).getTime();
  const now = Date.now();
  const diff = (now - t) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
  if (diff < 86400 * 30) return Math.floor(diff / 86400) + "d ago";
  return new Date(iso).toISOString().slice(0, 10);
}

// ---------- KPI render ----------

function renderKPIs(metrics) {
  const t = metrics.totals || {};
  document.getElementById("kpi-completed").textContent = fmtCount(t.chunks_completed);

  // Tokens metric: prefer actual when present, else estimated × completed-fraction proxy
  // For v1 we show estimated total (drops × 100k of all completed chunks).
  // We don't currently store completed-only token sum, so show actual + a hint to estimated.
  const tokensActual = t.tokens_actual || 0;
  const tokensEst = t.tokens_estimated || 0;
  // If contributors aren't filling cost_actual yet, actual will be 0. Show estimated as fallback.
  const display = tokensActual > 0 ? tokensActual : tokensEst;
  const label = tokensActual > 0 ? "" : " (est.)";
  document.getElementById("kpi-tokens").textContent = fmtTokens(display) + label;

  document.getElementById("kpi-claimable").textContent = fmtCount(t.chunks_claimable);
  document.getElementById("kpi-projects").textContent = fmtCount((metrics.per_consumer || []).length);

  document.getElementById("last-updated").textContent = fmtRelative(metrics.last_updated);

  document.getElementById("version-badge").textContent =
    `v0.4 · updated ${fmtRelative(metrics.last_updated)}`;
}

function renderPerConsumer(metrics) {
  const root = document.getElementById("per-consumer");
  root.innerHTML = "";
  for (const c of metrics.per_consumer || []) {
    const div = document.createElement("div");
    div.className = "bg-white border border-slate-200 rounded-lg p-5";
    div.innerHTML = `
      <div class="flex justify-between items-start mb-2">
        <div>
          <div class="font-semibold text-lg">${escapeHtml(c.display_name)}</div>
          <a href="https://github.com/${escapeHtml(c.repo)}" target="_blank" rel="noopener" class="text-xs text-slate-500 hover:text-slate-700">github.com/${escapeHtml(c.repo)} →</a>
        </div>
        <div class="text-right text-xs text-slate-500">
          ${c.contribute_url ? `<a href="${escapeHtml(c.contribute_url)}" target="_blank" rel="noopener" class="underline hover:text-slate-700">/contribute →</a>` : ""}
        </div>
      </div>
      <p class="text-sm text-slate-600 mb-3">${escapeHtml(c.description || "")}</p>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3 text-sm">
        <div><div class="font-mono text-lg">${fmtCount(c.chunks_completed)}</div><div class="text-xs text-slate-500">completed</div></div>
        <div><div class="font-mono text-lg">${fmtCount(c.chunks_active)}</div><div class="text-xs text-slate-500">active</div></div>
        <div><div class="font-mono text-lg">${fmtCount(c.chunks_claimable)}</div><div class="text-xs text-slate-500">claimable</div></div>
        <div><div class="font-mono text-lg">${fmtTokens(c.tokens_actual || c.tokens_estimated)}</div><div class="text-xs text-slate-500">tokens</div></div>
        <div><div class="font-mono text-lg">${fmtCount(c.contributors_unique)}</div><div class="text-xs text-slate-500">contributors</div></div>
      </div>
    `;
    root.appendChild(div);
  }
}

// ---------- Chunks table ----------

function renderChunks() {
  const tbody = document.getElementById("chunks-tbody");
  if (!chunksCache) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">No data.</td></tr>`;
    return;
  }
  const filterConsumer = document.getElementById("filter-consumer").value;
  const filterQueue = document.getElementById("filter-queue").value;

  const rows = (chunksCache.claimable || []).filter(c => {
    if (filterConsumer && c.consumer !== filterConsumer) return false;
    if (filterQueue && c.queue !== filterQueue) return false;
    return true;
  });

  if (rows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">No claimable chunks match these filters.</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map(c => `
    <tr class="border-t border-slate-100 hover:bg-slate-50">
      <td class="px-3 py-2">${escapeHtml(c.consumer_display || c.consumer)}</td>
      <td class="px-3 py-2">
        <div class="font-mono text-xs text-slate-700">${escapeHtml(c.chunk_id || "")}</div>
        <div class="text-xs text-slate-500">${escapeHtml(c.title || "")}</div>
      </td>
      <td class="px-3 py-2 text-center severity-${escapeAttr((c.severity || '').toLowerCase())}">
        ${escapeHtml(c.severity || "—")}
      </td>
      <td class="px-3 py-2 text-center">${escapeHtml(c.min_tier || "—")}</td>
      <td class="px-3 py-2 text-center">
        ${c.queue ? `<span class="queue-${escapeAttr(c.queue)} text-xs font-bold px-2 py-1 rounded">${escapeHtml(c.queue)}</span>` : "—"}
      </td>
      <td class="px-3 py-2 text-right font-mono">${c.drops != null ? c.drops.toFixed(1) : "—"}</td>
      <td class="px-3 py-2 text-xs">${escapeHtml(c.claim_method || "—")}</td>
      <td class="px-3 py-2">
        ${c.issue_url ? `<a href="${escapeHtml(c.issue_url)}" target="_blank" rel="noopener" class="text-emerald-700 hover:underline">#${c.issue_number} →</a>` : "—"}
      </td>
    </tr>
  `).join("");
}

// ---------- Install prompt ----------

function renderPrompt() {
  const sel = document.getElementById("install-project");
  const choice = sel.value;
  let promptText;
  if (choice === "generic") {
    promptText = GENERIC_PROMPT;
  } else {
    const c = (metricsCache?.per_consumer || []).find(c => c.name === choice);
    if (!c) {
      promptText = GENERIC_PROMPT;
    } else {
      promptText = PROMPT_TEMPLATE
        .replace("{{PROJECT_DISPLAY}}", c.display_name)
        .replace("{{REPO}}", c.repo);
    }
  }
  document.getElementById("prompt-text").textContent = promptText;
}

function setupCopyButton() {
  const btn = document.getElementById("copy-prompt");
  btn.addEventListener("click", () => {
    const text = document.getElementById("prompt-text").textContent;
    navigator.clipboard.writeText(text).then(() => {
      btn.textContent = "Copied!";
      setTimeout(() => { btn.textContent = "Copy"; }, 2000);
    });
  });
}

function setupFilters() {
  document.getElementById("filter-consumer").addEventListener("change", renderChunks);
  document.getElementById("filter-queue").addEventListener("change", renderChunks);
  document.getElementById("install-project").addEventListener("change", renderPrompt);
}

function populateProjectDropdowns(metrics) {
  const consumers = metrics.per_consumer || [];
  const fc = document.getElementById("filter-consumer");
  const ip = document.getElementById("install-project");
  for (const c of consumers) {
    const opt1 = document.createElement("option");
    opt1.value = c.name;
    opt1.textContent = c.display_name;
    fc.appendChild(opt1);
    const opt2 = document.createElement("option");
    opt2.value = c.name;
    opt2.textContent = c.display_name;
    ip.appendChild(opt2);
  }
}

// ---------- HTML escape helpers ----------

function escapeHtml(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function escapeAttr(s) {
  return escapeHtml(s).replace(/[^a-zA-Z0-9-_]/g, "");
}

// ---------- Boot ----------

async function load() {
  try {
    const [m, c] = await Promise.all([
      fetch("metrics.json", { cache: "no-cache" }).then(r => r.json()),
      fetch("chunks.json", { cache: "no-cache" }).then(r => r.json()),
    ]);
    metricsCache = m;
    chunksCache = c;
    renderKPIs(m);
    renderPerConsumer(m);
    populateProjectDropdowns(m);
    renderChunks();
    renderPrompt();
  } catch (err) {
    console.error("Failed to load landing data:", err);
    document.getElementById("kpi-completed").textContent = "—";
    document.getElementById("last-updated").textContent = "data unavailable";
    document.getElementById("prompt-text").textContent = GENERIC_PROMPT;
  }
}

setupCopyButton();
setupFilters();
load();
