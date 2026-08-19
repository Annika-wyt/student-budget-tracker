# Student Budget Tracker

A local web application for an international student living in Sweden to record
expenses and understand where their money goes.

The app is built with Python, Streamlit, SQLite, pandas, and Plotly.

See [Product and UI Recommendations](docs/PRODUCT_AND_UI_RECOMMENDATIONS.md)
for the prioritized product roadmap and suggested interface improvements.

## Features

- Add Expense, Income, and Transfer transactions from one page
- Record income sources separately from expense categories
- Move money to savings without counting it as spending
- Save transactions in a local SQLite database
- Save monthly budgets by category in the local SQLite database
- View a period-aligned overview dashboard with expense, income, and budget charts
- View all saved transactions in a table
- Filter transactions by month, type, and category
- Delete a transaction
- View expense-only spending totals and monthly budget usage
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

## Get This Branch From GitHub

If you have not downloaded the project yet, clone only the multi-tab MVP
branch:

```bash
git clone --branch option-2-mvp --single-branch https://github.com/Annika-wyt/student-budget-tracker.git
cd student-budget-tracker
```

If you already cloned the repository, download the latest branch information
and switch to this branch:

```bash
git fetch origin
git switch option-2-mvp
git pull origin option-2-mvp
```

If Git says the branch does not exist locally, create it from the GitHub branch:

```bash
git switch --track origin/option-2-mvp
```

Confirm that you are on the correct branch:

```bash
git branch --show-current
```

The command should print `option-2-mvp`.

## How To Run The App

Open the project folder in VS Code, then open the integrated terminal by
selecting **Terminal > New Terminal**. Make sure the terminal is inside the
`student-budget-tracker` folder before running the commands below.

### What Is a Python Virtual Environment?

A virtual environment is a private place for this project's Python packages.
It keeps packages such as Streamlit separate from packages used by your other
Python projects. The `.venv` folder created below is that private place.

You create the virtual environment once. Each time you open a new VS Code
terminal to work on the project, activate it again before running the app.

### Should I Use `python` or `python3`?

Both commands can run Python 3. The correct command depends on how Python was
installed and configured on your computer. For example, a computer with Python
3.13.15 may still use the `python` command instead of `python3`.

Check which command works in your VS Code terminal:

```bash
python --version
```

If that command is not found, try:

```bash
python3 --version
```

Use the command that displays `Python 3.x.x` when creating the virtual
environment. After the environment is activated, `python` will normally point
to the Python inside `.venv`.

### Linux

In the VS Code terminal, create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If your computer uses `python` for Python 3, use `python -m venv .venv` instead.

Install the packages and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

After activation, `python` uses the Python installation inside `.venv`, even if
you used `python3` to create it.

### macOS

In the VS Code terminal, create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If your computer uses `python` for Python 3, use `python -m venv .venv` instead.

Install the packages and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

After activation, `python` uses the Python installation inside `.venv`, even if
you used `python3` to create it.

### Windows

VS Code normally opens PowerShell on Windows. Create and activate the virtual
environment with:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If your computer uses `python3` for Python 3, use `python3 -m venv .venv`
instead.

Install the packages and start the app:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If you use Command Prompt instead of PowerShell, activate the environment with:

```bat
.venv\Scripts\activate.bat
```

### Run the App Again Later

After the first setup, open a new VS Code terminal and activate the existing
virtual environment. On Linux or macOS, run:

```bash
source .venv/bin/activate
```

On Windows PowerShell, run:

```powershell
.venv\Scripts\Activate.ps1
```

Then start the app:

```bash
python -m streamlit run app.py
```

The app will open in your browser. If it does not open automatically, open the
local URL shown in the terminal. Press **Ctrl+C** in the terminal to stop the
app. Run `deactivate` when you want to leave the virtual environment.

To run the tests while the virtual environment is active:

```bash
python -m pytest tests
```

## Database

The app uses SQLite through Python's built-in `sqlite3` module.

The database file is created locally as:

```text
student_budget.db
```

This file is ignored by Git because it is local user data.

The app uses one legacy-named table called `expenses` for all transaction types
and one table called `budgets` for saved monthly category budgets.

Table fields:

- `id`
- `description`
- `amount`
- `category`
- `transaction_type`
- `from_account`
- `to_account`
- `expense_date`
- `created_at`

Budget fields:

- `id`
- `year_month`
- `category`
- `amount`
- `created_at`
- `updated_at`

Dates are stored as text in ISO format:

```text
YYYY-MM-DD
```

Budget periods are stored as `YYYY-MM`. A category can have a separate budget
for each month. Existing category-only budgets are preserved and assigned to
the current month when the database schema is upgraded.

SQL queries use parameters, such as `?`, instead of directly inserting user
input into SQL strings.

Legacy rows are upgraded automatically: rows in the old Income category become
Income transactions, and all other rows become Expense transactions. Transfers
are stored with source and destination accounts and are excluded from spending,
income, and budget calculations.

## File Responsibilities

`app.py`

This is the Streamlit navigation file. It controls the sidebar page names and
keeps `streamlit run app.py` as the local run command.

`database.py`

This file contains the SQLite functions. It migrates and stores transactions,
deletes transactions, saves monthly budgets, and reads both datasets.

`analytics.py`

This file contains the summary calculations. It calculates total spending,
number of expenses, spending by category, budget overview numbers, and category
analysis percentages.

`pages/expense_by_category.py`

This file contains the Streamlit page for category analysis. It displays month,
year, and category filters, a donut chart, and a category summary table.

`pages/overview.py`

This file contains the first dashboard page. It displays period-aligned expense,
income, and signed category-budget charts.

`pages/add_expense.py`

This file contains the unified Expense, Income, and Transfer form. It also lets
the user view, filter, and delete saved transactions.

`pages/set_budget.py`

This file contains the form for saving monthly category budgets and displays the
budget dashboard.

`requirements.txt`

This file lists the external Python packages needed to run the app.

## Important Functions

`create_expenses_table()`

Creates the `expenses` table if it does not already exist.

`add_transaction(...)`

Saves an Expense, Income, or Transfer transaction in the database.

`get_all_expenses()`

Reads all transactions from the database and returns them as a pandas DataFrame.

`delete_transaction(transaction_id)`

Deletes one transaction using its unique ID.

`validate_transaction(...)`

Checks the type-specific form values before saving.

`calculate_total_spending(expenses)`

Calculates the total amount spent.

`calculate_number_of_expenses(expenses)`

Counts the number of expenses.

`calculate_spending_by_category(expenses)`

Groups expenses by category and calculates the total spending per category.

`calculate_expense_category_summary(expenses)`

Groups spending by category while excluding Income and Transfer rows.

`calculate_income_summary(expenses)`

Groups Income transactions by source for chart display.

`get_filtered_expenses(year, month, category, transaction_type)`

Reads transactions using optional period, category, and type filters.

`save_budget(category, amount, year_month)`

Saves or updates one category budget for a specific month.

`get_budgets(year_month)`

Reads saved category budgets from SQLite, optionally filtered by month.

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

Keeps both positive and negative category balances so over-budget categories
remain visible in the overview chart.

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

- Export expenses to CSV
- Add editing for existing expenses
- Add more charts
- Add recurring transactions
