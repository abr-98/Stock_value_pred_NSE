const state = {
  authMode: "login",
  token: localStorage.getItem("stockAuthToken") || "",
  user: JSON.parse(localStorage.getItem("stockUserProfile") || "null"),
  apiBaseUrl: localStorage.getItem("stockApiBaseUrl") || "http://localhost:8000",
  streamlitUrl: localStorage.getItem("stockStreamlitUrl") || "http://localhost:8501",
  threads: [],
  activeThreadId: null,
};

const els = {
  apiBaseUrl: document.getElementById("apiBaseUrl"),
  streamlitUrl: document.getElementById("streamlitUrl"),
  saveConfigBtn: document.getElementById("saveConfigBtn"),
  authTabBtns: [...document.querySelectorAll(".tab-btn")],
  authSubmitBtn: document.getElementById("authSubmitBtn"),
  emailInput: document.getElementById("emailInput"),
  passwordInput: document.getElementById("passwordInput"),
  planTypeInput: document.getElementById("planTypeInput"),
  logoutBtn: document.getElementById("logoutBtn"),
  refreshUsageBtn: document.getElementById("refreshUsageBtn"),
  currentUserLabel: document.getElementById("currentUserLabel"),
  tokenUsagePanel: document.getElementById("tokenUsagePanel"),
  usageInput: document.getElementById("usageInput"),
  usageOutput: document.getElementById("usageOutput"),
  usageTotal: document.getElementById("usageTotal"),
  usageCost: document.getElementById("usageCost"),
  threadTitleInput: document.getElementById("threadTitleInput"),
  createThreadBtn: document.getElementById("createThreadBtn"),
  threadSelect: document.getElementById("threadSelect"),
  messagesBox: document.getElementById("messagesBox"),
  messageRoleInput: document.getElementById("messageRoleInput"),
  messageModelInput: document.getElementById("messageModelInput"),
  messageContentInput: document.getElementById("messageContentInput"),
  sendMessageBtn: document.getElementById("sendMessageBtn"),
  watchTickerInput: document.getElementById("watchTickerInput"),
  addWatchBtn: document.getElementById("addWatchBtn"),
  watchlistList: document.getElementById("watchlistList"),
  portfolioTickerInput: document.getElementById("portfolioTickerInput"),
  portfolioQtyInput: document.getElementById("portfolioQtyInput"),
  portfolioAvgInput: document.getElementById("portfolioAvgInput"),
  addPortfolioBtn: document.getElementById("addPortfolioBtn"),
  portfolioList: document.getElementById("portfolioList"),
  streamlitFrame: document.getElementById("streamlitFrame"),
  openStreamlitBtn: document.getElementById("openStreamlitBtn"),
  toast: document.getElementById("toast"),
};

function notify(message) {
  els.toast.textContent = message;
  els.toast.classList.remove("hidden");
  setTimeout(() => els.toast.classList.add("hidden"), 2500);
}

