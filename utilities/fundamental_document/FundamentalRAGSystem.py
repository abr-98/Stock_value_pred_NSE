import os
import sys
from langchain_openai import ChatOpenAI
from utilities.fundamental_document.ReportSummarizationAgent import ReportSummarizationAgent
from utilities.fundamental_document.FundamentalReasoningAgent import FundamentalReasoningAgent
from utilities.fundamental_document.InterpretationAgent import InterpretationAgent

class FundamentalRAGSystem:
    def __init__(self, vectordb):
        self.vectordb = vectordb
        
        # Ensure API key is available
        if not os.environ.get("OPENAI_API_KEY"):
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
                key_file = os.path.join(project_root, "OpenAI-Key.txt")
                if os.path.exists(key_file):
                    with open(key_file) as f:
                        api_key_value = f.readline().strip()
                        if api_key_value:
                            os.environ["OPENAI_API_KEY"] = api_key_value
            except Exception as e:
                print(f"Warning: Could not auto-load API key: {e}", file=sys.stderr)
        
        api_key = os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

        self.summarizer = ReportSummarizationAgent(self.llm)
        self.reasoner = FundamentalReasoningAgent(self.llm)
        self.interpreter = InterpretationAgent(self.llm)

    def retrieve(self, query, company, k=8):
        try:
            # Try with filter first for better performance
            return self.vectordb.similarity_search(
                query,
                k=k,
                filter={"company": company}
            )
        except Exception as e:
            # Fall back to retrieving all results and filtering in Python
            # This handles ChromaDB API changes or incompatibilities
            try:
                all_results = self.vectordb.similarity_search(query, k=k*3)
                filtered_results = [
                    doc for doc in all_results 
                    if doc.metadata.get("company") == company
                ][:k]
                return filtered_results
            except Exception:
                # If even that fails, return an empty list or raise a more informative error
                print(f"Error retrieving documents for company: {company}", file=__import__('sys').stderr)
                return []

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