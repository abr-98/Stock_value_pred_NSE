def hhi(weights: dict):
    return sum(w**2 for w in weights.values())

def effective_number(weights: dict):
    return 1 / hhi(weights) if hhi(weights) > 0 else 0