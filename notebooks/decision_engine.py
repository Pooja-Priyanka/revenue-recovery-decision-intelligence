import pandas as pd


# ==========================================
# 1. LOAD CUSTOMER RISK SCORES
# ==========================================

input_path = "data/processed/customer_risk_scores.csv"

df = pd.read_csv(input_path)

print("====================================")
print("REVENUE RECOVERY DECISION ENGINE")
print("====================================")

print("\nCustomers loaded:", len(df))


# ==========================================
# 2. DEFINE PRIORITY
# ==========================================

def assign_priority(row):

    churn_probability = row["churn_probability"]
    revenue_at_risk = row["revenue_at_risk"]

    if (
        churn_probability >= 0.50
        or revenue_at_risk >= 7500
    ):
        return "High"

    elif (
        churn_probability >= 0.30
        and revenue_at_risk < 7500
    ):
        return "Medium"

    else:
        return "Low"


df["priority"] = df.apply(
    assign_priority,
    axis=1
)


# ==========================================
# 3. DEFINE RECOMMENDED ACTION
# ==========================================

def recommend_action(row):

    if row["escalation_rate"] >= 0.30:

        return "Priority support intervention"

    elif row["avg_satisfaction"] <= 3:

        return "Customer satisfaction outreach"

    elif row["has_downgraded"] == True:

        return "Account retention review"

    elif row["total_usage_count"] < 200:

        return "Product adoption outreach"

    else:

        return "Proactive retention outreach"


df["recommended_action"] = df.apply(
    recommend_action,
    axis=1
)


# ==========================================
# 4. SORT CUSTOMERS
# ==========================================

priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

df["priority_order"] = df["priority"].map(
    priority_order
)

df = df.sort_values(
    by=["priority_order", "revenue_at_risk"],
    ascending=[True, False]
)

df = df.drop(
    columns=["priority_order"]
)


# ==========================================
# 5. SAVE FINAL DECISIONS
# ==========================================

output_path = "data/processed/customer_risk_decisions.csv"

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 6. DISPLAY PRIORITY SUMMARY
# ==========================================

print("\n====================================")
print("PRIORITY DISTRIBUTION")
print("====================================")

print(
    df["priority"].value_counts()
)


# ==========================================
# 7. DISPLAY RECOMMENDED ACTIONS
# ==========================================

print("\n====================================")
print("RECOMMENDED ACTIONS")
print("====================================")

print(
    df["recommended_action"].value_counts()
)


# ==========================================
# 8. DISPLAY HIGH PRIORITY CUSTOMERS
# ==========================================

print("\n====================================")
print("HIGH PRIORITY CUSTOMERS")
print("====================================")

high_priority = df[
    df["priority"] == "High"
]

display_columns = [
    "account_id",
    "account_name",
    "churn_probability_percent",
    "current_mrr",
    "revenue_at_risk",
    "priority",
    "recommended_action"
]

print(
    high_priority[display_columns]
    .head(20)
    .to_string(index=False)
)


# ==========================================
# 9. SUMMARY
# ==========================================

print("\n====================================")
print("DECISION ENGINE COMPLETED")
print("====================================")

print(
    "High priority:",
    len(df[df["priority"] == "High"])
)

print(
    "Medium priority:",
    len(df[df["priority"] == "Medium"])
)

print(
    "Low priority:",
    len(df[df["priority"] == "Low"])
)

print(
    f"\nTotal revenue at risk: "
    f"${df['revenue_at_risk'].sum():,.2f}"
)

print(
    f"\nSaved to: {output_path}"
)