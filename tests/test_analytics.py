import unittest
from datetime import date

import pandas as pd

from analytics import (
    calculate_category_budget_summary,
    calculate_budget_overview,
    calculate_budget_status,
    calculate_monthly_spending,
    calculate_saved_budget_overview,
)


class BudgetAnalyticsTests(unittest.TestCase):
    def test_calculate_monthly_spending_only_includes_current_month(self):
        expenses = pd.DataFrame(
            [
                {"amount": 100.0, "expense_date": "2026-08-01"},
                {"amount": 250.0, "expense_date": "2026-08-15"},
                {"amount": 90.0, "expense_date": "2026-07-30"},
            ]
        )

        result = calculate_monthly_spending(expenses, date(2026, 8, 20))

        self.assertEqual(result, 350.0)

    def test_calculate_monthly_spending_returns_zero_for_empty_data(self):
        expenses = pd.DataFrame(columns=["amount", "expense_date"])

        result = calculate_monthly_spending(expenses, date(2026, 8, 20))

        self.assertEqual(result, 0.0)

    def test_calculate_budget_status_on_track(self):
        self.assertEqual(calculate_budget_status(79.9), "On track")

    def test_calculate_budget_status_close_to_budget(self):
        self.assertEqual(calculate_budget_status(80.0), "Close to budget")
        self.assertEqual(calculate_budget_status(99.9), "Close to budget")

    def test_calculate_budget_status_over_budget(self):
        self.assertEqual(calculate_budget_status(100.0), "Over budget")
        self.assertEqual(calculate_budget_status(125.0), "Over budget")

    def test_calculate_budget_overview(self):
        result = calculate_budget_overview(5000.0, 1250.0)

        self.assertEqual(result["budget"], 5000.0)
        self.assertEqual(result["spent"], 1250.0)
        self.assertEqual(result["remaining"], 3750.0)
        self.assertEqual(result["percentage_used"], 25.0)
        self.assertEqual(result["status"], "On track")

    def test_calculate_category_budget_summary(self):
        budgets = pd.DataFrame(
            [
                {"category": "Groceries", "amount": 1000.0},
                {"category": "Transport", "amount": 500.0},
            ]
        )
        expenses = pd.DataFrame(
            [
                {"category": "Groceries", "amount": 250.0, "expense_date": "2026-08-01"},
                {"category": "Groceries", "amount": 550.0, "expense_date": "2026-08-12"},
                {"category": "Transport", "amount": 700.0, "expense_date": "2026-08-20"},
                {"category": "Groceries", "amount": 999.0, "expense_date": "2026-07-20"},
            ]
        )

        result = calculate_category_budget_summary(
            budgets,
            expenses,
            date(2026, 8, 21),
        )

        groceries = result[result["category"] == "Groceries"].iloc[0]
        transport = result[result["category"] == "Transport"].iloc[0]

        self.assertEqual(groceries["spent"], 800.0)
        self.assertEqual(groceries["remaining"], 200.0)
        self.assertEqual(groceries["status"], "Close to budget")
        self.assertEqual(transport["spent"], 700.0)
        self.assertEqual(transport["status"], "Over budget")

    def test_calculate_saved_budget_overview(self):
        category_budget_summary = pd.DataFrame(
            [
                {
                    "category": "Groceries",
                    "budget": 1000.0,
                    "spent": 800.0,
                    "remaining": 200.0,
                    "percentage_used": 80.0,
                    "status": "Close to budget",
                },
                {
                    "category": "Transport",
                    "budget": 500.0,
                    "spent": 700.0,
                    "remaining": -200.0,
                    "percentage_used": 140.0,
                    "status": "Over budget",
                },
            ]
        )

        result = calculate_saved_budget_overview(category_budget_summary)

        self.assertEqual(result["budget"], 1500.0)
        self.assertEqual(result["spent"], 1500.0)
        self.assertEqual(result["remaining"], 0.0)
        self.assertEqual(result["percentage_used"], 100.0)
        self.assertEqual(result["number_of_budgets"], 2)
        self.assertEqual(result["on_track_count"], 1)
        self.assertEqual(result["over_budget_count"], 1)
        self.assertEqual(result["status"], "Over budget")


if __name__ == "__main__":
    unittest.main()
