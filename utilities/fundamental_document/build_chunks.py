from utilites.fundamental_document.detect_section import detect_section
from utilites.fundamental_document.chunk_text import chunk_text


def build_chunks(pages, company, year):
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
                    "page": page["page"]
                }
            })
    return docs
