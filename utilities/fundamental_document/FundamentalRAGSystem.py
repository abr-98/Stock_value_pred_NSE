from langchain_openai import ChatOpenAI
from utilities.fundamental_document.ReportSummarizationAgent import ReportSummarizationAgent
from utilities.fundamental_document.FundamentalReasoningAgent import FundamentalReasoningAgent
from utilities.fundamental_document.InterpretationAgent import InterpretationAgent

class FundamentalRAGSystem:
    def __init__(self, vectordb):
        self.vectordb = vectordb
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        self.summarizer = ReportSummarizationAgent(self.llm)
        self.reasoner = FundamentalReasoningAgent(self.llm)
        self.interpreter = InterpretationAgent(self.llm)

    def retrieve(self, query, company, k=8):
        return self.vectordb.similarity_search(
            query,
            k=k,
            filter={"company": company}
        )

    def summarize_company(self, company):
        docs_fiancial = self.retrieve("financial", company)
        docs_growth = self.retrieve("growth", company)
        docs_margin = self.retrieve("margin", company)
        docs_risk = self.retrieve("risk", company)
        docs_capital = self.retrieve("allocation", company)
        docs_goals = self.retrieve("goals", company)
        docs_changes = self.retrieve("changes", company)

        docs = docs_fiancial + docs_growth + docs_margin + docs_risk + docs_capital + docs_goals + docs_changes
        return self.summarizer.summarize(docs)

    def analyze_company(self, company):
        summary = self.summarize_company(company)
        reasoning = self.reasoner.reason(summary)
        return summary, reasoning

    def explain_company(self, company, audience="investor"):
        summary, reasoning = self.analyze_company(company)
        explanation = self.interpreter.explain(reasoning, audience)
        return explanation