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

st.title("📈 Analytics")

st.markdown(
    """
    **Understand the patterns behind customer churn risk and revenue exposure.**
    
    Explore portfolio-level risk, priority distribution, retention actions,
    industry exposure, and the customers contributing the most estimated risk.
    """
)

st.caption("RavenStack SaaS Analytics • Portfolio Intelligence")

st.divider()


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

total_customers = len(df)

total_risk = df["revenue_at_risk"].sum()

avg_churn = df["churn_probability"].mean()

median_mrr = df["current_mrr"].median()

max_risk = df["revenue_at_risk"].max()

high_priority = (df["priority"] == "High").sum()


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "💰 Revenue at Risk",
        f"${total_risk:,.0f}"
    )

with col3:
    st.metric(
        "📉 Avg. Churn Risk",
        f"{avg_churn:.2%}"
    )

with col4:
    st.metric(
        "🔴 High Priority",
        high_priority
    )

with col5:
    st.metric(
        "🚨 Highest Risk",
        f"${max_risk:,.0f}"
    )


st.divider()


# --------------------------------------------------
# PRIORITY ANALYSIS
# --------------------------------------------------

st.subheader("🎯 Portfolio Risk by Priority")

col1, col2 = st.columns(2)


with col1:

    st.markdown("**Customer Distribution**")

    priority_counts = (
        df["priority"]
        .value_counts()
        .reindex(
            ["High", "Medium", "Low"]
        )
        .fillna(0)
    )

    st.bar_chart(
        priority_counts,
        height=350
    )


with col2:

    st.markdown("**Revenue Exposure**")

    risk_by_priority = (
        df.groupby("priority")["revenue_at_risk"]
        .sum()
        .reindex(
            ["High", "Medium", "Low"]
        )
        .fillna(0)
    )

    st.bar_chart(
        risk_by_priority,
        height=350
    )


st.divider()


# --------------------------------------------------
# RISK CONCENTRATION
# --------------------------------------------------

st.subheader("💰 Where Is Revenue Risk Concentrated?")

col1, col2 = st.columns(2)


with col1:

    high_risk_revenue = df.loc[
        df["priority"] == "High",
        "revenue_at_risk"
    ].sum()

    medium_risk_revenue = df.loc[
        df["priority"] == "Medium",
        "revenue_at_risk"
    ].sum()

    low_risk_revenue = df.loc[
        df["priority"] == "Low",
        "revenue_at_risk"
    ].sum()

    concentration_df = pd.DataFrame(
        {
            "Revenue at Risk": [
                high_risk_revenue,
                medium_risk_revenue,
                low_risk_revenue
            ]
        },
        index=[
            "High Priority",
            "Medium Priority",
            "Low Priority"
        ]
    )

    st.bar_chart(
        concentration_df,
        height=320
    )


with col2:

    top_10_risk = (
        df.sort_values(
            "revenue_at_risk",
            ascending=False
        )
        .head(10)["revenue_at_risk"]
        .sum()
    )

    top_10_percentage = (
        top_10_risk / total_risk * 100
        if total_risk > 0
        else 0
    )

    st.metric(
        "Top 10 Customer Risk",
        f"${top_10_risk:,.0f}"
    )

    st.metric(
        "Top 10 Share of Total Risk",
        f"{top_10_percentage:.1f}%"
    )

    st.info(
        "This indicates how concentrated the estimated revenue exposure "
        "is among the highest-risk accounts."
    )


st.divider()


# --------------------------------------------------
# RECOMMENDED ACTION ANALYSIS
# --------------------------------------------------

st.subheader("📌 Recommended Retention Actions")

action_counts = (
    df["recommended_action"]
    .value_counts()
    .sort_values(ascending=True)
)

st.bar_chart(
    action_counts,
    height=350
)


# Action summary table

action_summary = (
    df.groupby("recommended_action")
    .agg(
        Customers=("account_id", "count"),
        Revenue_at_Risk=("revenue_at_risk", "sum")
    )
    .sort_values(
        "Revenue_at_Risk",
        ascending=False
    )
    .reset_index()
)

