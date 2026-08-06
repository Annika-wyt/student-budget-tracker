from calendar import month_name
from datetime import date

import plotly.express as px
import streamlit as st

from analytics import (
    calculate_category_summary,
    calculate_total_spending,
    format_currency,
    get_transaction_rows,
    get_highest_spending_category,
)
from database import get_all_expenses, get_filtered_expenses


ALL_CATEGORIES = "All categories"
ALL_MONTHS = "All months"


def get_filter_options(expenses):
    """Create year and expense-category options from saved records."""
    if expenses.empty:
        return [], [ALL_CATEGORIES]

    years = sorted(expenses["expense_date"].str.slice(0, 4).unique(), reverse=True)
    categories = sorted(expenses["category"].unique())

    return years, [ALL_CATEGORIES] + categories


def get_month_options(expenses, selected_year):
    """Create month options that are valid for the selected year."""
    year_expenses = expenses[
        expenses["expense_date"].str.startswith(str(selected_year))
    ]
    months = sorted(
        year_expenses["expense_date"].str.slice(5, 7).unique(),
        reverse=True,
    )
    return [ALL_MONTHS] + months


def format_month_option(month):
    """Display numeric database months as month names."""
    if month == ALL_MONTHS:
        return month

    return month_name[int(month)]


def create_category_donut_chart(category_summary, total_spending):
    """Create a donut chart for spending by category."""
    chart = px.pie(
        category_summary,
        names="category",
        values="amount",
        title="Expenses by Category",
        hole=0.45,
    )

    chart.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>%{value:.2f} SEK<br>%{percent}<extra></extra>",
    )
    chart.update_layout(
        annotations=[
            {
                "text": format_currency(total_spending),
                "x": 0.5,
                "y": 0.5,
                "font_size": 16,
                "showarrow": False,
            }
        ],
        legend_title_text="Category",
    )

    return chart


st.title("Expense by Category")
st.write("Analyze which categories use the largest share of your spending.")

all_transactions = get_all_expenses()
all_expenses = get_transaction_rows(all_transactions, "Expense")
year_options, category_options = get_filter_options(all_expenses)

if all_expenses.empty:
    st.info("No expenses have been saved yet. Add one on Add Transaction first.")
else:
    filter_column_one, filter_column_two, filter_column_three = st.columns(3)

    with filter_column_one:
        current_year = str(date.today().year)
        year_index = (
            year_options.index(current_year) if current_year in year_options else 0
        )
        selected_year = st.selectbox("Year", year_options, index=year_index)

    with filter_column_two:
        month_options = get_month_options(all_expenses, selected_year)
        current_month = date.today().strftime("%m")
        month_index = (
            month_options.index(current_month)
            if selected_year == current_year and current_month in month_options
            else 0
        )
        selected_month = st.selectbox(
            "Month",
            month_options,
            index=month_index,
            format_func=format_month_option,
        )

    with filter_column_three:
        selected_category = st.selectbox("Category", category_options)

    filtered_expenses = get_filtered_expenses(
        year=selected_year,
        month=None if selected_month == ALL_MONTHS else selected_month,
        category=selected_category,
        transaction_type="Expense",
    )

    if filtered_expenses.empty:
        st.info(
            "No expenses were found for the selected period. "
            "Add an expense or change the filters."
        )
    else:
        total_spending = calculate_total_spending(filtered_expenses)
        category_summary = calculate_category_summary(filtered_expenses)
        if category_summary.empty:
            st.info("No expense records were found for the selected filters.")
            st.stop()

        highest_category = get_highest_spending_category(category_summary)
        active_categories = len(category_summary)

        metric_column_one, metric_column_two, metric_column_three = st.columns(3)

        with metric_column_one:
            st.metric("Total spending", format_currency(total_spending))

        with metric_column_two:
            st.metric("Highest-spending category", highest_category)

        with metric_column_three:
            st.metric("Active categories", active_categories)

        donut_chart = create_category_donut_chart(category_summary, total_spending)
        st.plotly_chart(donut_chart, use_container_width=True)

        display_summary = category_summary.copy()
        display_summary["amount"] = display_summary["amount"].apply(format_currency)
        display_summary["percentage"] = display_summary["percentage"].map(
            "{:.1f}%".format
        )
        display_summary = display_summary.rename(
            columns={
                "category": "Category",
                "amount": "Amount",
                "percentage": "Percentage",
                "expenses": "Expenses",
            }
        )

        st.subheader("Category summary")
        st.dataframe(display_summary, use_container_width=True, hide_index=True)
