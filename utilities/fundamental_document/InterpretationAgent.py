class InterpretationAgent:
    def __init__(self, llm):
        self.llm = llm

    def explain(self, reasoning_text, audience="investor"):
      prompt = f"""
        You are an expert financial communicator.

        Convert the following analysis into clear, plain language suitable for an {audience}.
        Do NOT add new analysis or new facts.
        Just rewrite the analysis so it’s easier to understand.

        ANALYSIS:
        {reasoning_text}
        """

      return self.llm.invoke(prompt).content
