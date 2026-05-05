from datetime import datetime
from utilities.fundamental_document.get_annual_reports_feed import get_annual_reports_feed
from utilities.fundamental_document.download_pdf import download_pdf
from utilities.fundamental_document.extract_pdf_text import extract_pdf_text
from utilities.fundamental_document.build_chunks import build_chunks
from utilities.fundamental_document.build_vector_store import build_vector_store
from utilities.fundamental_document.FundamentalRAGSystem import FundamentalRAGSystem
import sys

def get_company_earning_analysis(symbol):
    try:
        symbol = symbol.upper().replace(".NS", "")
        print(f"Starting fundamental analysis for {symbol}", file=sys.stderr)
        
        annual_report_url = get_annual_reports_feed(symbol)
        print(f"Found annual report URL for {symbol}", file=sys.stderr)
        
        path = download_pdf(annual_report_url, f"{symbol}.pdf")
        print(f"Downloaded PDF to {path}", file=sys.stderr)
        
        pages = extract_pdf_text(path)
        print(f"Extracted {len(pages)} pages from PDF", file=sys.stderr)
        
        documents = build_chunks(pages, company=symbol, year=datetime.now().year)
        print(f"Built {len(documents)} chunks from pages", file=sys.stderr)
        
        vectordb = build_vector_store(documents)
        print(f"Built vector store successfully", file=sys.stderr)

        system = FundamentalRAGSystem(vectordb)
        print(f"Created RAG system, starting interpretation for {symbol}", file=sys.stderr)
        
        interpretation = system.explain_company(symbol)
        print(f"Completed interpretation for {symbol}", file=sys.stderr)

        return interpretation
    except Exception as e:
        print(f"Error in get_company_earning_analysis: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise