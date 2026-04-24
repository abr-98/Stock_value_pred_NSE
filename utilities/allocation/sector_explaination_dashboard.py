import sys
from utilities.allocation.aggregate_lime_by_feature import aggregate_lime_by_feature

def sector_explanation_dashboard(
    allocation,
    explanations,
    top_k_features=5
):
    print("\n" + "=" * 80, file=sys.stderr)
    print("📊 SECTOR ALLOCATION EXPLANATION DASHBOARD", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    for sector, weight in allocation.items():
        print(f"\n🔹 Sector: {sector}", file=sys.stderr)
        print(f"   Allocation Weight: {weight:.2%}", file=sys.stderr)

        if sector not in explanations:
            print("   Explanation: Rule-based / Regime-driven", file=sys.stderr)
            continue

        explanation = explanations[sector]
        agg = aggregate_lime_by_feature(explanation)

        print("   Top Drivers:", file=sys.stderr)
        for feat, val in list(agg.items())[:top_k_features]:
            direction = "↑" if val > 0 else "↓"
            print(f"     {direction} {feat:<10s} {val:+.3f}", file=sys.stderr)
