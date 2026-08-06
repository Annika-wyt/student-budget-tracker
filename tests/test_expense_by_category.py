import sqlite3
from datetime import date

import pandas as pd
import pytest

import database
from analytics import (
    calculate_category_summary,
    calculate_total_spending,
    get_highest_spending_category,
)


@pytest.fixture
def sample_expenses():
    return pd.DataFrame(
        [
            {
                "id": 1,
                "description": "Food shop",
                "amount": 200.0,
                "category": "Groceries",
                "expense_date": "2026-08-01",
            },
            {
                "id": 2,
                "description": "More food",
                "amount": 300.0,
                "category": "Groceries",
                "expense_date": "2026-08-03",
            },
            {
                "id": 3,
                "description": "Bus card",
                "amount": 500.0,
                "category": "Transport",
                "expense_date": "2026-08-04",
            },
        ]
    )


def test_multiple_expenses_in_same_category(sample_expenses):
    summary = calculate_category_summary(sample_expenses)
    groceries = summary[summary["category"] == "Groceries"].iloc[0]

    assert groceries["amount"] == 500.0
    assert groceries["expenses"] == 2


def test_expenses_across_several_categories(sample_expenses):
    summary = calculate_category_summary(sample_expenses)

    assert set(summary["category"]) == {"Groceries", "Transport"}
    assert get_highest_spending_category(summary) == "Groceries"


def test_percentages_add_up_to_approximately_100(sample_expenses):
    summary = calculate_category_summary(sample_expenses)

    assert summary["percentage"].sum() == pytest.approx(100.0)


def test_empty_expense_list():
    expenses = pd.DataFrame(columns=["id", "amount", "category", "expense_date"])

    summary = calculate_category_summary(expenses)

    assert summary.empty
    assert get_highest_spending_category(summary) == "None"


def test_category_containing_only_one_expense(sample_expenses):
    summary = calculate_category_summary(sample_expenses)
    transport = summary[summary["category"] == "Transport"].iloc[0]

    assert transport["amount"] == 500.0
    assert transport["expenses"] == 1
    assert transport["percentage"] == pytest.approx(50.0)


def test_example_category_percentages(sample_expenses):
    summary = calculate_category_summary(sample_expenses)
    groceries = summary[summary["category"] == "Groceries"].iloc[0]
    transport = summary[summary["category"] == "Transport"].iloc[0]

    assert groceries["amount"] == 500.0
    assert transport["amount"] == 500.0
    assert groceries["percentage"] == pytest.approx(50.0)
    assert transport["percentage"] == pytest.approx(50.0)


def test_income_is_excluded_from_expense_totals_and_categories(sample_expenses):
    expenses = pd.concat(
        [
            sample_expenses,
            pd.DataFrame(
                [
                    {
                        "id": 4,
                        "description": "CSN",
                        "amount": 12500.0,
                        "category": "Income",
                        "expense_date": "2026-08-25",
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    summary = calculate_category_summary(expenses)

    assert calculate_total_spending(expenses) == 1000.0
    assert "Income" not in set(summary["category"])
    assert get_highest_spending_category(summary) == "Groceries"


def test_filtering_by_month(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "test_student_budget.db")

    try:
        database.create_expenses_table()
        database.add_expense("August food", 100.0, "Groceries", "2026-08-01")
        database.add_expense("July food", 200.0, "Groceries", "2026-07-01")

        expenses = database.get_filtered_expenses(year="2026", month="08")

        assert len(expenses) == 1
        assert expenses.iloc[0]["description"] == "August food"
    finally:
        database.DATABASE_NAME = original_database_name


def test_filtering_by_category(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "test_student_budget.db")

    try:
        database.create_expenses_table()
        database.add_expense("Food", 100.0, "Groceries", "2026-08-01")
        database.add_expense("Bus", 200.0, "Transport", "2026-08-01")

        expenses = database.get_filtered_expenses(category="Transport")

        assert len(expenses) == 1
        assert expenses.iloc[0]["category"] == "Transport"
    finally:
        database.DATABASE_NAME = original_database_name


def test_saving_and_updating_budget_for_each_month(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "test_student_budget.db")

    try:
        database.create_budgets_table()
        database.save_budget("Groceries", 3000.0, "2026-08")
        database.save_budget("Groceries", 3500.0, "2026-08")
        database.save_budget("Groceries", 3200.0, "2026-09")

        august_budgets = database.get_budgets("2026-08")
        september_budgets = database.get_budgets("2026-09")

        assert len(august_budgets) == 1
        assert august_budgets.iloc[0]["category"] == "Groceries"
        assert august_budgets.iloc[0]["amount"] == 3500.0
        assert september_budgets.iloc[0]["amount"] == 3200.0
    finally:
        database.DATABASE_NAME = original_database_name


def test_legacy_budgets_are_migrated_to_the_current_month(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "legacy_student_budget.db")

    try:
        connection = sqlite3.connect(database.DATABASE_NAME)
        connection.execute(
            """
            CREATE TABLE budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            "INSERT INTO budgets (category, amount) VALUES (?, ?)",
            ("Housing", 6000.0),
        )
        connection.commit()
        connection.close()

        database.create_budgets_table()

        migration_month = date.today().strftime("%Y-%m")
        migrated_budgets = database.get_budgets(migration_month)
        assert len(migrated_budgets) == 1
        assert migrated_budgets.iloc[0]["category"] == "Housing"
        assert migrated_budgets.iloc[0]["amount"] == 6000.0

        database.save_budget("Housing", 6100.0, "2027-01")
        assert len(database.get_budgets()) == 2
    finally:
        database.DATABASE_NAME = original_database_name


def test_legacy_records_migrate_to_explicit_transaction_types(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "legacy_transactions.db")

    try:
        connection = sqlite3.connect(database.DATABASE_NAME)
        connection.execute(
            """
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO expenses (description, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Food", 200.0, "Groceries", "2026-08-01"),
                ("CSN", 12500.0, "Income", "2026-08-25"),
            ],
        )
        connection.commit()
        connection.close()

        database.create_expenses_table()
        transactions = database.get_all_expenses()

        groceries = transactions[transactions["description"] == "Food"].iloc[0]
        csn = transactions[transactions["description"] == "CSN"].iloc[0]
        assert groceries["transaction_type"] == "Expense"
        assert csn["transaction_type"] == "Income"
        assert "from_account" in transactions.columns
        assert "to_account" in transactions.columns
    finally:
        database.DATABASE_NAME = original_database_name


def test_saving_transfer_is_stored_and_filtered_separately(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "transfer_transactions.db")

    try:
        database.create_expenses_table()
        database.add_transaction(
            description="Emergency fund",
            amount=1000.0,
            category="Transfer",
            transaction_type="Transfer",
            expense_date="2026-08-15",
            from_account="Everyday account",
            to_account="Savings account",
        )

        transfers = database.get_filtered_expenses(transaction_type="Transfer")

        assert len(transfers) == 1
        assert transfers.iloc[0]["from_account"] == "Everyday account"
        assert transfers.iloc[0]["to_account"] == "Savings account"
        assert transfers.iloc[0]["amount"] == 1000.0
    finally:
        database.DATABASE_NAME = original_database_name
