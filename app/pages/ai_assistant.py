import os
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI

from components.styles import load_css


# ============================================================
# PAGE STYLE
# ============================================================

load_css()


# ============================================================
# OPENAI SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "OpenAI API key not found. Please check your .env file."
    )
    st.stop()

client = OpenAI(api_key=api_key)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/processed/customer_risk_decisions.csv"
)


# ============================================================
# BUSINESS METRICS
# ============================================================

eligible_customers = len(df)

total_revenue_at_risk = df["revenue_at_risk"].sum()

average_churn_probability = df["churn_probability"].mean()

priority_counts = (
    df["priority"]
    .value_counts()
    .reindex(["High", "Medium", "Low"])
    .fillna(0)
    .astype(int)
)

action_counts = (
    df["recommended_action"]
    .value_counts()
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🤖 Revenue Recovery AI Assistant")

st.markdown(
    """
    **Ask questions about customer risk, revenue exposure, and retention decisions.**

    The assistant is grounded in the project's customer risk dataset and
    decision-engine outputs.
    """
)

st.caption(
    "AI Decision Support • RavenStack SaaS Analytics"
)

st.divider()


# ============================================================
# ASSISTANT MODE
# ============================================================

assistant_mode = st.radio(
    "Choose analysis mode",
    [
        "👤 Customer Analysis",
        "🏢 Business Analysis"
    ],
    horizontal=True
)

st.divider()


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

if assistant_mode == "👤 Customer Analysis":

    st.subheader("👤 Customer Risk Copilot")

    st.caption(
        "Investigate one customer using observed account data, "
        "model predictions, and decision-engine outputs."
    )


    # --------------------------------------------------------
    # CUSTOMER SELECTION
    # --------------------------------------------------------

    customer_options = (
        df["account_name"]
        .sort_values()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Select a customer",
        customer_options
    )

    customer = df[
        df["account_name"] == selected_customer
    ].iloc[0]


    # --------------------------------------------------------
    # CUSTOMER KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Account",
            customer["account_id"]
        )

    with col2:
        st.metric(
            "Current MRR",
            f"${customer['current_mrr']:,.0f}"
        )

    with col3:
        st.metric(
            "Churn Probability",
            f"{customer['churn_probability']:.2%}"
        )

    with col4:
        st.metric(
            "Revenue at Risk",
            f"${customer['revenue_at_risk']:,.0f}"
        )


    st.divider()


    # --------------------------------------------------------
    # CUSTOMER OVERVIEW
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 Decision")

        st.info(
            f"**Priority:** {customer['priority']}\n\n"
            f"**Recommended Action:** "
            f"{customer['recommended_action']}"
        )


    with col2:

        st.subheader("📊 Risk Signals")

        # Convert every value to string so the dataframe
        # contains a consistent column type.
        risk_data = pd.DataFrame(
            {
                "Signal": [
                    "Plan Tier",
                    "Seats",
                    "Usage Count",
                    "Support Tickets",
                    "Avg. Satisfaction",
                    "Escalation Rate"
                ],
                "Value": [
                    str(customer["plan_tier"]),
                    f"{customer['seats']:.0f}",
                    f"{customer['total_usage_count']:.0f}",
                    f"{customer['ticket_count']:.0f}",
                    f"{customer['avg_satisfaction']:.2f}",
                    f"{customer['escalation_rate']:.1%}"
                ]
            }
        )

        st.dataframe(
            risk_data,
            width="stretch",
            hide_index=True
        )


    st.divider()


    # --------------------------------------------------------
    # SUGGESTED QUESTIONS
    # --------------------------------------------------------

    st.subheader("💡 Suggested Questions")

    suggestion_col1, suggestion_col2, suggestion_col3 = st.columns(3)

    with suggestion_col1:
        st.markdown(
            "• Why is this customer considered risky?"
        )

    with suggestion_col2:
        st.markdown(
            "• What retention action should we take?"
        )

    with suggestion_col3:
        st.markdown(
            "• How much revenue is at risk?"
        )


    # --------------------------------------------------------
    # CUSTOMER QUESTION
    # --------------------------------------------------------

    st.subheader("💬 Ask about this customer")

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: Why is this customer considered risky?"
        ),
        key="customer_question"
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

You are analyzing ONE selected customer.

Use ONLY the customer information provided below.

Do not invent facts, numbers, events, or explanations.

Clearly distinguish between:

1. Observed customer information
2. Model predictions
3. Decision-engine recommendations

CUSTOMER INFORMATION

Account ID: {customer['account_id']}
Account Name: {customer['account_name']}
Industry: {customer['industry']}
Country: {customer['country']}
Referral Source: {customer['referral_source']}
Plan Tier: {customer['plan_tier']}
Seats: {customer['seats']}
Trial: {customer['is_trial']}
Tenure Days: {customer['tenure_days']}

