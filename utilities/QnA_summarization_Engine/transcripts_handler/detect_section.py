def detect_section(text):
    SECTION_KEYWORDS = [
        "Management Discussion",
        "Risk",
        "Financial",
        "Business Overview",
        "Strategy",
        "Outlook",
        "Corporate Governance",
        "Financial Results",
        "Financial Information",
        "performance",
        "presentation",
        "revenue",
        "ebitda",
        "growth",
        "subscriber",
        "market",
        "demand",
        "margin",
        "capex",
        "guidance",
        "outlook"
        
    ]
    for key in SECTION_KEYWORDS:
        if key.lower() in text.lower():
            return key
    return "Other"