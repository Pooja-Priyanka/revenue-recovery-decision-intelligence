import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Revenue Recovery",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = "data/processed/customer_risk_decisions.csv"

df = pd.read_csv(DATA_PATH)


# --------------------------------------------------
# PAGE DEFINITIONS
# --------------------------------------------------

overview = st.Page(
    "pages/overview.py",
    title="Overview",
    icon="🏠",
    default=True
)

customers = st.Page(
    "pages/customers.py",
    title="Customers",
    icon="👥"
)

decisions = st.Page(
    "pages/decisions.py",
    title="Decision Center",
    icon="🎯"
)

analytics = st.Page(
    "pages/analytics.py",
    title="Analytics",
    icon="📈"
)

ai_assistant = st.Page(
    "pages/ai_assistant.py",
    title="AI Assistant",
    icon="🤖"
)


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

pg = st.navigation(
    [
        overview,
        customers,
        decisions,
        analytics,
        ai_assistant
    ]
)


# --------------------------------------------------
# CUSTOM SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("💰 Revenue Recovery")

    st.caption(
        "Decision Intelligence Platform"
    )

    st.divider()

    st.caption(
        "RavenStack SaaS Analytics"
    )


# --------------------------------------------------
# RUN SELECTED PAGE
# --------------------------------------------------

pg.run()
