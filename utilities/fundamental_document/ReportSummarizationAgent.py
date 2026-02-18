

class ReportSummarizationAgent:
    def __init__(self, llm):
        self.llm = llm

    def summarize(self, retrieved_docs):
      context = "\n\n".join(d.page_content for d in retrieved_docs)

      prompt = f"""
        You are an expert summarizer.

        Summarize ONLY factual content from the following company annual report text.
        Organize your output exactly in these labeled bullet points:

        BUSINESS MODEL:
        - Describe what the company does and its core segments.

        FINANCIAL TRENDS:
        - Key figures and trends (revenue, margins, profits, ratios).
        - Do NOT infer beyond what’s stated in the text.

        RISKS:
        - List specific risk categories described.

        MANAGEMENT OUTLOOK:
        - Statements describing future goals, strategy or guidance.

        KEY CHANGES:
        - Explicit changes from prior year that are factual and quantitative.

        TEXT:
        {context}
        """

      return self.llm.invoke(prompt).content