Current MRR: ${customer['current_mrr']:,.2f}
Current ARR: ${customer['current_arr']:,.2f}

Usage Count: {customer['total_usage_count']}
Support Tickets: {customer['ticket_count']}
Average Satisfaction: {customer['avg_satisfaction']}
Escalation Rate: {customer['escalation_rate']}

Has Upgraded: {customer['has_upgraded']}
Has Downgraded: {customer['has_downgraded']}

MODEL PREDICTION

Churn Probability:
{customer['churn_probability']:.4%}

Revenue at Risk:
${customer['revenue_at_risk']:,.2f}

DECISION ENGINE

Priority:
{customer['priority']}

Recommended Action:
{customer['recommended_action']}

USER QUESTION

{question}

Answer concisely and in a business-friendly way.

Do not claim that the customer will definitely churn.

Revenue at Risk is an estimate, not guaranteed lost revenue.
"""

            with st.spinner(
                "Analyzing customer information..."
            ):

                try:

                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        input=prompt
                    )

                    st.success("🤖 AI Analysis")

                    st.markdown(
                        response.output_text
                    )

                except Exception as e:

                    st.error(
                        f"AI request failed: {e}"
                    )


# ============================================================
# BUSINESS ANALYSIS
# ============================================================

else:

    st.subheader("🏢 Business Intelligence Copilot")

    st.caption(
        "Ask questions using the complete 420-customer portfolio."
    )


    # --------------------------------------------------------
    # BUSINESS KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Eligible Customers",
            f"{eligible_customers:,}"
        )

    with col2:
        st.metric(
            "Revenue at Risk",
            f"${total_revenue_at_risk:,.2f}"
        )

    with col3:
        st.metric(
            "High Priority",
            f"{priority_counts['High']:,}"
        )

    with col4:
        st.metric(
            "Avg. Churn Risk",
            f"{average_churn_probability:.2%}"
        )


    st.divider()


    # --------------------------------------------------------
    # BUSINESS SNAPSHOT
    # --------------------------------------------------------

    st.subheader("📊 Portfolio Snapshot")

    col1, col2 = st.columns(2)

    with col1:

        priority_table = pd.DataFrame(
            {
                "Priority": [
                    "High",
                    "Medium",
                    "Low"
                ],
                "Customers": [
                    priority_counts["High"],
                    priority_counts["Medium"],
                    priority_counts["Low"]
                ]
            }
        )

        st.markdown("**Priority Distribution**")

        st.dataframe(
            priority_table,
            width="stretch",
            hide_index=True
        )


    with col2:

        action_table = (
            action_counts
            .rename_axis("Recommended Action")
            .reset_index(name="Customers")
        )

        st.markdown("**Recommended Actions**")

        st.dataframe(
            action_table,
            width="stretch",
            hide_index=True
        )


    st.divider()


    # --------------------------------------------------------
    # SUGGESTED BUSINESS QUESTIONS
    # --------------------------------------------------------

    st.subheader("💡 Suggested Business Questions")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            • How many high-priority customers are there?

            • What is the total revenue at risk?

            • How much revenue is at risk?

            • What is the average churn probability?
            """
        )

    with col2:

        st.markdown(
            """
            • Which industry has the highest revenue risk?

            • Which retention action should we prioritize?

            • Which customers have the highest revenue exposure?
            """
        )


    # --------------------------------------------------------
    # BUSINESS QUESTION
    # --------------------------------------------------------

    st.subheader("💬 Ask about the business")

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: Which industry has the highest revenue at risk?"
        ),
        key="business_question"
    )


    if st.button(
        "🤖 Ask AI",
        type="primary",
        key="business_ai_button"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            q = question.lower().strip()

            exact_answer = None


            # =================================================
            # EXACT DATA ANSWERS
            # =================================================

            # Eligible customers
            if (
                "eligible" in q
                and "customer" in q
                and (
                    "how many" in q
                    or "number" in q
                    or "count" in q
                )
            ):

                exact_answer = (
                    f"There are **{eligible_customers:,} eligible "
                    f"customers** in the dataset."
                )


            # ------------------------------------------------
            # TOTAL REVENUE AT RISK
            # ------------------------------------------------
            # Any question containing "revenue at risk"
            # gets the exact portfolio value.
            elif "revenue at risk" in q:

                exact_answer = (
                    f"The estimated total revenue at risk is "
                    f"**${total_revenue_at_risk:,.2f}**. "
                    f"This is a model-based estimate, not guaranteed "
                    f"lost revenue."
                )


            # High priority
            elif (
                "high priority" in q
                and (
                    "how many" in q
                    or "number" in q
                    or "count" in q
                )
            ):

                exact_answer = (
                    f"There are **{priority_counts['High']:,} "
                    f"high-priority customers**."
                )


            # Medium priority
            elif (
                "medium priority" in q
                and (
                    "how many" in q
                    or "number" in q
                    or "count" in q
                )
            ):

                exact_answer = (
                    f"There are **{priority_counts['Medium']:,} "
                    f"medium-priority customers**."
                )


            # Low priority
            elif (
                "low priority" in q
                and (
                    "how many" in q
                    or "number" in q
                    or "count" in q
                )
            ):

                exact_answer = (
                    f"There are **{priority_counts['Low']:,} "
                    f"low-priority customers**."
                )


            # Average churn
            elif (
                "average churn" in q
                or "average churn probability" in q
            ):

                exact_answer = (
                    f"The average predicted churn probability "
                    f"is **{average_churn_probability:.2%}**."
                )


            # =================================================
            # DISPLAY EXACT ANSWER
            # =================================================

            if exact_answer:

                st.success("📊 Business Analysis")

                st.markdown(
                    exact_answer
                )


            # =================================================
            # AI FOR COMPLEX QUESTIONS
            # =================================================

            else:

                priority_summary = f"""
High Priority: {priority_counts['High']} customers
Medium Priority: {priority_counts['Medium']} customers
Low Priority: {priority_counts['Low']} customers
"""


                action_summary = "\n".join(
                    [
                        f"{action}: {count} customers"
                        for action, count
                        in action_counts.items()
                    ]
                )


                # ------------------------------------------------
                # TOP 10 CUSTOMERS
                # ------------------------------------------------

                top_customers = (
                    df.nlargest(
                        10,
                        "revenue_at_risk"
                    )
                )


                top_customer_summary = "\n".join(
                    [
                        f"{row['account_name']} "
                        f"({row['account_id']}): "
                        f"Priority={row['priority']}, "
                        f"Churn Probability="
                        f"{row['churn_probability']:.2%}, "
                        f"Revenue at Risk="
                        f"${row['revenue_at_risk']:,.2f}, "
                        f"Action="
                        f"{row['recommended_action']}"
                        for _, row
                        in top_customers.iterrows()
                    ]
                )


                # ------------------------------------------------
                # INDUSTRY RISK
                # ------------------------------------------------

                industry_risk = (
                    df.groupby("industry")[
                        "revenue_at_risk"
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )


                industry_summary = "\n".join(
                    [
                        f"{industry}: "
                        f"${risk:,.2f}"
                        for industry, risk
                        in industry_risk.items()
                    ]
                )


                # ------------------------------------------------
                # BUSINESS AI PROMPT
                # ------------------------------------------------

                prompt = f"""
You are a business decision-support assistant
for a SaaS revenue recovery platform.

You are analyzing the COMPLETE customer portfolio.

There are {eligible_customers} eligible customers.

Use ONLY the business information supplied below.

Do not invent facts, customers, numbers, events,
or explanations.

IMPORTANT:

For numerical questions, ALWAYS use the exact
portfolio-level numbers supplied below.

Do NOT calculate portfolio revenue at risk
from a single customer.

Do NOT invent or estimate another value.

BUSINESS KPIs

Eligible Customers:
{eligible_customers}

Total Estimated Revenue at Risk:
${total_revenue_at_risk:,.2f}

Average Predicted Churn Probability:
{average_churn_probability:.4%}

PRIORITY DISTRIBUTION

{priority_summary}

RECOMMENDED ACTIONS

{action_summary}

REVENUE AT RISK BY INDUSTRY

{industry_summary}

TOP CUSTOMERS BY REVENUE AT RISK

{top_customer_summary}

DEFINITIONS

Revenue at Risk =
churn probability × current MRR

Revenue at Risk is an estimate and is NOT
guaranteed lost revenue.

Churn probability is a MODEL PREDICTION.

Customer information such as MRR, usage,
tickets, satisfaction and plan is OBSERVED DATA.

Priority and recommended action are
DECISION ENGINE outputs.

USER QUESTION

{question}

Answer using ONLY the supplied information.

For numerical questions, use the exact numbers
provided above.

For comparisons, clearly state which category,
industry, customer, or action ranks highest.

Keep the response concise and business-friendly.
"""

                with st.spinner(
                    "Analyzing complete business dataset..."
                ):

                    try:

                        response = client.responses.create(
                            model="gpt-5.6-luna",
                            input=prompt
                        )

                        st.success(
                            "🤖 Business AI Analysis"
                        )

                        st.markdown(
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
    "AI responses are grounded in the available RavenStack "
    "customer risk and decision-engine data."
)

st.caption(
    "Predictions and Revenue at Risk are estimates and should "
    "support—not replace—business judgment."
)
