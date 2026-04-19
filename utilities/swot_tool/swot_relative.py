def swot_relative(df, ticker):
    row = df[df["ticker"] == ticker].iloc[0]

    swot = {"Strengths": [], "Weaknesses": [], "Opportunities": [], "Threats": []}

    # Strengths (top 30%)
    if row["quality"] > 0.7:
        swot["Strengths"].append("High quality vs peers")

    if row["growth"] > 0.7:
        swot["Strengths"].append("Strong growth vs peers")

    # Weaknesses (bottom 30%)
    if row["leverage"] < 0.3:
        swot["Weaknesses"].append("High debt vs peers")

    if row["valuation"] < 0.3:
        swot["Weaknesses"].append("Expensive vs peers")

    # Opportunities (mid but improving)
    if 0.4 < row["growth"] < 0.7:
        swot["Opportunities"].append("Moderate growth potential")

    # Threats
    if row["quality"] < 0.4:
        swot["Threats"].append("Weak fundamentals vs peers")

    return swot