import yfinance as yf

def swot_absolute(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow

    swot = {
        "Strengths": [],
        "Weaknesses": [],
        "Opportunities": [],
        "Threats": []
    }
    


    # --- Strengths ---
    if info.get("returnOnEquity", 0) > 0.15:
        swot["Strengths"].append("High ROE")

    if info.get("revenueGrowth", 0) > 0.1:
        swot["Strengths"].append("Strong revenue growth")

    if info.get("profitMargins", 0) > 0.15:
        swot["Strengths"].append("Healthy profit margins")

    # --- Weaknesses ---
    if info.get("debtToEquity", 0) > 150:
        swot["Weaknesses"].append("High debt")

    if info.get("freeCashflow", 1) < 0:
        swot["Weaknesses"].append("Negative cash flow")

    # --- Opportunities ---
    if info.get("earningsGrowth", 0) > 0.1:
        swot["Opportunities"].append("Earnings expansion potential")

    # --- Threats ---
    if info.get("beta", 0) > 1.5:
        swot["Threats"].append("High volatility risk")

    if info.get("trailingPE", 0) > 40:
        swot["Threats"].append("Overvaluation risk")

    return swot