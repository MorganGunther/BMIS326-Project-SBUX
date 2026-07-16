import pandas as pd

# ============================================================
# Load the cleaned/reduced dataset from Deliverable 1
# ============================================================
df = pd.read_csv("sbux_reduced.csv")

print("Starting shape:", df.shape)

# ============================================================
# NEW VARIABLE 1: Membership_Num
# Recode Membership (Yes/No) to numeric (1/0) for use in regression
# Reference category = "No" (0), since it's the more common response
# ============================================================
df["Membership_Num"] = df["Membership"].map({"No": 0, "Yes": 1})

print("\nMembership_Num check:")
print(df[["Membership", "Membership_Num"]].value_counts())

# ============================================================
# NEW VARIABLE 2: Continue_Num
# Recode Continue (Yes/No) to numeric (1/0) - this is the TARGET
# variable for the logistic regression model
# ============================================================
df["Continue_Num"] = df["Continue"].map({"No": 0, "Yes": 1})

print("\nContinue_Num check:")
print(df[["Continue", "Continue_Num"]].value_counts())

# ============================================================
# NEW VARIABLE 3: Age dummy variables
# Reference category = "Below 20" (dropped, becomes the baseline)
# Three new columns represent the other three age groups
#
# NOTE: We explicitly set Age as an ordered category here and drop
# "Below 20" by name (rather than relying on drop_first, which
# defaults to alphabetical order and would incorrectly drop
# "40 and above" instead once the category order is lost on CSV export)
# ============================================================
age_order = ["Below 20", "From 20 to 29", "From 30 to 39", "40 and above"]
df["Age"] = pd.Categorical(df["Age"], categories=age_order, ordered=True)

age_dummies = pd.get_dummies(df["Age"], prefix="Age")
age_dummies = age_dummies.drop(columns=["Age_Below 20"])  # set reference category
print("\nAge dummy columns created:", age_dummies.columns.tolist())

df = pd.concat([df, age_dummies], axis=1)

# Convert True/False to 1/0 for clarity in regression output
for col in age_dummies.columns:
    df[col] = df[col].astype(int)

print("\nAge dummy check:")
print(df[["Age"] + age_dummies.columns.tolist()].drop_duplicates())

# ============================================================
# NEW VARIABLE 4: VisitFrequency_Num
# Convert ordinal text to a 0-4 numeric scale
# ============================================================
freq_map = {
    "Never": 0,
    "Rarely": 1,
    "Monthly": 2,
    "Weekly": 3,
    "Daily": 4
}
df["VisitFrequency_Num"] = df["VisitFrequency"].map(freq_map)

print("\nVisitFrequency_Num check:")
print(df[["VisitFrequency", "VisitFrequency_Num"]].value_counts())

# ============================================================
# Confirm no missing values introduced by these transformations
# ============================================================
new_cols = ["Membership_Num", "Continue_Num", "VisitFrequency_Num"] + age_dummies.columns.tolist()
print("\nNull check on new columns (should all be 0):")
print(df[new_cols].isnull().sum())

# ============================================================
# Export updated dataset for modeling
# ============================================================
output_path = "sbux_modeling.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved modeling-ready dataset to: {output_path}")
print("Final shape:", df.shape)
