import pandas as pd
import pytest

import database
from analytics import calculate_category_summary, get_highest_spending_category


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


def test_saving_and_updating_budget(tmp_path):
    original_database_name = database.DATABASE_NAME
    database.DATABASE_NAME = str(tmp_path / "test_student_budget.db")

    try:
        database.create_budgets_table()
        database.save_budget("Groceries", 3000.0)
        database.save_budget("Groceries", 3500.0)

        budgets = database.get_budgets()

        assert len(budgets) == 1
        assert budgets.iloc[0]["category"] == "Groceries"
        assert budgets.iloc[0]["amount"] == 3500.0
    finally:
        database.DATABASE_NAME = original_database_name
