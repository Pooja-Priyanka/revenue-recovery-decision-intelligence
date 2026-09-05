import pandas as pd
import os

# --------------------------------------------------
# 1. Load raw datasets
# --------------------------------------------------

accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")
subscriptions = pd.read_csv("data/raw/ravenstack_subscriptions.csv")
usage = pd.read_csv("data/raw/ravenstack_feature_usage.csv")
tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
churn_events = pd.read_csv("data/raw/ravenstack_churn_events.csv")


# --------------------------------------------------
# 2. Convert date columns
# --------------------------------------------------

accounts["signup_date"] = pd.to_datetime(accounts["signup_date"])
subscriptions["start_date"] = pd.to_datetime(subscriptions["start_date"])
subscriptions["end_date"] = pd.to_datetime(subscriptions["end_date"])
usage["usage_date"] = pd.to_datetime(usage["usage_date"])
tickets["submitted_at"] = pd.to_datetime(tickets["submitted_at"])
churn_events["churn_date"] = pd.to_datetime(churn_events["churn_date"])


# --------------------------------------------------
# 3. Define prediction cutoff
# --------------------------------------------------

CUTOFF_DATE = pd.Timestamp("2024-09-30")
PREDICTION_END = pd.Timestamp("2024-12-29")


# --------------------------------------------------
# 4. Keep only accounts existing at cutoff
# --------------------------------------------------

eligible_accounts = accounts[
    accounts["signup_date"] <= CUTOFF_DATE
].copy()

print("Eligible accounts:", len(eligible_accounts))


# --------------------------------------------------
# 5. Filter subscriptions available at cutoff
# --------------------------------------------------

subscriptions_at_cutoff = subscriptions[
    (subscriptions["start_date"] <= CUTOFF_DATE)
    &
    (
        subscriptions["end_date"].isna()
        |
        (subscriptions["end_date"] > CUTOFF_DATE)
    )
].copy()


# --------------------------------------------------
# 6. Select current subscription per account
# --------------------------------------------------

subscriptions_at_cutoff = subscriptions_at_cutoff.sort_values(
    ["account_id", "start_date"]
)

current_subscription = (
    subscriptions_at_cutoff
    .groupby("account_id")
    .tail(1)
)


# --------------------------------------------------
# 7. Aggregate subscription information
# --------------------------------------------------

subscription_features = current_subscription[
    [
        "account_id",
        "plan_tier",
        "seats",
        "mrr_amount",
        "arr_amount",
        "is_trial"
    ]
].copy()

subscription_features = subscription_features.rename(
    columns={
        "mrr_amount": "current_mrr",
        "arr_amount": "current_arr"
    }
)


# --------------------------------------------------
# 8. Historical usage up to cutoff
# --------------------------------------------------

usage_before_cutoff = usage[
    usage["usage_date"] <= CUTOFF_DATE
].copy()

usage_features = (
    usage_before_cutoff
    .merge(
        subscriptions[["subscription_id", "account_id"]],
        on="subscription_id",
        how="left"
    )
    .groupby("account_id")
    .agg(
        total_usage_count=("usage_count", "sum")
    )
    .reset_index()
)


# --------------------------------------------------
# 9. Historical support tickets up to cutoff
# --------------------------------------------------

tickets_before_cutoff = tickets[
    tickets["submitted_at"] <= CUTOFF_DATE
].copy()

support_features = (
    tickets_before_cutoff
    .groupby("account_id")
    .agg(
        ticket_count=("ticket_id", "count"),
        avg_satisfaction=("satisfaction_score", "mean"),
        escalation_rate=("escalation_flag", "mean")
    )
    .reset_index()
)


# --------------------------------------------------
# 10. Calculate upgrade/downgrade history
# --------------------------------------------------

subscription_history = subscriptions[
    subscriptions["start_date"] <= CUTOFF_DATE
].copy()

upgrade_features = (
    subscription_history
    .groupby("account_id")["upgrade_flag"]
    .max()
    .reset_index()
    .rename(columns={"upgrade_flag": "has_upgraded"})
)

downgrade_features = (
    subscription_history
    .groupby("account_id")["downgrade_flag"]
    .max()
    .reset_index()
    .rename(columns={"downgrade_flag": "has_downgraded"})
)


# --------------------------------------------------
# 11. Build customer feature table
# --------------------------------------------------

features = eligible_accounts[
    [
        "account_id",
        "account_name",
        "industry",
        "country",
        "signup_date",
        "referral_source"
    ]
].copy()

features = features.merge(
    subscription_features,
    on="account_id",
    how="left"
)

features = features.merge(
    usage_features,
    on="account_id",
    how="left"
)

features = features.merge(
    support_features,
    on="account_id",
    how="left"
)

features = features.merge(
    upgrade_features,
    on="account_id",
    how="left"
)

features = features.merge(
    downgrade_features,
    on="account_id",
    how="left"
)


# --------------------------------------------------
# 12. Calculate tenure
# --------------------------------------------------

features["tenure_days"] = (
    CUTOFF_DATE - features["signup_date"]
).dt.days


# --------------------------------------------------
# 13. Fill missing aggregate values
# --------------------------------------------------

features["total_usage_count"] = (
    features["total_usage_count"].fillna(0)
)

features["ticket_count"] = (
    features["ticket_count"].fillna(0)
)

features["escalation_rate"] = (
    features["escalation_rate"].fillna(0)
)

features["has_upgraded"] = (
    features["has_upgraded"].fillna(0)
)

features["has_downgraded"] = (
    features["has_downgraded"].fillna(0)
)


# --------------------------------------------------
# 14. Create future churn target
# --------------------------------------------------

future_churn = churn_events[
    (churn_events["churn_date"] > CUTOFF_DATE)
    &
    (churn_events["churn_date"] <= PREDICTION_END)
].copy()

future_churn_accounts = set(
    future_churn["account_id"]
)

features["churn_target"] = (
    features["account_id"]
    .isin(future_churn_accounts)
    .astype(int)
)


# --------------------------------------------------
# 15. Save processed dataset
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

output_file = (
    "data/processed/temporal_account_features.csv"
)

features.to_csv(
    output_file,
    index=False
)

print("\nFeature dataset created!")
print("Shape:", features.shape)
print("Saved to:", output_file)

print("\nTarget distribution:")
print(features["churn_target"].value_counts())