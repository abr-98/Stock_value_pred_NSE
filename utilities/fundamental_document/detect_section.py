def detect_section(text):
    normalized_text = text.lower()
    section_keywords = {
        "Management Discussion": [
            "management discussion",
            "md&a",
            "management's discussion",
            "chairman message",
            "ceo message",
        ],
        "Risk": [
            "risk",
            "uncertaint",
            "headwind",
            "litigation",
            "cybersecurity",
            "internal control",
        ],
        "Financial": [
            "financial",
            "revenue",
            "profit",
            "ebit",
            "ebitda",
            "cash flow",
            "balance sheet",
            "income statement",
        ],
        "Business Overview": [
            "business overview",
            "about the company",
            "our business",
            "segment",
            "customers",
            "markets",
        ],
        "Strategy": [
            "strategy",
            "capital allocation",
            "investment",
            "acquisition",
            "dividend",
            "buyback",
        ],
        "Outlook": [
            "outlook",
            "guidance",
            "future",
            "pipeline",
            "opportunity",
            "priorities",
        ],
        "Corporate Governance": [
            "corporate governance",
            "board of directors",
            "committee",
            "compliance",
            "ethics",
        ],
    }
    for section, keywords in section_keywords.items():
        if any(keyword in normalized_text for keyword in keywords):
            return section
    return "Other"