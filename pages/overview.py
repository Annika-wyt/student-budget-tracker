from datetime import date, datetime

import plotly.express as px
import streamlit as st

from analytics import (
    calculate_budget_remaining_summary,
    calculate_category_budget_summary,
    calculate_expense_category_summary,
    calculate_income_summary,
    calculate_saved_budget_overview,
    calculate_transfer_summary,
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


def create_budget_balance_chart(data):
    """Create a signed balance chart that keeps over-budget categories visible."""
    chart_data = data.sort_values("remaining")
    chart = px.bar(
        chart_data,
        x="remaining",
        y="category",
        color="status",
        orientation="h",
        title="Budget Balance by Category",
        color_discrete_map={
            "On track": "#2e8b57",
            "Close to budget": "#e0a800",
            "Over budget": "#d9534f",
        },
    )
    chart.update_traces(
        hovertemplate="%{y}<br>%{x:.2f} SEK remaining<extra></extra>"
    )
    chart.add_vline(x=0, line_color="#555", line_width=1)
    chart.update_layout(xaxis_title="Remaining budget (SEK)", yaxis_title=None)
    return chart


def get_month_options(expenses, budgets):
    """Create month filter options from transactions and saved budgets."""
    months = {date.today().strftime("%Y-%m")}

    if not expenses.empty:
        months.update(expenses["expense_date"].str.slice(0, 7).unique())

    if not budgets.empty:
        months.update(budgets["year_month"].unique())

    return [ALL_MONTHS] + sorted(months, reverse=True)


def format_month_option(year_month):
    """Display a stored YYYY-MM period as a readable month name."""
    if year_month == ALL_MONTHS:
        return year_month

    return datetime.strptime(year_month, "%Y-%m").strftime("%B %Y")


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
all_budgets = get_budgets()

month_options = get_month_options(expenses, all_budgets)
category_options = get_category_options(expenses)
current_month = date.today().strftime("%Y-%m")

filter_column_one, filter_column_two = st.columns(2)

with filter_column_one:
    selected_month = st.selectbox(
        "Filter by month",
        month_options,
        index=month_options.index(current_month),
        format_func=format_month_option,
    )

with filter_column_two:
    selected_category = st.selectbox("Filter by category", category_options)

filtered_expenses = filter_overview_records(
    expenses,
    selected_month,
    selected_category,
)

expense_summary = calculate_expense_category_summary(filtered_expenses)
income_summary = calculate_income_summary(filtered_expenses)
transfer_summary = calculate_transfer_summary(filtered_expenses)

total_expenses = 0.0 if expense_summary.empty else expense_summary["amount"].sum()
total_income = 0.0 if income_summary.empty else income_summary["amount"].sum()
total_transfers = 0.0 if transfer_summary.empty else transfer_summary["amount"].sum()
net_balance = total_income - total_expenses

metric_column_one, metric_column_two, metric_column_three, metric_column_four = (
    st.columns(4)
)

with metric_column_one:
    st.metric("Total expenses", format_currency(total_expenses))

with metric_column_two:
    st.metric("Total income", format_currency(total_income))

with metric_column_three:
    st.metric("Income minus expenses", format_currency(net_balance))

with metric_column_four:
    st.metric("Account transfers", format_currency(total_transfers))

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
            names_column="source",
            values_column="amount",
            title="Income Sources",
            center_text=format_currency(total_income),
        )
        st.plotly_chart(income_chart, use_container_width=True)

if not transfer_summary.empty:
    transfer_chart = create_donut_chart(
        transfer_summary,
        names_column="destination",
        values_column="amount",
        title="Transfer Destinations",
        center_text=format_currency(total_transfers),
    )
    st.plotly_chart(transfer_chart, use_container_width=True)

if selected_month == ALL_MONTHS:
    st.info("Choose a specific month to compare spending with monthly budgets.")
else:
    budget_year, budget_month = selected_month.split("-")
    budget_date = date(int(budget_year), int(budget_month), 1)
    budgets = all_budgets[all_budgets["year_month"] == selected_month]
    category_budget_summary = calculate_category_budget_summary(
        budgets,
        expenses,
        budget_date,
    )
    category_budget_summary = filter_budget_rows(
        category_budget_summary,
        selected_category,
    )
    budget_balance_summary = calculate_budget_remaining_summary(
        category_budget_summary
    )
    budget_overview = calculate_saved_budget_overview(category_budget_summary)

    st.subheader(f"Budget for {format_month_option(selected_month)}")

    budget_column_one, budget_column_two, budget_column_three = st.columns(3)

    with budget_column_one:
        st.metric("Saved budgets", budget_overview["number_of_budgets"])

    with budget_column_two:
        st.metric("Budget used", f"{budget_overview['percentage_used']:.1f}%")

    with budget_column_three:
        st.metric("Budget status", budget_overview["status"])

    if budget_balance_summary.empty:
        st.info("No category budgets match the selected month and category.")
    else:
        budget_chart = create_budget_balance_chart(budget_balance_summary)
        st.plotly_chart(budget_chart, use_container_width=True)

if expenses.empty:
    st.info("Add a transaction on the Add Transaction page to fill this overview.")
