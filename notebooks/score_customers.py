import pandas as pd
import joblib


# ==========================================
# 1. LOAD DATA
# ==========================================

data_path = "data/processed/temporal_account_features.csv"
model_path = "models/churn_risk_model.joblib"

df = pd.read_csv(data_path)

model = joblib.load(model_path)


print("====================================")
print("CUSTOMER RISK SCORING")
print("====================================")

print("\nCustomers loaded:", len(df))


# ==========================================
# 2. PREPARE FEATURES
# ==========================================

drop_columns = [
    "account_id",
    "account_name",
    "signup_date",
    "churn_target"
]

X = df.drop(columns=drop_columns)


# ==========================================
# 3. PREDICT CHURN PROBABILITY
# ==========================================

print("\nCalculating churn probabilities...")

df["churn_probability"] = model.predict_proba(X)[:, 1]


# ==========================================
# 4. CALCULATE REVENUE AT RISK
# ==========================================

df["revenue_at_risk"] = (
    df["churn_probability"] * df["current_mrr"]
)


# ==========================================
# 5. CONVERT PROBABILITY TO PERCENTAGE
# ==========================================

df["churn_probability_percent"] = (
    df["churn_probability"] * 100
)


# ==========================================
# 6. SORT BY REVENUE AT RISK
# ==========================================

df = df.sort_values(
    by="revenue_at_risk",
    ascending=False
)


# ==========================================
# 7. SAVE RESULTS
# ==========================================

output_path = "data/processed/customer_risk_scores.csv"

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n====================================")
print("TOP 10 HIGH-RISK CUSTOMERS")
print("====================================")

display_columns = [
    "account_id",
    "account_name",
    "current_mrr",
    "churn_probability_percent",
    "revenue_at_risk"
]

print(
    df[display_columns].head(10).to_string(index=False)
)


print("\n====================================")
print("SCORING COMPLETED")
print("====================================")

print("Customers scored:", len(df))

print(
    f"Total estimated revenue at risk: "
    f"${df['revenue_at_risk'].sum():,.2f}"
)

print(
    f"Average churn probability: "
    f"{df['churn_probability'].mean() * 100:.2f}%"
)

print(f"\nSaved to: {output_path}")