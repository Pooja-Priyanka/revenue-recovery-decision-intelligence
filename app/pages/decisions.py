import streamlit as st
import pandas as pd

from components.styles import load_css

load_css()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/customer_risk_decisions.csv"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎯 Decision Center")

st.markdown(
    """
    **Turn customer risk predictions into actionable retention decisions.**
    
    Prioritize accounts using predicted churn probability, estimated revenue
    exposure, and recommended recovery actions.
    """
)

st.caption("RavenStack SaaS Analytics • Decision Intelligence Layer")

st.divider()


# --------------------------------------------------
# PRIORITY SUMMARY
# --------------------------------------------------

high_count = (df["priority"] == "High").sum()
medium_count = (df["priority"] == "Medium").sum()
low_count = (df["priority"] == "Low").sum()

high_risk_revenue = df.loc[
    df["priority"] == "High",
    "revenue_at_risk"
].sum()

total_risk = df["revenue_at_risk"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔴 High Priority",
        high_count
    )

with col2:
    st.metric(
        "🟡 Medium Priority",
        medium_count
    )

with col3:
    st.metric(
        "🟢 Low Priority",
        low_count
    )

with col4:
    st.metric(
        "💰 High-Priority Risk",
        f"${high_risk_revenue:,.0f}"
    )


st.divider()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("🔎 Decision Filters")

col1, col2 = st.columns(2)

with col1:
    priority = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"]
    )

with col2:
    actions = ["All"] + sorted(
        df["recommended_action"].dropna().unique().tolist()
    )

    selected_action = st.selectbox(
        "Recommended Action",
        actions
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

decision_df = df.copy()

if priority != "All":
    decision_df = decision_df[
        decision_df["priority"] == priority
    ]

if selected_action != "All":
    decision_df = decision_df[
        decision_df["recommended_action"] == selected_action
    ]


decision_df = decision_df.sort_values(
    "revenue_at_risk",
    ascending=False
)


st.caption(
    f"Showing **{len(decision_df)}** customers matching the selected filters."
)


# --------------------------------------------------
# DECISION TABLE
# --------------------------------------------------

st.subheader("📋 Recommended Retention Actions")

display_df = decision_df[
    [
        "account_id",
        "account_name",
        "churn_probability",
        "revenue_at_risk",
        "priority",
        "recommended_action"
    ]
].copy()


display_df["churn_probability"] = (
    display_df["churn_probability"] * 100
).round(2)


display_df["revenue_at_risk"] = (
    display_df["revenue_at_risk"]
).round(2)


display_df = display_df.rename(
    columns={
        "account_id": "Account ID",
        "account_name": "Customer",
        "churn_probability": "Churn Risk (%)",
        "revenue_at_risk": "Revenue at Risk ($)",
        "priority": "Priority",
        "recommended_action": "Recommended Action"
    }
)


st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Churn Risk (%)": st.column_config.NumberColumn(
            "Churn Risk (%)",
            format="%.2f%%"
        ),
        "Revenue at Risk ($)": st.column_config.NumberColumn(
            "Revenue at Risk ($)",
            format="$%.2f"
        )
    }
)


# --------------------------------------------------
# DECISION DETAILS
# --------------------------------------------------

st.divider()

st.subheader("👤 Customer Decision Investigation")

