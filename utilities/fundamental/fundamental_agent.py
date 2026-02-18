from utilites.fundamental.valuation_indicators import valuation_indicators
from utilites.fundamental.roe_roic import roe_roic
from utilites.fundamental.margin_quality import margin_quality
from utilites.fundamental.earnings_quality import earnings_quality
from utilites.fundamental.growth_indicators import growth_indicators
from utilites.fundamental.health_indicators import health_indicators
from utilites.fundamental.event_markers import derive_events
from utilites.datafeeds.yfinance_config import yf
from utilites.fundamental.quarter_analysis import quarterly_analysis
from utilites.fundamental.governance_penalty import governance_penalty
from utilites.serialization_helper import convert_to_serializable


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
