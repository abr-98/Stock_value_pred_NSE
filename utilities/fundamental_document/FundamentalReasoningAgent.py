class FundamentalReasoningAgent:
    def __init__(self, llm):
        self.llm = llm

    def reason(self, summary_text):
        prompt = f"""
        You are a financial analyst.

        Based ONLY on the summary below, analyze:
        1. Growth quality
        2. Margin trend
        3. Risk evolution
        4. Capital allocation intent

        If information is insufficient, state so explicitly.

        SUMMARY:
        {summary_text}
        """

        return self.llm.predict(prompt)
