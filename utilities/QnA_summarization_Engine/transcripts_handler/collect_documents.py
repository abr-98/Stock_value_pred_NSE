from utilities.QnA_summarization_Engine.transcripts_handler.get_annual_reports_feed import get_annual_reports_feed
from utilities.QnA_summarization_Engine.transcripts_handler.download_pdf import download_pdf
import shutil
import os
import sys

def collect_documents_for_company(company_slug, force_refresh=False):
    """
    Collect annual report documents for a company.
    
    Args:
        company_slug: Company symbol (e.g., 'TCS', 'INFY')
        force_refresh: If True, re-download documents
        
    Returns:
        Path to documents directory
        
    Raises:
        ValueError: If no documents can be found or downloaded
    """
    # Documents are stored per company so one query does not invalidate another.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_root = os.path.join(current_dir, "documents")
    documents_dir = os.path.join(documents_root, company_slug)
    pdf_path = os.path.join(documents_dir, f"{company_slug}.pdf")

    if force_refresh and os.path.exists(documents_dir):
        shutil.rmtree(documents_dir)

    os.makedirs(documents_dir, exist_ok=True)

    if os.path.exists(pdf_path) and not force_refresh:
        print(f"Using cached documents for {company_slug} from {pdf_path}", file=sys.stderr)
        return documents_dir

    try:
        print(f"Collecting documents for company {company_slug}...", file=sys.stderr)
        annual_reports = get_annual_reports_feed(company_slug)
        print(f"Fetched annual reports URL for {company_slug}: {annual_reports}", file=sys.stderr)
        
        download_pdf(annual_reports, pdf_path)
        print(f"Downloaded PDF to {pdf_path}", file=sys.stderr)
        
        return documents_dir
    except Exception as e:
        error_msg = f"Failed to collect documents for {company_slug}: {str(e)}"
        print(error_msg, file=sys.stderr)
        # Check if we have any cached documents as fallback
        if os.path.exists(documents_dir) and os.listdir(documents_dir):
            print(f"Using existing cached documents as fallback", file=sys.stderr)
            return documents_dir
        raise ValueError(error_msg)