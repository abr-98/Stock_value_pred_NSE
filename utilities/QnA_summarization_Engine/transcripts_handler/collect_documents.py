from utilities.QnA_summarization_Engine.transcripts_handler.read_transcripts import read_transcripts_from_database
from utilities.QnA_summarization_Engine.transcripts_handler.get_annual_reports_feed import get_annual_reports_feed
from utilities.QnA_summarization_Engine.transcripts_handler.download_pdf import download_pdf
import shutil
import os


def collect_documents_for_company(company_slug, workspace_root=None):
    if workspace_root is None:
        workspace_root = os.getcwd()
    
    transcript__paths = read_transcripts_from_database(company_slug)
    path = workspace_root
    
    if os.path.exists("documents"):
        shutil.rmtree("documents")  # deletes folder recursively
    
    os.mkdir("documents")
    
    annual_reports = get_annual_reports_feed(company_slug)
    path_downloadable = download_pdf(annual_reports, f"documents/{company_slug}.pdf")
    
    for filepath in transcript__paths:
        print(filepath)
        full_path = os.path.join(path, filepath.replace("//", "/"))
        shutil.copy(full_path, "documents/")
    