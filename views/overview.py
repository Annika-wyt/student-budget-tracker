"""Overview page for the Student Budget Tracker."""

import streamlit as st

from analytics import calculate_balance


st.title("Overview")
st.write("This page will become the budget dashboard.")

# These placeholder values keep the starter application runnable.
# TODO: Load transactions from database.py and calculate real values.
total_income = 0.0
total_expenses = 0.0
balance = calculate_balance(total_income, total_expenses)

income_column, expense_column, balance_column = st.columns(3)

with income_column:
    st.metric("Income", f"{total_income:.2f} SEK")

with expense_column:
    st.metric("Expenses", f"{total_expenses:.2f} SEK")

with balance_column:
    st.metric("Balance", f"{balance:.2f} SEK")

st.info(
    "Starter task: connect this page to the database and replace the "
    "placeholder values with real calculations."
)
