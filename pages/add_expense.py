import sqlite3
from datetime import date

import streamlit as st

from database import (
    add_transaction,
    create_budgets_table,
    create_expenses_table,
    delete_transaction,
    get_all_expenses,
)


TRANSACTION_TYPES = ["Expense", "Income", "Transfer"]
EXPENSE_CATEGORIES = [
    "Housing",
    "Groceries",
    "Transport",
    "Eating out",
    "Phone and internet",
    "Study materials",
    "Entertainment",
    "Relocation",
    "Other",
]
INCOME_CATEGORIES = [
    "CSN",
    "Salary",
    "Scholarship",
    "Family support",
    "Other income",
]
ACCOUNTS = [
    "Everyday account",
    "Savings account",
    "Cash",
    "Investment account",
]

ALL_MONTHS = "All months"
ALL_CATEGORIES = "All categories"
ALL_TYPES = "All types"


def get_month_options(transactions):
    """Create month options from saved transaction dates."""
    if transactions.empty:
        return [ALL_MONTHS]

    months = sorted(
        transactions["expense_date"].str.slice(0, 7).unique(),
        reverse=True,
    )
    return [ALL_MONTHS] + months


def filter_transactions(
    transactions,
    selected_month,
    selected_type,
    selected_category,
):
    """Filter transactions by month, type, and category."""
    filtered_transactions = transactions.copy()

    if selected_month != ALL_MONTHS:
        filtered_transactions = filtered_transactions[
            filtered_transactions["expense_date"].str.startswith(selected_month)
        ]

    if selected_type != ALL_TYPES:
        filtered_transactions = filtered_transactions[
            filtered_transactions["transaction_type"] == selected_type
        ]

    if selected_category != ALL_CATEGORIES:
        filtered_transactions = filtered_transactions[
            filtered_transactions["category"] == selected_category
        ]

    return filtered_transactions


def format_transaction_option(transaction):
    """Create a readable label for the delete dropdown."""
    if transaction["transaction_type"] == "Transfer":
        detail = f"{transaction['from_account']} → {transaction['to_account']}"
    else:
        detail = transaction["category"]

    return (
        f"{transaction['id']}: {transaction['expense_date']} - "
        f"{transaction['transaction_type']} - {detail} - "
        f"{transaction['description']} ({transaction['amount']:.2f} SEK)"
    )


def validate_transaction(
    description,
    amount,
    transaction_type,
    category,
    transaction_date,
    from_account=None,
    to_account=None,
):
    """Validate values for an expense, income, or transfer."""
    errors = []

    if transaction_type in {"Expense", "Income"} and description.strip() == "":
        errors.append("Please enter a description.")

    if amount is None:
        errors.append("Please enter an amount in SEK.")
    elif amount <= 0:
        errors.append("Please enter an amount greater than 0 SEK.")

    if transaction_type == "Expense" and category not in EXPENSE_CATEGORIES:
        errors.append("Please choose a valid expense category.")

    if transaction_type == "Income" and category not in INCOME_CATEGORIES:
        errors.append("Please choose a valid income source.")

    if transaction_type == "Transfer":
        if from_account not in ACCOUNTS or to_account not in ACCOUNTS:
            errors.append("Please choose valid source and destination accounts.")
        elif from_account == to_account:
            errors.append("Source and destination accounts must be different.")

    if transaction_date is None:
        errors.append("Please choose a date.")

    return errors


create_expenses_table()
create_budgets_table()

st.title("Add Transaction")
st.write("Record an expense, income payment, or transfer to savings.")

if "transaction_success_message" in st.session_state:
    st.success(st.session_state.pop("transaction_success_message"))

if "delete_success_message" in st.session_state:
    st.success(st.session_state.pop("delete_success_message"))

transaction_type = st.radio(
    "Transaction type",
    TRANSACTION_TYPES,
    horizontal=True,
)

