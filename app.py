"""Main entry point for the Student Budget Tracker."""

import streamlit as st


st.set_page_config(
    page_title="Student Budget Tracker",
    page_icon="💰",
)

pages = [
    st.Page("views/overview.py", title="Overview", icon="📊"),
    st.Page("views/add_transaction.py", title="Add Transaction", icon="➕"),
]

selected_page = st.navigation(pages)
selected_page.run()
