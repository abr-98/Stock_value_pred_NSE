import re

def classify_document(title):
    t = title.lower()

    # ---------------------------
    # 🎯 TRANSCRIPT
    # ---------------------------
    if (
        "transcript" in t or
        "earnings call" in t or
        re.search(r"q[1-4].*(call|transcript)", t)
    ):
        return "transcript"

    # ---------------------------
    # 📊 PRESENTATION
    # ---------------------------
    elif (
        "presentation" in t or
        "investor meet" in t or
        "analyst meet" in t
    ):
        return "presentation"

    # ---------------------------
    # 📈 RESULTS
    # ---------------------------
    elif (
        "result" in t or
        "financial result" in t or
        "quarter ended" in t
    ):
        return "results"

    # ---------------------------
    # ❓ OTHER
    # ---------------------------
    return "other"