with st.form(f"add_{transaction_type.lower()}_form"):
    if transaction_type == "Expense":
        description = st.text_input("Description", key="expense_description")
        category = st.selectbox("Expense category", EXPENSE_CATEGORIES)
        from_account = None
        to_account = None
    elif transaction_type == "Income":
        description = st.text_input("Description", key="income_description")
        category = st.selectbox("Income source", INCOME_CATEGORIES)
        from_account = None
        to_account = None
    else:
        description = st.text_input(
            "Note or savings goal (optional)",
            key="transfer_description",
        )
        category = "Transfer"
        account_column_one, account_column_two = st.columns(2)
        with account_column_one:
            from_account = st.selectbox("From account", ACCOUNTS)
        with account_column_two:
            to_account = st.selectbox("To account", ACCOUNTS, index=1)

    amount = st.number_input(
        "Amount in SEK",
        min_value=0.0,
        value=0.0,
        step=10.0,
    )
    transaction_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Save transaction")

if submitted:
    validation_errors = validate_transaction(
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        transaction_date=transaction_date,
        from_account=from_account,
        to_account=to_account,
    )

    if validation_errors:
        for error in validation_errors:
            st.error(error)
    else:
        record_description = description.strip()
        if transaction_type == "Transfer" and record_description == "":
            record_description = f"{from_account} to {to_account}"

        try:
            add_transaction(
                description=record_description,
                amount=amount,
                category=category,
                transaction_type=transaction_type,
                expense_date=transaction_date.isoformat(),
                from_account=from_account,
                to_account=to_account,
            )
            st.session_state["transaction_success_message"] = (
                f"{transaction_type} saved successfully."
            )
            st.rerun()
        except sqlite3.Error:
            st.error("The transaction could not be saved. Please try again.")

st.subheader("Transactions")

transactions = get_all_expenses()

if transactions.empty:
    st.info("No transactions have been saved yet.")
else:
    filter_column_one, filter_column_two, filter_column_three = st.columns(3)
    with filter_column_one:
        selected_month = st.selectbox(
            "Filter by month",
            get_month_options(transactions),
        )
    with filter_column_two:
        selected_type = st.selectbox(
            "Filter by type",
            [ALL_TYPES] + TRANSACTION_TYPES,
        )
    with filter_column_three:
        category_options = [ALL_CATEGORIES] + sorted(
            transactions["category"].unique()
        )
        selected_category = st.selectbox(
            "Filter by category",
            category_options,
        )

    filtered_transactions = filter_transactions(
        transactions=transactions,
        selected_month=selected_month,
        selected_type=selected_type,
        selected_category=selected_category,
    )

    if filtered_transactions.empty:
        st.info("No transactions match the selected filters.")
    else:
        display_transactions = filtered_transactions[
            [
                "transaction_type",
                "description",
                "amount",
                "category",
                "from_account",
                "to_account",
                "expense_date",
            ]
        ].rename(
            columns={
                "transaction_type": "Type",
                "description": "Description",
                "amount": "Amount (SEK)",
                "category": "Category / source",
                "from_account": "From",
                "to_account": "To",
                "expense_date": "Date",
            }
        )
        st.dataframe(display_transactions, use_container_width=True, hide_index=True)

        with st.expander("Delete a transaction"):
            delete_options = {}
            for _, transaction in filtered_transactions.iterrows():
                option_label = format_transaction_option(transaction)
                delete_options[option_label] = int(transaction["id"])

            selected_transaction = st.selectbox(
                "Choose a transaction to delete",
                delete_options.keys(),
            )

            if st.button("Delete selected transaction"):
                deleted_rows = delete_transaction(
                    delete_options[selected_transaction]
                )

                if deleted_rows == 0:
                    st.error("That transaction could not be found.")
                else:
                    st.session_state["delete_success_message"] = (
                        "Transaction deleted successfully."
                    )
                    st.rerun()
