const state = {
  authMode: "login",
  token: localStorage.getItem("stockAuthToken") || "",
  user: JSON.parse(localStorage.getItem("stockUserProfile") || "null"),
  apiBaseUrl: window.location.origin,
  streamlitUrl: localStorage.getItem("stockStreamlitUrl") || "http://localhost:8501",
};

const PAGE_LABELS = {
  account: "Account",
  home: "Home",
  streamlit: "Streamlit",
  token: "Token Usage",
  watchlist: "Watchlist",
  portfolio: "Portfolio",
};

const els = {
  appTopbar: document.getElementById("appTopbar"),
  authTabBtns: [...document.querySelectorAll(".tab-btn")],
  authSubmitBtn: document.getElementById("authSubmitBtn"),
  emailInput: document.getElementById("emailInput"),
  passwordInput: document.getElementById("passwordInput"),
  planTypeInput: document.getElementById("planTypeInput"),
  sessionBanner: document.getElementById("sessionBanner"),
  logoutBtn: document.getElementById("logoutBtn"),
  currentUserLabel: document.getElementById("currentUserLabel"),
  breadcrumb: document.getElementById("breadcrumb"),
  activePageTitle: document.getElementById("activePageTitle"),

  accountPage: document.getElementById("accountPage"),
  loadingPage: document.getElementById("loadingPage"),

  refreshUsageBtn: document.getElementById("refreshUsageBtn"),
  usageInput: document.getElementById("usageInput"),
  usageOutput: document.getElementById("usageOutput"),
  usageTotal: document.getElementById("usageTotal"),
  usageCost: document.getElementById("usageCost"),

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
  if (!els.toast) {
    return;
  }
  els.toast.textContent = message;
  els.toast.classList.remove("hidden");
  setTimeout(() => els.toast.classList.add("hidden"), 2500);
}

async function api(path, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(`${state.apiBaseUrl}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = {};
  try {
    data = await response.json();
  } catch (e) {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.detail || data.message || `HTTP ${response.status}`);
  }

  return data;
}

function setAuthMode(mode) {
  if (!els.authSubmitBtn || !els.planTypeInput) {
    return;
  }
  state.authMode = mode;
  els.authSubmitBtn.textContent = mode === "login" ? "Login" : "Register";
  els.planTypeInput.style.display = mode === "register" ? "block" : "none";
  els.authTabBtns.forEach(btn => btn.classList.toggle("active", btn.dataset.authMode === mode));
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
  if (state.authMode === "register") {
    payload.plan_type = els.planTypeInput.value;
  }

  if (els.accountPage) els.accountPage.classList.add("hidden");
  if (els.loadingPage) els.loadingPage.classList.remove("hidden");
  const data = await api(path, "POST", payload);

  state.token = data.access_token;
  state.user = data.user;

  localStorage.setItem("stockAuthToken", state.token);
  localStorage.setItem("stockUserProfile", JSON.stringify(state.user));

  setTimeout(() => {
    window.location.href = "/frontend/streamlit.html";
  }, 450);
  notify(`${state.authMode} successful`);
}

function logout() {
  state.token = "";
  state.user = null;
  localStorage.removeItem("stockAuthToken");
  localStorage.removeItem("stockUserProfile");
  window.location.href = "/frontend/index.html";
  notify("Logged out");
}


function showSessionBannerFromQuery() {
  if (!els.sessionBanner) {
    return;
  }
  const params = new URLSearchParams(window.location.search || "");
  const reason = params.get("reason");

  if (reason === "session-expired") {
    els.sessionBanner.textContent = "Your session expired. Please login again.";
    els.sessionBanner.classList.remove("hidden");
  } else if (reason === "unauthorized") {
    els.sessionBanner.textContent = "Please login to continue.";
    els.sessionBanner.classList.remove("hidden");
  } else {
    els.sessionBanner.classList.add("hidden");
  }
}


function setPageStrip(page) {
  const label = PAGE_LABELS[page] || "Workspace";
  if (els.activePageTitle) {
    els.activePageTitle.textContent = label;
  }
  if (els.breadcrumb) {
    els.breadcrumb.textContent = `Stock AI Workspace / ${label}`;
  }
}

async function refreshUsage() {
  const usage = await api("/api/v1/users/token-usage");
  els.usageInput.textContent = usage.input_tokens;
  els.usageOutput.textContent = usage.output_tokens;
  els.usageTotal.textContent = usage.total_tokens;
  els.usageCost.textContent = Number(usage.total_cost || 0).toFixed(6);
}

async function refreshWatchlist() {
  const items = await api("/api/v1/users/watchlist");
  els.watchlistList.innerHTML = "";
  items.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${item.ticker}</span><button data-ticker="${item.ticker}">Remove</button>`;
    li.querySelector("button").addEventListener("click", async () => {
      await api(`/api/v1/users/watchlist/${encodeURIComponent(item.ticker)}`, "DELETE");
      await refreshWatchlist();
    });
    els.watchlistList.appendChild(li);
  });
}

