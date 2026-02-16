def detect_section(text):
    SECTION_KEYWORDS = [
        "Management Discussion",
        "Risk",
        "Financial",
        "Business Overview",
        "Strategy",
        "Outlook",
        "Corporate Governance"
    ]
    for key in SECTION_KEYWORDS:
        if key.lower() in text.lower():
            return key
    return "Other"