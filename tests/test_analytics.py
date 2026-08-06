"""Starter tests for analytics.py."""

import pandas as pd

from analytics import (
    calculate_balance,
    calculate_total_expenses,
    calculate_total_income,
)


def test_calculate_balance():
    assert calculate_balance(5000.0, 1250.0) == 3750.0


def test_empty_transactions_have_zero_expenses():
    transactions = pd.DataFrame()
    assert calculate_total_expenses(transactions) == 0.0


def test_empty_transactions_have_zero_income():
    transactions = pd.DataFrame()
    assert calculate_total_income(transactions) == 0.0


# TODO: Add tests containing Expense and Income rows before implementing the
# remaining analytics functions. Ask your AI assistant to explain the expected
# result rather than asking it to write every test at once.