async function api(path, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;

  const res = await fetch(`${state.apiBaseUrl}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = {};
  try {
    data = await res.json();
  } catch (e) {
    data = {};
  }

  if (!res.ok) {
    const detail = data.detail || data.message || `HTTP ${res.status}`;
    throw new Error(detail);
  }
  return data;
}

function setAuthMode(mode) {
  state.authMode = mode;
  els.authSubmitBtn.textContent = mode === "login" ? "Login" : "Register";
  els.planTypeInput.style.display = mode === "register" ? "block" : "none";
  els.authTabBtns.forEach(btn => btn.classList.toggle("active", btn.dataset.authMode === mode));
}

function renderProfile() {
  if (state.user) {
    els.currentUserLabel.textContent = `Logged in: ${state.user.email} (${state.user.plan_type})`;
    els.tokenUsagePanel.classList.remove("hidden");
  } else {
    els.currentUserLabel.textContent = "Not logged in";
    els.tokenUsagePanel.classList.add("hidden");
    els.messagesBox.innerHTML = "";
    els.watchlistList.innerHTML = "";
    els.portfolioList.innerHTML = "";
  }
}

async function loginOrRegister() {
  const email = els.emailInput.value.trim();
  const password = els.passwordInput.value.trim();
  if (!email || !password) {
    notify("Email and password are required");
    return;
  }

  const path = state.authMode === "login" ? "/api/v1/users/login" : "/api/v1/users/register";
  const payload = { email, password };
  if (state.authMode === "register") payload.plan_type = els.planTypeInput.value;

  const data = await api(path, "POST", payload);
  state.token = data.access_token;
  state.user = data.user;

  localStorage.setItem("stockAuthToken", state.token);
  localStorage.setItem("stockUserProfile", JSON.stringify(state.user));

  renderProfile();
  await Promise.all([refreshThreads(), refreshUsage(), refreshWatchlist(), refreshPortfolio()]);
  notify(`${state.authMode} successful`);
}

function logout() {
  state.token = "";
  state.user = null;
  state.threads = [];
  state.activeThreadId = null;
  localStorage.removeItem("stockAuthToken");
  localStorage.removeItem("stockUserProfile");
  renderProfile();
  renderThreads();
  notify("Logged out");
}

async function refreshUsage() {
  if (!state.token) return;
  const usage = await api("/api/v1/users/token-usage");
  els.usageInput.textContent = usage.input_tokens;
  els.usageOutput.textContent = usage.output_tokens;
  els.usageTotal.textContent = usage.total_tokens;
  els.usageCost.textContent = Number(usage.total_cost || 0).toFixed(6);
}

async function refreshThreads() {
  if (!state.token) return;
  state.threads = await api("/api/v1/users/threads");
  renderThreads();
  if (!state.activeThreadId && state.threads.length) {
    state.activeThreadId = Number(state.threads[0].id);
    els.threadSelect.value = String(state.activeThreadId);
    await refreshMessages();
  }
}

function renderThreads() {
  els.threadSelect.innerHTML = "";
  if (!state.threads.length) {
    const opt = document.createElement("option");
    opt.textContent = "No threads";
    opt.value = "";
    els.threadSelect.appendChild(opt);
    return;
  }

  state.threads.forEach(t => {
    const opt = document.createElement("option");
    opt.value = String(t.id);
    opt.textContent = `${t.title} (#${t.id})`;
    if (Number(t.id) === Number(state.activeThreadId)) opt.selected = true;
    els.threadSelect.appendChild(opt);
  });
}

async function createThread() {
  const title = els.threadTitleInput.value.trim() || "New Chat";
  const thread = await api("/api/v1/users/threads", "POST", { title });
  state.activeThreadId = Number(thread.id);
  await refreshThreads();
  notify("Thread created");
}

async function refreshMessages() {
  if (!state.token || !state.activeThreadId) return;
  const messages = await api(`/api/v1/users/threads/${state.activeThreadId}/messages`);
  els.messagesBox.innerHTML = "";
  messages.forEach(m => {
    const item = document.createElement("div");
    item.className = "msg";
    item.innerHTML = `<strong>${m.role}</strong> <span class="muted">(${m.token_count} tok, ${m.model})</span><div>${escapeHtml(m.content)}</div>`;
    els.messagesBox.appendChild(item);
  });
}

async function sendMessageToThread() {
  if (!state.activeThreadId) {
    notify("Create/select a thread first");
    return;
  }
  const role = els.messageRoleInput.value;
  const content = els.messageContentInput.value.trim();
  const model = els.messageModelInput.value.trim() || "gpt-4o";

  if (!content) {
    notify("Message content required");
    return;
  }

  await api(`/api/v1/users/threads/${state.activeThreadId}/messages`, "POST", { role, content, model });
  els.messageContentInput.value = "";
  await Promise.all([refreshMessages(), refreshUsage()]);
  notify("Message stored");
}

