import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    pages = []

    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        text = page.get_text("text")   # best general-purpose mode

        if text.strip():
            pages.append({
                "page": i + 1,
                "text": text
            })

    return pages
