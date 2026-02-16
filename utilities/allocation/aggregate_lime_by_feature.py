from collections import defaultdict

def aggregate_lime_by_feature(explanation):
    agg = defaultdict(float)

    for name, weight in explanation.as_list():
        # t3_RSI > 52.1  → RSI
        feature = name.split("_", 1)[1].split(" ")[0]
        agg[feature] += weight

    return dict(sorted(agg.items(), key=lambda x: -abs(x[1])))
