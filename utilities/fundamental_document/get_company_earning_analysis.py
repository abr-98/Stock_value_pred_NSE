import time
from utilites.fundamental_document.get_annual_reports_feed import get_annual_reports_feed
from utilites.fundamental_document.download_pdf import download_pdf
from utilites.fundamental_document.extract_pdf_text import extract_pdf_text
from utilites.fundamental_document.build_chunks import build_chunks
from utilites.fundamental_document.build_vector_store import build_vector_store
from agents.FundamentalRAGSystem import FundamentalRAGSystem

def get_company_earning_analysis(symbol):
    annual_report_url = get_annual_reports_feed(symbol)
    path = download_pdf(annual_report_url, f"{symbol}.pdf")
    pages = extract_pdf_text(path)
    documents = build_chunks(pages, company=symbol, year=time.time.now().year)

    vectordb = build_vector_store(documents)

    system = FundamentalRAGSystem(vectordb)

    interpretation = system.explain_company(symbol)
    summarization, reasoning = system.analyze_company(symbol)

    return {
        "interpretation": interpretation,
        "summarization": summarization,
        "reasoning": reasoning
    }