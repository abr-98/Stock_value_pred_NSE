import asyncio
import io
import os
import re
import sys
import uuid
from typing import Any

import httpx
import ipykernel.iostream
import streamlit as st
import tiktoken
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, create_react_agent, tools_condition
from typing_extensions import Annotated, NotRequired, Optional, TypedDict


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    portfolio: NotRequired[Optional[dict]]


SYSTEM_PROMPT = """
You are a stock investment assistant.
Your task is to help users analyze stock portfolios and provide insights.

You have tools for stock, allocation, portfolio, correlation, fundamentals, memory, explainability, QnA, SWOT, and web search.
Use tools only when the user asks analysis/search actions. For greetings and small talk, respond directly without tools.

Conversation memory rule:
If the user already provided a valid stock ticker earlier in this thread (for example TCS.NS), reuse it for follow-up requests
such as SWOT analysis, news, fundamental report, or price analysis. Do not ask for ticker again unless it is missing.

Important tool-call rule:
For portfolio-dependent tools, always pass BOTH keys exactly as:
{"portfolio": {"INFY.NS": 10, "RELIANCE.NS": 4}, "value": 65500}
If either is missing, return a guided error and ask once.

Transcript tool rule:
Call query_transcripts only when the user asks a specific question about annual reports, earnings-call transcripts,
management commentary, or asks for a document-grounded summary. For generic requests like "fundamental annual report"
or "give me the annual report", prefer get_fundamental_annual_earnings_report and do not call query_transcripts.
""".strip()


FUNDAMENTAL_TOOL_NAME = "get_fundamental_annual_earnings_report"


def _api_base_url() -> str:
    return (os.environ.get("STOCK_API_BASE_URL") or "http://localhost:8000").rstrip("/")


def _api_request(method: str, path: str, token: str | None = None, payload: dict | None = None):
    url = _api_base_url() + path
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with httpx.Client(verify=False, timeout=30.0) as client:
        response = client.request(method.upper(), url, json=payload, headers=headers)

    if response.status_code >= 400:
        detail = ""
        try:
            detail = response.json().get("detail") or response.text
        except Exception:
            detail = response.text
        raise RuntimeError(f"API {method.upper()} {path} failed ({response.status_code}): {detail}")

    return response.json() if response.content else {}


def _count_tokens_local(text: str, model: str = "gpt-4o") -> int:
    model_name = model or "gpt-4o"
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text or ""))


def _persist_message(role: str, content: str, model: str = "gpt-4o"):
    token = st.session_state.get("auth_token")
    db_thread_id = st.session_state.get("db_thread_id")
    if not token or not db_thread_id:
        return

    token_count = _count_tokens_local(content, model)
    input_tokens = token_count if role == "user" else 0
    output_tokens = token_count if role == "assistant" else 0

    st.session_state["session_input_tokens"] = int(st.session_state.get("session_input_tokens", 0)) + input_tokens
    st.session_state["session_output_tokens"] = int(st.session_state.get("session_output_tokens", 0)) + output_tokens
    st.session_state["session_total_tokens"] = int(st.session_state.get("session_total_tokens", 0)) + token_count

    try:
        _api_request(
            "POST",
            f"/api/v1/users/threads/{db_thread_id}/messages",
            token=token,
            payload={
                "role": role,
                "content": content,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            },
        )
    except Exception as exc:
        st.sidebar.warning(f"Message persistence failed: {exc}")


def _load_db_threads():
    token = st.session_state.get("auth_token")
    if not token:
        return []
    threads = _api_request("GET", "/api/v1/users/threads", token=token)
    st.session_state["db_threads"] = threads
    return threads


def _set_active_db_thread(thread_obj: dict):
    thread_id = int(thread_obj["id"])
    st.session_state["db_thread_id"] = thread_id
    st.session_state["thread_id"] = f"user-{st.session_state.get('user_profile', {}).get('id', 'na')}-thread-{thread_id}"

    token = st.session_state.get("auth_token")
    if not token:
        return

    messages = _api_request("GET", f"/api/v1/users/threads/{thread_id}/messages", token=token)
    st.session_state["messages"] = [
        {"role": m.get("role", "assistant"), "content": m.get("content", "")}
        for m in messages
    ]
    st.session_state["is_first_turn"] = len(st.session_state["messages"]) == 0