async function refreshWatchlist() {
  if (!state.token) return;
  const items = await api("/api/v1/users/watchlist");
  els.watchlistList.innerHTML = "";
  items.forEach(w => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${w.ticker}</span><button data-ticker="${w.ticker}">Remove</button>`;
    li.querySelector("button").addEventListener("click", async () => {
      await api(`/api/v1/users/watchlist/${encodeURIComponent(w.ticker)}`, "DELETE");
      await refreshWatchlist();
    });
    els.watchlistList.appendChild(li);
  });
}

async function addWatchlist() {
  const ticker = els.watchTickerInput.value.trim().toUpperCase();
  if (!ticker) return;
  await api("/api/v1/users/watchlist", "POST", { ticker });
  els.watchTickerInput.value = "";
  await refreshWatchlist();
}

async function refreshPortfolio() {
  if (!state.token) return;
  const items = await api("/api/v1/users/portfolio");
  els.portfolioList.innerHTML = "";
  items.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${p.ticker} | qty ${p.quantity} | avg ${p.avg_buy_price}</span><button data-ticker="${p.ticker}">Remove</button>`;
    li.querySelector("button").addEventListener("click", async () => {
      await api(`/api/v1/users/portfolio/${encodeURIComponent(p.ticker)}`, "DELETE");
      await refreshPortfolio();
    });
    els.portfolioList.appendChild(li);
  });
}

async function addPortfolio() {
  const ticker = els.portfolioTickerInput.value.trim().toUpperCase();
  const quantity = Number(els.portfolioQtyInput.value);
  const avg_buy_price = Number(els.portfolioAvgInput.value);
  if (!ticker || !quantity || !avg_buy_price) return;

  await api("/api/v1/users/portfolio", "POST", { ticker, quantity, avg_buy_price });
  els.portfolioTickerInput.value = "";
  els.portfolioQtyInput.value = "";
  els.portfolioAvgInput.value = "";
  await refreshPortfolio();
}

function configureUrls() {
  state.apiBaseUrl = els.apiBaseUrl.value.trim() || "http://localhost:8000";
  state.streamlitUrl = els.streamlitUrl.value.trim() || "http://localhost:8501";
  localStorage.setItem("stockApiBaseUrl", state.apiBaseUrl);
  localStorage.setItem("stockStreamlitUrl", state.streamlitUrl);
  els.streamlitFrame.src = state.streamlitUrl;
  notify("URLs saved");
}

function escapeHtml(input) {
  return String(input)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function wireEvents() {
  els.authTabBtns.forEach(btn => btn.addEventListener("click", () => setAuthMode(btn.dataset.authMode)));
  els.authSubmitBtn.addEventListener("click", () => loginOrRegister().catch(err => notify(err.message)));
  els.logoutBtn.addEventListener("click", logout);
  els.refreshUsageBtn.addEventListener("click", () => refreshUsage().catch(err => notify(err.message)));

  els.saveConfigBtn.addEventListener("click", configureUrls);
  els.createThreadBtn.addEventListener("click", () => createThread().catch(err => notify(err.message)));
  els.threadSelect.addEventListener("change", () => {
    state.activeThreadId = Number(els.threadSelect.value || 0) || null;
    refreshMessages().catch(err => notify(err.message));
  });
  els.sendMessageBtn.addEventListener("click", () => sendMessageToThread().catch(err => notify(err.message)));

  els.addWatchBtn.addEventListener("click", () => addWatchlist().catch(err => notify(err.message)));
  els.addPortfolioBtn.addEventListener("click", () => addPortfolio().catch(err => notify(err.message)));

  els.openStreamlitBtn.addEventListener("click", () => window.open(state.streamlitUrl, "_blank", "noopener"));
}

async function init() {
  els.apiBaseUrl.value = state.apiBaseUrl;
  els.streamlitUrl.value = state.streamlitUrl;
  els.streamlitFrame.src = state.streamlitUrl;
  setAuthMode("login");
  renderProfile();
  wireEvents();

  if (state.token) {
    try {
      await api("/api/v1/users/me");
      await Promise.all([refreshThreads(), refreshUsage(), refreshWatchlist(), refreshPortfolio()]);
    } catch (err) {
      logout();
      notify(`Session expired: ${err.message}`);
    }
  }
}

init();
