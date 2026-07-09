import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Load the cleaned/reduced dataset from Deliverable 1's data prep step
# ============================================================
df = pd.read_csv("sbux_reduced.csv")

# ============================================================
# STORY 1: "Price is the sore spot"
# Average rating across all 7 satisfaction categories, sorted low to high
# ============================================================
rating_cols = [
    "Rating_Price", "Rating_WiFi", "Rating_LikelyReturn", "Rating_Quality",
    "Rating_Service", "Rating_Ambiance", "Rating_Promotions"
]
# rename for cleaner x-axis labels
label_map = {
    "Rating_Price": "Price",
    "Rating_WiFi": "WiFi",
    "Rating_LikelyReturn": "Likely to Return",
    "Rating_Quality": "Quality",
    "Rating_Service": "Service",
    "Rating_Ambiance": "Ambiance",
    "Rating_Promotions": "Promotions"
}

avg_ratings = df[rating_cols].mean().sort_values()
avg_ratings.index = [label_map[c] for c in avg_ratings.index]

plt.figure(figsize=(8, 5))
bars = plt.bar(avg_ratings.index, avg_ratings.values, color="#4B2E1E")
plt.axhline(y=avg_ratings.mean(), color="gray", linestyle="--", linewidth=1, label="Overall average")
plt.title("Average Satisfaction Rating by Category")
plt.ylabel("Average Rating (1-5 scale)")
plt.ylim(0, 5)
plt.xticks(rotation=30, ha="right")
plt.legend()

# add value labels on top of bars
for bar, value in zip(bars, avg_ratings.values):
    plt.text(bar.get_x() + bar.get_width()/2, value + 0.05, f"{value:.2f}",
              ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("story1_price_gap.png", dpi=200)
plt.show()

print("Story 1 - Average ratings sorted low to high:")
print(avg_ratings)

# ============================================================
# STORY 2: "Membership predicts loyalty"
# Membership rate among those who will continue buying vs. those who won't
# ============================================================
membership_pct = (
    df.groupby("Continue")["Membership"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reindex(["No", "Yes"])  # No = won't continue, Yes = will continue
)

plt.figure(figsize=(6, 5))
bars2 = plt.bar(
    ["Won't Continue", "Will Continue"],
    membership_pct.values,
    color=["#B0B0B0", "#00704A"]  # neutral gray vs Starbucks green
)
plt.title("Membership Rate by Customer Loyalty Status")
plt.ylabel("% Holding a Membership Card")
plt.ylim(0, 100)

for bar, value in zip(bars2, membership_pct.values):
    plt.text(bar.get_x() + bar.get_width()/2, value + 2, f"{value:.1f}%",
              ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.savefig("story2_membership_loyalty.png", dpi=200)
plt.show()

print("\nStory 2 - Membership rate by loyalty status:")
print(membership_pct)
