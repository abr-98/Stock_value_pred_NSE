class FundamentalReasoningAgent:
    def __init__(self, llm):
        self.llm = llm

    def reason(self, summary_text):
      prompt = f"""
        You are a financial analyst.

        Based ONLY on the summary text below, write brief, factual points for:

        1. **Growth Quality** – is revenue or profit growth stable, volatile, accelerating, or slowing?
        2. **Margin Trend** – are margins expanding, contracting, stable? Include figures if present.
        3. **Risk Evolution** – what risk categories grew or reduced based on the summary?
        4. **Capital Allocation Intent** – what the company is spending on capex, dividends, buybacks, or strategic investments?

        If the summary text does NOT mention one of these, explicitly state:
        “Insufficient data to determine <bullet category>”.

        SUMMARY:
        {summary_text}
        """

      return self.llm.invoke(prompt).content
