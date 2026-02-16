import numpy as np
from utilites.allocation.check_trend import check_trend
from utilites.model_utilities.predict_lstm import predict_lstm
from utilites.allocation.trend_strength import trend_strength
from utilites.allocation.sector_score import score_sector
from utilites.model_utilities.explain_lstm_instance import explain_lstm_instance

class UnifiedSectorAllocatorAgent:
    def __init__(
        self,
        threshold=0.3,
        max_weight=0.30,
        trend_lookback=50,
        trend_weight=0.6,
        regime_weight=0.4
    ):
        self.threshold = threshold
        self.max_weight = max_weight
        self.trend_lookback = trend_lookback
        self.trend_weight = trend_weight
        self.regime_weight = regime_weight

    def trend_bias(self, trend):
        return {
            "STRONG_UPTREND": 1.5,
            "WEAK_UPTREND": 0.7,
            "RANGE": 0.0,
            "WEAK_DOWNTREND": -0.7,
            "STRONG_DOWNTREND": -1.5
        }.get(trend, 0.0)

    def explain_sector(self, model, X_seq, feature_names, device="cpu"):
        return explain_lstm_instance(
            model=model,
            X_seq=X_seq,
            feature_names=feature_names,
            seq_len=X_seq.shape[0],
            n_features=X_seq.shape[1],
            device=device
        )

    def decide(
        self,
        nifty_df,
        nifty_X,
        nifty_model,
        sector_inputs,
        weights_existing=None,
        feature_names=None,
        device="cpu",
        explain=False
    ):
        nifty_trend = check_trend(nifty_df, self.trend_lookback)
        nifty_bias = self.trend_bias(nifty_trend)

        nifty_pred = predict_lstm(
            nifty_model, nifty_X[-1], device
        )

        scores = {}
        explanations = {}

        for sector, data in sector_inputs.items():

            # ---------- Gold / Silver ----------
            if sector in ["GOLDBEES", "SILVERBEES"]:
                df = data["df"]
                row = df.iloc[-1]

                sector_trend = check_trend(df, self.trend_lookback)
                bias = self.trend_bias(sector_trend)

                score = (
                    trend_strength(row) +
                    (-nifty_bias) * 1.2 +
                    bias * self.trend_weight
                )

                scores[sector] = score
                continue

            # ---------- No data / no model ----------
            if sector in ["OIL & GAS", "HEALTHCARE"]:
                df = data["df"]
                row = df.iloc[-1]
                sector_trend = check_trend(df, self.trend_lookback)
                bias = self.trend_bias(sector_trend)

                score = (
                    trend_strength(row, no_adx=True) +
                    (-nifty_bias) * 1.2 +
                    bias * self.trend_weight
                )

                scores[sector] = score
                continue

            # ---------- Data present ----------
            df = data["df"]
            row = df.iloc[-1]

            sector_trend = check_trend(df, self.trend_lookback)
            sector_bias = self.trend_bias(sector_trend)

            # ML-backed
            if "model" in data and data["model"] is not None:
                pred = predict_lstm(
                    data["model"],
                    data["X"][-1],
                    device
                )

                base_score = score_sector(
                    row=row,
                    model_pred=pred
                )

                if explain and feature_names is not None:
                    explanations[sector] = self.explain_sector(
                        model=data["model"],
                        X_seq=data["X"],
                        feature_names=feature_names,
                        device=device
                    )

            # Non-ML fallback
            else:
                base_score = (
                    trend_strength(row) +
                    sector_bias * self.regime_weight
                )

            base_score += self.trend_weight * sector_bias

            if nifty_bias < 0 and sector_bias < 0:
                base_score -= 0.5

            scores[sector] = base_score

        if nifty_trend == "STRONG_DOWNTREND":
            scores = {
                k: v for k, v in scores.items()
                if k in ["GOLDBEES", "SILVERBEES"]
            }

        scores = {
            k: v for k, v in scores.items()
            if v > self.threshold
        }

        if not scores:
            alloc = {"CASH": 1.0}
        else:
            alloc = self.allocate(scores, existing_sector_weights=weights_existing)

        if explain:
            return alloc, explanations

        return alloc

    """def allocate(self, scores):
        keys = list(scores.keys())
        values = np.array(list(scores.values()))

        exp = np.exp(values - values.max())
        weights = exp / exp.sum()

        alloc = {
            k: min(w, self.max_weight)
            for k, w in zip(keys, weights)
        }

        total = sum(alloc.values())
        return {k: v / total for k, v in alloc.items()}
    """
    def allocate(self, scores, existing_sector_weights=None, concentration=2.0):
      """
      scores → opportunity strength
      existing_sector_weights → current portfolio exposure
      concentration → penalty intensity (higher = stronger diversification)
      """

      keys = list(scores.keys())
      values = np.array(list(scores.values()))

      # ---- Softmax opportunity weights ----
      exp = np.exp(values - values.max())
      base_weights = exp / exp.sum()

      # ---- Diversification adjustment ----
      if existing_sector_weights:

          penalties = np.array([
              1 / (1 + concentration * existing_sector_weights.get(k, 0.0))
              for k in keys
          ])

          adjusted_weights = base_weights * penalties
          adjusted_weights /= adjusted_weights.sum()

      else:
          adjusted_weights = base_weights

      # ---- Concentration cap ----
      alloc = {
          k: min(w, self.max_weight)
          for k, w in zip(keys, adjusted_weights)
      }

      # ---- Re-normalize ----
      total = sum(alloc.values())

      return {k: v / total for k, v in alloc.items()}

