from utilites.fundamental.utility import cagr

def margin_quality(income_a):
    revenue = income_a.loc["Total Revenue"]
    gross = income_a.loc["Gross Profit"]
    ebitda = income_a.loc["EBITDA"]
    ebit = income_a.loc["EBIT"]

    gm = gross / revenue
    ebitda_m = ebitda / revenue
    ebit_m = ebit / revenue

    return {
        "gross_margin": gm.iloc[0],
        "gross_margin_trend": cagr(gm),
        "ebitda_margin": ebitda_m.iloc[0],
        "ebit_margin_trend": cagr(ebit_m)
    }