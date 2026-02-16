

class ReportSummarizationAgent:
    def __init__(self, llm):
        self.llm = llm

    def summarize(self, retrieved_docs):
        context = "\n\n".join(d.page_content for d in retrieved_docs)

        prompt = f"""
        Summarize the following company report text.
        Extract ONLY factual information.

        Structure your output as:
        - Business Model
        - Financial Trends
        - Risks
        - Management Outlook
        - Key Changes

        Do NOT add information not present in the text.

        TEXT:
        {context}
        """

        return self.llm.predict(prompt)