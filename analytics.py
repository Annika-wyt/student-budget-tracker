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
