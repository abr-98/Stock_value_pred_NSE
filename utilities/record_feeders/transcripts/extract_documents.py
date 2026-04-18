from .classify_document import classify_document

def extract_documents(data):
    docs = {
        "transcript": [],
        "presentation": [],
        "results": []
    }

    for item in data:
        title = item.get("desc", "")
        url = item.get("attchmntFile")

        if not url:
            continue

        doc_type = classify_document(title)

        if doc_type in docs:
            docs[doc_type].append({
                "title": title,
                "url": url
            })

    return docs