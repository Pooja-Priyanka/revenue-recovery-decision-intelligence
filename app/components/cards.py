import streamlit as st


def metric_card(title, value, icon="📊"):

    st.markdown(
        f'<div style="background:#ffffff;padding:20px;border-radius:14px;border:1px solid #e6e9ef;box-shadow:0 2px 8px rgba(0,0,0,0.04);min-height:105px;">'
        f'<div style="font-size:14px;color:#5f6368;margin-bottom:8px;">{icon} {title}</div>'
        f'<div style="font-size:28px;font-weight:700;color:#202124;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
