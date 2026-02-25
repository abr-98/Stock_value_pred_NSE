let API = "http://localhost:8000";

function initDashboard() {
  const savedBase = localStorage.getItem("api_base_url");
  const apiInput = document.getElementById("api-base");

  if (savedBase) {
    API = savedBase;
  }

  if (apiInput) {
    apiInput.value = API;
  }

  if (document.getElementById("portfolio-body")) {
    addRow();
  }
}

let charts = {};

function destroyChart(id) {
  if (charts[id]) {
    charts[id].destroy();
    delete charts[id];
  }
}

function renderPortfolioAnalysis(data) {

  const p = data.portfolio_analysis;
  const d = data.diversification_analysis;

  document.getElementById("portfolio-metrics").innerHTML = `
    <div class="metric-grid">
      <div class="metric">Avg Correlation<br><b>${p.avg_correlation.toFixed(3)}</b></div>
      <div class="metric">Effective Bets<br><b>${p.effective_bets.toFixed(2)}</b></div>
      <div class="metric">Risk Score<br><b>${p.risk_score}</b></div>
      <div class="metric">Confidence<br><b>${p.confidence}</b></div>
    </div>
  `;

  renderVarianceChart(p.variance_concentration);
  renderRiskChart(p);

  renderSectorReturns(d.sector_level.sector_returns);

  renderSectorWeights(d.sector_level.weights);
  renderSectorRisk(d.sector_level.variance_contribution);

  renderRationale(data.rationale);
}

function renderVarianceChart(v) {

  destroyChart("varianceChart");

  charts["varianceChart"] = new Chart(document.getElementById("varianceChart"), {
    type: "bar",
    data: {
      labels: ["PC1", "Top 3"],
      datasets: [{
        label: "Variance Share",
        data: [v.pc1_variance, v.top3_variance]
      }]
    },
    options: {
      plugins: {
        title: { display: true, text: "Principal Component Concentration" },
        legend: { display: false }
      }
    }
  });
}


function renderRiskChart(p) {

  destroyChart("riskChart");

  charts["riskChart"] = new Chart(document.getElementById("riskChart"), {
    type: "bar",
    data: {
      labels: ["Volatility", "CVaR", "Diversification"],
      datasets: [{
        label: "Risk Metrics",
        data: [p.annual_volatility, Math.abs(p.cvar), p.diversification_ratio]
      }]
    },
    options: {
      plugins: {
        title: { display: true, text: "Portfolio Risk Structure" },
        legend: { display: false }
      }
    }
  });
}


function renderDiversification(data) {

  const d = data.diversification_analysis;

  document.getElementById("diversification-metrics").innerHTML = `
    <div class="metric-grid">
      <div class="metric">Effective Assets<br><b>${d.asset_level.effective_assets.toFixed(2)}</b></div>
      <div class="metric">Effective Sectors<br><b>${d.sector_level.effective_sectors.toFixed(2)}</b></div>
    </div>
  `;

  renderSectorWeights(d.sector_level.weights);
  renderSectorRisk(d.sector_level.variance_contribution);
}

function renderSectorWeights(weights) {

  destroyChart("sectorWeightChart");

  charts["sectorWeightChart"] = new Chart(document.getElementById("sectorWeightChart"), {
    type: "pie",
    data: {
      labels: Object.keys(weights),
      datasets: [{ data: Object.values(weights) }]
    },
    options: {
      plugins: { title: { display: true, text: "Sector Exposure Mix" } }
    }
  });
}

function renderSectorRisk(contrib) {

  destroyChart("sectorRiskChart");

  charts["sectorRiskChart"] = new Chart(document.getElementById("sectorRiskChart"), {
    type: "bar",
    data: {
      labels: Object.keys(contrib),
      datasets: [{ label: "Variance Contribution", data: Object.values(contrib) }]
    },
    options: {
      plugins: {
        title: { display: true, text: "Sector Risk Drivers" },
        legend: { display: false }
      }
    }
  });
}

