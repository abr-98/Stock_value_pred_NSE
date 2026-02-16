class InterpretationAgent:
    def __init__(self, llm):
        self.llm = llm

    def explain(self, reasoning_text, audience="investor"):
        prompt = f"""
        Convert the following analysis into clear language
        suitable for a {audience}.

        Do NOT add new analysis.
        Do NOT speculate.

        ANALYSIS:
        {reasoning_text}
        """

        return self.llm.predict(prompt)