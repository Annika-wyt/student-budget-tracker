# Student Budget Tracker

A local web application for an international student living in Sweden to record
expenses and understand where their money goes.

The app is built with Python, Streamlit, SQLite, pandas, and Plotly.

## Features

- Add an expense with description, amount in SEK, category, and date
- Save expenses in a local SQLite database
- View all saved expenses in a table
- Filter expenses by month and category
- Delete an expense
- View total spending and number of expenses
- View spending totals by category
- View a bar chart of spending by category
- Show clear error messages for invalid input

## Project Structure

```text
student-budget-tracker/
├── app.py
├── database.py
├── analytics.py
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

## Database

The app uses SQLite through Python's built-in `sqlite3` module.

The database file is created locally as:

```text
student_budget.db
```

This file is ignored by Git because it is local user data.

The app uses one table called `expenses`.

Table fields:

- `id`
- `description`
- `amount`
- `category`
- `expense_date`
- `created_at`

Dates are stored as text in ISO format:

```text
YYYY-MM-DD
```

SQL queries use parameters, such as `?`, instead of directly inserting user
input into SQL strings.

## File Responsibilities

`app.py`

This is the Streamlit user interface. It displays the form, filters, tables,
summary numbers, chart, messages, and delete controls.

`database.py`

This file contains the SQLite functions. It creates the table, adds expenses,
reads expenses, and deletes expenses.

`analytics.py`

This file contains the summary calculations. It calculates total spending,
number of expenses, and spending by category.

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

## Interview Notes

This project demonstrates:

- separating user interface code from database code
- using SQLite for local persistent storage
- using parameterized SQL queries
- validating user input before saving
- using pandas for tabular data
- using Plotly for a simple chart
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
