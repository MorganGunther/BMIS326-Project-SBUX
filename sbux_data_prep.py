import pandas as pd
import os

# ============================================================
# STEP 1: DATA ACCESS
# ============================================================
# Update this path to wherever the CSV lives on your Mac
file_path = "BMIS326_SBUXData.csv"
df = pd.read_csv(file_path)

print("Original shape:", df.shape)
print(df.columns.tolist())

# ============================================================
# STEP 2: DATA REDUCTION
# ============================================================
# Drop Timestamp (no analytical value) and Q19 (promotion channels,
# not tied to any of the 3 objectives)
cols_to_drop = [
    "Timestamp",
    "19. How do you come to hear of promotions at Coffee House? Check all that apply."
]
df_reduced = df.drop(columns=cols_to_drop)

print("\nShape after reduction:", df_reduced.shape)

# ============================================================
# STEP 3: DATA TRANSFORMATION - rename columns
# ============================================================
# Rename to short, code-friendly names
rename_map = {
    "1. Your Gender": "Gender",
    "2. Your Age": "Age",
    "3. Are you currently....?": "Employment",
    "4. What is your annual income?": "Income",
    "5. How often do you visit Coffee House?": "VisitFrequency",
    "6. How do you usually enjoy Coffee House?": "EnjoyMethod",
    "7. How much time do you normally  spend during your visit?": "VisitDuration",
    "8. The nearest Coffee House's outlet to you is...?": "NearestOutlet",
    "9. Do you have Coffee House membership card?": "Membership",
    "10. What do you most frequently purchase at Coffee House?": "PurchaseType",
    "11. On average, how much would you spend at Coffee House per visit?": "SpendPerVisit",
    "12. How would you rate the quality of Coffee House compared to other brands (Coffee Bean, Old Town White Coffee..) to be:": "Rating_Quality",
    "13. How would you rate the price range at Coffee House?": "Rating_Price",
    "14. How important are sales and promotions in your purchase decision?": "Rating_Promotions",
    "15. How would you rate the ambiance at Coffee House? (lighting, music, etc...)": "Rating_Ambiance",
    "16. You rate the WiFi quality at Coffee House as..": "Rating_WiFi",
    "17. How would you rate the service at Coffee House? (Promptness, friendliness, etc..)": "Rating_Service",
    "18. How likely you will choose Coffee House for doing business meetings or hangout with friends?": "Rating_LikelyReturn",
    "20. Will you continue buying Coffee House?": "Continue"
}
df_reduced = df_reduced.rename(columns=rename_map)

print("\nRenamed columns:", df_reduced.columns.tolist())

# ============================================================
# STEP 4: DATA CLEANING
# ============================================================

# --- Clean EnjoyMethod (Q6) ---
print("\nEnjoyMethod before cleaning:")
print(df_reduced["EnjoyMethod"].value_counts(dropna=False))

enjoy_cleanup = {
    "never": "Never",
    "Never buy": "Never",
    "I dont like coffee": "Never"
}
df_reduced["EnjoyMethod"] = df_reduced["EnjoyMethod"].replace(enjoy_cleanup)
df_reduced["EnjoyMethod"] = df_reduced["EnjoyMethod"].fillna("Unknown")

print("\nEnjoyMethod after cleaning:")
print(df_reduced["EnjoyMethod"].value_counts(dropna=False))

# --- Clean PurchaseType (Q10) ---
print("\nPurchaseType before cleaning:")
print(df_reduced["PurchaseType"].value_counts(dropna=False))

junk_values = [
    "Jaws chip", "cake", "Nothing", "Never buy any", "never", "Never"
]
df_reduced["PurchaseType"] = df_reduced["PurchaseType"].apply(
    lambda x: "Other/None" if x in junk_values else x
)

print("\nPurchaseType after cleaning:")
print(df_reduced["PurchaseType"].value_counts(dropna=False))

# --- Confirm rating columns are already clean ---
rating_cols = [
    "Rating_Quality", "Rating_Price", "Rating_Promotions",
    "Rating_Ambiance", "Rating_WiFi", "Rating_Service", "Rating_LikelyReturn"
]
print("\nRating columns null check (should all be 0):")
print(df_reduced[rating_cols].isnull().sum())
print("\nRating columns dtype check (should all be int64):")
print(df_reduced[rating_cols].dtypes)

# ============================================================
# STEP 5: DATA TRANSFORMATION - ordering + new column
# ============================================================

# Order Age as a proper category so charts sort logically
age_order = ["Below 20", "From 20 to 29", "From 30 to 39", "40 and above"]
df_reduced["Age"] = pd.Categorical(df_reduced["Age"], categories=age_order, ordered=True)

# New column: average satisfaction across the 7 rating categories
df_reduced["Avg_Satisfaction"] = df_reduced[rating_cols].mean(axis=1)

print("\nSample of Avg_Satisfaction:")
print(df_reduced[["Age", "Avg_Satisfaction"]].head())

# ============================================================
# STEP 6: EXPORT
# ============================================================
output_path = "sbux_reduced.csv"
df_reduced.to_csv(output_path, index=False)
print(f"\nSaved cleaned/reduced file to: {os.path.abspath(output_path)}")
print("Final shape:", df_reduced.shape)