function renderRationale(text) {

  if (!text) {
    document.getElementById("portfolio-result").innerHTML = "No rationale available.";
    return;
  }

  // Remove line breaks that break formatting
  const cleaned = text.replace(/\n/g, " ");

  const points = cleaned
      .split("|")
      .map(t => t.trim())
      .filter(t => t.length > 0);

  document.getElementById("portfolio-result").innerHTML =
      "<ul class='rationale-list'>" +
      points.map(p => `<li>${p}</li>`).join("") +
      "</ul>";
}

function renderAllocationPie(allocations) {

  destroyChart("allocationPieChart");

  charts["allocationPieChart"] = new Chart(
    document.getElementById("allocationPieChart"),
    {
      type: "pie",
      data: {
        labels: Object.keys(allocations),
        datasets: [{
          data: Object.values(allocations)
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: "Portfolio Sector Distribution"
          },
          legend: {
            position: "right"
          }
        }
      }
    }
  );
}

function renderAllocationBar(allocations) {

  destroyChart("allocationBarChart");

  const sorted = Object.entries(allocations)
    .sort((a, b) => b[1] - a[1]);

  charts["allocationBarChart"] = new Chart(
    document.getElementById("allocationBarChart"),
    {
      type: "bar",
      data: {
        labels: sorted.map(x => x[0]),
        datasets: [{
          label: "Allocation Weight",
          data: sorted.map(x => x[1])
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: "Sector Allocation Ranking"
          },
          legend: { display: false }
        }
      }
    }
  );
}




function renderSectorReturns(sectorReturns) {

  destroyChart("sectorReturnChart");

  const labels = sectorReturns.map((_, i) => i + 1);

  const sectors = Object.keys(sectorReturns[0]);

  const datasets = sectors.map(sector => ({
    label: sector,
    data: sectorReturns.map(r => r[sector]),
    fill: false
  }));

  charts["sectorReturnChart"] = new Chart(document.getElementById("sectorReturnChart"), {
    type: "line",
    data: { labels, datasets },
    options: {
      plugins: {
        title: { display: true, text: "Sector Return Behaviour (Historical Window)" },
        legend: { display: true }
      },
      elements: { point: { radius: 0 } }
    }
  });
}




function saveApiBase() {
  const input = document.getElementById("api-base");
  if (!input) {
    return;
  }

  const value = input.value.trim().replace(/\/$/, "");
  if (!value) {
    setText("status-result", "Please provide a valid API base URL.");
    return;
  }

  API = value;
  localStorage.setItem("api_base_url", API);
  setText("status-result", `API base updated to ${API}`);
}

function setText(elementId, message) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
  }
}

function readSymbol() {
  const element = document.getElementById("stock-symbol");
  if (!element) {
    return "";
  }
  return element.value.trim().toUpperCase();
}

async function apiCall(path, options = {}) {
  const url = `${API}${path}`;
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    const message = data?.detail || data?.message || `HTTP ${response.status}`;
    throw new Error(message);
  }

  return data;
}

function renderExplainabilityDashboard(data) {

  const analysis = data.report.analysis;

  renderLinearExplain(analysis.linear_explanation);
  renderTreeExplain(analysis.decision_tree_explanation);
  renderExplainRationale(data.report.rationale);
}


function renderLinearExplain(coeffs) {

  destroyChart("linearExplainChart");

  const values = Object.values(coeffs);
  const maxAbs = Math.max(...values.map(v => Math.abs(v)));

  const normalized = values.map(v => v / maxAbs);

  charts["linearExplainChart"] = new Chart(
    document.getElementById("linearExplainChart"),
    {
      type: "bar",
      data: {
        labels: Object.keys(coeffs),
        datasets: [{ data: normalized }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Relative Feature Influence (Linear Model)" }
        },
        scales: {
          y: { min: -1, max: 1 }
        }
      }
    }
  );
}

