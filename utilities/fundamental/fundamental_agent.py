from utilities.fundamental.valuation_indicators import valuation_indicators
from utilities.fundamental.roe_roic import roe_roic
from utilities.fundamental.margin_quality import margin_quality
from utilities.fundamental.earnings_quality import earnings_quality
from utilities.fundamental.growth_indicators import growth_indicators
from utilities.fundamental.health_indicators import health_indicators
from utilities.fundamental.event_markers import derive_events
from utilities.datafeeds.yfinance_config import yf
from utilities.fundamental.quarter_analysis import quarterly_analysis
from utilities.fundamental.governance_penalty import governance_penalty
from utilities.serialization_helper import convert_to_serializable


def fundamental_agent(ticker):
    t = yf.Ticker(ticker)

    result = {}
    result.update(valuation_indicators(t.info, t.income_stmt, t.cashflow))
    result.update(roe_roic(t.balance_sheet, t.income_stmt))
    result.update(margin_quality(t.income_stmt))
    result.update(earnings_quality(t.income_stmt))
    result.update(growth_indicators(t.income_stmt, t.quarterly_income_stmt, t.cash_flow))
    result.update(health_indicators(t.balance_sheet,t.income_stmt, t.info))
    result.update(quarterly_analysis(t.quarterly_income_stmt))

    result["governance_penalty"] = governance_penalty(t.info)

    # Convert all numpy/pandas types to Python native types
    return convert_to_serializable(result)
