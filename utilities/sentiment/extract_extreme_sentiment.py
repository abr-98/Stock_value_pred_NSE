import numpy as np

POS_THRESH = 0.6
NEG_THRESH = -0.6


def extract_extremes(sentiments, pos_thresh=POS_THRESH, neg_thresh=NEG_THRESH):

    compounds = [s["compound"] for s in sentiments]

    positives = [c for c in compounds if c >= pos_thresh]
    negatives = [c for c in compounds if c <= neg_thresh]

    return {
        "positive_count": len(positives),
        "negative_count": len(negatives),
        "max_positive": max(positives) if positives else 0.0,
        "max_negative": min(negatives) if negatives else 0.0
    }
