from utilities.fundamental_document.detect_section import detect_section
from utilities.fundamental_document.chunk_text import chunk_text


def build_chunks(pages, company, year, source="annual_report"):
    """
    Convert extracted PDF pages into text chunks with metadata.

    Args:
        pages:  list of {"page": int, "text": str} dicts from extract_pdf_text.
        company: company slug / symbol.
        year:   publication year (integer).
        source: "annual_report" or "transcript" – stored in chunk metadata so
                retrieval can filter or display the origin of evidence.
    """
    docs = []
    for page in pages:
        section = detect_section(page["text"])
        chunks = chunk_text(page["text"])

        for chunk in chunks:
            docs.append({
                "text": chunk,
                "metadata": {
                    "company": company,
                    "year": year,
                    "section": section,
                    "page": page["page"],
                    "source": source,
                }
            })
    return docs
