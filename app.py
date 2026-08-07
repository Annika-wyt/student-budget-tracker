import streamlit as st


st.set_page_config(page_title="Student Budget Tracker", layout="wide")

pages = [
    st.Page("pages/overview.py", title="Overview"),
    st.Page("pages/add_expense.py", title="Add Transaction"),
    st.Page("pages/set_budget.py", title="Set Budget"),
    st.Page("pages/expense_by_category.py", title="Expense by Category"),
]

selected_page = st.navigation(pages)
selected_page.run()