if len(decision_df) > 0:

    customer_options = (
        decision_df["account_name"]
        + " — "
        + decision_df["account_id"]
    ).tolist()

    selected_customer = st.selectbox(
        "Select a customer to investigate",
        customer_options
    )

    selected_account_id = selected_customer.split(" — ")[-1]

    customer = decision_df[
        decision_df["account_id"] == selected_account_id
    ].iloc[0]


    # --------------------------------------------------
    # CUSTOMER METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Churn Probability",
            f"{customer['churn_probability']:.2%}"
        )

    with col2:
        st.metric(
            "Revenue at Risk",
            f"${customer['revenue_at_risk']:,.2f}"
        )

    with col3:
        st.metric(
            "Priority",
            customer["priority"]
        )

    with col4:
        st.metric(
            "Current MRR",
            f"${customer['current_mrr']:,.0f}"
        )


    st.divider()


    # --------------------------------------------------
    # ACTION
    # --------------------------------------------------

    st.markdown("### 🎯 Recommended Action")

    st.success(
        f"**{customer['recommended_action']}**"
    )


    # --------------------------------------------------
    # WHY THIS CUSTOMER MATTERS
    # --------------------------------------------------

    st.markdown("### 💡 Why This Customer Matters")

    risk_pct = customer["churn_probability"] * 100
    revenue_risk = customer["revenue_at_risk"]

    st.write(
        f"This account has a predicted churn probability of "
        f"**{risk_pct:.2f}%** and approximately "
        f"**${revenue_risk:,.2f}** in estimated revenue exposure."
    )


    # --------------------------------------------------
    # RISK SIGNALS
    # --------------------------------------------------

    st.markdown("### 📊 Risk Signals")

    signal_col1, signal_col2 = st.columns(2)

    with signal_col1:

        st.markdown("**Customer Profile**")

        profile_df = pd.DataFrame(
            {
                "Metric": [
                    "Industry",
                    "Country",
                    "Plan Tier",
                    "Seats",
                    "Tenure (days)"
                ],
                "Value": [
                    customer.get("industry", "N/A"),
                    customer.get("country", "N/A"),
                    customer.get("plan_tier", "N/A"),
                    customer.get("seats", "N/A"),
                    customer.get("tenure_days", "N/A")
                ]
            }
        )

        st.dataframe(
            profile_df,
            width="stretch",
            hide_index=True
        )


    with signal_col2:

        st.markdown("**Risk Indicators**")

        risk_df = pd.DataFrame(
            {
                "Signal": [
                    "Usage Count",
                    "Support Tickets",
                    "Avg. Satisfaction",
                    "Escalation Rate",
                    "Upgraded",
                    "Downgraded"
                ],
                "Value": [
                    customer.get("total_usage_count", "N/A"),
                    customer.get("ticket_count", "N/A"),
                    customer.get("avg_satisfaction", "N/A"),
                    (
                        f"{customer['escalation_rate']:.1%}"
                        if pd.notna(customer.get("escalation_rate"))
                        else "N/A"
                    ),
                    customer.get("has_upgraded", "N/A"),
                    customer.get("has_downgraded", "N/A")
                ]
            }
        )

        st.dataframe(
            risk_df,
            width="stretch",
            hide_index=True
        )


    # --------------------------------------------------
    # BUSINESS INTERPRETATION
    # --------------------------------------------------

    st.markdown("### 🧠 Decision Interpretation")

    reasons = []

    if customer["churn_probability"] >= 0.50:
        reasons.append(
            "The predicted churn probability crosses the high-risk threshold."
        )

    if customer["revenue_at_risk"] >= 7500:
        reasons.append(
            "The estimated revenue exposure is significant."
        )

    if customer.get("escalation_rate", 0) >= 0.30:
        reasons.append(
            "The account has a relatively high support escalation rate."
        )

    if (
        pd.notna(customer.get("avg_satisfaction"))
        and customer["avg_satisfaction"] <= 3
    ):
        reasons.append(
            "Customer satisfaction is low and may require intervention."
        )

    if customer.get("has_downgraded", False):
        reasons.append(
            "A downgrade signal is present in the account history."
        )

    if (
        pd.notna(customer.get("total_usage_count"))
        and customer["total_usage_count"] < 200
    ):
        reasons.append(
            "Low product usage suggests an opportunity for adoption outreach."
        )

    if not reasons:
        reasons.append(
            "The account is prioritized based on the overall risk decision rules."
        )

    for reason in reasons:
        st.markdown(f"- {reason}")


    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    st.caption(
        "Revenue at Risk is an estimated exposure calculated from "
        "predicted churn probability × current MRR. It is not guaranteed "
        "lost revenue."
    )

else:

    st.info(
        "No customers match the selected filters."
    )
