import os
from utilities.QnA_summarization_Engine.transcripts_handler.collect_documents import collect_documents_for_company
from utilities.QnA_summarization_Engine.transcripts_handler.build_chunks import build_chunks
from utilities.QnA_summarization_Engine.transcripts_handler.extract_pdf_text import extract_pdf_text
from utilities.QnA_summarization_Engine.transcripts_handler.build_vector_store import build_vector_store
from datetime import datetime


def initiate_query_database(company_slug):
    # Determine documents folder relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents")
    
    if not os.path.exists(documents_dir):
        raise FileNotFoundError(f"Documents directory not found at {documents_dir}. Please run collect_documents_for_company first.")
    
    collect_documents_for_company(company_slug)
    
    files = os.listdir(documents_dir)
    for file in files:
        pages = extract_pdf_text(os.path.join(documents_dir, file))
        documents = build_chunks(pages, company_slug, datetime.now().year)
        vectordb = build_vector_store(documents)
    

    
    return vectordb