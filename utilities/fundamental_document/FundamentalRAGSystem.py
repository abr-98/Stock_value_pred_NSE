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
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        self.summarizer = ReportSummarizationAgent(self.llm)
        self.reasoner = FundamentalReasoningAgent(self.llm)
        self.interpreter = InterpretationAgent(self.llm)

    def _dedupe_docs(self, docs):
        unique_docs = []
        seen = set()

        for doc in docs:
            page = doc.metadata.get("page")
            section = doc.metadata.get("section")
            key = (page, section, doc.page_content[:200])
            if key in seen:
                continue
            seen.add(key)
            unique_docs.append(doc)

        return unique_docs

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

    def _retrieve_for_queries(self, company, queries, k_per_query=3):
        docs = []
        for query in queries:
            docs.extend(self.retrieve(query, company, k=k_per_query))
        return self._dedupe_docs(docs)

    def summarize_company(self, company):
        business_docs = self._retrieve_for_queries(company, [
            "business model segments services products customers markets geographies",
            "company overview operations segment mix business overview",
        ])
        financial_docs = self._retrieve_for_queries(company, [
            "revenue profit margin operating margin net profit cash flow return on capital financial performance",
            "financial statements highlights revenue growth profitability expenses working capital",
        ])
        risk_docs = self._retrieve_for_queries(company, [
            "risk factors uncertainties headwinds regulatory currency competition cybersecurity attrition",
            "principal risks internal control litigation macroeconomic risk",
        ])
        capital_docs = self._retrieve_for_queries(company, [
            "capital allocation dividend buyback capex acquisitions investments cash return to shareholders",
            "cash flow capital expenditure dividend policy treasury acquisition investment",
        ])
        outlook_docs = self._retrieve_for_queries(company, [
            "management outlook guidance strategy priorities demand pipeline future growth",
            "chairman message ceo message management discussion outlook strategic priorities",
        ])
        change_docs = self._retrieve_for_queries(company, [
            "compared with previous year increase decrease changed during the year improved declined",
            "year over year change margin expansion contraction new initiatives restructuring",
        ])

        docs = self._dedupe_docs(
            business_docs + financial_docs + risk_docs + capital_docs + outlook_docs + change_docs
        )
        return self.summarizer.summarize(docs)

    def analyze_company(self, company):
        summary = self.summarize_company(company)
        reasoning = self.reasoner.reason(summary)
        return summary, reasoning

    def explain_company(self, company, audience="investor"):
        summary, reasoning = self.analyze_company(company)
        explanation = self.interpreter.explain(reasoning, audience)
        return (
            "ANNUAL REPORT SUMMARY\n"
            f"{summary}\n\n"
            "ANALYSIS\n"
            f"{explanation}"
        )