def _create_db_thread(title: str = "New Chat"):
    token = st.session_state.get("auth_token")
    if not token:
        raise RuntimeError("Login required to create thread")

    thread = _api_request("POST", "/api/v1/users/threads", token=token, payload={"title": title})
    threads = _load_db_threads()
    for t in threads:
        if int(t.get("id", -1)) == int(thread.get("id", -2)):
            _set_active_db_thread(t)
            return t
    _set_active_db_thread(thread)
    return thread


def _extract_nse_ticker(text: str):
    match = re.search(r"\b[A-Za-z]{2,10}\.NS\b", text or "")
    return match.group(0).upper() if match else None


def _required_tools_for_query(text: str):
    q = (text or "").lower()
    tools_needed = []

    if any(k in q for k in ["fundamental", "earning", "annual report"]):
        tools_needed.append(FUNDAMENTAL_TOOL_NAME)

    if any(k in q for k in ["company news", "news"]):
        tools_needed.append("get_company_news")

    if _should_use_transcript_query(q):
        tools_needed.append("query_transcripts")

    if any(k in q for k in ["historical", "price movement", "price action", "trend", "past performance"]):
        tools_needed.extend(["analyze_memory", "analyze_stock"])

    if "swot" in q:
        tools_needed.append("swot_analysis")

    return list(dict.fromkeys(tools_needed))


def _should_use_transcript_query(text: str) -> bool:
    q = (text or "").lower()

    transcript_terms = [
        "transcript",
        "earnings call",
        "conference call",
        "management commentary",
        "q&a",
        "qa",
        "from the annual report",
        "from annual report",
        "from transcript",
    ]
    if any(term in q for term in transcript_terms):
        return True

    annual_report_question_terms = [
        "annual report summary",
        "summarize annual report",
        "summarise annual report",
        "annual report highlights",
        "what does the annual report",
        "what did the annual report",
        "according to the annual report",
    ]
    return any(term in q for term in annual_report_question_terms)


def _extract_tool_calls(messages):
    called = []
    for msg in messages or []:
        direct_calls = getattr(msg, "tool_calls", None)
        if isinstance(direct_calls, list):
            for call in direct_calls:
                if isinstance(call, dict):
                    name = call.get("name")
                    if name:
                        called.append(name)

        additional = getattr(msg, "additional_kwargs", {}) or {}
        ak_calls = additional.get("tool_calls") if isinstance(additional, dict) else None
        if isinstance(ak_calls, list):
            for call in ak_calls:
                if isinstance(call, dict):
                    fn = call.get("function", {})
                    if isinstance(fn, dict) and fn.get("name"):
                        called.append(fn["name"])

    return list(dict.fromkeys(called))


def _extract_latest_text(messages) -> str:
    for msg in reversed(messages or []):
        content = getattr(msg, "content", "")
        if str(content).strip():
            return str(content)
    return ""


