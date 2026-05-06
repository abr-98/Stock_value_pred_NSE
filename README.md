# Stock_value_pred_NSE

## Streamlit Chat Integration

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The app includes:
- Persistent thread memory for follow-up queries.
- MCP-backed tool orchestration (stock, fundamental, memory, QnA, SWOT, etc.).
- Optional debug panel showing required tools vs called tools.
- Optional force-refresh toggle for transcript QnA index rebuild.

## Web Frontend (APIs + Streamlit)

A browser frontend is available under [frontend/index.html](frontend/index.html).

It supports:
- User login/register with JWT
- Chat thread and message APIs
- Token usage summary
- Watchlist and portfolio management
- Embedded Streamlit app in the same page

Run API and Streamlit first, then open [frontend/index.html](frontend/index.html) in your browser.

Configurable in UI:
- API URL (default `http://localhost:8000`)
- Streamlit URL (default `http://localhost:8501`)

## User Accounts And Chat APIs

New API module is available at `/api/v1/users` with:

- JWT-based register/login (`/register`, `/login`, `/me`)
- Chat threads and messages (`/threads`, `/threads/{id}/messages`)
- Token tracking with `tiktoken` + cost estimates (`/token-usage`)
- Watchlist management (`/watchlist`)
- Portfolio management (`/portfolio`)

On API startup, user-related tables are auto-created in PostgreSQL.

Install new auth dependency if needed:

```bash
pip install PyJWT
```