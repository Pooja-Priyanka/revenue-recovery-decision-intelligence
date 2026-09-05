import streamlit as st
import pandas as pd

from components.styles import load_css
from components.cards import metric_card


# ============================================================
# PAGE SETUP
# ============================================================

load_css()


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/processed/customer_risk_decisions.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "Revenue Recovery & Decision Intelligence Platform"
)

st.write(
    "AI-powered customer churn risk, revenue exposure, "
    "and retention decision platform."
)

st.caption(
    "RavenStack SaaS Analytics • 420 eligible customers"
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_customers = len(df)

total_revenue_risk = (
    df["revenue_at_risk"].sum()
)

high_priority = (
    df["priority"] == "High"
).sum()

medium_priority = (
    df["priority"] == "Medium"
).sum()

low_priority = (
    df["priority"] == "Low"
).sum()

average_churn_probability = (
    df["churn_probability"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(
        "Eligible Customers",
        f"{total_customers:,}",
        "👥"
    )

with col2:

    metric_card(
        "Revenue at Risk",
        f"${total_revenue_risk:,.2f}",
        "💰"
    )

with col3:

    metric_card(
        "High Priority",
        f"{high_priority:,}",
        "🔴"
    )

with col4:

    metric_card(
        "Avg Churn Probability",
        f"{average_churn_probability:.2%}",
        "📉"
    )


st.divider()


# ============================================================
# RISK OVERVIEW
# ============================================================

st.header("📊 Risk Overview")

col1, col2 = st.columns(2)


# ============================================================
# PRIORITY DISTRIBUTION
# ============================================================

with col1:

    st.subheader("🎯 Customer Priority")

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

    st.caption(
        f"{high_priority} high-priority customers "
        f"require immediate attention."
    )


# ============================================================
# REVENUE AT RISK BY PRIORITY
# ============================================================

with col2:

    st.subheader("💰 Revenue at Risk by Priority")

    risk_by_priority = (
        df.groupby("priority")[
            "revenue_at_risk"
        ]
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

    st.caption(
        "Higher values indicate greater estimated "
        "revenue exposure."
    )


st.divider()


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.header("💡 Business Insights")

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# HIGH PRIORITY REVENUE
# ------------------------------------------------------------

high_priority_risk = (
    df.loc[
        df["priority"] == "High",
        "revenue_at_risk"
    ].sum()
)

high_priority_percentage = (
    high_priority_risk /
    total_revenue_risk
    if total_revenue_risk > 0
    else 0
)


with col1:

    st.metric(
        "High-Priority Revenue Risk",
        f"${high_priority_risk:,.2f}"
    )

    st.caption(
        f"{high_priority_percentage:.1%} of total "
        "estimated revenue exposure"
    )


# ------------------------------------------------------------
# MEDIUM PRIORITY REVENUE
# ------------------------------------------------------------

medium_priority_risk = (
    df.loc[
        df["priority"] == "Medium",
        "revenue_at_risk"
    ].sum()
)


with col2:

    st.metric(
        "Medium-Priority Revenue Risk",
        f"${medium_priority_risk:,.2f}"
    )

    st.caption(
        f"{medium_priority} customers in this segment"
    )


# ------------------------------------------------------------
# LOW PRIORITY REVENUE
# ------------------------------------------------------------

low_priority_risk = (
    df.loc[
        df["priority"] == "Low",
        "revenue_at_risk"
    ].sum()
)


with col3:

    st.metric(
        "Low-Priority Revenue Risk",
        f"${low_priority_risk:,.2f}"
    )

    st.caption(
        f"{low_priority} customers in this segment"
    )


st.divider()


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

st.header("⚡ Recommended Retention Actions")

action_counts = (
    df["recommended_action"]
    .value_counts()
)

action_table = (
    action_counts
    .rename_axis("Recommended Action")
    .reset_index(name="Customers")
)

st.dataframe(
    action_table,
    width="stretch",
    hide_index=True
)


st.divider()


# ============================================================
# TOP CUSTOMERS
# ============================================================

st.header("🚨 Top Customers by Revenue at Risk")

st.caption(
    "Customers with the highest estimated revenue exposure."
)

top_customers = (
    df[
        [
            "account_id",
            "account_name",
            "churn_probability",
            "current_mrr",
            "revenue_at_risk",
            "priority",
            "recommended_action"
        ]
    ]
    .sort_values(
        "revenue_at_risk",
        ascending=False
    )
    .head(10)
    .copy()
)


# Format values for display

top_customers["churn_probability"] = (
    top_customers["churn_probability"]
    .map(
        lambda x: f"{x:.2%}"
    )
)

top_customers["current_mrr"] = (
    top_customers["current_mrr"]
    .map(
        lambda x: f"${x:,.2f}"
    )
)

top_customers["revenue_at_risk"] = (
    top_customers["revenue_at_risk"]
    .map(
        lambda x: f"${x:,.2f}"
    )
)


st.dataframe(
    top_customers,
    width="stretch",
    hide_index=True
)


st.divider()


# ============================================================
# DECISION INTELLIGENCE SUMMARY
# ============================================================

st.header("🧠 Decision Intelligence Summary")

st.info(
    f"""
**{total_customers:,}** eligible customers were evaluated.

The model estimates **${total_revenue_risk:,.2f}**
in potential revenue exposure based on predicted churn.

**{high_priority} customers** are classified as high priority,
while **{medium_priority}** are medium priority and
**{low_priority}** are low priority.

The decision engine converts customer risk signals into
recommended retention actions such as support intervention,
customer satisfaction outreach, product adoption outreach,
and proactive retention outreach.
"""
)


# ============================================================
# IMPORTANT NOTE
# ============================================================

st.caption(
    "Revenue at Risk is an estimated exposure calculated "
    "as predicted churn probability × current MRR. "
    "It is not guaranteed lost revenue."
)
