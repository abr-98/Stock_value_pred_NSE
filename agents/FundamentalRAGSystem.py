from langchain_openai import ChatOpenAI
from utilites.fundamental_document.ReportSummarizationAgent import ReportSummarizationAgent
from utilites.fundamental_document.FundamentalReasoningAgent import FundamentalReasoningAgent
from utilites.fundamental_document.InterpretationAgent import InterpretationAgent


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
        docs = self.retrieve("annual report summary", company)
        return self.summarizer.summarize(docs)

    def analyze_company(self, company):
        summary = self.summarize_company(company)
        reasoning = self.reasoner.reason(summary)
        return summary, reasoning

    def explain_company(self, company, audience="investor"):
        summary, reasoning = self.analyze_company(company)
        explanation = self.interpreter.explain(reasoning, audience)
        return {"explaination": explanation,
                "summary": summary}
