from utilities.allocation.aggregate_lime_by_feature import aggregate_lime_by_feature

def sector_explanation_dashboard(
    allocation,
    explanations,
    top_k_features=5
):
    print("\n" + "=" * 80)
    print("📊 SECTOR ALLOCATION EXPLANATION DASHBOARD")
    print("=" * 80)

    for sector, weight in allocation.items():
        print(f"\n🔹 Sector: {sector}")
        print(f"   Allocation Weight: {weight:.2%}")

        if sector not in explanations:
            print("   Explanation: Rule-based / Regime-driven")
            continue

        explanation = explanations[sector]
        agg = aggregate_lime_by_feature(explanation)

        print("   Top Drivers:")
        for feat, val in list(agg.items())[:top_k_features]:
            direction = "↑" if val > 0 else "↓"
            print(f"     {direction} {feat:<10s} {val:+.3f}")
