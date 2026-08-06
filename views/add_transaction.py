"""Transaction form page for the Student Budget Tracker."""

from datetime import date

import streamlit as st


TRANSACTION_TYPES = ["Expense", "Income"]
CATEGORIES = ["Housing", "Groceries", "Transport", "Other"]


st.title("Add Transaction")
st.write("Start with the form, then connect it to the database.")

with st.form("transaction_form"):
    transaction_type = st.selectbox("Transaction type", TRANSACTION_TYPES)
    description = st.text_input("Description")
    amount = st.number_input("Amount in SEK", min_value=0.0, step=10.0)
    category = st.selectbox("Category", CATEGORIES)
    transaction_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save transaction")

if submitted:
    if description.strip() == "" or amount <= 0:
        st.error("Enter a description and an amount greater than 0 SEK.")
    else:
        # TODO: Call add_transaction from database.py here.
        st.warning(
            "The form works, but saving is your next task. "
            "Connect it to database.add_transaction()."
        )
