def merge_swot(swot1, swot2):
    final = {}

    for key in ["Strengths", "Weaknesses", "Opportunities", "Threats"]:
        # combine + remove duplicates
        final[key] = list(set(swot1[key] + swot2[key]))

    return final