def _get_loop() -> asyncio.AbstractEventLoop:
    loop = st.session_state.get("_event_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state["_event_loop"] = loop
    return loop


def _run_async(coro):
    loop = _get_loop()
    return loop.run_until_complete(coro)


def _find_web_tool(tools_by_name: dict[str, Any]):
    for name, tool in (tools_by_name or {}).items():
        lname = (name or "").lower()
        if "tavily" in lname or ("search" in lname and "news" not in lname):
            return tool
    return None


def _summarize_web_payload(payload: Any) -> str:
    if isinstance(payload, list):
        lines = []
        for item in payload[:3]:
            if isinstance(item, dict):
                title = item.get("title") or item.get("name") or "Untitled"
                url = item.get("url") or item.get("link") or ""
                snippet = item.get("content") or item.get("snippet") or ""
                lines.append(f"- {title}\n  {url}\n  {str(snippet)[:280]}")
            else:
                lines.append(f"- {str(item)[:320]}")
        return "\n".join(lines)
    if isinstance(payload, dict):
        return str({k: payload.get(k) for k in list(payload.keys())[:6]})
    return str(payload)


def _web_fallback_context(user_input: str, failed_tools: list[str], tools_by_name: dict[str, Any]) -> str:
    web_tool = _find_web_tool(tools_by_name)
    if web_tool is None:
        return ""

    try:
        payload = _run_async(web_tool.ainvoke({"query": user_input}))
        summarized = _summarize_web_payload(payload)
        if not summarized.strip():
            return ""
        return (
            "\n\nFallback web context used because some tools failed ("
            + ", ".join(failed_tools)
            + "):\n"
            + summarized
        )
    except Exception:
        return ""


async def _tool_calling_llm(state: State):
    react_agent = st.session_state["react_agent"]
    result = await react_agent.ainvoke({"messages": state["messages"]})

    if isinstance(result, dict) and result.get("messages"):
        return {"messages": [result["messages"][-1]]}

    return {}


async def _build_graph_and_tools():
    # MCP stdio on Windows expects stderr.fileno(); Jupyter/hosted streams may not implement it.
    if isinstance(sys.stderr, ipykernel.iostream.OutStream):
        try:
            sys.stderr.fileno()
        except io.UnsupportedOperation:
            ipykernel.iostream.OutStream.fileno = lambda self: 2

    load_dotenv()

    # Ensure API key is loaded for MCP subprocesses
    if not os.environ.get("OPENAI_API_KEY"):
        try:
            key_file = os.path.join(os.getcwd(), "OpenAI-Key.txt")
            if os.path.exists(key_file):
                with open(key_file) as f:
                    api_key_value = f.readline().strip()
                    if api_key_value:
                        os.environ["OPENAI_API_KEY"] = api_key_value
        except Exception:
            pass

    mcp_base: dict[str, Any] = {
        "command": sys.executable,
        "transport": "stdio",
        "cwd": os.getcwd(),
        "env": {**os.environ},  # Pass parent process environment to subprocess
    }

    stock_conn: dict[str, Any] = {
        "stock-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "stock_aggregator"],
        }
    }
    stock_mcp_client = MultiServerMCPClient(
        stock_conn
    )

    allocation_conn: dict[str, Any] = {
        "allocation-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "allocation_agent"],
        }
    }
    allocation_mcp_client = MultiServerMCPClient(
        allocation_conn
    )

    portfolio_conn: dict[str, Any] = {
        "portfolio-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "portfolio_agent"],
        }
    }
    portfolio_mcp_client = MultiServerMCPClient(
        portfolio_conn
    )

    correlation_conn: dict[str, Any] = {
        "correlation-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "correlation_agent"],
        }
    }
    correlation_mcp_client = MultiServerMCPClient(
        correlation_conn
    )

    fundamental_conn: dict[str, Any] = {
        "fundamental_annual_earnings-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "fundamental_documents_annual_earnings_agent"],
        }
    }
    fundamental_mcp_client = MultiServerMCPClient(
        fundamental_conn
    )

    memory_conn: dict[str, Any] = {
        "memory-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "memory_agent"],
        }
    }
    memory_mcp_client = MultiServerMCPClient(
        memory_conn
    )

    explain_conn: dict[str, Any] = {
        "explainability-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "explain_agent"],
        }
    }
    explainability_mcp_client = MultiServerMCPClient(
        explain_conn
    )

    qna_conn: dict[str, Any] = {
        "qna-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "qna_agent"],
        }
    }
    qna_mcp_client = MultiServerMCPClient(
        qna_conn
    )

    swot_conn: dict[str, Any] = {
        "swot-based_analyser": {
            **mcp_base,
            "args": ["apis/start_mcp_server.py", "swot_agent"],
        }
    }
    swot_mcp_client = MultiServerMCPClient(
        swot_conn
    )

    stock_mcp_tools = await stock_mcp_client.get_tools()
    allocation_mcp_tools = await allocation_mcp_client.get_tools()
    portfolio_mcp_tools = await portfolio_mcp_client.get_tools()
    correlation_mcp_tools = await correlation_mcp_client.get_tools()
    fundamental_mcp_tools = await fundamental_mcp_client.get_tools()
    memory_mcp_tools = await memory_mcp_client.get_tools()
    explainability_mcp_tools = await explainability_mcp_client.get_tools()
    qna_mcp_tools = await qna_mcp_client.get_tools()
    swot_mcp_tools = await swot_mcp_client.get_tools()

    tool_tavily = TavilySearch(max_results=2)

    tools = [
        *stock_mcp_tools,
        *allocation_mcp_tools,
        *portfolio_mcp_tools,
        *correlation_mcp_tools,
        *fundamental_mcp_tools,
        *memory_mcp_tools,
        *explainability_mcp_tools,
        *qna_mcp_tools,
        *swot_mcp_tools,
        tool_tavily,
    ]
    st.session_state["tools_by_name"] = {tool.name: tool for tool in tools if hasattr(tool, "name")}

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        http_client=httpx.Client(verify=False),
    )

    react_agent = create_react_agent(model=llm, tools=tools)
    st.session_state["react_agent"] = react_agent

    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", _tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition,
        {"tools": "tools", "__end__": END},
    )
    builder.add_edge("tools", "tool_calling_llm")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


