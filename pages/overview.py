from datetime import date

import plotly.express as px
import streamlit as st

from analytics import (
    calculate_budget_remaining_summary,
    calculate_category_budget_summary,
    calculate_expense_category_summary,
    calculate_income_summary,
    calculate_saved_budget_overview,
    format_currency,
)
from database import (
    create_budgets_table,
    create_expenses_table,
    get_all_expenses,
    get_budgets,
)


ALL_MONTHS = "All months"
ALL_CATEGORIES = "All categories"


def create_donut_chart(data, names_column, values_column, title, center_text):
    """Create a reusable donut chart for the overview dashboard."""
    chart = px.pie(
        data,
        names=names_column,
        values=values_column,
        title=title,
        hole=0.45,
    )
    chart.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>%{value:.2f} SEK<br>%{percent}<extra></extra>",
    )
    chart.update_layout(
        annotations=[
            {
                "text": center_text,
                "x": 0.5,
                "y": 0.5,
                "font_size": 15,
                "showarrow": False,
            }
        ],
        legend_title_text="Category",
    )

    return chart


def get_month_options(expenses):
    """Create month filter options from saved records."""
    if expenses.empty:
        return [ALL_MONTHS]

    months = sorted(expenses["expense_date"].str.slice(0, 7).unique(), reverse=True)
    return [ALL_MONTHS] + months


def get_category_options(expenses):
    """Create category filter options from saved records."""
    if expenses.empty:
        return [ALL_CATEGORIES]

    categories = sorted(expenses["category"].unique())
    return [ALL_CATEGORIES] + categories


def filter_overview_records(expenses, selected_month, selected_category):
    """Filter overview records by month and category."""
    filtered_expenses = expenses.copy()

    if selected_month != ALL_MONTHS:
        filtered_expenses = filtered_expenses[
            filtered_expenses["expense_date"].str.startswith(selected_month)
        ]

    if selected_category != ALL_CATEGORIES:
        filtered_expenses = filtered_expenses[
            filtered_expenses["category"] == selected_category
        ]

    return filtered_expenses


def filter_budget_rows(category_budget_summary, selected_category):
    """Filter budget rows to match the selected overview category."""
    if selected_category == ALL_CATEGORIES or category_budget_summary.empty:
        return category_budget_summary

    return category_budget_summary[
        category_budget_summary["category"] == selected_category
    ]


create_expenses_table()
create_budgets_table()

st.title("Overview")
st.write("Overview of spending, income, and remaining category budgets.")

expenses = get_all_expenses()
budgets = get_budgets()

month_options = get_month_options(expenses)
category_options = get_category_options(expenses)

filter_column_one, filter_column_two = st.columns(2)

with filter_column_one:
    selected_month = st.selectbox("Filter by month", month_options)

with filter_column_two:
    selected_category = st.selectbox("Filter by category", category_options)

filtered_expenses = filter_overview_records(
    expenses,
    selected_month,
    selected_category,
)

if selected_month == ALL_MONTHS:
    budget_date = date.today()
else:
    budget_year, budget_month = selected_month.split("-")
    budget_date = date(int(budget_year), int(budget_month), 1)

expense_summary = calculate_expense_category_summary(filtered_expenses)
income_summary = calculate_income_summary(filtered_expenses)
category_budget_summary = calculate_category_budget_summary(
    budgets,
    expenses,
    budget_date,
)
category_budget_summary = filter_budget_rows(
    category_budget_summary,
    selected_category,
)
budget_remaining_summary = calculate_budget_remaining_summary(category_budget_summary)
budget_overview = calculate_saved_budget_overview(category_budget_summary)

total_expenses = 0.0 if expense_summary.empty else expense_summary["amount"].sum()
total_income = 0.0 if income_summary.empty else income_summary["amount"].sum()
net_balance = total_income - total_expenses

metric_column_one, metric_column_two, metric_column_three = st.columns(3)

with metric_column_one:
    st.metric("Total expenses", format_currency(total_expenses))

with metric_column_two:
    st.metric("Total income", format_currency(total_income))

with metric_column_three:
    st.metric("Income minus expenses", format_currency(net_balance))

budget_column_one, budget_column_two, budget_column_three = st.columns(3)

with budget_column_one:
    st.metric("Saved budgets", budget_overview["number_of_budgets"])

with budget_column_two:
    st.metric("Budget used", f"{budget_overview['percentage_used']:.1f}%")

with budget_column_three:
    st.metric("Budget status", budget_overview["status"])

st.subheader("Overview charts")

chart_column_one, chart_column_two = st.columns(2)

with chart_column_one:
    if expense_summary.empty:
        st.info("No expense categories match the selected filters.")
    else:
        expense_chart = create_donut_chart(
            expense_summary,
            names_column="category",
            values_column="amount",
            title="Expenses per Category",
            center_text=format_currency(total_expenses),
        )
        st.plotly_chart(expense_chart, use_container_width=True)

with chart_column_two:
    if income_summary.empty:
        st.info("No income records match the selected filters.")
    else:
        income_chart = create_donut_chart(
            income_summary,
            names_column="description",
            values_column="amount",
            title="Income Sources",
            center_text=format_currency(total_income),
        )
        st.plotly_chart(income_chart, use_container_width=True)

if budget_remaining_summary.empty:
    st.info("No remaining category budgets match the selected filters.")
else:
    remaining_total = budget_remaining_summary["remaining"].sum()
    budget_chart = create_donut_chart(
        budget_remaining_summary,
        names_column="category",
        values_column="remaining",
        title="Budget Left per Category",
        center_text=format_currency(remaining_total),
    )
    st.plotly_chart(budget_chart, use_container_width=True)

if expenses.empty:
    st.info("Add expenses or income on the Add Expense page to fill this overview.")
