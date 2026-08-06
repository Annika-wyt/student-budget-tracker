import plotly.express as px
import streamlit as st

from analytics import (
    calculate_category_summary,
    calculate_total_spending,
    format_currency,
    get_highest_spending_category,
)
from database import get_all_expenses, get_filtered_expenses


ALL_CATEGORIES = "All categories"


def get_filter_options(expenses):
    """Create year, month, and category options from saved expenses."""
    if expenses.empty:
        return [], [], [ALL_CATEGORIES]

    years = sorted(expenses["expense_date"].str.slice(0, 4).unique(), reverse=True)
    months = sorted(expenses["expense_date"].str.slice(5, 7).unique())
    categories = sorted(expenses["category"].unique())

    return years, months, [ALL_CATEGORIES] + categories


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

all_expenses = get_all_expenses()
year_options, month_options, category_options = get_filter_options(all_expenses)

if all_expenses.empty:
    st.info("No expenses have been saved yet. Add an expense on the main page first.")
else:
    filter_column_one, filter_column_two, filter_column_three = st.columns(3)

    with filter_column_one:
        selected_year = st.selectbox("Year", year_options)

    with filter_column_two:
        selected_month = st.selectbox("Month", month_options)

    with filter_column_three:
        selected_category = st.selectbox("Category", category_options)

    filtered_expenses = get_filtered_expenses(
        year=selected_year,
        month=selected_month,
        category=selected_category,
    )

    if filtered_expenses.empty:
        st.info(
            "No expenses were found for the selected period. "
            "Add an expense or change the filters."
        )
    else:
        total_spending = calculate_total_spending(filtered_expenses)
        category_summary = calculate_category_summary(filtered_expenses)
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
