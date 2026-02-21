import pandas as pd

def build_impact_explaination_rationale(linear_exp: dict, tree_exp: pd.DataFrame) -> str:

    rationale = []

    # -----------------------------------------------------
    # Identify dominant features from tree
    # -----------------------------------------------------

    dominant_features = tree_exp.head(3).index.tolist()

    for feature in dominant_features:

        importance = float(tree_exp.loc[feature, "importance"])
        coef = linear_exp.get(feature, 0)

        strength = abs(coef)

        # -------------------------------------------------
        # Feature-specific interpretation logic
        # -------------------------------------------------

        if feature == "volatility":

            if coef > 0:
                rationale.append(
                    f"Volatility is a dominant driver (importance {importance:.2f}) → Higher volatility historically associated with stronger forward movement"
                )
            elif coef < 0:
                rationale.append(
                    f"Volatility is a dominant driver (importance {importance:.2f}) → Elevated volatility historically linked to weaker outcomes"
                )

        elif feature == "trend_strength":

            if coef > 0:
                rationale.append(
                    f"Trend strength meaningfully influences behaviour → Strong trends tend to support continuation dynamics"
                )
            elif coef < 0:
                rationale.append(
                    f"Trend strength exerts negative pressure → Strong trends historically prone to mean reversion"
                )

        elif feature == "distance_from_range":

            if coef > 0:
                rationale.append(
                    "Distance from trading range contributes positively → Breakout-like structures tend to persist"
                )
            elif coef < 0:
                rationale.append(
                    "Distance from trading range contributes negatively → Extended moves show reversion tendency"
                )

        elif feature == "volume_ratio":

            if coef > 0:
                rationale.append(
                    "Volume conditions provide supportive confirmation → Participation strength aligns with moves"
                )
            elif coef < 0:
                rationale.append(
                    "Volume conditions act as a moderating factor → High activity not translating into persistence"
                )

        # Generic fallback
        else:
            if coef != 0:
                direction = "positive" if coef > 0 else "negative"
                rationale.append(
                    f"{feature} materially affects model behaviour with {direction} influence"
                )

    # -----------------------------------------------------
    # Detect structural dominance pattern
    # -----------------------------------------------------

    top_feature = tree_exp.index[0]
    top_importance = float(tree_exp.iloc[0]["importance"])

    if top_importance > 0.35:
        rationale.append(
            f"Model behaviour primarily governed by {top_feature} → Regime sensitivity elevated"
        )

    # -----------------------------------------------------
    # Default safe fallback
    # -----------------------------------------------------

    if not rationale:
        rationale.append("Model explanations do not indicate strong directional bias")

    return " | ".join(rationale)
