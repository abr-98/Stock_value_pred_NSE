import os
import shutil
from utilities.QnA_summarization_Engine.transcripts_handler.collect_documents import collect_documents_for_company
from utilities.QnA_summarization_Engine.transcripts_handler.build_chunks import build_chunks
from utilities.QnA_summarization_Engine.transcripts_handler.extract_pdf_text import extract_pdf_text
from utilities.QnA_summarization_Engine.transcripts_handler.build_vector_store import build_vector_store
from datetime import datetime
from apis.logging_config import setup_logging, log_service_io


logger = setup_logging("service-utility-qna-db-init")


def initiate_query_database(company_slug, force_refresh=False):
    log_service_io(logger, "utility.qna.db_init.request", inputs={"company_slug": company_slug})
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents", company_slug)
    persist_dir = os.path.join(current_dir, "transcripts_db", company_slug)

    has_persisted_store = os.path.isdir(persist_dir) and any(os.scandir(persist_dir))
    if has_persisted_store and not force_refresh:
        log_service_io(
            logger,
            "utility.qna.db_init.cache_hit",
            outputs={"company_slug": company_slug, "persist_dir": persist_dir},
        )
        return build_vector_store(documents=None, persist_dir=persist_dir)

    collect_documents_for_company(company_slug, force_refresh=force_refresh)

    if force_refresh and os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    files = os.listdir(documents_dir)
    log_service_io(
        logger,
        "utility.qna.db_init.documents",
        outputs={"documents_dir": documents_dir, "file_count": len(files)},
    )
    if not files:
        raise FileNotFoundError(f"No documents found for company '{company_slug}' in {documents_dir}.")

    all_documents = []
    for file in files:
        pages = extract_pdf_text(os.path.join(documents_dir, file))
        all_documents.extend(build_chunks(pages, company_slug, datetime.now().year))

    vectordb = build_vector_store(all_documents, persist_dir=persist_dir)

    log_service_io(logger, "utility.qna.db_init.response", outputs={"vectordb_initialized": True})
    return vectordb