# Student Budget Tracker — Beginner Starter

This branch is a starting point for Python beginners learning how to build a
small application with help from an AI coding assistant.

The application uses:

- Python for the application logic
- Streamlit for the web interface
- SQLite for local data storage
- pandas for working with table-shaped data
- pytest for automated tests

The starter application runs, but it is intentionally incomplete. The form does
not save transactions yet, and the dashboard displays placeholder values. Your
job is to implement one small feature at a time, use AI to help you understand
the code, and verify every change.

## Clone the Starter Repository

Install Git before continuing, then open a terminal in the folder where you
want to keep the project.

Choose the branch you want to start from, then clone only that branch.

### Option 1: Basic starter

Clone only the basic starter branch:

```bash
git clone --branch option-1-basic --single-branch https://github.com/Annika-wyt/student-budget-tracker.git
```

Move into the downloaded project directory:

```bash
cd student-budget-tracker
```

Confirm that you are using the basic starter branch:

```bash
git branch --show-current
```

The command should print:

```text
option-1-basic
```

### Option 2: Multi-tab MVP

Clone only the multi-tab MVP branch:

```bash
git clone --branch option-2-mvp --single-branch https://github.com/Annika-wyt/student-budget-tracker.git
```

Move into the downloaded project directory:

```bash
cd student-budget-tracker
```

Confirm that you are using the multi-tab MVP branch:

```bash
git branch --show-current
```

The command should print:

```text
option-2-mvp
```

Using `--single-branch` downloads only the selected starter branch. Students do
not need the other branch options to follow this guide.

## What You Will Learn

By completing the project, you will practice:

- reading an unfamiliar Python project
- splitting code into files with different responsibilities
- creating forms with Streamlit
- validating user input
- creating and querying a SQLite database
- using pandas DataFrames
- writing calculation functions
- writing and running tests
- asking an AI assistant focused technical questions
- reviewing and verifying AI-generated code

## Project Structure

```text
student-budget-tracker/
├── app.py
├── analytics.py
├── database.py
├── views/
│   ├── overview.py
│   └── add_transaction.py
├── tests/
│   └── test_analytics.py
├── requirements.txt
├── .gitignore
└── README.md
```

## What Each File Is For

### `app.py`

This is the application entry point. Streamlit starts here.

It is responsible for:

- setting the browser page title and icon
- defining the pages shown in the sidebar
- running the page selected by the user

Keep this file small. Transaction forms, charts, and database queries belong in
other files.

### `views/overview.py`

This is the starter dashboard.

It currently displays placeholder values for income, expenses, and balance.
Later, it should:

- load transactions from the database
- calculate real totals with functions from `analytics.py`
- show recent transactions
- display charts or budget information

### `views/add_transaction.py`

This file contains the Streamlit form for entering a transaction.

The starter form collects:

- transaction type
- description
- amount
- category
- date

It performs basic validation but does not save anything yet. One of the first
project tasks is connecting this form to `add_transaction()` in `database.py`.

### `database.py`

All SQLite code belongs in this file.

The starter provides function names and documentation, but some functions are
unfinished:

- `create_connection()` opens the local database
- `create_transactions_table()` should create the table
- `add_transaction()` should insert one row
- `get_all_transactions()` should read saved rows into a DataFrame

Keeping SQL here prevents database details from spreading across the UI pages.

The SQLite file will be named `student_budget.db`. It is ignored by Git because
it contains local user data.

### `analytics.py`

This file contains calculations that do not draw anything on the screen and do
not access the database.

The starter includes:

- `calculate_total_expenses()`
- `calculate_total_income()`
- `calculate_balance()`

The first two functions contain TODOs. Keeping calculations separate makes them
easier to understand and test.

### `tests/test_analytics.py`

This file checks that analytics functions return the expected results.

The starter tests cover:

- calculating a balance
- handling an empty transaction table

Add a test containing sample Expense and Income rows before implementing the
remaining analytics logic. A failing test can describe the behavior you want to
build next.

### `requirements.txt`

This lists the external Python packages needed by the project. `pip` reads this
file when installing dependencies.

### `.gitignore`

This tells Git which local files should not be committed, including:

- the virtual environment
- Python cache files
- the local SQLite database

