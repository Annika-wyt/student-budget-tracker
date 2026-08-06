"""Calculation functions for the Student Budget Tracker.

Keep calculations separate from Streamlit so they are easy to understand and
test. Ask your AI assistant to help you implement one TODO at a time.
"""


def calculate_total_expenses(transactions):
    """Return the sum of all expense transaction amounts.

    TODO: Filter the data to Expense rows and add their amounts.
    """
    if transactions.empty:
        return 0.0

    # Starter behavior. Replace this while completing Learning Step 4.
    return 0.0


def calculate_total_income(transactions):
    """Return the sum of all income transaction amounts.

    TODO: Filter the data to Income rows and add their amounts.
    """
    if transactions.empty:
        return 0.0

    # Starter behavior. Replace this while completing Learning Step 4.
    return 0.0


def calculate_balance(total_income, total_expenses):
    """Return income minus expenses."""
    return total_income - total_expenses