function renderTreeExplain(importances) {

  destroyChart("treeExplainChart");

  const vals = importances.map(x => x.importance);

  charts["treeExplainChart"] = new Chart(
    document.getElementById("treeExplainChart"),
    {
      type: "bar",
      data: {
        labels: vals.map((_, i) => `Feature ${i + 1}`),
        datasets: [{ data: vals }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Decision Tree Importance Structure" }
        },
        scales: {
          y: { min: 0, max: Math.max(...vals) }
        }
      }
    }
  );
}

function renderExplainRationale(text) {

  const points = text.split("|").map(t => t.trim());

  document.getElementById("explain-rationale").innerHTML =
    "<ul class='rationale-list'>" +
    points.map(p => `<li>${p}</li>`).join("") +
    "</ul>";
}



async function runRequest(resultId, statusLabel, path, options = {}) {
  try {
    setText("status-result", `Running ${statusLabel}...`);
    setText(resultId, "Loading...");
    const data = await apiCall(path, options);

if (path.includes("/explain/analyze/")) {

    renderExplainabilityDashboard(data);

} else if (path.includes("/memory/analyze/")) {

    renderMemoryDashboard(data);

} else if (path.includes("/stock/analyze/")) {

    renderStockDashboard(data);

} else if (path.includes("/allocation/analyze")) {

    const allocations = data.allocation_analysis.allocations;

    renderAllocationPie(allocations);
    renderAllocationBar(allocations);

} else if (path.includes("/portfolio/analyze")) {

    renderPortfolioAnalysis(data);
    renderDiversification(data);

} else {
    setText(resultId, JSON.stringify(data, null, 2));
}

    setText("status-result", `${statusLabel} completed.`);
  } catch (error) {
    setText(resultId, `Error: ${error.message}`);
    setText("status-result", `${statusLabel} failed.`);
  }
}

async function checkHealth() {
  await runRequest("health-result", "Health check", "/health");
}

function addRow() {
  const table = document.getElementById("portfolio-body");
  if (!table) {
    return;
  }

  const row = document.createElement("tr");

  row.innerHTML = `
    <td><input placeholder="Symbol" class="symbol"></td>
    <td><input placeholder="Qty" class="qty" type="number"></td>
    <td><button class="danger" onclick="removeRow(this)">Remove</button></td>
  `;

  table.appendChild(row);
}

function removeRow(button) {
  const row = button.closest("tr");
  if (row) {
    row.remove();
  }
}

function collectPortfolio() {
  const symbols = document.querySelectorAll(".symbol");
  const qtys = document.querySelectorAll(".qty");

  const portfolio = {};

  symbols.forEach((s, i) => {
    const sym = s.value.trim();
    const qty = qtys[i].value;

    if (sym && qty) {
      portfolio[sym] = Number(qty);
    }
  });

  return portfolio;
}

async function analyzePortfolio() {
  const portfolio = collectPortfolio();
  const valueElement = document.getElementById("portfolio-value");
  const value = Number(valueElement ? valueElement.value : 0);

  if (!Object.keys(portfolio).length) {
    setText("status-result", "Please add at least one stock in portfolio input.");
    return;
  }

  if (!value || value <= 0) {
    setText("status-result", "Please enter a valid portfolio value.");
    return;
  }

  const payload = {
    portfolio,
    value
  };

  await runRequest(
    "portfolio-result",
    "Portfolio analysis",
    "/api/v1/portfolio/analyze",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );

  await runRequest(
    "allocation-result",
    "Allocation analysis",
    "/api/v1/allocation/analyze",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );
}

function renderStockDashboard(data) {

  const d = data.data;

  renderStockSummary(d);
  renderAgentScores(d.signals);
  renderAgentConfidence(d.signals);
  renderDiagnostics(d);
  renderRegime(d.regime);
  renderTechnical(d.evidence.technical);
  renderRationale(d.structural_rationale);
}


