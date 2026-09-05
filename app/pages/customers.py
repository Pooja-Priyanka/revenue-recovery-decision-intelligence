import streamlit as st
import pandas as pd

from components.styles import load_css


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

st.title("👥 Customer Risk Explorer")

st.write(
    "Explore customer-level churn risk, revenue exposure, "
    "risk signals, and recommended retention actions."
)

st.divider()


# ============================================================
# FILTERS
# ============================================================

st.subheader("🔎 Find Customers")

col1, col2, col3 = st.columns(3)

with col1:

    priority_filter = st.selectbox(
        "🎯 Priority",
        ["All", "High", "Medium", "Low"]
    )

with col2:

    action_filter = st.selectbox(
        "📌 Recommended Action",
        ["All"]
        + sorted(
            df["recommended_action"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with col3:

    search = st.text_input(
        "🔍 Search Customer",
        placeholder="Company name or Account ID"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if priority_filter != "All":

    filtered_df = filtered_df[
        filtered_df["priority"] == priority_filter
    ]


if action_filter != "All":

    filtered_df = filtered_df[
        filtered_df["recommended_action"]
        == action_filter
    ]


if search:

    search_value = search.lower().strip()

    filtered_df = filtered_df[
        filtered_df["account_name"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
        |
        filtered_df["account_id"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_value,
            na=False
        )
    ]


# ============================================================
# FILTER SUMMARY
# ============================================================

st.caption(
    f"Showing **{len(filtered_df):,}** "
    f"of **{len(df):,}** customers"
)


# ============================================================
# CUSTOMER TABLE
# ============================================================

st.subheader("📋 Customer Portfolio")

display_df = filtered_df[
    [
        "account_id",
        "account_name",
        "plan_tier",
        "current_mrr",
        "churn_probability",
        "revenue_at_risk",
        "priority",
        "recommended_action"
    ]
].copy()


display_df["churn_probability"] = (
    display_df["churn_probability"] * 100
).round(2)


display_df["current_mrr"] = (
    display_df["current_mrr"]
).round(2)


display_df["revenue_at_risk"] = (
    display_df["revenue_at_risk"]
).round(2)


display_df = display_df.rename(
    columns={
        "account_id": "Account ID",
        "account_name": "Customer",
        "plan_tier": "Plan",
        "current_mrr": "Current MRR ($)",
        "churn_probability": "Churn Probability (%)",
        "revenue_at_risk": "Revenue at Risk ($)",
        "priority": "Priority",
        "recommended_action": "Recommended Action"
    }
)


st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


# ============================================================
# CUSTOMER DETAIL
# ============================================================

st.divider()

st.header("👤 Customer Investigation")


if len(filtered_df) == 0:

    st.warning(
        "No customers match the selected filters."
    )

else:

    customer_names = (
        filtered_df["account_name"]
        .sort_values()
        .tolist()
    )

    selected_name = st.selectbox(
        "Select a customer to investigate",
        customer_names
    )

    customer = filtered_df[
        filtered_df["account_name"]
        == selected_name
    ].iloc[0]


    # ========================================================
    # CUSTOMER HEADER
    # ========================================================

    st.subheader(
        f"{customer['account_name']} "
        f"({customer['account_id']})"
    )

    st.caption(
        f"{customer['industry']} • "
        f"{customer['country']} • "
        f"{customer['plan_tier']}"
    )


    # ========================================================
    # CUSTOMER KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Churn Probability",
            f"{customer['churn_probability']:.2%}"
        )

    with col2:

        st.metric(
            "Current MRR",
            f"${customer['current_mrr']:,.2f}"
        )

    with col3:

        st.metric(
            "Revenue at Risk",
            f"${customer['revenue_at_risk']:,.2f}"
        )

    with col4:

        st.metric(
            "Priority",
            customer["priority"]
        )


    st.divider()


    # ========================================================
    # ACCOUNT INFORMATION
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏢 Account Information")

        account_info = pd.DataFrame({
            "Attribute": [
                "Account ID",
                "Industry",
                "Country",
                "Plan",
                "Seats",
                "Tenure",
                "Trial"
            ],
            "Value": [
                customer["account_id"],
                customer["industry"],
                customer["country"],
                customer["plan_tier"],
                customer["seats"],
                f"{customer['tenure_days']} days",
                customer["is_trial"]
            ]
        })

        st.dataframe(
            account_info,
            width="stretch",
            hide_index=True
        )


    # ========================================================
    # RISK SIGNALS
    # ========================================================

    with col2:

        st.subheader("📊 Risk Signals")

        risk_info = pd.DataFrame({
            "Signal": [
                "Usage Count",
                "Support Tickets",
                "Average Satisfaction",
                "Escalation Rate",
                "Has Upgraded",
                "Has Downgraded"
            ],
            "Value": [
                customer["total_usage_count"],
                customer["ticket_count"],
                customer["avg_satisfaction"],
                f"{customer['escalation_rate']:.2%}",
                customer["has_upgraded"],
                customer["has_downgraded"]
            ]
        })

        st.dataframe(
            risk_info,
            width="stretch",
            hide_index=True
        )


    st.divider()


    # ========================================================
    # RISK INTERPRETATION
    # ========================================================

    st.subheader("🚨 Risk Interpretation")

    risk_col1, risk_col2 = st.columns(2)

    with risk_col1:

        st.metric(
            "Predicted Churn",
            f"{customer['churn_probability']:.2%}"
        )

        st.caption(
            "Model prediction, not an observed churn event."
        )

    with risk_col2:

        st.metric(
            "Estimated Revenue Exposure",
            f"${customer['revenue_at_risk']:,.2f}"
        )

        st.caption(
            "Calculated as predicted churn probability × current MRR."
        )


    # ========================================================
    # RETENTION DECISION
    # ========================================================

    st.subheader("🎯 Retention Decision")

    st.info(
        f"""
**Priority:** {customer['priority']}

**Recommended Action:** {customer['recommended_action']}
"""
    )


    # ========================================================
    # AI EXPLANATION
    # ========================================================

    st.divider()

    st.subheader("🤖 AI Risk Explanation")

    st.write(
        "Ask the AI to explain this customer's risk "
        "and recommended retention action using only "
        "the available customer data."
    )

    question = st.text_input(
        "Your question",
        value=(
            "Why is this customer at risk and "
            "what should we do?"
        ),
        key="customer_ai_question"
    )


    if st.button(
        "🤖 Ask AI",
        type="primary",
        key="customer_ai_button"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            prompt = f"""
You are a business decision-support assistant
for a SaaS revenue recovery platform.

Analyze ONE customer using ONLY the supplied data.

Do not invent facts, numbers, events,
or explanations.

Clearly distinguish between:

1. Observed customer information
2. Model predictions
3. Decision-engine recommendations

CUSTOMER

Account ID:
{customer['account_id']}

Customer Name:
{customer['account_name']}

Industry:
{customer['industry']}

Country:
{customer['country']}

Plan:
{customer['plan_tier']}

Seats:
{customer['seats']}

Tenure:
{customer['tenure_days']} days

Current MRR:
${customer['current_mrr']:,.2f}

Current ARR:
${customer['current_arr']:,.2f}

USAGE & SUPPORT

Usage Count:
{customer['total_usage_count']}

Support Tickets:
{customer['ticket_count']}

Average Satisfaction:
{customer['avg_satisfaction']}

Escalation Rate:
{customer['escalation_rate']:.2%}

Has Upgraded:
{customer['has_upgraded']}

Has Downgraded:
{customer['has_downgraded']}

MODEL PREDICTION

Churn Probability:
{customer['churn_probability']:.2%}

Revenue at Risk:
${customer['revenue_at_risk']:,.2f}

DECISION ENGINE

Priority:
{customer['priority']}

Recommended Action:
{customer['recommended_action']}

USER QUESTION

{question}

INSTRUCTIONS

- Answer clearly and concisely.
- Use only the supplied information.
- Do not invent causes or events.
- Identify the strongest available risk signals.
- Explain the distinction between observed data
  and model predictions.
- Explain why the recommended action is appropriate.
"""

            with st.spinner(
                "Analyzing customer..."
            ):

                try:

                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        input=prompt
                    )

                    st.markdown(
                        "### 💡 AI Recommendation"
                    )

                    st.info(
                        response.output_text
                    )

                except Exception as e:

                    st.error(
                        f"AI request failed: {e}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Revenue at Risk is an estimated exposure calculated "
    "as predicted churn probability × current MRR. "
    "It is not guaranteed lost revenue."
)
