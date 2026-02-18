def build_sentiment_rationale(s: dict) -> str:
    """
    Deterministic rationale generator for sentiment diagnostics.

    s → output of sentiment MCP
    """

    rationale = []

    company_sent = s.get("company_sentiment")
    national_sent = s.get("national_sentiment")

    pos_news = s.get("company_positive_news")
    neg_news = s.get("company_negative_news")

    pressure = s.get("company_sentiment_pressure")
    shock = s.get("sentiment_shock")

    # =====================================================
    # ABSOLUTE SENTIMENT STATE
    # =====================================================

    if company_sent is not None:

        if company_sent > 0.3:
            rationale.append("Positive company sentiment regime")

        elif company_sent < -0.3:
            rationale.append("Negative company sentiment regime")

        else:
            rationale.append("Neutral company sentiment regime")

    if national_sent is not None:

        if national_sent > 0.3:
            rationale.append("Supportive national sentiment backdrop")

        elif national_sent < -0.3:
            rationale.append("Weak national sentiment backdrop")

    # =====================================================
    # NEWS FLOW IMBALANCE
    # =====================================================

    if pos_news is not None and neg_news is not None:

        if pos_news > neg_news:
            rationale.append("Positive news flow dominant")

        elif neg_news > pos_news:
            rationale.append("Negative news flow dominant")

        else:
            rationale.append("Balanced news flow")

    # =====================================================
    # SENTIMENT PRESSURE (VERY IMPORTANT)
    # =====================================================

    if pressure is not None:

        if pressure > 0.5:
            rationale.append("Elevated sentiment pressure → Narrative skewed")

        elif pressure < -0.5:
            rationale.append("Strong negative sentiment pressure → Persistent pessimism")

    # =====================================================
    # SENTIMENT SHOCK DETECTION
    # =====================================================

    if shock:
        rationale.append("Sentiment shock detected → Abrupt narrative shift")

    # =====================================================
    # CROSS-SIGNAL INTERPRETATION
    # =====================================================

    if company_sent is not None and national_sent is not None:

        if company_sent > 0 and national_sent < 0:
            rationale.append("Positive company tone vs weak macro backdrop")

        if company_sent < 0 and national_sent > 0:
            rationale.append("Company-specific weakness vs supportive macro tone")

    # =====================================================
    # DEFAULT SAFE CASE
    # =====================================================

    if not rationale:
        rationale.append("No dominant sentiment dynamics detected")

    return " | ".join(rationale)