function renderStockSummary(d) {

  document.getElementById("stock-summary").innerHTML = `
    <div class="summary-grid">
      <div class="summary-box">Final Score<br><b>${d.final_score.toFixed(2)}</b></div>
      <div class="summary-box">Confidence<br><b>${d.confidence.toFixed(2)}</b></div>
      <div class="summary-box">Disagreement<br><b>${d.disagreement.toFixed(2)}</b></div>
      <div class="summary-box">Regime<br><b>${d.regime.regime}</b></div>
    </div>
  `;
}

function renderMemoryDashboard(data) {

  const a = data.report.analysis;
  const instances = a.matched_instances;

  renderMemorySummary(a);
  renderMemoryBehaviour(a);
  renderMemoryDistances(a.distance_stats);
  renderMemoryReturns(instances);
  renderMemoryRisk(instances);
}

function renderMemorySummary(a) {

  document.getElementById("memory-summary").innerHTML = `
    <div class="summary-grid">
      <div class="summary-box">Matches<br><b>${a.matches}</b></div>
      <div class="summary-box">Avg Forward Return<br><b>${(a.avg_forward_return * 100).toFixed(2)}%</b></div>
      <div class="summary-box">Positive Ratio<br><b>${(a.positive_ratio * 100).toFixed(0)}%</b></div>
    </div>
  `;
}

