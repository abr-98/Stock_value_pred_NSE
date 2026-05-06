from utilities.QnA_summarization_Engine.transcripts_handler.get_annual_reports_feed import get_annual_reports_feed
from utilities.QnA_summarization_Engine.transcripts_handler.download_pdf import download_pdf
import shutil
import os
import sys


def _normalize_company_slug(company_slug):
    return (company_slug or "").upper().replace(".NS", "").strip()


def _download_transcripts_from_db(company_slug, documents_dir):
    """
    Download transcript PDFs listed in the database for the company.
    Skips any URL that fails without aborting the whole collection step.
    Returns the number of transcripts successfully saved.
    """
    try:
        from utilities.QnA_summarization_Engine.transcripts_handler.read_transcripts import read_transcripts_from_database
        urls = read_transcripts_from_database(company_slug)
        if not urls:
            print(f"No transcript URLs found in database for {company_slug}", file=sys.stderr)
            return 0
        saved = 0
        for i, url in enumerate(urls, start=1):
            dest = os.path.join(documents_dir, f"{company_slug}_transcript_{i}.pdf")
            if os.path.exists(dest):
                print(f"Transcript {i} already cached, skipping", file=sys.stderr)
                saved += 1
                continue
            try:
                download_pdf(url, dest)
                print(f"Downloaded transcript {i} for {company_slug}", file=sys.stderr)
                saved += 1
            except Exception as exc:
                print(f"Failed to download transcript {i} ({url}): {exc}", file=sys.stderr)
        return saved
    except Exception as exc:
        print(f"Could not fetch transcripts from database for {company_slug}: {exc}", file=sys.stderr)
        return 0


def collect_documents_for_company(company_slug, force_refresh=False):
    """
    Collect all documents for a company: annual report PDF + earnings-call
    transcripts from the database.  Both are placed in the same per-company
    documents folder so the vector store builder indexes everything together.
    
    Args:
        company_slug: Company symbol (e.g., 'TCS', 'INFY')
        force_refresh: If True, re-download all documents
        
    Returns:
        Path to documents directory
        
    Raises:
        ValueError: If no documents can be found or downloaded
    """
    company_slug = _normalize_company_slug(company_slug)

    # Documents are stored per company so one query does not invalidate another.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_root = os.path.join(current_dir, "documents")
    documents_dir = os.path.join(documents_root, company_slug)
    annual_report_path = os.path.join(documents_dir, f"{company_slug}.pdf")

    if force_refresh and os.path.exists(documents_dir):
        shutil.rmtree(documents_dir)

    os.makedirs(documents_dir, exist_ok=True)

    # ── Annual report ──────────────────────────────────────────────────────────
    if os.path.exists(annual_report_path) and not force_refresh:
        print(f"Using cached annual report for {company_slug}", file=sys.stderr)
    else:
        try:
            print(f"Downloading annual report for {company_slug}...", file=sys.stderr)
            url = get_annual_reports_feed(company_slug)
            download_pdf(url, annual_report_path)
            print(f"Downloaded annual report to {annual_report_path}", file=sys.stderr)
        except Exception as e:
            print(f"Annual report download failed for {company_slug}: {e}", file=sys.stderr)
            # Non-fatal if transcripts cover the gap; handled below.

    # ── Transcripts from database ──────────────────────────────────────────────
    transcripts_saved = _download_transcripts_from_db(company_slug, documents_dir)
    print(
        f"Transcript documents available for {company_slug}: {transcripts_saved}",
        file=sys.stderr,
    )

    # ── Final health check ─────────────────────────────────────────────────────
    available = os.listdir(documents_dir)
    if not available:
        raise ValueError(
            f"No documents (annual report or transcripts) found for {company_slug}. "
            "Check NSE connectivity and database transcript entries."
        )

    print(
        f"Total documents collected for {company_slug}: {len(available)} file(s)",
        file=sys.stderr,
    )
    return documents_dir
