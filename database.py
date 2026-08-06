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


def create_budgets_table():
    """Create the budgets table if it does not already exist."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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


def get_filtered_expenses(year=None, month=None, category=None):
    """Read expenses filtered by year, month, and category."""
    connection = create_connection()

    query = """
        SELECT id, description, amount, category, expense_date, created_at
        FROM expenses
        WHERE 1 = 1
    """
    parameters = []

    if year:
        query += " AND strftime('%Y', expense_date) = ?"
        parameters.append(str(year))

    if month:
        query += " AND strftime('%m', expense_date) = ?"
        parameters.append(f"{int(month):02d}")

    if category and category != "All categories":
        query += " AND category = ?"
        parameters.append(category)

    query += " ORDER BY expense_date DESC, id DESC"

    expenses = pd.read_sql_query(query, connection, params=parameters)

    connection.close()
    return expenses


def save_budget(category, amount):
    """Save or update a monthly budget for one category."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budgets (category, amount)
        VALUES (?, ?)
        ON CONFLICT(category)
        DO UPDATE SET
            amount = excluded.amount,
            updated_at = CURRENT_TIMESTAMP
        """,
        (category, amount),
    )

    connection.commit()
    connection.close()


def get_budgets():
    """Read all saved monthly budgets."""
    connection = create_connection()

    budgets = pd.read_sql_query(
        """
        SELECT id, category, amount, created_at, updated_at
        FROM budgets
        ORDER BY category
        """,
        connection,
    )

    connection.close()
    return budgets


def seed_dummy_data():
    """Add demo expenses, income, and budgets for January-August 2026."""
    create_expenses_table()
    create_budgets_table()

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM expenses
        WHERE description LIKE 'Demo %'
        """
    )
    demo_expense_count = cursor.fetchone()[0]

    if demo_expense_count == 0:
        demo_expenses = [
            ("Demo rent", 5200.0, "Housing", "2026-01-03"),
            ("Demo ICA groceries", 860.0, "Groceries", "2026-01-08"),
            ("Demo SL card", 650.0, "Transport", "2026-01-12"),
            ("Demo CSN", 12500.0, "Income", "2026-01-25"),
            ("Demo rent", 5200.0, "Housing", "2026-02-03"),
            ("Demo Willys groceries", 920.0, "Groceries", "2026-02-09"),
            ("Demo cafe lunch", 210.0, "Eating out", "2026-02-14"),
            ("Demo part-time job", 3400.0, "Income", "2026-02-27"),
            ("Demo rent", 5250.0, "Housing", "2026-03-03"),
            ("Demo textbooks", 740.0, "Study materials", "2026-03-06"),
            ("Demo phone plan", 249.0, "Phone and internet", "2026-03-10"),
            ("Demo CSN", 12500.0, "Income", "2026-03-25"),
            ("Demo rent", 5250.0, "Housing", "2026-04-03"),
            ("Demo groceries", 1050.0, "Groceries", "2026-04-11"),
            ("Demo cinema", 180.0, "Entertainment", "2026-04-18"),
            ("Demo family support", 2000.0, "Income", "2026-04-22"),
            ("Demo rent", 5300.0, "Housing", "2026-05-03"),
            ("Demo groceries", 980.0, "Groceries", "2026-05-08"),
            ("Demo train ticket", 420.0, "Transport", "2026-05-19"),
            ("Demo CSN", 12500.0, "Income", "2026-05-25"),
            ("Demo rent", 5300.0, "Housing", "2026-06-03"),
            ("Demo relocation supplies", 1350.0, "Relocation", "2026-06-13"),
            ("Demo restaurant", 390.0, "Eating out", "2026-06-21"),
            ("Demo part-time job", 4100.0, "Income", "2026-06-28"),
            ("Demo rent", 5350.0, "Housing", "2026-07-03"),
            ("Demo groceries", 1120.0, "Groceries", "2026-07-08"),
            ("Demo concert", 520.0, "Entertainment", "2026-07-17"),
            ("Demo CSN", 12500.0, "Income", "2026-07-25"),
            ("Demo rent", 5350.0, "Housing", "2026-08-03"),
            ("Demo groceries", 1190.0, "Groceries", "2026-08-07"),
            ("Demo phone plan", 249.0, "Phone and internet", "2026-08-10"),
            ("Demo part-time job", 3800.0, "Income", "2026-08-28"),
        ]

        cursor.executemany(
            """
            INSERT INTO expenses (description, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            demo_expenses,
        )

    demo_budgets = [
        ("Housing", 6000.0),
        ("Groceries", 2200.0),
        ("Transport", 900.0),
        ("Eating out", 800.0),
        ("Phone and internet", 350.0),
        ("Study materials", 900.0),
        ("Entertainment", 900.0),
        ("Relocation", 1500.0),
        ("Other", 700.0),
    ]

    cursor.executemany(
        """
        INSERT INTO budgets (category, amount)
        VALUES (?, ?)
        ON CONFLICT(category)
        DO UPDATE SET
            amount = excluded.amount,
            updated_at = CURRENT_TIMESTAMP
        """,
        demo_budgets,
    )

    connection.commit()
    connection.close()


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
    create_budgets_table()
    print("Database tables are ready.")
