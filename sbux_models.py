import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ============================================================
# STEP 1: LOAD DATA
# ============================================================
df = pd.read_csv("sbux_modeling.csv")

print("Shape:", df.shape)
print("\nAvailable columns:")
print(df.columns.tolist())

# NOTE: The PRD referred to the age predictors as Age_20to29, Age_30to39,
# Age_40plus, but the actual column names created in the modeling-prep
# step include the full category text (with spaces), since they were
# generated directly from the Age category labels. Using the real
# column names below rather than inventing new ones.
age_cols = ["Age_From 20 to 29", "Age_From 30 to 39", "Age_40 and above"]

# ============================================================
# MODEL 1: MULTIPLE LINEAR REGRESSION
# Predicting Avg_Satisfaction from Membership, VisitFrequency, and Age
# ============================================================
print("\n" + "=" * 60)
print("MODEL 1: Linear Regression - Predicting Avg_Satisfaction")
print("=" * 60)

model1_predictors = ["Membership_Num", "VisitFrequency_Num"] + age_cols
X1 = df[model1_predictors]
y1 = df["Avg_Satisfaction"]

# statsmodels requires manually adding a constant for the intercept
X1 = sm.add_constant(X1)

model1 = sm.OLS(y1, X1).fit()
print(model1.summary())

# --- Check for multicollinearity using VIF ---
# VIF is checked here because the three age dummy variables are related
# to each other by construction (a respondent is 1 in only one of them),
# which can distort coefficient estimates if not accounted for.
print("\nVariance Inflation Factors (VIF):")
vif_data = pd.DataFrame()
vif_data["Variable"] = X1.columns
vif_data["VIF"] = [variance_inflation_factor(X1.values, i) for i in range(X1.shape[1])]
print(vif_data)

# ============================================================
# MODEL 2: LOGISTIC REGRESSION
# Predicting Continue_Num from Membership, Avg_Satisfaction, VisitFrequency
# ============================================================
print("\n" + "=" * 60)
print("MODEL 2: Logistic Regression - Predicting Continue_Num")
print("=" * 60)

model2_predictors = ["Membership_Num", "Avg_Satisfaction", "VisitFrequency_Num"]
X2 = df[model2_predictors]
y2 = df["Continue_Num"]

# --- Full-data logistic regression for coefficients and p-values ---
X2_const = sm.add_constant(X2)
model2_full = sm.Logit(y2, X2_const).fit()
print(model2_full.summary())

# --- Train/test split for accuracy and confusion matrix ---
# 70/30 split with a fixed random_state so results are reproducible
X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.3, random_state=42
)

print(f"\nTraining set size: {X2_train.shape[0]} rows")
print(f"Testing set size: {X2_test.shape[0]} rows")

clf = LogisticRegression()
clf.fit(X2_train, y2_train)
y2_pred = clf.predict(X2_test)

accuracy = accuracy_score(y2_test, y2_pred)
print(f"\nModel 2 Accuracy on test set: {accuracy:.3f}")

cm = confusion_matrix(y2_test, y2_pred)
print("\nConfusion Matrix:")
print(cm)

# --- Display confusion matrix as a chart ---
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Won't Continue", "Will Continue"])
disp.plot(cmap="Greens")
plt.title("Model 2 Confusion Matrix")
plt.tight_layout()
plt.savefig("model2_confusion_matrix.png", dpi=200)
plt.show()

# ============================================================
# SUMMARY COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY: Basic Fit Comparison")
print("=" * 60)
print(f"Model 1 (Linear Regression) R-squared: {model1.rsquared:.3f}")
print(f"Model 2 (Logistic Regression) Accuracy: {accuracy:.3f}")