def _init_state():
    if "graph" not in st.session_state:
        st.session_state["graph"] = None

    if "graph_init_error" not in st.session_state:
        st.session_state["graph_init_error"] = None

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "last_ticker" not in st.session_state:
        st.session_state["last_ticker"] = None

    if "is_first_turn" not in st.session_state:
        st.session_state["is_first_turn"] = True

    if "last_called_tools" not in st.session_state:
        st.session_state["last_called_tools"] = []

    if "tools_by_name" not in st.session_state:
        st.session_state["tools_by_name"] = {}

    if "auth_token" not in st.session_state:
        st.session_state["auth_token"] = None

    if "user_profile" not in st.session_state:
        st.session_state["user_profile"] = None

    if "db_threads" not in st.session_state:
        st.session_state["db_threads"] = []

    if "db_thread_id" not in st.session_state:
        st.session_state["db_thread_id"] = None

    if "session_input_tokens" not in st.session_state:
        st.session_state["session_input_tokens"] = 0

    if "session_output_tokens" not in st.session_state:
        st.session_state["session_output_tokens"] = 0

    if "session_total_tokens" not in st.session_state:
        st.session_state["session_total_tokens"] = 0


def _sync_auth_from_query_params():
    params = st.query_params
    token_from_query = params.get("token")
    email_from_query = params.get("email")

    if isinstance(token_from_query, list):
        token_from_query = token_from_query[0] if token_from_query else None
    if isinstance(email_from_query, list):
        email_from_query = email_from_query[0] if email_from_query else None

    token_from_query = (token_from_query or "").strip()
    email_from_query = (email_from_query or "").strip()

    if not token_from_query:
        return

    token_changed = token_from_query != st.session_state.get("auth_token")
    if token_changed:
        st.session_state["auth_token"] = token_from_query

        try:
            profile = _api_request("GET", "/api/v1/users/me", token=token_from_query)
        except Exception as exc:
            st.session_state["auth_token"] = None
            st.session_state["user_profile"] = None
            st.session_state["db_threads"] = []
            st.session_state["db_thread_id"] = None
            st.session_state["messages"] = []
            st.session_state["is_first_turn"] = True
            st.error(f"Session validation failed: {exc}")
            st.stop()

        if not isinstance(profile, dict):
            profile = {}

        if email_from_query and not profile.get("email"):
            profile["email"] = email_from_query

        st.session_state["user_profile"] = profile
        threads = _load_db_threads()
        if threads and not st.session_state.get("db_thread_id"):
            _set_active_db_thread(threads[0])
    else:
        profile = st.session_state.get("user_profile") or {}
        if email_from_query and not profile.get("email"):
            profile["email"] = email_from_query
            st.session_state["user_profile"] = profile


def _tool_args_for_name(tool_name: str, user_input: str, ticker: str | None, force_refresh_qna: bool):
    if tool_name == FUNDAMENTAL_TOOL_NAME:
        return {"symbol": ticker} if ticker else None

    if tool_name == "analyze_memory":
        return {"symbol": ticker} if ticker else None

    if tool_name == "analyze_stock":
        return {"symbol": ticker} if ticker else None

    if tool_name == "swot_analysis":
        return {"ticker": ticker} if ticker else None

    if tool_name == "get_company_news":
        return {"company_slug": ticker} if ticker else None

    if tool_name == "query_transcripts":
        return {
            "company_slug": ticker,
            "query": user_input,
            "force_refresh": force_refresh_qna,
        } if ticker else None

    return None