function renderMemoryBehaviour(a) {

  destroyChart("memoryBehaviourChart");

  charts["memoryBehaviourChart"] = new Chart(
    document.getElementById("memoryBehaviourChart"),
    {
      type: "bar",
      data: {
        labels: ["Avg Return", "Positive Probability"],
        datasets: [{
          data: [a.avg_forward_return, a.positive_ratio]
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Historical Forward Behaviour" }
        },
        scales: {
          y: { min: 0, max: 1 }
        }
      }
    }
  );
}

function renderMemoryDistances(stats) {

  destroyChart("memoryDistanceChart");

  const normalized = [
    stats.min / stats.max,
    stats.mean / stats.max,
    1
  ];

  charts["memoryDistanceChart"] = new Chart(
    document.getElementById("memoryDistanceChart"),
    {
      type: "bar",
      data: {
        labels: ["Nearest", "Average", "Farthest"],
        datasets: [{ data: normalized }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Similarity Dispersion (Normalized)" }
        },
        scales: {
          y: { min: 0, max: 1 }
        }
      }
    }
  );
}

function renderMemoryReturns(instances) {

  destroyChart("memoryReturnsChart");

  charts["memoryReturnsChart"] = new Chart(
    document.getElementById("memoryReturnsChart"),
    {
      type: "bar",
      data: {
        labels: instances.map(x => x.date.slice(0, 10)),
        datasets: [{
          data: instances.map(x => x.features.r_20)
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "20-Day Returns of Matched Regimes" }
        }
      }
    }
  );
}

function renderMemoryRisk(instances) {

  destroyChart("memoryRiskChart");

  charts["memoryRiskChart"] = new Chart(
    document.getElementById("memoryRiskChart"),
    {
      type: "bar",
      data: {
        labels: instances.map(x => x.date.slice(0, 10)),
        datasets: [{
          data: instances.map(x => Math.abs(x.features.drawdown_20))
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Drawdown Severity of Matched Regimes" }
        }
      }
    }
  );
}


function renderAgentScores(signals) {

  destroyChart("agentScoreChart");

  charts["agentScoreChart"] = new Chart(document.getElementById("agentScoreChart"), {
    type: "bar",
    data: {
      labels: signals.map(s => s.agent.toUpperCase()),
      datasets: [{
        data: signals.map(s => s.score)
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Agent Signal Strength" }
      },
      scales: {
        y: {
          min: -1,
          max: 100    // Scores bounded visually
        }
      }
    }
  });
}

function renderAgentConfidence(signals) {

  destroyChart("agentConfidenceChart");

  const maxConf = Math.max(...signals.map(s => s.confidence));

  const normalized = signals.map(s => s.confidence / maxConf);

  charts["agentConfidenceChart"] = new Chart(document.getElementById("agentConfidenceChart"), {
    type: "bar",
    data: {
      labels: signals.map(s => s.agent.toUpperCase()),
      datasets: [{
        data: normalized
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Relative Agent Confidence" }
      },
      scales: {
        y: {
          min: 0,
          max: 1
        }
      }
    }
  });
}


function renderDiagnostics(d) {

  destroyChart("diagnosticsChart");

  charts["diagnosticsChart"] = new Chart(document.getElementById("diagnosticsChart"), {
    type: "bar",
    data: {
      labels: ["Score", "Confidence", "Disagreement"],
      datasets: [{
        data: [d.final_score, d.confidence, d.disagreement]
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: "System Diagnostics" }
      },
      scales: {
        y: {
          min: 0,
          max: 100
        }
      }
    }
  });
}

function renderRegime(regime) {

  destroyChart("regimeChart");

  const normalizedADX = regime.ADX / 100;
  const normalizedATR = regime.ATR_pct / 10;

  charts["regimeChart"] = new Chart(document.getElementById("regimeChart"), {
    type: "bar",
    data: {
      labels: ["Trend Strength", "Volatility State"],
      datasets: [{
        data: [normalizedADX, normalizedATR]
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Regime Structure (Normalized)" }
      },
      scales: {
        y: {
          min: 0,
          max: 1
        }
      }
    }
  });
}

function renderTechnical(t) {

  destroyChart("technicalChart");

  const emaSpread = (t.EMA_50 - t.EMA_200) / t.price;
  const normalizedRSI = t.RSI / 100;

  charts["technicalChart"] = new Chart(document.getElementById("technicalChart"), {
    type: "bar",
    data: {
      labels: ["EMA Trend Spread", "RSI State", "MACD Momentum"],
      datasets: [{
        data: [emaSpread, normalizedRSI, t.MACD_hist]
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Technical Structure (Relative)" }
      },
      scales: {
        y: {
          min: -1,
          max: 1
        }
      }
    }
  });
}

function renderRationale(text) {

  const cleaned = text.replace(/\n/g, " ");

  const points = cleaned.split("|").map(x => x.trim());

  document.getElementById("stock-rationale").innerHTML =
    "<ul class='rationale-list'>" +
    points.map(p => `<li>${p}</li>`).join("") +
    "</ul>";
}


async function runStockAnalysis() {
  const symbol = readSymbol();
  if (!symbol) {
    setText("status-result", "Please enter a stock symbol.");
    return;
  }

  await runRequest("stock-result", "Stock analysis", `/api/v1/stock/analyze/${symbol}`);
}

async function runCorrelationAnalysis() {
  const symbol = readSymbol();
  if (!symbol) {
    setText("status-result", "Please enter a stock symbol.");
    return;
  }

  await runRequest("correlation-result", "Correlation analysis", `/api/v1/correlation/analyze/${symbol}`);
}

async function runFundamentalReport() {
  const symbol = readSymbol();
  if (!symbol) {
    setText("status-result", "Please enter a stock symbol.");
    return;
  }

  await runRequest("fundamental-result", "Fundamental report", `/api/v1/fundamental/report/${symbol}`);
}

async function runMemoryAnalysis() {
  const symbol = readSymbol();
  if (!symbol) {
    setText("status-result", "Please enter a stock symbol.");
    return;
  }

  await runRequest("memory-result", "Memory analysis", `/api/v1/memory/analyze/${symbol}`);
}

async function runExplainAnalysis() {
  const symbol = readSymbol();
  if (!symbol) {
    setText("status-result", "Please enter a stock symbol.");
    return;
  }

  await runRequest("explain-result", "Explain analysis", `/api/v1/explain/analyze/${symbol}`);
}

async function analyzeStock() {
  await runStockAnalysis();
}
