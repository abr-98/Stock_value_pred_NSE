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
""".strip()


def _extract_nse_ticker(text: str):
    match = re.search(r"\b[A-Za-z]{2,10}\.NS\b", text or "")
    return match.group(0).upper() if match else None


def _required_tools_for_query(text: str):
    q = (text or "").lower()
    tools_needed = []

    if any(k in q for k in ["fundamental", "earning", "transcript", "annual report", "company news", "news"]):
        tools_needed.extend(["get_fundamental_report", "query_transcripts"])

    if any(k in q for k in ["historical", "price movement", "price action", "trend", "past performance"]):
        tools_needed.extend(["analyze_memory", "analyze_stock"])

    if "swot" in q:
        tools_needed.append("swot_analysis")

    return list(dict.fromkeys(tools_needed))


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


def _get_loop() -> asyncio.AbstractEventLoop:
    loop = st.session_state.get("_event_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state["_event_loop"] = loop
    return loop


def _run_async(coro):
    loop = _get_loop()
    return loop.run_until_complete(coro)


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

    api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=api_key,
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

    if st.session_state["is_first_turn"]:
        turn_messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=augmented_user_input),
        ]
        st.session_state["is_first_turn"] = False
    else:
        turn_messages = [HumanMessage(content=augmented_user_input)]

    result = _run_async(
        graph.ainvoke(
            {"messages": turn_messages},
            config={"configurable": {"thread_id": st.session_state["thread_id"]}},
        )
    )

    messages = result.get("messages", [])
    called_tools = _extract_tool_calls(messages)
    st.session_state["last_called_tools"] = called_tools

    bot_text = ""
    for msg in reversed(messages):
        content = getattr(msg, "content", "")
        if str(content).strip():
            bot_text = str(content)
            break

    return bot_text, required_tools, called_tools


def main():
    st.set_page_config(page_title="Stock Analyzer", page_icon="chart_with_upwards_trend", layout="wide")
    st.title("Stock Analyzer")
    st.caption("Stock analysis chat thread")

    _init_state()

    with st.sidebar:
        st.subheader("Controls")
        debug_tool_trace = st.checkbox("Show tool debug", value=True)
        force_refresh_qna = st.checkbox("Force refresh QnA index on transcript queries", value=False)

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
            st.rerun()

        st.write(f"Thread: {st.session_state['thread_id']}")

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about stock analysis, fundamentals, transcripts, memory trends, SWOT...")

    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_text, required_tools, called_tools = _ask_graph(prompt, force_refresh_qna)

            if not bot_text:
                bot_text = "I could not generate a response. Please try again."

            st.markdown(bot_text)

            if debug_tool_trace:
                st.info(
                    "required_tools="
                    + str(required_tools)
                    + "\n\ncalled_tools="
                    + str(called_tools)
                    + "\n\nforce_refresh_qna="
                    + str(force_refresh_qna)
                )

        st.session_state["messages"].append({"role": "assistant", "content": bot_text})


if __name__ == "__main__":
    main()