def _format_direct_tool_result(tool_name: str, payload: Any) -> str:
    if isinstance(payload, dict):
        if tool_name == FUNDAMENTAL_TOOL_NAME and isinstance(payload.get("report"), dict):
            return str(payload["report"])
        if tool_name in {"analyze_memory", "analyze_explain"} and isinstance(payload.get("report"), dict):
            return str(payload["report"])
        if tool_name == "analyze_stock" and isinstance(payload.get("data"), dict):
            return str(payload["data"])
        if tool_name == "swot_analysis" and isinstance(payload.get("swot"), dict):
            return str(payload["swot"])
        if tool_name == "get_company_news" and isinstance(payload.get("news"), list):
            return str(payload["news"])
        if tool_name == "query_transcripts" and isinstance(payload.get("results"), list):
            return str(payload["results"])
    return str(payload)


def _run_direct_tools(required_tools: list[str], user_input: str, force_refresh_qna: bool):
    ticker = st.session_state.get("last_ticker") or _extract_nse_ticker(user_input)
    if ticker:
        st.session_state["last_ticker"] = ticker

    tools_by_name = st.session_state.get("tools_by_name", {})
    direct_results = []
    called_tools = []
    failed_tools = []

    for tool_name in required_tools:
        tool = tools_by_name.get(tool_name)
        if tool is None:
            continue

        tool_args = _tool_args_for_name(tool_name, user_input, ticker, force_refresh_qna)
        if tool_args is None:
            continue

        try:
            payload = _run_async(tool.ainvoke(tool_args))
            called_tools.append(tool_name)
            direct_results.append(f"Tool {tool_name} output:\n{_format_direct_tool_result(tool_name, payload)}")
        except Exception as exc:
            failed_tools.append(tool_name)
            direct_results.append(
                f"Tool {tool_name} failed with error: {str(exc)}. "
                "Continue with available context and avoid stopping the response."
            )

    if failed_tools:
        web_context = _web_fallback_context(user_input, failed_tools, tools_by_name)
        if web_context:
            direct_results.append(web_context)

    return direct_results, called_tools, failed_tools


def _build_augmented_prompt(user_input: str, force_refresh_qna: bool):
    required_tools = _required_tools_for_query(user_input)

    detected_ticker = _extract_nse_ticker(user_input)
    if detected_ticker:
        st.session_state["last_ticker"] = detected_ticker

    directive_lines = []
    if st.session_state["last_ticker"]:
        directive_lines.append(f"Known ticker in this thread: {st.session_state['last_ticker']}")
        directive_lines.append("Do not ask for ticker again unless user asks to change it.")
    else:
        directive_lines.append("Ticker is currently unknown. Ask once for NSE ticker only if needed.")

    if required_tools:
        directive_lines.append(
            "Before final answer, you MUST call these tools when relevant: " + ", ".join(required_tools)
        )

    if "query_transcripts" in required_tools:
        directive_lines.append(f"For query_transcripts, set force_refresh={str(force_refresh_qna)}")

    augmented_user_input = user_input
    if directive_lines:
        augmented_user_input = user_input + "\n\nExecution directives:\n- " + "\n- ".join(directive_lines)

    return augmented_user_input, required_tools


def _ask_graph(user_input: str, force_refresh_qna: bool):
    if st.session_state["graph"] is None:
        with st.spinner("Initializing MCP tools and chat graph..."):
            try:
                st.session_state["graph"] = _run_async(_build_graph_and_tools())
                st.session_state["graph_init_error"] = None
            except Exception as exc:
                st.session_state["graph_init_error"] = str(exc)
                raise

    graph = st.session_state["graph"]
    augmented_user_input, required_tools = _build_augmented_prompt(user_input, force_refresh_qna)

    direct_results, direct_called_tools, failed_tools = _run_direct_tools(required_tools, user_input, force_refresh_qna)
    if direct_results:
        direct_context = "\n\nVerified tool outputs:\n" + "\n\n".join(direct_results)
        augmented_user_input += direct_context

    if st.session_state["is_first_turn"]:
        turn_messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=augmented_user_input),
        ]
        st.session_state["is_first_turn"] = False
    else:
        turn_messages = [HumanMessage(content=augmented_user_input)]

    try:
        result = _run_async(
            graph.ainvoke(
                {"messages": turn_messages},
                config={"configurable": {"thread_id": st.session_state["thread_id"]}},
            )
        )
    except Exception as exc:
        tools_by_name = st.session_state.get("tools_by_name", {})
        web_context = _web_fallback_context(user_input, failed_tools or ["graph_invoke"], tools_by_name)
        fallback_text = (
            "Some analysis tools failed during this turn, so I continued with a fallback path."
            f"\nError summary: {str(exc)}"
        )
        if web_context:
            fallback_text += "\n\n" + web_context
        called_tools = list(dict.fromkeys(direct_called_tools + (["web_fallback"] if web_context else [])))
        st.session_state["last_called_tools"] = called_tools
        return fallback_text, required_tools, called_tools

    messages = result.get("messages", [])
    called_tools = _extract_tool_calls(messages)
    if direct_called_tools:
        called_tools = list(dict.fromkeys(direct_called_tools + called_tools))
    st.session_state["last_called_tools"] = called_tools

    bot_text = _extract_latest_text(messages)

    return bot_text, required_tools, called_tools


