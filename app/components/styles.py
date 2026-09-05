import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* -------------------------------------------
           MAIN APP
        ------------------------------------------- */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* -------------------------------------------
           HEADINGS
        ------------------------------------------- */

        h1 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        h2 {
            font-weight: 650;
        }

        h3 {
            font-weight: 600;
        }


        /* -------------------------------------------
           METRIC CARDS
        ------------------------------------------- */

        div[data-testid="stMetric"] {
            background: white;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #e6e9ef;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
        }


        /* -------------------------------------------
           DATAFRAMES
           ------------------------------------------- */

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }


        /* -------------------------------------------
           BUTTONS
           ------------------------------------------- */

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }


        /* -------------------------------------------
           SIDEBAR
           ------------------------------------------- */

        section[data-testid="stSidebar"] {
            border-right: 1px solid #e6e9ef;
        }


        /* -------------------------------------------
           DIVIDERS
           ------------------------------------------- */

        hr {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
