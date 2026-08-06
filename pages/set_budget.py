import sqlite3
from datetime import date

import streamlit as st

from analytics import (
    calculate_category_budget_summary,
    calculate_saved_budget_overview,
    format_currency,
)
from database import (
    create_budgets_table,
    create_expenses_table,
    get_all_expenses,
    get_budgets,
    save_budget,
)


CATEGORIES = [
    "Housing",
    "Groceries",
    "Transport",
    "Eating out",
    "Phone and internet",
    "Study materials",
    "Entertainment",
    "Relocation",
    "Income",
    "Other",
]


create_expenses_table()
create_budgets_table()

st.title("Set Budget")
st.write("Save monthly budgets by category.")

if "budget_success_message" in st.session_state:
    st.success(st.session_state.pop("budget_success_message"))

with st.form("save_budget_form"):
    budget_category = st.selectbox("Budget category", CATEGORIES)
    budget_amount = st.number_input(
        "Monthly budget for this category in SEK",
        min_value=0.01,
        value=1000.0,
        step=100.0,
    )

    budget_submitted = st.form_submit_button("Save category budget")

if budget_submitted:
    try:
        save_budget(budget_category, budget_amount)
        st.session_state["budget_success_message"] = "Budget saved successfully."
        st.rerun()
    except sqlite3.Error:
        st.error("The budget could not be saved. Please try again.")

expenses = get_all_expenses()
budgets = get_budgets()

if budgets.empty:
    st.info("No budgets have been saved yet.")
else:
    category_budget_summary = calculate_category_budget_summary(
        budgets,
        expenses,
        date.today(),
    )
    monthly_overview = calculate_saved_budget_overview(category_budget_summary)
    progress_value = min(monthly_overview["percentage_used"] / 100, 1.0)

    budget_column, spent_column = st.columns(2)

    with budget_column:
        st.metric("Total budget", format_currency(monthly_overview["budget"]))

    with spent_column:
        st.metric("Amount spent", format_currency(monthly_overview["spent"]))

    remaining_column, percent_column = st.columns(2)

    with remaining_column:
        st.metric("Amount remaining", format_currency(monthly_overview["remaining"]))

    with percent_column:
        st.metric("Budget used", f"{monthly_overview['percentage_used']:.1f}%")

    st.progress(progress_value)
    st.write(monthly_overview["status"])

    summary_column_one, summary_column_two = st.columns(2)

    with summary_column_one:
        st.metric("Number of budgets", monthly_overview["number_of_budgets"])

    with summary_column_two:
        st.metric("Overall budget usage", f"{monthly_overview['percentage_used']:.1f}%")

    summary_column_three, summary_column_four = st.columns(2)

    with summary_column_three:
        st.metric("Budgets on track", monthly_overview["on_track_count"])

    with summary_column_four:
        st.metric("Budgets over limit", monthly_overview["over_budget_count"])

    display_budget_summary = category_budget_summary.copy()
    display_budget_summary["budget"] = display_budget_summary["budget"].apply(
        format_currency
    )
    display_budget_summary["spent"] = display_budget_summary["spent"].apply(
        format_currency
    )
    display_budget_summary["remaining"] = display_budget_summary[
        "remaining"
    ].apply(format_currency)
    display_budget_summary["percentage_used"] = display_budget_summary[
        "percentage_used"
    ].map("{:.1f}%".format)
    display_budget_summary = display_budget_summary.rename(
        columns={
            "category": "Category",
            "budget": "Budget",
            "spent": "Spent",
            "remaining": "Remaining",
            "percentage_used": "Used",
            "status": "Status",
        }
    )

    st.subheader("Saved category budgets")
    st.dataframe(display_budget_summary, use_container_width=True, hide_index=True)