### `README.md`

This is the project guide you are reading. Update it when the application gains
important new features or when setup instructions change.

## Setup

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

## Expected Starter Behavior

When the application opens:

- the sidebar contains Overview and Add Transaction
- the Overview metrics all display `0.00 SEK`
- Add Transaction contains a working form
- valid form input displays a message explaining that saving is not connected
- the tests pass

These are intentional starter behaviors, not bugs.

## Suggested Learning Steps

Complete one step and test it before moving to the next.

### Step 1: Explore the existing application

- run the app
- open both pages
- identify where each displayed label comes from
- change one piece of text and observe the result

### Step 2: Create the transactions table

Implement `create_transactions_table()` in `database.py`.

Suggested fields:

- `id`
- `transaction_type`
- `description`
- `amount`
- `category`
- `transaction_date`
- `created_at`

Call the function when the application starts and verify that
`student_budget.db` is created.

### Step 3: Save a transaction

Implement `add_transaction()` with a parameterized SQL query. Connect the form
to the function and show a success message after saving.

Test both valid and invalid form values.

### Step 4: Read and display transactions

Implement `get_all_transactions()` and display its DataFrame below the form or
on the Overview page.

Add an empty-state message for a database with no records.

### Step 5: Complete the analytics functions

Write tests with sample transactions, then implement:

- total expenses
- total income
- balance
- spending grouped by category

Connect the calculations to the Overview metrics.

### Step 6: Add filtering

Allow the user to filter transactions by:

- month
- transaction type
- category

Verify that the table and dashboard totals use the same filtered data.

### Step 7: Choose an extension

Possible beginner-friendly extensions include:

- deleting a transaction
- editing a transaction
- setting a monthly category budget
- adding a spending-by-category bar chart
- exporting transactions to CSV
- adding recurring rent or income records

Implement only one extension at a time.

## How to Work With an AI Assistant

AI is most useful when you give it context, ask for a small outcome, and verify
its answer.

### Ask for explanations first

Example:

> Explain what `create_connection()` does. Assume I know Python functions but
> have never used SQLite.

### Ask for one small change

Example:

> Help me implement `create_transactions_table()`. Explain the SQL fields and
> show only the changes needed in `database.py`.

### Ask AI to review your attempt

Example:

> Review my `add_transaction()` function. Check whether the SQL is parameterized
> and whether the database connection always closes. Do not rewrite unrelated
> files.

### Ask for a test before a solution

Example:

> Help me write a pytest test for calculating total expenses. Use a small pandas
> DataFrame with Expense and Income rows. Do not implement the function yet.

### Ask for debugging help with evidence

Include:

- what you expected
- what happened instead
- the complete error message
- the smallest relevant code section

Example:

> My form says the transaction was saved, but the table stays empty. Here is the
> error output and my two database functions. Help me find the cause before
> suggesting code changes.

## A Good AI-Assisted Workflow

Use this loop for every task:

1. State the small behavior you want.
2. Find the files responsible for that behavior.
3. Ask AI to explain unfamiliar code or concepts.
4. Write or update a test when possible.
5. Make one focused code change.
6. Run the tests and application.
7. Read the changed code and explain it in your own words.
8. Commit the working change to Git.

Avoid asking AI to build the entire project in one prompt. Large changes are
harder to understand, test, and debug.

## How to Verify AI-Generated Code

Before accepting a suggestion, check:

- Can you explain what each new line is doing?
- Did the AI edit only the relevant files?
- Are SQL values passed with `?` parameters instead of string formatting?
- Does the form reject empty descriptions and non-positive amounts?
- Do the tests pass?
- Does the application still start?
- Did you manually test the new behavior?

Never paste passwords, API keys, personal financial data, or other secrets into
an AI prompt.

## Project Completion Checklist

A basic completed version should:

- create the SQLite table automatically
- save Expense and Income transactions
- reject invalid form input
- display saved transactions
- calculate total income, expenses, and balance
- calculate spending by category
- provide useful empty states and error messages
- include tests for the main calculations
- have an updated README describing the finished features

The goal is not only to finish the application. The goal is to understand the
code well enough to explain the design choices, test the behavior, and continue
building without depending on one large AI-generated answer.
