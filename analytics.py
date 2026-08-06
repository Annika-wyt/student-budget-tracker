def calculate_total_spending(expenses):
    """Calculate the total amount spent."""
    if expenses.empty:
        return 0.0

    return expenses["amount"].sum()


def calculate_number_of_expenses(expenses):
    """Count how many expenses are in the data."""
    return len(expenses)


def calculate_spending_by_category(expenses):
    """Calculate total spending for each category."""
    if expenses.empty:
        return expenses

    return (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def calculate_expense_category_summary(expenses):
    """Calculate spending by category, excluding income rows."""
    if expenses.empty:
        return expenses

    expense_rows = expenses[expenses["category"] != "Income"]

    if expense_rows.empty:
        return expense_rows

    return (
        expense_rows.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def calculate_income_summary(expenses):
    """Calculate income totals grouped by description."""
    if expenses.empty:
        return expenses

    income_rows = expenses[expenses["category"] == "Income"]

    if income_rows.empty:
        return income_rows

    return (
        income_rows.groupby("description", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def calculate_category_summary(expenses):
    """Calculate category totals, percentages, and expense counts."""
    if expenses.empty:
        return expenses

    total_spending = expenses["amount"].sum()
    summary = (
        expenses.groupby("category", as_index=False)
        .agg(
            amount=("amount", "sum"),
            expenses=("id", "count"),
        )
        .sort_values("amount", ascending=False)
    )

    if total_spending == 0:
        summary["percentage"] = 0.0
    else:
        summary["percentage"] = (summary["amount"] / total_spending) * 100

    return summary


def get_highest_spending_category(category_summary):
    """Find the category with the highest total spending."""
    if category_summary.empty:
        return "None"

    return category_summary.iloc[0]["category"]


def format_currency(amount):
    """Format a number as Swedish kronor."""
    return f"{amount:,.2f} SEK"


def calculate_monthly_spending(expenses, current_date):
    """Calculate spending for the current calendar month."""
    if expenses.empty:
        return 0.0

    current_month = current_date.strftime("%Y-%m")
    monthly_expenses = expenses[
        expenses["expense_date"].str.startswith(current_month)
    ]

    return monthly_expenses["amount"].sum()


def calculate_budget_status(percentage_used):
    """Choose a budget status message from the percentage used."""
    if percentage_used < 80:
        return "On track"

    if percentage_used < 100:
        return "Close to budget"

    return "Over budget"


def calculate_budget_overview(budget_amount, spent_amount):
    """Calculate budget dashboard numbers."""
    remaining_amount = budget_amount - spent_amount
    percentage_used = (spent_amount / budget_amount) * 100
    status = calculate_budget_status(percentage_used)

    return {
        "budget": budget_amount,
        "spent": spent_amount,
        "remaining": remaining_amount,
        "percentage_used": percentage_used,
        "status": status,
    }


def calculate_category_budget_summary(budgets, expenses, current_date):
    """Compare each saved category budget with current-month spending."""
    if budgets.empty:
        return budgets

    current_month = current_date.strftime("%Y-%m")
    monthly_expenses = expenses[
        expenses["expense_date"].str.startswith(current_month)
    ]

    if monthly_expenses.empty:
        spending_by_category = {}
    else:
        spending_by_category = (
            monthly_expenses.groupby("category")["amount"].sum().to_dict()
        )

    budget_summary = budgets[["category", "amount"]].copy()
    budget_summary = budget_summary.rename(columns={"amount": "budget"})
    budget_summary["spent"] = budget_summary["category"].map(spending_by_category)
    budget_summary["spent"] = budget_summary["spent"].fillna(0.0)
    budget_summary["remaining"] = budget_summary["budget"] - budget_summary["spent"]
    budget_summary["percentage_used"] = (
        budget_summary["spent"] / budget_summary["budget"]
    ) * 100
    budget_summary["status"] = budget_summary["percentage_used"].apply(
        calculate_budget_status
    )

    return budget_summary.sort_values("percentage_used", ascending=False)


def calculate_saved_budget_overview(category_budget_summary):
    """Calculate dashboard totals from saved category budgets."""
    if category_budget_summary.empty:
        return {
            "budget": 0.0,
            "spent": 0.0,
            "remaining": 0.0,
            "percentage_used": 0.0,
            "number_of_budgets": 0,
            "on_track_count": 0,
            "over_budget_count": 0,
            "status": "No budgets saved",
        }

    total_budget = category_budget_summary["budget"].sum()
    total_spent = category_budget_summary["spent"].sum()
    percentage_used = (total_spent / total_budget) * 100

    return {
        "budget": total_budget,
        "spent": total_spent,
        "remaining": total_budget - total_spent,
        "percentage_used": percentage_used,
        "number_of_budgets": len(category_budget_summary),
        "on_track_count": (
            category_budget_summary["status"] != "Over budget"
        ).sum(),
        "over_budget_count": (
            category_budget_summary["status"] == "Over budget"
        ).sum(),
        "status": calculate_budget_status(percentage_used),
    }


def calculate_budget_remaining_summary(category_budget_summary):
    """Calculate remaining budget by category for chart display."""
    if category_budget_summary.empty:
        return category_budget_summary

    remaining_summary = category_budget_summary[
        category_budget_summary["remaining"] > 0
    ][["category", "remaining"]].copy()

    return remaining_summary.sort_values("remaining", ascending=False)
