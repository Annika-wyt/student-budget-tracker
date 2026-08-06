import sqlite3
from datetime import date

import streamlit as st

from database import (
    add_expense,
    create_budgets_table,
    create_expenses_table,
    delete_expense,
    get_all_expenses,
)


CATEGORIES = [
    "Housing",
    "Groceries",
    "Transport",
    "Eating out",
    "Phone and internet",
    "Study materials",
    "Entertainment",
    "Relocation",
    "Income",
    "Other",
]

ALL_MONTHS = "All months"
ALL_CATEGORIES = "All categories"


def get_month_options(expenses):
    """Create a list of month options from the saved expense dates."""
    if expenses.empty:
        return [ALL_MONTHS]

    months = expenses["expense_date"].str.slice(0, 7).drop_duplicates().tolist()
    return [ALL_MONTHS] + months


def filter_expenses(expenses, selected_month, selected_category):
    """Filter expenses by month and category."""
    filtered_expenses = expenses.copy()

    if selected_month != ALL_MONTHS:
        filtered_expenses = filtered_expenses[
            filtered_expenses["expense_date"].str.startswith(selected_month)
        ]

    if selected_category != ALL_CATEGORIES:
        filtered_expenses = filtered_expenses[
            filtered_expenses["category"] == selected_category
        ]

    return filtered_expenses


def format_expense_option(expense):
    """Create a readable label for one expense in the delete dropdown."""
    return (
        f"{expense['id']}: {expense['expense_date']} - "
        f"{expense['category']} - {expense['description']} "
        f"({expense['amount']:.2f} SEK)"
    )


def validate_expense(description, amount, category, expense_date):
    """Check the expense form values before saving."""
    errors = []

    if description.strip() == "":
        errors.append("Please enter a description.")

    if amount is None:
        errors.append("Please enter an amount in SEK.")
    elif amount <= 0:
        errors.append("Please enter an amount greater than 0 SEK.")

    if category not in CATEGORIES:
        errors.append("Please choose a valid category.")

    if expense_date is None:
        errors.append("Please choose a date.")

    return errors


create_expenses_table()
create_budgets_table()

st.title("Add Expense")
st.write("Save an expense or income record in SEK.")

if "delete_success_message" in st.session_state:
    st.success(st.session_state.pop("delete_success_message"))

with st.form("add_expense_form"):
    description = st.text_input("Description")
    amount = st.number_input("Amount in SEK", value=0.0, step=10.0)
    category = st.selectbox("Category", CATEGORIES)
    expense_date = st.date_input("Date", value=date.today())

    submitted = st.form_submit_button("Save record")

if submitted:
    validation_errors = validate_expense(description, amount, category, expense_date)

    if validation_errors:
        for error in validation_errors:
            st.error(error)
    else:
        try:
            add_expense(
                description=description.strip(),
                amount=amount,
                category=category,
                expense_date=expense_date.isoformat(),
            )
            st.success("Record saved successfully.")
        except sqlite3.Error:
            st.error("The record could not be saved. Please try again.")

st.subheader("Saved records")

expenses = get_all_expenses()

if expenses.empty:
    st.info("No records have been saved yet.")
else:
    month_options = get_month_options(expenses)

    selected_month = st.selectbox("Filter by month", month_options)
    selected_category = st.selectbox(
        "Filter by category",
        [ALL_CATEGORIES] + CATEGORIES,
    )

    filtered_expenses = filter_expenses(
        expenses=expenses,
        selected_month=selected_month,
        selected_category=selected_category,
    )

    if filtered_expenses.empty:
        st.info("No records match the selected filters.")
    else:
        st.dataframe(filtered_expenses, use_container_width=True, hide_index=True)

        st.subheader("Delete a record")

        delete_options = {}
        for _, expense in filtered_expenses.iterrows():
            option_label = format_expense_option(expense)
            delete_options[option_label] = int(expense["id"])

        selected_expense = st.selectbox(
            "Choose a record to delete",
            delete_options.keys(),
        )

        if st.button("Delete selected record"):
            deleted_rows = delete_expense(delete_options[selected_expense])

            if deleted_rows == 0:
                st.error("That record could not be found.")
            else:
                st.session_state["delete_success_message"] = (
                    "Record deleted successfully."
                )
                st.rerun()
