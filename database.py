import sqlite3

import pandas as pd


DATABASE_NAME = "student_budget.db"


def create_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_expenses_table():
    """Create the expenses table if it does not already exist."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def add_expense(description, amount, category, expense_date):
    """Save one expense in the expenses table."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (description, amount, category, expense_date)
        VALUES (?, ?, ?, ?)
        """,
        (description, amount, category, expense_date),
    )

    connection.commit()
    connection.close()


def get_all_expenses():
    """Read all saved expenses from the database."""
    connection = create_connection()

    expenses = pd.read_sql_query(
        """
        SELECT id, description, amount, category, expense_date, created_at
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """,
        connection,
    )

    connection.close()
    return expenses


def delete_expense(expense_id):
    """Delete one expense by its id."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,),
    )

    deleted_rows = cursor.rowcount
    connection.commit()
    connection.close()

    return deleted_rows


if __name__ == "__main__":
    create_expenses_table()
    print("Database and expenses table are ready.")
