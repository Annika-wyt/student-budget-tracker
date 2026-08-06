# Product and UI Recommendations

This document captures the recommended next steps for the Student Budget
Tracker after the introduction of explicit Expense, Income, and Transfer
transactions and month-specific category budgets.

## Current Foundation

The application currently supports:

- separate Expense, Income, and Transfer transaction types
- transfers between everyday, savings, cash, and investment accounts
- expense-only spending and budget calculations
- monthly category budgets with legacy-data migration
- month, transaction-type, and category filters
- expense, income, transfer, and budget visualizations
- a local SQLite database and automated analytics/database tests

## Recommended Priorities

### 1. Account balances and net savings

Transfers are currently displayed as gross transfer activity. The application
does not yet calculate the balance of each account or distinguish a savings
deposit from a savings withdrawal.

Recommended implementation:

- add an `accounts` table with account name, type, and opening balance
- calculate inflows and outflows for every account
- show current everyday-account and savings-account balances
- display net savings contributions rather than gross transfer volume
- allow accounts to be created, renamed, archived, and reordered

Success criteria:

- transferring money between two owned accounts does not change total wealth
- transferring money into savings increases the savings balance
- transferring money out of savings reduces the savings balance
- account balances reconcile with transaction history

### 2. Planned and completed transactions

Future-dated records currently appear in the same monthly totals as completed
records. This makes it difficult to distinguish actual spending from upcoming
bills or expected income.

Recommended implementation:

- add a transaction status such as `Planned` or `Completed`
- show actual and forecast totals separately
- allow a planned record to be marked as completed
- visually distinguish upcoming transactions in the transaction table
- calculate an "available after planned bills" amount

### 3. Transaction editing and duplication

Users can currently add and delete transactions but cannot correct or reuse
them.

Recommended implementation:

- add Edit and Duplicate actions to each transaction row
- validate edits using the same rules as transaction creation
- require confirmation before destructive deletion
- retain the original creation timestamp and add an update timestamp

### 4. Recurring transactions

Recurring records would reduce repeated entry for rent, subscriptions, CSN,
salary, and regular savings contributions.

Recommended implementation:

- support weekly, monthly, and yearly schedules
- allow optional start and end dates
- generate planned transactions ahead of their due dates
- provide pause, resume, edit, and delete controls for schedules
- clearly identify generated records in transaction history

### 5. Savings goals

Transfers can include a note, but they are not currently connected to a target.

Recommended implementation:

- add goals with a name, target amount, target date, and linked account
- associate savings transfers with a goal
- show saved amount, remaining amount, progress, and projected completion date
- support goals such as an emergency fund, travel, deposit, or tuition

### 6. Improved monthly budget workflows

Recommended implementation:

- copy all budgets from the previous month
- edit several category budgets in one table
- delete or archive a category budget
- optionally roll unused amounts into the following month
- forecast end-of-month spending using the current spending rate
- notify the user at configurable thresholds such as 80% and 100%

### 7. Data portability

Recommended implementation:

- export filtered transactions to CSV
- import common bank CSV formats with a preview step
- detect possible duplicates before importing
- create and restore database backups
- provide a safe demo-data reset action

### 8. Custom categories and income sources

Expense categories, income sources, and accounts are currently defined in code.

Recommended implementation:

- store categories and accounts in database tables
- let users create, rename, archive, color, and reorder them
- keep Expense and Income category lists separate
- prevent archived categories from being used for new records while preserving
  their historical data

## UI Recommendations

### Overview dashboard

Lead with the user's current financial position rather than equal-weight metric
cards. The primary summary should answer:

- how much money came in this month?
- how much has been spent?
- how much remains after planned bills?
- how much moved into savings?
- am I likely to exceed my budget?

Suggested layout:

1. A primary "Safe to spend" card with the selected month.
2. Income, expenses, remaining budget, and net savings as supporting metrics.
3. A daily or weekly spending trend compared with the previous month.
4. Horizontal category bars for budget versus actual spending.
5. Upcoming bills and recent transactions.

Replace most donut charts with bars or trend lines, which make category and
period comparisons easier.

### Transaction manager

Recommended improvements:

- add free-text search over description and category
- provide inline Edit, Duplicate, and Delete actions
- support date-range filtering
- make category options depend on the selected transaction type
- display readable dates and month names
- preserve filters after saving or editing a transaction
- provide a compact mobile-friendly transaction card layout

### Budget page

Recommended improvements:

- reduce repeated summary cards
- show one progress row per category
- retain a visible scale beyond 100% for over-budget categories
- use text and icons in addition to color for status
- provide Copy Previous Month and Edit All actions
- show forecast spending alongside current spending

### Formatting and accessibility

Recommended improvements:

- display Swedish currency as `5 350 kr`
- use readable dates such as `6 August 2026`
- ensure charts remain legible in light and dark themes
- avoid communicating budget status through color alone
- provide descriptive chart labels and keyboard-accessible controls
- stack metrics and filters appropriately on small screens

## Engineering Improvements

### Transaction-oriented naming

The legacy `expenses` table, `expense_date` field, and `add_expense.py` filename
now represent all transaction types. Rename these through a versioned migration
when convenient to reduce ambiguity.

### Versioned database migrations

Use a schema version, such as SQLite `PRAGMA user_version`, rather than checking
for individual columns during normal page rendering. Run migrations once during
application startup and test every supported upgrade path.

### Money storage

Store amounts as integer öre rather than SQLite `REAL` values to avoid
floating-point rounding issues.

### Shared configuration

Move transaction types, categories, income sources, and account definitions out
of individual Streamlit pages. A shared service or database-backed configuration
will prevent lists from becoming inconsistent.

### Validation and constraints

Keep UI validation, but also enforce important rules in the data layer:

- valid transaction types
- positive amounts
- valid ISO dates and budget periods
- different source and destination accounts for transfers
- unique category budgets per month

### Testing

Add permanent Streamlit application tests for:

- submitting each transaction type
- editing and deleting transactions
- type-aware filtering
- planned versus completed calculations
- transfer effects on account balances
- month switching and empty states
- budget progress above 100%

## Suggested Delivery Plan

### Release 1: Reliable cash flow

- planned and completed transaction statuses
- transaction editing and duplication
- actual-versus-forecast dashboard totals
- future-transaction handling

### Release 2: Automation

- recurring transactions
- copy-previous-month budgets
- CSV export and database backup

### Release 3: Savings and accounts

- account balances
- net savings calculation
- savings goals
- custom accounts and categories

### Release 4: UI refinement

- dashboard trend charts
- inline transaction management
- mobile layout improvements
- Swedish formatting and accessibility review
