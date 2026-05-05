from utilities.QnA_summarization_Engine.transcripts_handler.get_annual_reports_feed import get_annual_reports_feed
from utilities.QnA_summarization_Engine.transcripts_handler.download_pdf import download_pdf
import shutil
import os


def collect_documents_for_company(company_slug, force_refresh=False):
    # Documents are stored per company so one query does not invalidate another.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_root = os.path.join(current_dir, "documents")
    documents_dir = os.path.join(documents_root, company_slug)
    pdf_path = os.path.join(documents_dir, f"{company_slug}.pdf")

    if force_refresh and os.path.exists(documents_dir):
        shutil.rmtree(documents_dir)

    os.makedirs(documents_dir, exist_ok=True)

    if os.path.exists(pdf_path) and not force_refresh:
        return documents_dir

    annual_reports = get_annual_reports_feed(company_slug)
    download_pdf(annual_reports, pdf_path)
    return documents_dir
    