async function addWatchlist() {
  const ticker = els.watchTickerInput.value.trim().toUpperCase();
  if (!ticker) {
    notify("Ticker is required");
    return;
  }
  await api("/api/v1/users/watchlist", "POST", { ticker });
  els.watchTickerInput.value = "";
  await refreshWatchlist();
  notify("Watchlist updated");
}

async function refreshPortfolio() {
  const items = await api("/api/v1/users/portfolio");
  els.portfolioList.innerHTML = "";
  items.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${item.ticker} | qty ${item.quantity} | avg ${item.avg_buy_price}</span><button data-ticker="${item.ticker}">Remove</button>`;
    li.querySelector("button").addEventListener("click", async () => {
      await api(`/api/v1/users/portfolio/${encodeURIComponent(item.ticker)}`, "DELETE");
      await refreshPortfolio();
    });
    els.portfolioList.appendChild(li);
  });
}

async function addPortfolio() {
  const ticker = els.portfolioTickerInput.value.trim().toUpperCase();
  const quantity = Number(els.portfolioQtyInput.value);
  const avg_buy_price = Number(els.portfolioAvgInput.value);
  if (!ticker || !quantity || !avg_buy_price) {
    notify("Ticker, quantity and avg price are required");
    return;
  }

  await api("/api/v1/users/portfolio", "POST", { ticker, quantity, avg_buy_price });
  els.portfolioTickerInput.value = "";
  els.portfolioQtyInput.value = "";
  els.portfolioAvgInput.value = "";
  await refreshPortfolio();
  notify("Portfolio updated");
}

async function hydrateApp() {
  if (els.currentUserLabel) {
    if (state.user && state.user.email) {
      els.currentUserLabel.textContent = `${state.user.email} (${state.user.plan_type || "free"})`;
    } else {
      els.currentUserLabel.textContent = "Logged in";
    }
  }

  if (els.streamlitFrame) {
    const base = String(state.streamlitUrl || "http://localhost:8501").replace(/\/+$/, "");
    const params = new URLSearchParams({ embed: "true" });
    if (state.token) {
      params.set("token", state.token);
    }
    if (state.user && state.user.email) {
      params.set("email", state.user.email);
    }
    els.streamlitFrame.src = `${base}/?${params.toString()}`;
  }

  const page = document.body.dataset.page;
  if (page === "token") {
    await refreshUsage();
  }
  if (page === "watchlist") {
    await refreshWatchlist();
  }
  if (page === "portfolio") {
    await refreshPortfolio();
  }
}

function wireEvents() {
  if (els.authTabBtns && els.authTabBtns.length) {
    els.authTabBtns.forEach(btn => {
      btn.addEventListener("click", () => setAuthMode(btn.dataset.authMode));
    });
  }

  if (els.authSubmitBtn) {
    els.authSubmitBtn.addEventListener("click", () => loginOrRegister().catch(err => {
      if (els.loadingPage) els.loadingPage.classList.add("hidden");
      if (els.accountPage) els.accountPage.classList.remove("hidden");
      notify(err.message);
    }));
  }

  if (els.logoutBtn) {
    els.logoutBtn.addEventListener("click", logout);
  }

  if (els.refreshUsageBtn) {
    els.refreshUsageBtn.addEventListener("click", () => refreshUsage().catch(err => notify(err.message)));
  }
  if (els.addWatchBtn) {
    els.addWatchBtn.addEventListener("click", () => addWatchlist().catch(err => notify(err.message)));
  }
  if (els.addPortfolioBtn) {
    els.addPortfolioBtn.addEventListener("click", () => addPortfolio().catch(err => notify(err.message)));
  }

  if (els.openStreamlitBtn) {
    els.openStreamlitBtn.addEventListener("click", () => {
      const base = String(state.streamlitUrl || "http://localhost:8501").replace(/\/+$/, "");
      const params = new URLSearchParams({ embed: "true" });
      if (state.token) {
        params.set("token", state.token);
      }
      if (state.user && state.user.email) {
        params.set("email", state.user.email);
      }
      window.open(`${base}/?${params.toString()}`, "_blank", "noopener");
    });
  }
}

async function init() {
  const page = document.body.dataset.page || "account";
  setPageStrip(page);

  // Only initialize auth form controls on the account page.
  if (page === "account") {
    setAuthMode("login");
  }

  wireEvents();

  if (page === "account") {
    showSessionBannerFromQuery();
    if (state.token) {
      try {
        const me = await api("/api/v1/users/me");
        state.user = me;
        localStorage.setItem("stockUserProfile", JSON.stringify(me));
        window.location.href = "/frontend/home.html";
      } catch (err) {
        localStorage.removeItem("stockAuthToken");
        localStorage.removeItem("stockUserProfile");
      }
    }
    return;
  }

  if (!state.token) {
    window.location.href = "/frontend/index.html?reason=unauthorized";
    return;
  }

  try {
    const me = await api("/api/v1/users/me");
    state.user = me;
    localStorage.setItem("stockUserProfile", JSON.stringify(me));
    await hydrateApp();
  } catch (err) {
    localStorage.removeItem("stockAuthToken");
    localStorage.removeItem("stockUserProfile");
    window.location.href = "/frontend/index.html?reason=session-expired";
    notify(`Session expired: ${err.message}`);
  }
}

init();
