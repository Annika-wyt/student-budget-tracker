"""Database functions for the Student Budget Tracker.

This module is deliberately incomplete. It gives students one place for all
SQLite code without mixing database work into the Streamlit pages.
"""

import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path(__file__).with_name("student_budget.db")


def create_connection():
    """Create and return a connection to the local SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


def create_transactions_table():
    """Create the transactions table.

    TODO: Write a CREATE TABLE IF NOT EXISTS query with these fields:
    id, transaction_type, description, amount, category, transaction_date,
    and created_at.
    """
    # The function is intentionally empty for the database learning exercise.
    pass


def add_transaction(
    transaction_type,
    description,
    amount,
    category,
    transaction_date,
):
    """Save one transaction.

    TODO: Insert the supplied values with a parameterized SQL query.
    """
    raise NotImplementedError("Complete add_transaction in database.py")


def get_all_transactions():
    """Return all transactions as a pandas DataFrame.

    TODO: Replace the empty DataFrame with a SELECT query.
    """
    return pd.DataFrame(
        columns=[
            "id",
            "transaction_type",
            "description",
            "amount",
            "category",
            "transaction_date",
            "created_at",
        ]
    )
