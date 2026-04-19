def compute_roe(stock):
    try:
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        net_income = financials.loc["Net Income"].iloc[0]
        equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

        if equity == 0:
            return None

        return net_income / equity

    except Exception as e:
        print("ROE error:", e)
        return None