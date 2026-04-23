from utilities.QnA_summarization_Engine.transcripts_handler.get_annual_reports_feed import get_annual_reports_feed
from utilities.QnA_summarization_Engine.transcripts_handler.download_pdf import download_pdf
import shutil
import os


def collect_documents_for_company(company_slug):
    # Documents folder is in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents")
    
    if os.path.exists(documents_dir):
        shutil.rmtree(documents_dir)  # deletes folder recursively
    
    os.mkdir(documents_dir)
    
    # Download annual reports PDF
    annual_reports = get_annual_reports_feed(company_slug)
    download_pdf(annual_reports, os.path.join(documents_dir, f"{company_slug}.pdf"))
    