def main():
    st.set_page_config(page_title="Stock Analyzer", page_icon="chart_with_upwards_trend", layout="wide")
    st.title("Stock Analyzer")
    st.caption("Stock analysis chat thread")

    _init_state()
    _sync_auth_from_query_params()

    with st.sidebar:
        st.subheader("Controls")
        force_refresh_qna = False

        st.markdown("---")
        st.subheader("Account")

        if not st.session_state.get("auth_token"):
            st.warning("No active session found. Please login from the main web app and reopen Streamlit.")
            st.stop()

        profile = st.session_state.get("user_profile") or {}
        st.caption(f"Logged in as {profile.get('email', 'user')}")

        if st.button("Refresh threads"):
            try:
                _load_db_threads()
            except Exception as exc:
                st.error(str(exc))

        if st.button("New cloud thread"):
            try:
                _create_db_thread("New Chat")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        threads = st.session_state.get("db_threads", [])
        if threads:
            options = {f"{t.get('title', 'Untitled')} (#{t.get('id')})": t for t in threads}
            selected_label = st.selectbox("Cloud thread", list(options.keys()))
            selected = options[selected_label]
            if st.session_state.get("db_thread_id") != int(selected.get("id")):
                try:
                    _set_active_db_thread(selected)
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

        st.markdown("---")
        st.subheader("Session Token Usage")
        st.write(f"Input: {st.session_state.get('session_input_tokens', 0)}")
        st.write(f"Output: {st.session_state.get('session_output_tokens', 0)}")
        st.write(f"Total: {st.session_state.get('session_total_tokens', 0)}")

        if st.session_state["graph"] is None:
            st.warning("Backend not initialized yet. It will start when you send the first message.")
        else:
            st.success("Backend initialized")

        if st.session_state.get("graph_init_error"):
            st.error("Last initialization error: " + st.session_state["graph_init_error"])

        if st.button("Reset chat session"):
            st.session_state["thread_id"] = str(uuid.uuid4())
            st.session_state["messages"] = []
            st.session_state["last_ticker"] = None
            st.session_state["is_first_turn"] = True
            st.session_state["last_called_tools"] = []
            st.session_state["graph"] = None
            st.session_state["graph_init_error"] = None
            st.session_state["session_input_tokens"] = 0
            st.session_state["session_output_tokens"] = 0
            st.session_state["session_total_tokens"] = 0
            st.rerun()

        st.write(f"Thread: {st.session_state['thread_id']}")

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about stock analysis, fundamentals, transcripts, memory trends, SWOT...")

    if prompt:
        if st.session_state.get("auth_token") and not st.session_state.get("db_thread_id"):
            try:
                _create_db_thread(prompt[:50] if prompt else "New Chat")
            except Exception as exc:
                st.sidebar.warning(f"Could not create cloud thread: {exc}")

        st.session_state["messages"].append({"role": "user", "content": prompt})
        _persist_message("user", prompt, model="gpt-4o")
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_text, _, _ = _ask_graph(prompt, force_refresh_qna)

            if not bot_text:
                bot_text = "I could not generate a response. Please try again."

            st.markdown(bot_text)

        st.session_state["messages"].append({"role": "assistant", "content": bot_text})
        _persist_message("assistant", bot_text, model="gpt-4o")


if __name__ == "__main__":
    main()
