# Student Budget Tracker

A local web application for an international student living in Sweden to record
expenses and understand where their money goes.

The app is built with Python, Streamlit, SQLite, pandas, and Plotly.

## Features

- Add an expense with description, amount in SEK, category, and date
- Add income records using the Income category
- Save expenses in a local SQLite database
- Save monthly budgets by category in the local SQLite database
- View an overview dashboard with expense, income, and remaining budget charts
- View all saved expenses in a table
- Filter expenses by month and category
- Delete an expense
- View total spending, number of expenses, and monthly budget usage
- View spending totals by category
- View a bar chart of spending by category
- View an Expense by Category page with a donut chart and category summary
- Use dummy data from January 2026 to August 2026 for portfolio demos
- Show clear error messages for invalid input

## Project Structure

```text
student-budget-tracker/
├── app.py
├── pages/
│   ├── overview.py
│   ├── add_expense.py
│   ├── set_budget.py
│   └── expense_by_category.py
├── database.py
├── analytics.py
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## How To Run The App

From inside the `student-budget-tracker` folder, create and activate a virtual
environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser. If it does not open automatically, use the
local URL shown in the terminal.

Run the tests:

```bash
pytest tests
```

## Database

The app uses SQLite through Python's built-in `sqlite3` module.

The database file is created locally as:

```text
student_budget.db
```

This file is ignored by Git because it is local user data.

The app uses one table called `expenses` for expense records and one table
called `budgets` for saved monthly category budgets.

Table fields:

- `id`
- `description`
- `amount`
- `category`
- `expense_date`
- `created_at`

Budget fields:

- `id`
- `category`
- `amount`
- `created_at`
- `updated_at`

Dates are stored as text in ISO format:

```text
YYYY-MM-DD
```

SQL queries use parameters, such as `?`, instead of directly inserting user
input into SQL strings.

## File Responsibilities

`app.py`

This is the Streamlit navigation file. It controls the sidebar page names and
keeps `streamlit run app.py` as the local run command.

`database.py`

This file contains the SQLite functions. It creates the table, adds expenses,
reads expenses, deletes expenses, saves budgets, and reads budgets.

`analytics.py`

This file contains the summary calculations. It calculates total spending,
number of expenses, spending by category, budget overview numbers, and category
analysis percentages.

`pages/expense_by_category.py`

This file contains the Streamlit page for category analysis. It displays month,
year, and category filters, a donut chart, and a category summary table.

`pages/overview.py`

This file contains the first dashboard page. It displays filters and pie charts
for expenses by category, income sources, and remaining budget by category.

`pages/add_expense.py`

This file contains the form for adding expense and income records. It also lets
the user view, filter, and delete saved records.

`pages/set_budget.py`

This file contains the form for saving monthly category budgets and displays the
budget dashboard.

`requirements.txt`

This file lists the external Python packages needed to run the app.

## Important Functions

`create_expenses_table()`

Creates the `expenses` table if it does not already exist.

`add_expense(description, amount, category, expense_date)`

Saves one expense in the database.

`get_all_expenses()`

Reads all expenses from the database and returns them as a pandas DataFrame.

`delete_expense(expense_id)`

Deletes one expense using its unique ID.

`validate_expense(description, amount, category, expense_date)`

Checks the form values before saving and returns a list of error messages.

`calculate_total_spending(expenses)`

Calculates the total amount spent.

`calculate_number_of_expenses(expenses)`

Counts the number of expenses.

`calculate_spending_by_category(expenses)`

Groups expenses by category and calculates the total spending per category.

`calculate_expense_category_summary(expenses)`

Groups spending by category while excluding Income rows.

`calculate_income_summary(expenses)`

Groups Income rows by description so income sources can be shown in a pie chart.

`get_filtered_expenses(year, month, category)`

Reads expenses from SQLite using optional year, month, and category filters.

`save_budget(category, amount)`

Saves or updates the monthly budget for one category.

`get_budgets()`

Reads saved category budgets from SQLite.

`calculate_category_summary(expenses)`

Groups filtered expenses by category and calculates total amount, percentage of
total spending, and number of expenses.

`get_highest_spending_category(category_summary)`

Returns the category name with the highest total spending.

`format_currency(amount)`

Formats a number as a SEK amount for display.

`calculate_category_budget_summary(budgets, expenses, current_date)`

Compares each saved category budget with spending from the current month.

`calculate_saved_budget_overview(category_budget_summary)`

Calculates total budget, total spent, remaining amount, usage percentage, and
budget status counts.

`calculate_budget_remaining_summary(category_budget_summary)`

Keeps categories with remaining budget and prepares them for the overview pie
chart.

`seed_dummy_data()`

Adds demo expenses, income records, and budgets for January 2026 through August
2026. It checks for existing demo rows first so repeated runs do not duplicate
demo expenses.

## Interview Notes

This project demonstrates:

- separating user interface code from database code
- using SQLite for local persistent storage
- using parameterized SQL queries
- validating user input before saving
- using pandas for tabular data
- using Plotly for a simple chart
- using pytest to test calculation and filtering behavior
- organizing a beginner Python project into multiple files

One important design choice is that the chart and summary numbers use the
currently filtered data. This means the table, totals, and chart all describe
the same set of expenses.

## Possible Future Improvements

- Add a monthly budget target
- Export expenses to CSV
- Add editing for existing expenses
- Add more charts
- Add tests for database and analytics functions
