def governance_penalty(info):
    return info.get("overallRisk", 5) / 10