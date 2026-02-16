def aggregate_weights(weights, group_map):
    agg = {}
    for asset, w in weights.items():
        group = group_map.get(asset, "Unknown")
        agg[group] = agg.get(group, 0) + w
    return agg