action_summary["Revenue_at_Risk"] = (
    action_summary["Revenue_at_Risk"]
    .round(2)
)

action_summary = action_summary.rename(
    columns={
        "recommended_action": "Recommended Action",
        "Customers": "Customers",
        "Revenue_at_Risk": "Revenue at Risk ($)"
    }
)

st.dataframe(
    action_summary,
    width="stretch",
    hide_index=True,
    column_config={
        "Revenue at Risk ($)": st.column_config.NumberColumn(
            "Revenue at Risk ($)",
            format="$%.2f"
        )
    }
)


st.divider()


# --------------------------------------------------
# CHURN PROBABILITY DISTRIBUTION
# --------------------------------------------------

st.subheader("📉 Churn Probability Distribution")

st.write(
    "Distribution of predicted churn probabilities across eligible customers."
)

churn_distribution = pd.DataFrame(
    {
        "Churn Probability": df[
            "churn_probability"
        ]
        .sort_values()
        .reset_index(drop=True)
    }
)

st.area_chart(
    churn_distribution,
    height=300
)


st.divider()


# --------------------------------------------------
# INDUSTRY ANALYSIS
# --------------------------------------------------

st.subheader("🏢 Revenue at Risk by Industry")

industry_risk = (
    df.groupby("industry")["revenue_at_risk"]
    .sum()
    .sort_values(ascending=True)
)

st.bar_chart(
    industry_risk,
    height=450
)


st.divider()


# --------------------------------------------------
# TOP RISK CUSTOMERS
# --------------------------------------------------

st.subheader("🚨 Top 10 Customers by Revenue at Risk")

top_risk = (
    df[
        [
            "account_id",
            "account_name",
            "plan_tier",
            "churn_probability",
            "current_mrr",
            "revenue_at_risk",
            "priority"
        ]
    ]
    .sort_values(
        "revenue_at_risk",
        ascending=False
    )
    .head(10)
    .copy()
)


top_risk["churn_probability"] = (
    top_risk["churn_probability"]
    .round(4)
)

top_risk["current_mrr"] = (
    top_risk["current_mrr"]
    .round(2)
)

top_risk["revenue_at_risk"] = (
    top_risk["revenue_at_risk"]
    .round(2)
)


top_risk = top_risk.rename(
    columns={
        "account_id": "Account ID",
        "account_name": "Customer",
        "plan_tier": "Plan",
        "churn_probability": "Churn Probability",
        "current_mrr": "Current MRR ($)",
        "revenue_at_risk": "Revenue at Risk ($)",
        "priority": "Priority"
    }
)


st.dataframe(
    top_risk,
    width="stretch",
    hide_index=True,
    column_config={
        "Churn Probability": st.column_config.NumberColumn(
            "Churn Probability",
            format="%.2f%%"
        ),
        "Current MRR ($)": st.column_config.NumberColumn(
            "Current MRR ($)",
            format="$%.2f"
        ),
        "Revenue at Risk ($)": st.column_config.NumberColumn(
            "Revenue at Risk ($)",
            format="$%.2f"
        )
    }
)


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("💡 Key Business Insights")


highest_priority = (
    df.groupby("priority")["revenue_at_risk"]
    .sum()
    .idxmax()
)

highest_industry = (
    df.groupby("industry")["revenue_at_risk"]
    .sum()
    .idxmax()
)

highest_action = (
    df.groupby("recommended_action")["revenue_at_risk"]
    .sum()
    .idxmax()
)


col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        f"**Largest risk category**\n\n"
        f"{highest_priority} priority accounts contribute "
        f"the largest estimated revenue exposure."
    )

with col2:
    st.info(
        f"**Highest-risk industry**\n\n"
        f"{highest_industry} has the highest aggregate "
        f"estimated revenue at risk."
    )

with col3:
    st.info(
        f"**Primary intervention**\n\n"
        f"{highest_action} represents the largest "
        f"revenue exposure among recommended actions."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Analytics are based on the 420 eligible customers in the "
    "leakage-safe prediction dataset."
)

st.caption(
    "Revenue at Risk is an estimated exposure calculated as "
    "predicted churn probability × current MRR. It is not guaranteed lost revenue."
)
