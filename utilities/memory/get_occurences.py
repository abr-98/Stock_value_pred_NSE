import yfinance as yf
from utilities.memory.build_pattern_memory_from_yf import build_pattern_memory_from_yf
from utilities.memory.save_artifacts import save_artifacts
from utilities.memory.load_pattern_memory import load_pattern_memory
from utilities.memory.query_current_state import query_current_state
import os
import shutil

def get_occurences(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="max")

    ret = build_pattern_memory_from_yf(hist)

    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    if os.path.exists(f"artifacts/{symbol}"):
        shutil.rmtree(f"artifacts/{symbol}")

    os.mkdir(f"artifacts/{symbol}")
    save_artifacts(ret, path=f"artifacts/{symbol}")

    memory = load_pattern_memory(f"artifacts/{symbol}")

    diagnostics = query_current_state(hist, memory)
    return diagnostics

